<div align="center">

# 📐 Math · 数学基础

### 🌱 地基有多深，树就能长多高

> 框架会过时、API 会更换，但 **向量、矩阵、梯度** 这些底层的东西不会。
>
> *看得穿原理的人，走到哪里都不慌。*

`Math` · Mathematical Foundations · 从公式到直觉

</div>

---

## 🧭 它在地图上的位置

仓库路线共五级，`Math` 守的是**第一级 · 数学与算法地基**里的「核心数学」——一切的起点，也是我们能走多远的底气。

> 🕳️ **先扎根**
> 我们愿意在「根」上多花笨功夫，而不是急着开枝散叶。
> 这一层不用急着求新，但一定要**求深**——地基打不牢，上面盖得越高越危险。

---

## 🗺️ 三个主题

<div align="center"><small>（每个主题都可点开 / 收起 ↓）</small></div>

### 📐 线性代数 · Linear Algebra

<details open>
<summary>🚧 建设中 · 展开看范围</summary>

- **向量 / 矩阵 / 张量** — Vector / Matrix / Tensor 及其基本运算
- **矩阵分解** — `SVD`、Eigenvalue / Eigenvector
- **下游衔接** — 优化、降维（`PCA`）、神经网络中的矩阵求导

👉 前往 [`LinearAlgebra/`](LinearAlgebra/)

</details>

### 🎲 概率与统计 · Probability & Statistics

<details>
<summary>📭 待建</summary>

随机变量、常见分布、`贝叶斯`、最大似然 → 理解不确定性与泛化。

</details>

### 📈 微积分与优化 · Calculus & Optimization

<details>
<summary>📭 待建</summary>

导数、梯度、链式法则 → 看懂反向传播与梯度下降；理解凸 / 非凸。

</details>

---

## 📏 结构说明

三个主题彼此**并列**，不是先后顺序，因此不做编号——区别于 [`CV/`](../CV/) 下按实验次序编号的目录。

| 中文 | English | 目录 | 状态 |
|------|---------|------|:----:|
| 线性代数 | Linear Algebra | [`LinearAlgebra/`](LinearAlgebra/) | 🚧 建设中 |
| 概率与统计 | Probability & Statistics | — | 📭 待建 |
| 微积分与优化 | Calculus & Optimization | — | 📭 待建 |

---

## 🧪 我们怎么做这一层

- ✍️ **手写优先** — 核心运算先自己实现一遍，不依赖框架的自动求导
- 🔬 **对照验证** — 跑通后再与成熟库的结果对照，用数据检验直觉
- 🧱 **连回系统** — 每个概念都要回答一句：它在模型或系统里到底用在哪

---

<div align="center">

*Math · 把公式磨成直觉，让直觉长出系统* 🌱

</div>
