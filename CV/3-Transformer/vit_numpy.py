"""
Vision Transformer (ViT) 实现 - MNIST分类
"""

import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import time
from scipy.ndimage import zoom

# ============== 配置参数 ==============
class Config:
    img_size = 28
    patch_size = 7       # 4个patches，保持计算量可控
    num_channels = 1
    num_classes = 10
    hidden_size = 144    # 适度增加 (+16)，提升容量
    num_heads = 4
    mlp_ratio = 2        # MLP隐藏层288
    num_blocks = 2
    dropout = 0.0
    learning_rate = 0.001   # 提高学习率，加速收敛
    weight_decay = 0.001
    batch_size = 96      # 适中batch，平衡速度和稳定性
    epochs = 22          # 增加4轮，让模型充分收敛到80%+
    val_split = 0.1
    seed = 42

np.random.seed(Config.seed)


# ============== 数据增强 ==============
def random_crop(img, crop_size):
    h, w = img.shape
    top = np.random.randint(0, h - crop_size + 1)
    left = np.random.randint(0, w - crop_size + 1)
    return img[top:top+crop_size, left:left+crop_size]

def resize_image(img, target_size):
    """快速缩放"""
    h, w = img.shape
    zoom_factors = (target_size / h, target_size / w)
    return zoom(img, zoom_factors, order=1).astype(np.float32)

def strong_augmentation(img, target_size=32):
    """轻度数据增强 - 折中方案"""
    # 偶尔水平翻转
    if np.random.random() < 0.2:
        img = np.fliplr(img)
    # 小范围随机裁剪
    pad = 2
    padded = np.pad(img, pad, mode='constant', constant_values=0)
    crop_size = target_size
    h, w = padded.shape
    top = np.random.randint(0, h - crop_size + 1)
    left = np.random.randint(0, w - crop_size + 1)
    img = padded[top:top+crop_size, left:left+crop_size]
    # 缩放
    img = resize_image(img, target_size)
    # 轻微亮度抖动 (±10%)
    img = img * (1 + np.random.uniform(-0.1, 0.1))
    return np.clip(img, 0, 1)


# ============== 数据加载 ==============
def load_mnist():
    """加载MNIST数据集"""
    # 以脚本自身位置为基准定位数据集，与运行时工作目录无关
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'MNIST')
    
    # 加载训练集图像
    with open(f'{data_dir}/train-images.idx3-ubyte', 'rb') as f:
        magic = int.from_bytes(f.read(4), 'big')
        num_images = int.from_bytes(f.read(4), 'big')
        rows = int.from_bytes(f.read(4), 'big')
        cols = int.from_bytes(f.read(4), 'big')
        X_train_full = np.frombuffer(f.read(), np.uint8).reshape(num_images, rows, cols)
    
    with open(f'{data_dir}/train-labels.idx1-ubyte', 'rb') as f:
        f.read(8)
        y_train_full = np.frombuffer(f.read(), np.uint8)
    
    with open(f'{data_dir}/t10k-images.idx3-ubyte', 'rb') as f:
        f.read(16)
        X_test = np.frombuffer(f.read(), np.uint8).reshape(-1, rows, cols)
    
    with open(f'{data_dir}/t10k-labels.idx1-ubyte', 'rb') as f:
        f.read(8)
        y_test = np.frombuffer(f.read(), np.uint8)
    
    print(f"训练集: {X_train_full.shape[0]} 样本")
    print(f"测试集: {X_test.shape[0]} 样本")
    
    return X_train_full.astype(np.float32) / 255.0, y_train_full, X_test.astype(np.float32) / 255.0, y_test


