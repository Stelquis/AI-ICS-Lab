"""
MLP MNIST 分类
"""

import numpy as np
import struct
from array import array
from os.path import join
import matplotlib.pyplot as plt
import os
import random

# ============================================
# 第1步：数据读取
# ============================================
print("第1步：读取 MNIST 数据集")

# 使用标准化的数据路径
input_path = '/workspace/data/MNIST'

# 文件路径
training_images_filepath = join(input_path, 'train-images.idx3-ubyte')
training_labels_filepath = join(input_path, 'train-labels.idx1-ubyte')
test_images_filepath = join(input_path, 't10k-images.idx3-ubyte')
test_labels_filepath = join(input_path, 't10k-labels.idx1-ubyte')

# 读取训练标签
with open(training_labels_filepath, 'rb') as file:
    magic, size = struct.unpack(">II", file.read(8))
    y_train_full = np.array(array("B", file.read()))
print(f"训练标签: {len(y_train_full)} 个")

# 读取训练图片
with open(training_images_filepath, 'rb') as file:
    magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
    image_data = array("B", file.read())
    x_train_full = np.array([np.array(image_data[i * 784:(i + 1) * 784])
                            for i in range(size)])
print(f"训练图片: {x_train_full.shape}")

# 读取测试标签
with open(test_labels_filepath, 'rb') as file:
    magic, size = struct.unpack(">II", file.read(8))
    y_test = np.array(array("B", file.read()))
print(f"测试标签: {len(y_test)} 个")

# 读取测试图片
with open(test_images_filepath, 'rb') as file:
    magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
    image_data = array("B", file.read())
    x_test = np.array([np.array(image_data[i * 784:(i + 1) * 784])
                    for i in range(size)])
print(f"测试图片: {x_test.shape}")

def show_images(images, title_texts, save_path):
    """显示图片列表并保存"""
    cols = 5
    rows = int(len(images) / cols) + 1
    plt.figure(figsize=(30, 20))
    index = 1
    for x in zip(images, title_texts):
        image = x[0]
        title_text = x[1]
        plt.subplot(rows, cols, index)
        plt.imshow(image, cmap=plt.cm.gray)
        if title_text != '':
            plt.title(title_text, fontsize=15)
        index += 1
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"可视化数据样本图片已保存到 {save_path}")

# 将 1D 向量转换为 28x28 图片用于显示
x_train_images = [x.reshape(28, 28) for x in x_train_full]
x_test_images = [x.reshape(28, 28) for x in x_test]

# 随机选择样本
images_2_show = []
titles_2_show = []

# 10 张训练集样本
for i in range(10):
    r = random.randint(1, 60000)
    images_2_show.append(x_train_images[r])
    titles_2_show.append(f'training [{r}] = {y_train_full[r]}')

# 5 张测试集样本
for i in range(5):
    r = random.randint(1, 10000)
    images_2_show.append(x_test_images[r])
    titles_2_show.append(f'test [{r}] = {y_test[r]}')

show_images(images_2_show, titles_2_show, './2-MultilayerPerceptron/mnist_samples.png')

# ============================================
# 第2步：数据采样（每类30%）
# ============================================
print("\n第2步：按类别采样 30%")

x_train_list, y_train_list = [], []
for cls in range(10):
    idx = np.where(y_train_full == cls)[0]
    n_sample = int(len(idx) * 0.3)
    x_train_list.append(x_train_full[idx[:n_sample]])
    y_train_list.append(y_train_full[idx[:n_sample]])
x_train = np.vstack(x_train_list)
y_train = np.hstack(y_train_list)
print(f"采样后训练集: {len(x_train)} 张")

x_val_list, y_val_list = [], []
for cls in range(10):
    idx = np.where(y_test == cls)[0]
    n_sample = int(len(idx) * 0.3)
    x_val_list.append(x_test[idx[:n_sample]])
    y_val_list.append(y_test[idx[:n_sample]])
x_val = np.vstack(x_val_list)
y_val = np.hstack(y_val_list)
print(f"采样后验证集: {len(x_val)} 张")

# ============================================
# 第3步：数据预处理
# ============================================
print("\n第3步：数据归一化")

