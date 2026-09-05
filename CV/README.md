# 📷 CV — 计算机视觉前沿技术

课程实验仓库。**不依赖任何深度学习框架的自动求导**，全部使用纯 NumPy 手写前向传播与反向传播，
从线性分类器一路实现到 Vision Transformer，配合课程课件、实验报告与技术报告，形成完整学习闭环。

## 🧪 实验一览

| 实验 | 主题 | 任务 | 实现 | 目录 |
|:---:|------|------|------|------|
| 一 | 线性神经网络与二分类 | 二维特征二分类 | NumPy + PyTorch 对照 | [`1-LinearNeuralNetwork/`](1-LinearNeuralNetwork/) |
| 二 | 多层感知机 (MLP) | MNIST 手写数字识别 | 纯 NumPy | [`2-MultilayerPerceptron/`](2-MultilayerPerceptron/) |
| 三 | Vision Transformer (ViT) | MNIST 手写数字识别 | 纯 NumPy | [`3-Transformer/`](3-Transformer/) |

## 📁 目录结构

```
CV/
├── 1-LinearNeuralNetwork/          # 实验一：线性神经网络
│   ├── train_numpy.py              #   NumPy 主实现（10 epochs, lr=0.1, SGD, Xavier, seed=42）
│   ├── train_numpy_s.py            #   NumPy 简化版（seed=0，便于对照初始化差异）
│   ├── train_pytorch.py            #   PyTorch 对照实现（200 epochs，训练至收敛）
│   ├── visualization.py            #   损失曲线 + 决策边界演化可视化
│   ├── binary_classification.txt   #   数据集：feature1, feature2, label
│   ├── loss_curve_*.png            #   损失曲线（numpy / numpy_s / pytorch）
│   ├── decision_boundary_*.png     #   决策边界演化图
│   └── 第一次实验报告.pdf
│
├── 2-MultilayerPerceptron/         # 实验二：多层感知机
│   ├── mlp_mnist_numpy.py          #   MLP 实现（784 → 256 → 10）
│   ├── mlp_training_curves.png     #   损失曲线 + 验证准确率曲线
│   ├── mnist_samples.png           #   MNIST 样本可视化
│   └── 第二次实验报告.pdf
│
├── 3-Transformer/                  # 实验三：Vision Transformer
│   ├── vit_numpy.py                #   ViT 实现（纯 NumPy，含 AdamW）
│   ├── training_history.png        #   训练 / 验证曲线
│   ├── result.txt                  #   完整训练日志（22 epochs）
│   ├── ViT.png                     #   模型结构图
│   └── 第三次实验报告.pdf
│
├── data/MNIST/                     # MNIST 数据集（IDX 原始格式）
│   ├── train-images.idx3-ubyte     #   训练集图像 60000 × 28 × 28
│   ├── train-labels.idx1-ubyte     #   训练集标签
│   ├── t10k-images.idx3-ubyte      #   测试集图像 10000 × 28 × 28
│   ├── t10k-labels.idx1-ubyte      #   测试集标签
│   └── test_mnist.py               #   IDX 格式读取示例（MnistDataloader）
│
├── files/                          # 课程课件 PDF
├── Paper/                          # 课程技术报告（Agentic AI 选题）
└── README.md
```

## 🚀 快速开始

### 环境依赖

```bash
pip install numpy matplotlib scikit-learn scipy   # 实验二、三必需
pip install torch torchvision                      # 仅实验一的 PyTorch 对照组需要
```

### 运行实验

所有脚本的数据集与输出图片路径均**以脚本自身位置为基准**解析，
因此在任意工作目录下直接运行都可以，结果始终写入对应实验目录：

```bash
# 实验一：线性神经网络（二分类，秒级完成）
python CV/1-LinearNeuralNetwork/train_numpy.py      # NumPy 实现
python CV/1-LinearNeuralNetwork/train_numpy_s.py    # NumPy 简化版
python CV/1-LinearNeuralNetwork/train_pytorch.py    # PyTorch 对照实现

# 实验二：多层感知机（MNIST，约 1 分钟）
python CV/2-MultilayerPerceptron/mlp_mnist_numpy.py

# 实验三：Vision Transformer（MNIST，CPU 上约 66 分钟）
python CV/3-Transformer/vit_numpy.py

# 附：MNIST IDX 格式读取示例
python CV/data/MNIST/test_mnist.py
```

## 🔍 实验详情

### 实验一：线性神经网络与二分类

**任务**：对二维特征做二分类，并用 PyTorch 实现交叉验证手推梯度是否正确。

**数据格式**：`binary_classification.txt` 每行 `feature1, feature2, label`（逗号分隔，`label ∈ {0, 1}`）。

**实现要点**：

- Z-score 标准化，并拼接全 1 列作为偏置项
- Softmax 激活 + 多分类交叉熵损失
- 解析梯度 `∂L/∂W = Xᵀ(P − Y) / N`，SGD 更新
- Xavier 初始化，固定随机种子保证可复现
- 可视化：损失曲线（标注起止点）+ 各 epoch 决策边界叠加演化

