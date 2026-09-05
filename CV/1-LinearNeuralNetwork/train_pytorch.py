import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from visualization import visualize_training

# 以脚本自身位置为基准定位数据，与运行时工作目录无关
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────── 数据处理 ────────────────────────────

def load_data(filepath):
    data = np.loadtxt(filepath, delimiter=',')
    return data[:, :2], data[:, 2].astype(np.int64)

def normalize(X):
    mean, std = X.mean(axis=0), X.std(axis=0)
    return (X - mean) / std, mean, std

# ─────────────────────────── 模型 ────────────────────────────

class LinearClassifier(nn.Module):
    """单层线性分类器（等价于手搓版的 W @ x + b）"""

    def __init__(self, input_dim=2, output_dim=2):
        super().__init__()
        self.linear = nn.Linear(input_dim, output_dim)
        # Xavier 初始化，与手搓版策略一致
        nn.init.xavier_normal_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)

    def forward(self, x):
        return self.linear(x)  # logits，CrossEntropyLoss 内部自带 softmax

def get_weights_as_numpy(model):
    """
    提取权重并整理为与 NumPy 版相同的 (3,2) 格式：
        行 0 → bias  (1, 2)
        行 1 → w_feat1
        行 2 → w_feat2
    供可视化模块绘制决策边界使用
    """
    W = model.linear.weight.detach().numpy().T  # (2, 2)：行=特征, 列=类别
    b = model.linear.bias.detach().numpy().reshape(1, -1)  # (1, 2)
    return np.vstack([b, W])  # (3, 2)

# ─────────────────────────── 训练 ────────────────────────────

def train_pytorch(filepath, epochs=200, lr=0.1):
    """
    PyTorch 验证版：训练至收敛（默认 200 epochs），不限制 epoch 数
    """
    print("=" * 60)
    print("线性二分类 —— PyTorch 验证版")
    print("=" * 60)

    # 加载 & 预处理
    X_raw, y_np = load_data(filepath)
    print(f"\n[数据]  N={len(y_np)},  类别0={np.sum(y_np == 0)},  类别1={np.sum(y_np == 1)}")
    X_norm, _, _ = normalize(X_raw)

    X_t = torch.from_numpy(X_norm).float()
    y_t = torch.from_numpy(y_np)

    # 模型 / 损失 / 优化器
    torch.manual_seed(0)
    model = LinearClassifier()
    criterion = nn.CrossEntropyLoss()  # 内置 softmax + 交叉熵
    optimizer = optim.SGD(model.parameters(), lr=lr)

    print(f"[模型]  {model}")
    print(f"[优化]  SGD，lr={lr}，epochs={epochs}（训练至收敛）")
    print("-" * 60)

    loss_history = []
    weights_history = []

    # 打印间隔：epoch 数 ≤ 20 则每轮打印，否则打印约 10 个节点
    print_interval = 1 if epochs <= 20 else max(1, epochs // 10)

    for epoch in range(epochs):
        # 前向传播
        logits = model(X_t)
        loss = criterion(logits, y_t)

        # 记录（在参数更新前，与手搓版时序一致）
        loss_history.append(loss.item())
        with torch.no_grad():
            weights_history.append(get_weights_as_numpy(model))

        # 反向传播 + 参数更新
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch == 0 or epoch == epochs - 1 or (epoch + 1) % print_interval == 0:
            with torch.no_grad():
                acc = (torch.argmax(logits, 1) == y_t).float().mean().item()
            print(f"Epoch [{epoch + 1:4d}/{epochs}]  Loss: {loss.item():.6f}  Acc: {acc * 100:.2f}%")

    print("-" * 60)
    with torch.no_grad():
        final_logits = model(X_t)
        final_acc = (torch.argmax(final_logits, 1) == y_t).float().mean().item()
    print(f"\n训练完成 | 最终 Loss={loss_history[-1]:.6f} | 最终 Acc={final_acc * 100:.2f}%")

    return X_norm, y_np, loss_history, weights_history

# ─────────────────────────── 入口 ────────────────────────────

if __name__ == "__main__":
    DATA_FILE = os.path.join(SCRIPT_DIR, 'binary_classification.txt')

    X_norm, y, loss_history, weights_history = train_pytorch(
        filepath=DATA_FILE,
        epochs=200,  # ← 充分训练至收敛，不受 10 epochs 限制
        lr=0.1
    )

    print("\n" + "=" * 60)
    print("可视化中...")
    visualize_training(
        X_norm, y, loss_history, weights_history,
        loss_filename='loss_curve_pytorch.png',
        boundary_filename='decision_boundary_pytorch.png',
        title_prefix='[PyTorch] '
    )