x_train = x_train / 255.0
x_val = x_val / 255.0
print("像素值归一化到 [0, 1]")

# ============================================
# 第4步：定义网络参数
# ============================================
print("\n第4步：初始化网络参数")

np.random.seed(42)
input_size = 784
hidden_size = 256
output_size = 10

# Xavier 初始化
W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
b2 = np.zeros((1, output_size))

print(f"W1: {W1.shape}, b1: {b1.shape}")
print(f"W2: {W2.shape}, b2: {b2.shape}")
print("网络结构: 784 → 256 → 10")

# ============================================
# 第5步：定义激活函数和损失函数
# ============================================
print("\n第5步：定义激活函数和损失函数")

def relu(z):
    """ReLU: max(0, z)"""
    return np.maximum(0, z)

def relu_derivative(z):
    """ReLU 导数"""
    return (z > 0).astype(float)

def softmax(z):
    """Softmax"""
    z_shift = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_shift)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def cross_entropy_loss(probs, y):
    """交叉熵损失"""
    n = len(y)
    return -np.mean(np.log(probs[np.arange(n), y] + 1e-12))

print("激活函数: ReLU (隐藏层), Softmax (输出层)")
print("损失函数: 交叉熵")

# ============================================
# 第6步：训练
# ============================================
print("\n第6步：开始训练")  

epochs = 30
lr = 0.1
batch_size = 128
n_samples = len(x_train)

loss_history = []
val_acc_history = []

for epoch in range(epochs):
    # 打乱数据
    indices = np.random.permutation(n_samples)
    X_shuffled = x_train[indices]
    y_shuffled = y_train[indices]

    epoch_loss = 0
    n_batches = 0

    # 小批量训练
    for i in range(0, n_samples, batch_size):
        X_batch = X_shuffled[i:i + batch_size]
        y_batch = y_shuffled[i:i + batch_size]

        # 前向传播
        z1 = X_batch @ W1 + b1
        a1 = relu(z1)
        z2 = a1 @ W2 + b2
        probs = softmax(z2)

        # 计算损失
        loss = cross_entropy_loss(probs, y_batch)
        epoch_loss += loss
        n_batches += 1

        # 反向传播
        n = len(y_batch)
        y_onehot = np.zeros((n, 10))
        y_onehot[np.arange(n), y_batch] = 1

        # 输出层梯度
        dz2 = (probs - y_onehot) / n
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        # 隐藏层梯度
        da1 = dz2 @ W2.T
        dz1 = da1 * relu_derivative(z1)
        dW1 = X_batch.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # 更新参数
        W1 -= lr * dW1
        b1 -= lr * db1
        W2 -= lr * dW2
        b2 -= lr * db2

    # 记录损失
    avg_loss = epoch_loss / n_batches
    loss_history.append(avg_loss)

    # 验证集准确率
    z1_val = x_val @ W1 + b1
    a1_val = relu(z1_val)
    z2_val = a1_val @ W2 + b2
    probs_val = softmax(z2_val)
    val_pred = np.argmax(probs_val, axis=1)
    val_acc = np.mean(val_pred == y_val)
    val_acc_history.append(val_acc)

    if (epoch + 1) % 5 == 0:
        print(f"Epoch [{epoch + 1:2d}/{epochs}] Loss: {avg_loss:.4f} Val Acc: {val_acc * 100:.2f}%")

# ============================================
# 第7步：结果可视化
# ============================================
print("\n第7步：绘制训练曲线")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 损失曲线
ax1.plot(loss_history, 'b-', linewidth=2)
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('Training Loss Curve')
ax1.grid(True, alpha=0.3)

# 准确率曲线
ax2.plot(np.array(val_acc_history) * 100, 'r-', linewidth=2)
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy (%)')
ax2.set_title('Validation Accuracy Curve')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('./2-MultilayerPerceptron/mlp_training_curves.png', dpi=150)
plt.close()
print("训练曲线已保存到 MultilayerPerceptron/mlp_training_curves.png")

# ============================================
# 最终结果
# ============================================
print("\n第8步：最终结果")
print(f"最终验证集准确率: {val_acc_history[-1] * 100:.2f}%")