def create_patches(images, patch_size, img_size):
    """将图像分割成patches"""
    n = images.shape[0]
    n_patches = (img_size // patch_size) ** 2
    patches = np.zeros((n, n_patches, patch_size * patch_size), dtype=np.float32)
    for idx, img in enumerate(images):
        for i in range(img_size // patch_size):
            for j in range(img_size // patch_size):
                patch = img[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size]
                patches[idx, i * (img_size // patch_size) + j] = patch.flatten()
    return patches


def preprocess_data(X, y, config, augment=False):
    """数据预处理"""
    n = X.shape[0]
    processed = np.zeros((n, config.img_size, config.img_size), dtype=np.float32)
    for i in range(n):
        processed[i] = strong_augmentation(X[i], config.img_size) if augment else resize_image(X[i], config.img_size)
    patches = create_patches(processed, config.patch_size, config.img_size)
    return patches, y


# ============== 激活函数 ==============
def gelu(x):
    """GELU激活函数 - 更精确实现"""
    return 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))

def gelu_derivative(x):
    """GELU导数"""
    sqrt_2_pi = np.sqrt(2 / np.pi)
    cdf = 0.5 * (1 + np.tanh(sqrt_2_pi * (x + 0.044715 * x**3)))
    pdf = np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
    return cdf + x * pdf

def softmax(x):
    x_shifted = x - np.max(x, axis=-1, keepdims=True)
    exp_x = np.exp(x_shifted)
    return exp_x / (np.sum(exp_x, axis=-1, keepdims=True) + 1e-8)


# ============== ViT 模型 ==============
class ViT:
    def __init__(self, config):
        self.config = config
        self.n_patches = (config.img_size // config.patch_size) ** 2
        self.total_seq_len = self.n_patches + 1  # +1 for cls token
        
        # Patch Embedding
        self.proj = np.random.randn(config.patch_size**2, config.hidden_size) * np.sqrt(2.0 / config.patch_size**2)
        self.cls_token = np.random.randn(1, config.hidden_size) * 0.02
        self.pos_embed = np.random.randn(self.total_seq_len, config.hidden_size) * 0.02
        
        # Transformer Blocks
        self.blocks = []
        for _ in range(config.num_blocks):
            block = TransformerBlock(config)
            self.blocks.append(block)
        
        # Classification head
        self.ln = LayerNorm(config.hidden_size)
        self.head = np.random.randn(config.hidden_size, config.num_classes) * np.sqrt(2.0 / config.hidden_size)
        
        self.cache = {}
    
    def forward(self, patches, training=False):
        """前向传播"""
        B = patches.shape[0]
        
        # Patch embedding
        x = np.dot(patches, self.proj)  # (B, n_patches, hidden)
        
        # Add cls token
        cls_tokens = np.tile(self.cls_token, (B, 1, 1))
        x = np.concatenate([cls_tokens, x], axis=1)  # (B, seq+1, hidden)
        
        # Add position embedding
        x = x + self.pos_embed
        
        self.cache['x'] = x.copy()
        self.cache['patches'] = patches.copy()
        
        # Transformer blocks
        for i, block in enumerate(self.blocks):
            x = block.forward(x)
            self.cache[f'block_{i}'] = x.copy()
        
        # Final LN
        x = self.ln.forward(x)
        
        # CLS token output
        cls_output = x[:, 0, :]  # (B, hidden)
        
        # Classification
        logits = np.dot(cls_output, self.head)
        
        self.cache['logits'] = logits
        self.cache['cls_output'] = cls_output
        
        return logits
    
    def backward(self, grad_output):
        """反向传播"""
        B = grad_output.shape[0]
        T = self.total_seq_len
        
        # Head gradient
        cls_output = self.cache['cls_output']
        grad_head = np.dot(cls_output.T, grad_output) / B
        
        # Create full sequence gradient (only cls token has gradient from head)
        grad_full = np.zeros((B, T, self.config.hidden_size))
        grad_full[:, 0, :] = np.dot(grad_output, self.head.T)
        
        # Final LayerNorm backward (grad_full flows through final LN)
        grad_after_ln = self.ln.backward(grad_full)
        
        # Block gradients
        grad = grad_after_ln
        for i in reversed(range(len(self.blocks))):
            grad = self.blocks[i].backward(grad)
        
        self.grads = {
            'head': grad_head,
            'ln_gamma': self.ln.grads['gamma'],
            'ln_beta': self.ln.grads['beta']
        }
        
        for i in range(len(self.blocks)):
            self.grads[f'block_{i}'] = self.blocks[i].grads
        
        # Patch embedding gradient
        # x = patches @ proj, x shape: (B, n_patches, H), proj shape: (patch_dim, H)
        # grad_proj[p, d] = sum over b of sum over patches of grad_x[b, p, d] * patches[b, p, p]
        x_cached = self.cache['x']
        patches_cached = self.cache.get('patches')
        grad_proj = np.einsum('bpd,bpf->fd', grad[:, 1:1+self.n_patches, :], patches_cached) / B
        
        self.grads['proj'] = grad_proj
        self.grads['pos_embed'] = np.sum(grad[:, 1:, :], axis=(0, 1))
        self.grads['cls_token'] = np.sum(grad[:, 0, :], axis=0)
        
        return grad
    
    def get_params(self):
        params = {
            'proj': self.proj,
            'cls_token': self.cls_token,
            'pos_embed': self.pos_embed,
            'head': self.head,
            'ln_gamma': self.ln.gamma,
            'ln_beta': self.ln.beta
        }
        for i, block in enumerate(self.blocks):
            params[f'block_{i}_attn_Wq'] = block.attention.W_q
            params[f'block_{i}_attn_Wk'] = block.attention.W_k
            params[f'block_{i}_attn_Wv'] = block.attention.W_v
            params[f'block_{i}_attn_Wo'] = block.attention.W_o
            params[f'block_{i}_mlp_W1'] = block.mlp.W1
            params[f'block_{i}_mlp_b1'] = block.mlp.b1
            params[f'block_{i}_mlp_W2'] = block.mlp.W2
            params[f'block_{i}_mlp_b2'] = block.mlp.b2
            params[f'block_{i}_ln1_gamma'] = block.ln1.gamma
            params[f'block_{i}_ln1_beta'] = block.ln1.beta
            params[f'block_{i}_ln2_gamma'] = block.ln2.gamma
            params[f'block_{i}_ln2_beta'] = block.ln2.beta
        return params


class LayerNorm:
    def __init__(self, hidden_size, eps=1e-8):
        self.hidden_size = hidden_size
        self.eps = eps
        self.gamma = np.ones(hidden_size)
        self.beta = np.zeros(hidden_size)
    
    def forward(self, x):
        self.cache = {'x': x.copy()}
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        x_norm = (x - mean) / np.sqrt(var + self.eps)
        out = self.gamma * x_norm + self.beta
        self.cache['x_norm'] = x_norm
        self.cache['mean'] = mean
        self.cache['var'] = var
        return out
    
    def backward(self, grad_output):
        x = self.cache['x']
        x_norm = self.cache['x_norm']
        mean = self.cache['mean']
        var = self.cache['var']
        B, T, H = x.shape
        
        self.grads = {
            'gamma': np.sum(grad_output * x_norm, axis=(0, 1)),
            'beta': np.sum(grad_output, axis=(0, 1))
        }
        
        grad_x_norm = grad_output * self.gamma
        
        grad_var = -0.5 * np.sum(grad_x_norm * (x - mean), axis=-1, keepdims=True) / (var + self.eps)
        grad_mean = -np.sum(grad_x_norm, axis=-1, keepdims=True) / np.sqrt(var + self.eps)
        
        grad_x = grad_x_norm / np.sqrt(var + self.eps) + \
                2 * grad_var * (x - mean) / H + grad_mean / H
        
        return grad_x


class TransformerBlock:
    def __init__(self, config):
        self.config = config
        self.attention = MultiHeadAttention(config)
        self.mlp = MLP(config)
        self.ln1 = LayerNorm(config.hidden_size)
        self.ln2 = LayerNorm(config.hidden_size)
        self.cache = {}
    
    def forward(self, x):
        """Pre-LN结构: 更稳定且易于训练"""
        self.cache['x'] = x.copy()
        
        # Pre-LN Attention + residual
        x_norm1 = self.ln1.forward(x)
        attn_out = self.attention.forward(x_norm1)
        x = x + attn_out
        self.cache['x_after_attn'] = x.copy()
        
        # Pre-LN MLP + residual
        x_norm2 = self.ln2.forward(x)
        mlp_out = self.mlp.forward(x_norm2)
        x = x + mlp_out
        
        self.cache['attn_out'] = attn_out
        self.cache['mlp_out'] = mlp_out
        self.cache['x_norm1'] = x_norm1
        self.cache['x_norm2'] = x_norm2
        
        return x
    
    def backward(self, grad_output):
        """Pre-LN backward: 清晰正确的梯度流"""
        x = self.cache['x']
        x_after_attn = self.cache['x_after_attn']
        x_norm1 = self.cache['x_norm1']
        x_norm2 = self.cache['x_norm2']
        
        # 第二路: MLP分支 (residual + mlp_out = output)
        # grad_output 同时流向残差和MLP
        grad_mlp_branch = grad_output  # MLP分支的梯度
        grad_res2 = grad_output        # 残差连接的梯度
        
        # MLP backward (输入是LN后的x)
        grad_ln2_out = self.mlp.backward(grad_mlp_branch)
        grad_ln2_in = self.ln2.backward(grad_ln2_out)
        
        # 合并MLP路的梯度到残差
        grad_after_attn = grad_res2 + grad_ln2_in
        
        # 第一路: Attention分支
        grad_attn_branch = grad_after_attn
        grad_res1 = grad_after_attn
        
        # Attention backward (输入是LN后的x)
        grad_ln1_out = self.attention.backward(grad_attn_branch)
        grad_ln1_in = self.ln1.backward(grad_ln1_out)
        
        # 合并到输入
        grad_input = grad_res1 + grad_ln1_in
        
        self.grads = {
            'attn': self.attention.grads,
            'mlp': self.mlp.grads,
            'ln1': self.ln1.grads,
            'ln2': self.ln2.grads
        }
        
        return grad_input


class MultiHeadAttention:
    def __init__(self, config):
        H = config.hidden_size
        self.num_heads = config.num_heads
        self.head_dim = H // config.num_heads
        self.scale = self.head_dim ** -0.5
        
        self.W_q = np.random.randn(H, H) * np.sqrt(2.0 / H)
        self.W_k = np.random.randn(H, H) * np.sqrt(2.0 / H)
        self.W_v = np.random.randn(H, H) * np.sqrt(2.0 / H)
        self.W_o = np.random.randn(H, H) * np.sqrt(2.0 / H)
        
        self.cache = {}
    
    def forward(self, x):
        B, T, H = x.shape
        
        Q = np.dot(x, self.W_q)
        K = np.dot(x, self.W_k)
        V = np.dot(x, self.W_v)
        
        # Reshape for multi-head
        Q = Q.reshape(B, T, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        K = K.reshape(B, T, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        V = V.reshape(B, T, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        
        self.cache = {'Q': Q, 'K': K, 'V': V, 'x': x}
        
        # Attention scores
        scores = np.matmul(Q, K.transpose(0, 1, 3, 2)) * self.scale
        attn = softmax(scores)
        
        self.cache['attn'] = attn
        
        # Apply attention
        context = np.matmul(attn, V)
        context = context.transpose(0, 2, 1, 3).reshape(B, T, H)
        
        out = np.dot(context, self.W_o)
        
        return out
    
    def backward(self, grad_output):
        Q, K, V = self.cache['Q'], self.cache['K'], self.cache['V']
        attn = self.cache['attn']
        x = self.cache['x']
        B, T, H = x.shape
        
        # Output projection gradient
        grad_context = np.dot(grad_output, self.W_o.T)
        grad_context_rs = grad_context.reshape(B, T, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        
        # Attention gradient
        grad_attn = np.matmul(grad_context_rs, V.transpose(0, 1, 3, 2))
        
        # Softmax gradient
        grad_attn = attn * (grad_attn - np.sum(attn * grad_attn, axis=-1, keepdims=True))
        
        grad_Q = np.matmul(grad_attn, K)
        grad_K = np.matmul(grad_attn.transpose(0, 1, 3, 2), Q)
        grad_V = np.matmul(attn.transpose(0, 1, 3, 2), grad_context_rs)
        
        # Reshape gradients
        grad_Q = grad_Q.transpose(0, 2, 1, 3).reshape(B, T, H)
        grad_K = grad_K.transpose(0, 2, 1, 3).reshape(B, T, H)
        grad_V = grad_V.transpose(0, 2, 1, 3).reshape(B, T, H)
        
        # Parameter gradients
        self.grads = {
            'W_q': np.zeros_like(self.W_q),
            'W_k': np.zeros_like(self.W_k),
            'W_v': np.zeros_like(self.W_v),
            'W_o': np.zeros_like(self.W_o)
        }
        
        for b in range(B):
            self.grads['W_q'] += np.dot(x[b].T, grad_Q[b])
            self.grads['W_k'] += np.dot(x[b].T, grad_K[b])
            self.grads['W_v'] += np.dot(x[b].T, grad_V[b])
            self.grads['W_o'] += np.dot(
                np.matmul(attn[b], V[b]).reshape(T, H).T,
                grad_output[b]
            )
        
        self.grads['W_q'] /= B
        self.grads['W_k'] /= B
        self.grads['W_v'] /= B
        self.grads['W_o'] /= B
        
        # Input gradient
        grad_x = np.dot(grad_Q, self.W_q.T) + np.dot(grad_K, self.W_k.T) + np.dot(grad_V, self.W_v.T)
        
        return grad_x


class MLP:
    def __init__(self, config):
        H = config.hidden_size
        hidden = H * config.mlp_ratio
        
        self.W1 = np.random.randn(H, hidden) * np.sqrt(2.0 / H)
        self.b1 = np.zeros(hidden)
        self.W2 = np.random.randn(hidden, H) * np.sqrt(2.0 / hidden)
        self.b2 = np.zeros(H)
        
        self.cache = {}
    
    def forward(self, x):
        B, T, H = x.shape
        x_flat = x.reshape(B * T, H)
        self.cache['x_flat'] = x_flat
        self.cache['shape'] = (B, T, H)
        
        h_flat = np.dot(x_flat, self.W1) + self.b1
        h_flat = gelu(h_flat)
        self.cache['h_flat'] = h_flat
        
        out_flat = np.dot(h_flat, self.W2) + self.b2
        return out_flat.reshape(B, T, H)
    
    def backward(self, grad_output):
        x_flat = self.cache['x_flat']
        h_flat = self.cache['h_flat']
        B, T, H = self.cache['shape']
        hidden = self.W1.shape[1]
        
        # Reshape gradient
        grad_out_flat = grad_output.reshape(B * T, H)
        
        # Output layer: grad_h = grad_out @ W2.T
        grad_h_flat = np.dot(grad_out_flat, self.W2.T)  # (B*T, hidden)
        
        # GELU gradient
        gelu_input = x_flat @ self.W1 + self.b1
        gelu_grad = gelu_derivative(gelu_input)
        grad_h_flat = grad_h_flat * gelu_grad
        
        # Parameter gradients
        grad_W2 = np.dot(h_flat.T, grad_out_flat) / B
        grad_b2 = np.mean(grad_out_flat, axis=0)
        grad_W1 = np.dot(x_flat.T, grad_h_flat) / B
        grad_b1 = np.mean(grad_h_flat, axis=0)
        
        # Input gradient: grad_x = grad_h @ W1.T
        grad_x_flat = np.dot(grad_h_flat, self.W1.T)
        grad_x = grad_x_flat.reshape(B, T, H)
        
        self.grads = {
            'W1': grad_W1, 'b1': grad_b1,
            'W2': grad_W2, 'b2': grad_b2
        }
        
        return grad_x


# ============== AdamW 优化器 ==============
class AdamW:
    def __init__(self, params, lr=0.001, weight_decay=0.01, lr_decay=0.95):
        self.params = params
        self.initial_lr = lr
        self.lr = lr
        self.weight_decay = weight_decay
        self.lr_decay = lr_decay
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
        self.beta1, self.beta2 = 0.9, 0.999
        self.eps = 1e-8
    
    def step(self, grads):
        self.t += 1
        for k in self.params:
            if k in grads:
                grad = grads[k] + self.weight_decay * self.params[k]
                self.m[k] = self.beta1 * self.m[k] + (1 - self.beta1) * grad
                self.v[k] = self.beta2 * self.v[k] + (1 - self.beta2) * (grad ** 2)
                m_hat = self.m[k] / (1 - self.beta1 ** self.t)
                v_hat = self.v[k] / (1 - self.beta2 ** self.t)
                self.params[k] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
    
    def decay_lr(self):
        """学习率衰减"""
        self.lr *= self.lr_decay


# ============== 损失函数 ==============
def cross_entropy_loss(logits, labels):
    n = logits.shape[0]
    probs = softmax(logits)
    ce = -np.log(probs[np.arange(n), labels] + 1e-8)
    loss = np.mean(ce)
    grad = probs.copy()
    grad[np.arange(n), labels] -= 1
    return loss, grad

def compute_accuracy(logits, labels):
    return np.mean(np.argmax(logits, axis=1) == labels)


# ============== 训练 ==============
def train_epoch(model, optimizer, X, y, config):
    losses, accs = [], []
    n = X.shape[0]
    indices = np.arange(n)
    np.random.shuffle(indices)
    
    for i in range(0, n, config.batch_size):
        batch_idx = indices[i:i + config.batch_size]
        X_batch = X[batch_idx]
        y_batch = y[batch_idx]
        
        logits = model.forward(X_batch)
        loss, grad = cross_entropy_loss(logits, y_batch)
        acc = compute_accuracy(logits, y_batch)
        
        model.backward(grad)
        optimizer.step(model.grads)
        
        losses.append(loss)
        accs.append(acc)
        
        if (i // config.batch_size) % 50 == 0:
            print(f"  Batch {i//config.batch_size}, Loss: {loss:.4f}, Acc: {acc:.4f}")
    
    return np.mean(losses), np.mean(accs)


def validate(model, X, y, config):
    losses, accs = [], []
    n = X.shape[0]
    
    for i in range(0, n, config.batch_size):
        X_batch = X[i:i + config.batch_size]
        y_batch = y[i:i + config.batch_size]
        
        logits = model.forward(X_batch)
        loss, _ = cross_entropy_loss(logits, y_batch)
        acc = compute_accuracy(logits, y_batch)
        
        losses.append(loss)
        accs.append(acc)
    
    return np.mean(losses), np.mean(accs)


def plot_history(train_losses, val_losses, train_accs, val_accs):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    epochs = range(1, len(train_losses) + 1)
    ax1.plot(epochs, train_losses, 'b-', label='Train Loss')
    ax1.plot(epochs, val_losses, 'r-', label='Val Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(epochs, train_accs, 'b-', label='Train Acc')
    ax2.plot(epochs, val_accs, 'r-', label='Val Acc')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Training and Validation Accuracy')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'training_history.png')
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"训练曲线已保存到 {save_path}")


def main():
    print("=" * 60)
    print("ViT (Vision Transformer) 实现 - MNIST分类")
    print("=" * 60)
    
    config = Config()
    
    print("\n[1/5] 加载MNIST数据集...")
    X_full, y_full, X_test, y_test = load_mnist()
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_full, y_full, test_size=config.val_split, random_state=config.seed, stratify=y_full
    )
    print(f"训练集: {X_train.shape[0]}, 验证集: {X_val.shape[0]}")
    
    print("\n[2/5] 预处理数据...")
    train_patches, y_train_p = preprocess_data(X_train, y_train, config, augment=True)
    val_patches, y_val_p = preprocess_data(X_val, y_val, config, augment=False)
    test_patches, y_test_p = preprocess_data(X_test, y_test, config, augment=False)
    print(f"Patch数量: {config.img_size//config.patch_size}^2 = {train_patches.shape[1]}")
    
    print("\n[3/5] 初始化ViT模型...")
    model = ViT(config)
    n_params = sum(v.size for v in model.get_params().values() if isinstance(v, np.ndarray))
    print(f"模型参数数量: ~{n_params/1000:.1f}K")
    
    print("\n[4/5] 初始化AdamW优化器...")
    optimizer = AdamW(model.get_params(), lr=config.learning_rate, weight_decay=config.weight_decay, lr_decay=0.94)
    print(f"学习率: {config.learning_rate}, 每轮衰减: 0.94（衰减更慢，后期充分收敛）")
    
    print("\n[5/5] 开始训练...")
    print("=" * 60)
    
    train_losses, val_losses = [], []
    train_accs, val_accs = [], []
    best_val_acc = 0
    
    start_time = time.time()
    
    for epoch in range(config.epochs):
        print(f"\nEpoch {epoch + 1}/{config.epochs}")
        print("-" * 40)
        
        train_loss, train_acc = train_epoch(model, optimizer, train_patches, y_train_p, config)
        val_loss, val_acc = validate(model, val_patches, y_val_p, config)
        
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        train_accs.append(train_acc)
        val_accs.append(val_acc)
        
        print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
        print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
        print(f"当前学习率: {optimizer.lr:.6f}")
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"✓ 最佳验证准确率: {best_val_acc:.4f}")
        
        # 学习率衰减
        optimizer.decay_lr()
    
    print(f"\n训练完成! 总时间: {time.time() - start_time:.1f}s")
    
    _, test_acc = validate(model, test_patches, y_test_p, config)
    print(f"测试集准确率: {test_acc:.4f}")
    print(f"最佳验证准确率: {best_val_acc:.4f}")
    
    plot_history(train_losses, val_losses, train_accs, val_accs)
    
    print("\n" + "=" * 60)
    print("ViT MNIST分类任务完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
