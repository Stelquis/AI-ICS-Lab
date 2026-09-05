import os
import numpy as np
from visualization import visualize_training

# 以脚本自身位置为基准定位数据，与运行时工作目录无关
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据处理
def load_data(filepath):
    """读取 CSV，返回特征矩阵 X(N,2) 和标签 y(N,)"""
    data = np.loadtxt(filepath, delimiter=',')
    return data[:, :2], data[:, 2].astype(int)
def normalize(X):
    """Z-score 标准化"""
    mean, std = X.mean(axis=0), X.std(axis=0)
    return (X - mean) / std, mean, std
def add_bias(X):
    """拼接偏置列：(N,2) → (N,3)"""
    return np.hstack([np.ones((len(X), 1)), X])
#  核心组件
def softmax(z):
    """Softmax 激活函数"""
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)
def cross_entropy_loss(probs, y):
    """多分类交叉熵损失"""
    return -np.mean(np.log(probs[np.arange(len(y)), y] + 1e-15))
def compute_gradients(X, y, probs):
    """反向传播梯度"""
    N, C = len(y), probs.shape[1]
    one_hot = np.zeros((N, C))
    one_hot[np.arange(N), y] = 1.0
    return X.T @ (probs - one_hot) / N
#  训练
def train_numpy(filepath, epochs=10, lr=0.1):
    """纯 NumPy 线性分类器训练（默认10 epochs）"""
    # 加载 & 预处理
    X_raw, y = load_data(filepath)
    print(f"\n[数据]  N={len(y)},  类别0={np.sum(y == 0)},  类别1={np.sum(y == 1)}")
    X_norm, _, _ = normalize(X_raw)
    X = add_bias(X_norm)  # (N, 3)
    # Xavier 初始化
    np.random.seed(42)
    n_feat, n_cls = X.shape[1], 2
    W = np.random.randn(n_feat, n_cls) * np.sqrt(2.0 / n_feat)
    print(f"[模型]  W shape={W.shape}（含偏置行），Xavier 初始化，seed=42")
    print(f"[优化]  SGD，lr={lr}，epochs={epochs}")
    loss_history = []
    weights_history = []
    for epoch in range(epochs):
        # 前向传播
        probs = softmax(X @ W)
        loss = cross_entropy_loss(probs, y)
        # 在参数更新前记录（损失与权重对应同一时刻）
        loss_history.append(loss)
        weights_history.append(W.copy())
        # 反向传播 + SGD 更新
        W -= lr * compute_gradients(X, y, probs)
        acc = np.mean(np.argmax(probs, axis=1) == y)
        print(f"Epoch [{epoch + 1:2d}/{epochs}]  Loss: {loss:.6f}  Acc: {acc * 100:.2f}%")
    print("-" * 60)
    final_acc = np.mean(np.argmax(softmax(X @ W), axis=1) == y)
    print(f"\n训练完成 | 最终 Loss={loss_history[-1]:.6f} | 最终 Acc={final_acc * 100:.2f}%")
    return X_norm, y, loss_history, weights_history
# 入口
if __name__ == "__main__":
    DATA_FILE = os.path.join(SCRIPT_DIR, 'binary_classification.txt')
    X_norm, y, loss_history, weights_history = train_numpy(
        filepath=DATA_FILE,
        epochs=10,  # ← epochs
        lr=0.1
    )
    visualize_training(
        X_norm, y, loss_history, weights_history,
        loss_filename='loss_curve_numpy.png',
        boundary_filename='decision_boundary_numpy.png',
        title_prefix='[NumPy] '
    )