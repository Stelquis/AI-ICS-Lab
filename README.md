# AI-ICS-Lab

计算机视觉前沿技术课程实验仓库，通过纯 NumPy 实现深度学习核心算法，深入理解计算机视觉模型原理。

## 📋 项目概述

本仓库包含课程核心实验的完整实现：

| 实验 | 主题 | 实现方式 |
|:---:|------|---------|
| 1 | 线性神经网络与二分类 | NumPy + PyTorch |
| 2 | 多层感知机 (MLP) | NumPy |
| 3 | 注意力机制 | 理论学习 |
| 4 | Vision Transformer (ViT) | NumPy |

## 🧠 核心理念   

**纯 NumPy 实现**：不依赖任何深度学习框架，从零实现神经网络、注意力机制等核心算法，夯实理论基础。

## 📁 项目结构

```
AI-ICS-Lab/
├── 1-LinearNeuralNetwork/      # 实验一：线性神经网络
│   ├── train_numpy.py           # NumPy 实现
│   ├── train_pytorch.py         # PyTorch 对比实现
│   ├── visualization.py         # 可视化工具
│   ├── binary_classification.txt
│   └── *.png                    # 损失曲线、决策边界图
│
├── 2-MultilayerPerceptron/      # 实验二：多层感知机
│   └── mlp_mnist_numpy.py       # MLP 实现 (784→256→10)
│
├── 3-AttentionMechanism/         # 实验三：注意力机制
│   └── 注意力机制.pdf
│
├── 4-Transformer/               # 实验四：Vision Transformer
│   └── vit_numpy.py             # ViT 实现 (纯 NumPy)
│
├── data/MNIST/                  # MNIST 数据集
│   ├── train-images.idx3-ubyte
│   ├── train-labels.idx1-ubyte
│   ├── t10k-images.idx3-ubyte
│   └── t10k-labels.idx1-ubyte
│
├── file/                        # 报告模板
├── scripts/                    # 初始化脚本
├── Dockerfile                  # Docker 镜像配置
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.12+
- NumPy
- Matplotlib
- scikit-learn

### 运行实验

```bash
# 实验一：线性神经网络
cd 1-LinearNeuralNetwork
python train_numpy.py        # NumPy 实现
python train_pytorch.py      # PyTorch 实现

# 实验二：多层感知机
cd 2-MultilayerPerceptron
python mlp_mnist_numpy.py

# 实验四：Vision Transformer
cd 4-Transformer
python vit_numpy.py
```

## 📊 实验详情

### 实验一：线性神经网络

**任务**：二分类任务，对比 NumPy 和 PyTorch 实现

**实现要点**：
- Softmax 激活函数
- 交叉熵损失
- SGD 优化器
- Xavier 初始化
- 损失曲线与决策边界可视化

### 实验二：多层感知机

**任务**：MNIST 手写数字识别

**网络结构**：
```
输入层: 784 (28×28)
  ↓
隐藏层: 256 (ReLU)
  ↓
输出层: 10 (Softmax)
```

**实现要点**：
- 完整的反向传播推导
- 小批量训练 (batch_size=128)
- MNIST `.idx` 格式数据读取

### 实验四：Vision Transformer

**任务**：使用纯 NumPy 实现 ViT 进行 MNIST 分类

**网络配置**：
```python
img_size = 28
patch_size = 7
hidden_size = 144
num_heads = 4
num_blocks = 2
```

**实现要点**：
- Patch Embedding 与位置编码
- Multi-Head Self-Attention
- Transformer Encoder Block
- Layer Normalization + Residual Connection
- AdamW 优化器
- 数据增强 (Random Crop, Flip)

## 🔧 技术栈

| 类别 | 技术 |
|-----|------|
| 语言 | Python 3.12 |
| 核心实现 | NumPy (纯手写反向传播) |
| 框架对比 | PyTorch |
| 可视化 | Matplotlib |
| 工具 | Docker, VS Code |

## 📄 协议

MIT License - 详见 [LICENSE](LICENSE)