| 脚本 | epochs | lr | 说明 |
|------|:---:|:---:|------|
| `train_numpy.py` | 10 | 0.1 | 主实现，Xavier 初始化，seed=42 |
| `train_numpy_s.py` | 10 | 0.1 | 简化版，小随机初始化，seed=0 |
| `train_pytorch.py` | 200 | 0.1 | `nn.Linear` + `CrossEntropyLoss`，权重整理成与 NumPy 版一致的 `(3, 2)` 供可视化复用 |

**参考结果**（`train_numpy.py`，10 epochs）：

| 指标 | 数值 |
|------|------|
| 最终 Loss | 0.2689 |
| 最终准确率 | 96.25% |

### 实验二：多层感知机

**任务**：MNIST 手写数字识别。

**网络结构**：

```
输入层: 784 (28 × 28 展平)
   ↓  W1 (784 → 256)
隐藏层: 256 (ReLU)
   ↓  W2 (256 → 10)
输出层: 10  (Softmax)
```

**超参数**：`epochs = 30`，`lr = 0.1`，`batch_size = 128`，Xavier 初始化，seed=42。

> 为控制 NumPy 训练耗时，脚本按类别各随机采样 **30%** 数据（训练集 17995 / 验证集 2996）。

**实现要点**：

- 手写反向传播：输出层 `dZ₂ = (P − Y)/N`，隐藏层 `dZ₁ = (dZ₂ W₂ᵀ) ⊙ 1{Z₁ > 0}`
- 每轮随机打乱数据后小批量训练
- 直接解析 MNIST `.idx` 二进制格式（`struct` + `array`），不依赖 `torchvision`
- 输出训练损失曲线与验证准确率曲线

**参考结果**（CPU 上约 1 分钟）：

| 指标 | 数值 |
|------|------|
| 最终验证集准确率 | 94.96% |

### 实验三：Vision Transformer

**任务**：用纯 NumPy 实现 ViT 完成 MNIST 分类。

**模型配置**：

| 参数 | 取值 | 参数 | 取值 |
|------|------|------|------|
| `img_size` | 28 | `num_heads` | 4 |
| `patch_size` | 7（共 4² = 16 个 patch） | `mlp_ratio` | 2（FFN 隐藏层 288） |
| `hidden_size` | 144 | `num_blocks` | 2 |
| `num_classes` | 10 | `batch_size` | 96 |
| `epochs` | 22 | `learning_rate` | 0.001（每轮 ×0.94 衰减） |
| `weight_decay` | 0.001 | 参数量 | ≈ 345.2K |

**实现要点**：

- Patch Embedding + 可学习位置编码
- Multi-Head Self-Attention（缩放点积注意力）
- Transformer Encoder Block：LayerNorm + 残差连接 + FFN
- 手写 AdamW 优化器（含动量、二阶矩估计与权重衰减）
- 数据增强：随机水平翻转（p=0.2）、padding 后随机裁剪、缩放、亮度抖动（±10%）
- 训练 / 验证 / 测试三段划分（54000 / 6000 / 10000），按最佳验证准确率监控

**参考结果**（见 `result.txt`，CPU 训练 3952.6s）：

| 指标 | 数值 |
|------|------|
| 最佳验证准确率 | 78.62% |
| 测试集准确率 | 79.42% |

## 📚 课程资料

### 课件 PDF（`files/`）

| 文件 | 主题 |
|------|------|
| `第2章+线性神经网络.pdf` | 线性神经网络 |
| `第3章+多层感知机.pdf` | 多层感知机 |
| `第5章+注意力机制.pdf` | 注意力机制 |
| `第6章+Transformer.pdf` | Transformer |
| `第7章+PyTorch基本概念.pdf` | PyTorch 基础 |
| `第8章+强化学习核心概念.pdf` | 强化学习核心概念 |
| `第9章+LLM常用强化学习方法.pdf` | LLM 强化学习方法 |
| `第10章+扩散模型与流匹配.pdf` | 扩散模型与流匹配 |
| `pytorch-cheatsheet-en.pdf` / `pytorch_cheatsheet.png` | PyTorch 速查表 |

### 技术报告（`Paper/`）

课程技术报告选题为 **Agentic AI**，要求 5 页以内、包含深度分析与未来预测。

| 文件 | 说明 |
|------|------|
| `demo.md` | 技术报告撰写要求（评分标准） |
| `idea.md` | 选题复盘与最终立意 |
| `paper.md` | 报告正文（Markdown） |
| `paper.html` / `paper.png` | 报告排版成品 |
| `poster.png` | 汇报海报 |
| `references.md` | 参考文献 |
| `聊天框之外：Agentic AI 的下一种形态.pdf` | 最终报告 PDF |

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.12 |
| 核心实现 | NumPy（全部反向传播手写） |
| 框架对照 | PyTorch（仅实验一） |
| 数据处理 | NumPy / scikit-learn（`train_test_split`）/ SciPy（`ndimage.zoom`） |
| 可视化 | Matplotlib |
| 报告排版 | Markdown → HTML / XeLaTeX |

## 📄 协议

MIT License - 详见 [LICENSE](../LICENSE)
