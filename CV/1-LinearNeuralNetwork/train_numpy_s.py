import os
import numpy as np
from visualization import visualize_training

# 以脚本自身位置为基准定位数据，与运行时工作目录无关
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data(path):
    data = np.loadtxt(path, delimiter=',')
    return data[:, :2], data[:, 2].astype(int)
def normalize_data(X):
    mu = X.mean(axis=0)
    sigma = X.std(axis=0)
    return (X - mu) / sigma
def softmax(z):
    z_shift = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_shift)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)
def cross_entropy(p, y):
    n = len(y)
    return -np.mean(np.log(p[np.arange(n), y] + 1e-12))
def gradient(X, y, p):
    n, c = len(y), p.shape[1]
    y_onehot = np.zeros((n, c))
    y_onehot[np.arange(n), y] = 1
    return X.T @ (p - y_onehot) / n
def train(path, epochs=10, lr=0.1):
    X_raw, y = load_data(path)
    X = normalize_data(X_raw)
    X_bias = np.column_stack([np.ones(len(X)), X])
    n_features, n_classes = X_bias.shape[1], 2
    np.random.seed(0)
    W = np.random.randn(n_features, n_classes) * 0.01
    losses = []
    weights = []
    for i in range(epochs):
        z = X_bias @ W
        probs = softmax(z)
        loss = cross_entropy(probs, y)
        losses.append(loss)
        weights.append(W.copy())
        grad = gradient(X_bias, y, probs)
        W = W - lr * grad
    return X, y, losses, weights

X, y, losses, weights = train(os.path.join(SCRIPT_DIR, 'binary_classification.txt'), epochs=10, lr=0.1)
visualize_training(X, y, losses, weights, 'loss_curve_numpy_s.png', 'decision_boundary_numpy_s.png', '[NumPyS] ')