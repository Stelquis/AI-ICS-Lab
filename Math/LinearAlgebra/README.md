<div align="center">

# 📐 Linear Algebra · 线性代数

### 🧱 第一级 · 数学与算法地基 · 核心数学

> 向量是一个点，矩阵是一场运动，特征值则告诉你——**在这场运动里，什么没有改变方向**。
>
> *当代 AI 的一切运算，归根到底都是矩阵乘法。*

[↑ 上一级](../README.md) · `Math` · Linear Algebra

</div>

---

## 🎯 为什么先学它

不是因为它排在教材第一章，而是因为**后面每一层都在调用它**：

| 你会遇到 | 底下站着的其实是 |
|---------|----------------|
| 反向传播 | 矩阵求导 + 链式法则 |
| `PCA` 降维 | 一次特征值分解 |
| `Attention` | 一堆矩阵乘法与 `Softmax` |
|  embeddings 检索 | 向量内积与余弦相似度 |
| 优化是否收敛 | 二次型与正定矩阵 |

跳过这一层，后面每一个概念都会变成"能用但说不清"。

---

## 🗺️ 范围 Scope

<details open>
<summary>📖 展开 · 核心内容</summary>

**🔹 基本对象**
- **标量 / 向量 / 矩阵 / 张量** — Scalar / Vector / Matrix / Tensor，及其基本运算
- **线性变换** — Linear Transformation：矩阵的本质不是一张数表，而是一场「运动」

**🔹 关键分解**
- **`SVD` 奇异值分解** — Singular Value Decomposition，降维与压缩的理论底座
- **特征分解** — Eigendecomposition；**特征值 Eigenvalue** 与 **特征向量 Eigenvector**

**🔹 下游衔接**
- **优化** — Optimization：二次型与正定矩阵，决定一个问题好不好解
- **降维** — `PCA` 背后的数学，就是一次特征值分解
- **反向传播** — 神经网络里的梯度，本质是矩阵求导的链式法则

</details>

---

## 📖 术语对照

<details>
<summary>🔤 展开 · 中英对照表</summary>

| 中文 | English |
|------|---------|
| 标量 / 向量 / 矩阵 / 张量 | Scalar / Vector / Matrix / Tensor |
| 转置 | Transpose |
| 逆矩阵 | Inverse Matrix |
| 行列式 | Determinant |
| 秩 | Rank |
| 线性变换 | Linear Transformation |
| 基 / 基变换 | Basis / Change of Basis |
| 特征值 / 特征向量 | Eigenvalue / Eigenvector |
| 特征分解 | Eigendecomposition |
| 奇异值分解 | Singular Value Decomposition (`SVD`) |
| 正交 | Orthogonal |
| 范数 | Norm |
| 内积 / 外积 | Inner Product / Outer Product |
| 二次型 / 正定 | Quadratic Form / Positive Definite |
| 最小二乘 | Least Squares |

</details>

---

## 🧪 原则

和 [`CV/`](../../CV/) 保持一致的三条：

- ✍️ **手写优先** — 核心运算先自己实现一遍，不依赖框架的自动求导
- 🔬 **对照验证** — 跑通后再与成熟库的结果对照，用数据检验直觉
- 🧱 **连回系统** — 每个概念都要回答一句：它在模型或系统里到底用在哪

---

<div align="center">

🚧 **建设中** — 第一个实验落地后，这里会长出目录结构与快速开始

*Linear Algebra · 把矩阵看成运动，而不是数表* 📐

</div>
