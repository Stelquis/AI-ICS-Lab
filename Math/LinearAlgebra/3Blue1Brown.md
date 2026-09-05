# 🎥 3Blue1Brown · 线性代数的本质

> *用几何直觉理解数学，而不是死记公式。*

---

## 📐 向量是什么

### 三种视角

向量是什么？取决于你问谁——

| 视角 | 向量是 | 典型场景 |
|------|--------|----------|
| **物理系** | 一支箭（有方向的量） | 力、速度、加速度 |
| **计算机系** | 一组有序的数 | `[3, 4, 5]` |
| **数学系** | 满足加法和数乘的"东西" | 向量空间中的元素 |

3Blue1Brown 的核心观点：**这三种视角不是矛盾，而是同一个东西的不同面向。**

---

### 视角一：物理学——箭头

向量是空间中的一支箭，从原点出发，指向某个点。

关键特征：
- **起点**不重要，重要的是**方向**和**长度**
- 把箭头平移到哪里，它还是同一个向量

---

### 视角二：计算机——一组数

向量是一列数字，用坐标描述"从原点走多远"。

比如这个向量：

$$
\vec{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}
$$

**读法**：这个向量有两个分量，第一个是 3，第二个是 4。

**含义**：从原点出发，**x 方向走 3**，**y 方向走 4**。

**写法**：
- 竖着写叫**列向量**：$\begin{bmatrix} 3 \\ 4 \end{bmatrix}$
- 横着写叫**行向量**：$\begin{bmatrix} 3 & 4 \end{bmatrix}$
- 用转置符号互相转换：$\begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} 3 & 4 \end{bmatrix}^T$

---

### 视角三：数学——向量空间

数学家不关心向量"长什么样"，只关心它**能不能做两件事**：

1. **加法**：两个向量相加，结果还是向量
2. **数乘**：一个数乘以一个向量，结果还是向量

满足这两条规则的任何"东西"，都可以叫向量。

---

### 向量加法：首尾相接

两个向量怎么加？**首尾相接**。

比如：

$$
\vec{u} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}, \quad
\vec{v} = \begin{bmatrix} 3 \\ 1 \end{bmatrix}
$$

**第一步**：分别看每个分量
- x 分量：$1 + 3 = 4$
- y 分量：$2 + 1 = 3$

**第二步**：写成新向量

$$
\vec{u} + \vec{v} = \begin{bmatrix} 1 + 3 \\ 2 + 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 3 \end{bmatrix}
$$

**几何直觉**：先走 $\vec{u}$（从原点走到 [1, 2]），再从终点走 $\vec{v}$（再走 [3, 1]），最终到达 [4, 3]。

---

### 数乘：拉伸或压缩

一个数乘以一个向量，是什么意思？

$$
c \cdot \vec{v} = c \cdot \begin{bmatrix} v_1 \\ v_2 \end{bmatrix} = \begin{bmatrix} c \cdot v_1 \\ c \cdot v_2 \end{bmatrix}
$$

**规则**：把每个分量都乘以这个数。

**例子**：

$$
2 \cdot \begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} 2 \times 3 \\ 2 \times 4 \end{bmatrix} = \begin{bmatrix} 6 \\ 8 \end{bmatrix}
$$

**几何直觉**：
- $c = 2$：向量变长 2 倍（拉伸）
- $c = 0.5$：向量变短一半（压缩）
- $c = -1$：向量方向反转（关于原点对称）

---

### 一句话总结

> **向量 = 从原点出发的运动 = 一组有序的数。**
>
> 加法是首尾相接，数乘是拉伸压缩。

---

## 🧩 线性组合：张成的空间与基

### 核心问题

> **给定两个向量，你能用它们"造出"哪些向量？**

---

### 线性组合 Linear Combination

给定两个向量 $\vec{v}$ 和 $\vec{w}$，以及两个数 $a$ 和 $b$：

$$
a\vec{v} + b\vec{w}
$$

就是 $\vec{v}$ 和 $\vec{w}$ 的一个**线性组合**。

**拆解每一步**：

1. $a\vec{v}$：把 $\vec{v}$ 拉伸 $a$ 倍
2. $b\vec{w}$：把 $\vec{w}$ 拉伸 $b$ 倍
3. 两者相加：首尾相接，得到新向量

**例子**：

$$
\vec{v} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
\vec{w} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
$$

取 $a = 3, b = 2$：

$$
3\vec{v} + 2\vec{w}
= 3\begin{bmatrix} 1 \\ 0 \end{bmatrix} + 2\begin{bmatrix} 0 \\ 1 \end{bmatrix}
= \begin{bmatrix} 3 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ 2 \end{bmatrix}
= \begin{bmatrix} 3 \\ 2 \end{bmatrix}
$$

**直觉**：用两个向量作为"原料"，通过拉伸和相加，制造新向量。

---

### 张成的空间 Span

所有可能的线性组合构成的集合，叫做这两个向量的**张成空间**（Span）。

$$
\text{Span}(\vec{v}, \vec{w}) = \{ a\vec{v} + b\vec{w} \mid a, b \text{ 是任意实数} \}
$$

**读法**：$\vec{v}$ 和 $\vec{w}$ 的 Span，是所有形如 $a\vec{v} + b\vec{w}$ 的向量的集合，其中 $a$ 和 $b$ 可以取任意实数。

#### 二维空间的情况

| 向量关系 | Span 是什么 | 直觉 |
|---------|-------------|------|
| 两个不共线的向量 | **整个二维平面** | 任意方向都能到达 |
| 两个共线的向量 | **一条直线** | 被锁在一条线上 |
| 其中一个是零向量 | **一条直线或原点** | 零向量没有贡献 |

**为什么两个不共线的向量能张成整个平面？**

因为通过调整 $a$ 和 $b$ 的值，可以到达平面上的任意一点。

---

### 基 Basis

**基**是一组向量，满足两个条件：

1. **线性无关**：谁都不是谁的"复制品"
2. **张成全空间**：它们的 Span 是整个空间

#### 标准基

二维空间最常见的基：

$$
\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
$$

**为什么叫"标准基"？** 因为它们分别指向 x 轴和 y 轴的正方向，长度都是 1。

**任何向量都能唯一地表示为基的线性组合**：

$$
\begin{bmatrix} 3 \\ 5 \end{bmatrix}
= 3\begin{bmatrix} 1 \\ 0 \end{bmatrix} + 5\begin{bmatrix} 0 \\ 1 \end{bmatrix}
= 3\vec{e}_1 + 5\vec{e}_2
$$

**系数 3 和 5 就是这个向量的坐标**。

---

### 线性相关与线性无关

#### 线性相关

如果一组向量中，某个向量可以由其他向量线性表示，就叫**线性相关**。

**例子**：

$$
\vec{v} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}, \quad
\vec{w} = \begin{bmatrix} 2 \\ 4 \end{bmatrix}
$$

注意到 $\vec{w} = 2\vec{v}$，所以它们**线性相关**。

**直觉**：$\vec{w}$ 是 $\vec{v}$ 的"复制品"，没有提供新信息。

#### 线性无关

如果一组向量中，没有任何一个可以由其他向量线性表示，就叫**线性无关**。

**例子**：

$$
\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
$$

$\vec{e}_1$ 不能由 $\vec{e}_2$ 表示（因为 $\vec{e}_2$ 没有 x 分量），反之亦然。所以它们**线性无关**。

**直觉**：每个向量都贡献了"新的方向"，没有冗余。

---

### 维数 Dimension

**维数** = 基中向量的个数

- 二维空间：需要 2 个基向量
- 三维空间：需要 3 个基向量
- n 维空间：需要 n 个基向量

---

### 一句话总结

> **线性组合是"用原料造新东西"，张成空间是"所有能造出来的东西"，基是"最少的、不冗余的原料"。**

---

## 🔄 矩阵与线性变换

### 核心观点

> **矩阵不是一张数表，而是一场「运动」。**

---

### 线性变换 Linear Transformation

**变换** = 函数：输入一个向量，输出另一个向量

**线性** = 满足两个条件：
1. **直线保持直线**：网格线不会弯曲
2. **原点保持不动**：原点不会跑掉

**直觉**：对空间进行"拉伸、旋转、剪切"，但不弯曲、不撕裂。

---

### 矩阵 = 线性变换的"配方"

一个 2×2 矩阵：

$$
A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}
$$

**第一列** $\begin{bmatrix} a \\ c \end{bmatrix}$ 是基向量 $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ 变换后的位置。

**第二列** $\begin{bmatrix} b \\ d \end{bmatrix}$ 是基向量 $\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ 变换后的位置。

**为什么？** 因为任何向量都能表示为基的线性组合，只要知道基变到哪，整个空间的变换就确定了。

#### 例子：旋转 90°

$$
R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
$$

**第一列** $\begin{bmatrix} 0 \\ 1 \end{bmatrix}$：$\vec{e}_1$ 从 x 轴正方向变成了 y 轴正方向。

**第二列** $\begin{bmatrix} -1 \\ 0 \end{bmatrix}$：$\vec{e}_2$ 从 y 轴正方向变成了 x 轴负方向。

这就是逆时针旋转 90°！

---

### 矩阵向量乘法的几何意义

给定矩阵 $A$ 和向量 $\vec{v} = \begin{bmatrix} v_1 \\ v_2 \end{bmatrix}$：

$$
A\vec{v} = v_1 \cdot (\text{第1列}) + v_2 \cdot (\text{第2列})
$$

**拆解**：

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \end{bmatrix}
= v_1 \begin{bmatrix} a \\ c \end{bmatrix} + v_2 \begin{bmatrix} b \\ d \end{bmatrix}
= \begin{bmatrix} av_1 + bv_2 \\ cv_1 + dv_2 \end{bmatrix}
$$

**直觉**：把向量的分量 $v_1, v_2$ 当作"权重"，对变换后的基向量做加权求和。

---

### 常见的线性变换

| 变换 | 矩阵 | 基向量去哪了 | 效果 |
|------|------|-------------|------|
| 旋转 θ | $\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$ | $\vec{e}_1 \to [\cos\theta, \sin\theta]^T$ | 整体旋转 |
| 缩放 | $\begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}$ | $\vec{e}_1 \to [s_x, 0]^T$ | 拉伸/压缩 |
| 剪切 | $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ | $\vec{e}_1 \to [1, 0]^T$（不动），$\vec{e}_2 \to [k, 1]^T$（被推） | 推斜 |
| 反射（x轴） | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ | $\vec{e}_2 \to [0, -1]^T$ | 上下翻转 |

---

### 一句话总结

> **矩阵的每一列，就是基向量变换后的位置。知道基去哪了，整个空间的变换就确定了。**

---

## 🔗 矩阵乘法与复合变换

### 核心问题

> **为什么矩阵乘法要那样定义？它和连续做两次变换有什么关系？**

---

### 复合变换

假设你想对空间做两次变换：
1. **先旋转**（矩阵 $R$）
2. **再缩放**（矩阵 $S$）

问：能不能用**一个矩阵** $M$ 代替这两步？

$$
M\vec{v} = S(R(\vec{v}))
$$

**答案**：$M = SR$

---

### 顺序很重要：从右往左读

| 表达式 | 含义 |
|--------|------|
| $SR$ | 先 R，后 S |
| $RS$ | 先 S，后 R |

一般情况下 $SR \neq RS$，变换顺序不同，结果不同。

---

### 为什么是 SR 而不是 RS？

**从右往左**应用变换。

$$
SR\vec{v} = S(R(\vec{v}))
$$

**读法**：先算 $R\vec{v}$（旋转），再对结果算 $S$（缩放）。

**为什么从右往左？** 因为函数的写法就是这样：$f(g(x))$ 是先算 $g(x)$，再算 $f$。

---

### 为什么矩阵乘法要那样定义？

矩阵的每一列是**基向量变换后的位置**。

做复合变换 $AB$ 时：

1. $B$ 先把基向量变到新位置：$\vec{e}_1 \to \vec{b}_1$，$\vec{e}_2 \to \vec{b}_2$
2. $A$ 再把这些新位置变到最终位置：$\vec{b}_1 \to A\vec{b}_1$，$\vec{b}_2 \to A\vec{b}_2$

所以 $AB$ 的第 $j$ 列 = $A$ 作用于 $B$ 的第 $j$ 列：

$$
AB = \begin{bmatrix} A\vec{b}_1 & A\vec{b}_2 \end{bmatrix}
$$

---

### 计算规则的由来

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}
\begin{bmatrix} e & f \\ g & h \end{bmatrix}
=
\begin{bmatrix} ae+bg & af+bh \\ ce+dg & cf+dh \end{bmatrix}
$$

**逐项拆解**：

- **第1列第1行**：$A$ 作用于 $B$ 的第1列 $\begin{bmatrix} e \\ g \end{bmatrix}$，取第1个分量 $ae + bg$
- **第2列第1行**：$A$ 作用于 $B$ 的第2列 $\begin{bmatrix} f \\ h \end{bmatrix}$，取第1个分量 $af + bh$
- **第1列第2行**：$A$ 作用于 $B$ 的第1列 $\begin{bmatrix} e \\ g \end{bmatrix}$，取第2个分量 $ce + dg$
- **第2列第2行**：$A$ 作用于 $B$ 的第2列 $\begin{bmatrix} f \\ h \end{bmatrix}$，取第2个分量 $cf + dh$

这不是人为规定的，而是**变换复合的自然结果**。

---

### 从二维到三维

前面的例子都是二维的，但矩阵乘法的逻辑**完全一样**。

**三维向量**有三个分量：

$$
\vec{v} = \begin{bmatrix} x \\ y \\ z \end{bmatrix}
$$

**三维基向量**有三个：

$$
\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \quad
\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \quad
\vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}
$$

**3×3 矩阵**的三列，分别对应三个基向量变换后的位置：

$$
A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
\quad \Rightarrow \quad
\begin{cases}
\vec{e}_1 \to \begin{bmatrix} a \\ d \\ g \end{bmatrix} \\
\vec{e}_2 \to \begin{bmatrix} b \\ e \\ h \end{bmatrix} \\
\vec{e}_3 \to \begin{bmatrix} c \\ f \\ i \end{bmatrix}
\end{cases}
$$

**三维矩阵向量乘法**：

$$
A\vec{v} = v_1 \cdot (\text{第1列}) + v_2 \cdot (\text{第2列}) + v_3 \cdot (\text{第3列})
$$

---

### 常见的三维变换

#### 绕 z 轴旋转 θ

$$
R_z(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

**为什么第三列是 $\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$？**

因为绕 z 轴旋转时，z 坐标不变，只有 x 和 y 在变化。所以 $\vec{e}_3$ 保持不动。

#### 绕 x 轴旋转 θ

$$
R_x(\theta) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta \\ 0 & \sin\theta & \cos\theta \end{bmatrix}
$$

**为什么第一列是 $\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}$？**

因为绕 x 轴旋转时，x 坐标不变，只有 y 和 z 在变化。所以 $\vec{e}_1$ 保持不动。

#### 绕 y 轴旋转 θ

$$
R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{bmatrix}
$$

**注意**：$-\sin\theta$ 在左下角，而不是右上角。这是因为 y 轴旋转的方向约定与其他轴不同。

---

### 三维复合变换

矩阵乘法在三维中同样适用：

$$
(R_y(90°) \cdot R_x(90°))\vec{v}
$$

**含义**：先绕 x 轴转 90°，再绕 y 轴转 90°。

**注意顺序**：从右往左读！

---

### 一句话总结

> **矩阵乘法 = 复合变换。$AB$ 意味着先 $B$ 后 $A$，计算规则只是这个几何事实的代数翻译。**
>
> **二维和三维本质相同：矩阵的列是基变换后的位置。**

---

## 📊 行列式

### 核心问题

> **一个线性变换，对面积（二维）或体积（三维）的缩放因子是多少？**

---

### 行列式的几何意义

**行列式 = 变换后面积（或体积）的缩放倍数**

**二维情况**：

想象一个 $1 \times 1$ 的正方形（面积 = 1），经过矩阵 $A$ 变换后，面积变成了多少？

答案就是 $\det(A)$。

**三维情况**：

想象一个 $1 \times 1 \times 1$ 的正方体（体积 = 1），经过矩阵 $A$ 变换后，体积变成了多少？

答案就是 $\det(A)$。

---

### 二维行列式的公式

对于 2×2 矩阵：

$$
A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}
$$

行列式：

$$
\det(A) = ad - bc
$$

**例子**：

$$
A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}
$$

$$
\det(A) = 2 \times 3 - 1 \times 0 = 6
$$

**几何意义**：这个变换把面积放大了 6 倍。

---

### 行列式的符号

| $\det(A)$ | 含义 |
|-----------|------|
| $> 1$ | 面积放大 |
| $= 1$ | 面积不变 |
| $0 < \det(A) < 1$ | 面积缩小 |
| $= 0$ | 空间被"压扁"了 |
| $< 0$ | 翻转了方向（镜像） |

**$\det(A) = 0$ 意味着什么？**

空间被压缩到更低维度了：
- 二维 → 一维（压成一条线）
- 三维 → 二维（压成一个面）

这样的矩阵叫**奇异矩阵**，它**不可逆**。

**$\det(A) < 0$ 意味着什么？**

变换翻转了空间的"手性"：
- 二维：把右手系变成了左手系（像照镜子）
- 三维：把右手系变成了左手系

**绝对值 $|\det(A)|$** 才是真正的缩放倍数，符号只表示有没有翻转。

---

### 行列式为零的直觉

为什么 $\det(A) = 0$ 意味着空间被压扁了？

**二维情况**：

$$
A = \begin{bmatrix} 2 & 4 \\ 1 & 2 \end{bmatrix}
$$

$$
\det(A) = 2 \times 2 - 4 \times 1 = 0
$$

**发生了什么？**

看矩阵的两列：
- 第1列：$\begin{bmatrix} 2 \\ 1 \end{bmatrix}$
- 第2列：$\begin{bmatrix} 4 \\ 2 \end{bmatrix} = 2 \times \begin{bmatrix} 2 \\ 1 \end{bmatrix}$

两列共线！整个平面被压成了一条线。

---

### 三维行列式的公式

对于 3×3 矩阵：

$$
A = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
$$

行列式：

$$
\det(A) = a(ei - fh) - b(di - fg) + c(dh - eg)
$$

**拆解**：

$$
\det(A) = a \cdot \det\begin{bmatrix} e & f \\ h & i \end{bmatrix}
         - b \cdot \det\begin{bmatrix} d & f \\ g & i \end{bmatrix}
         + c \cdot \det\begin{bmatrix} d & e \\ g & h \end{bmatrix}
$$

**规律**：沿着第一行展开，每个元素乘以它对应的 2×2 子行列式，正负交替。

---

### 行列式的性质

#### 性质 1：单位矩阵的行列式是 1

$$
\det(I) = 1
$$

**为什么？** 单位矩阵不做任何变换，面积（体积）不变。

#### 性质 2：乘积的行列式 = 行列式的乘积

$$
\det(AB) = \det(A) \cdot \det(B)
$$

**几何直觉**：先做 B 变换（缩放 $\det(B)$ 倍），再做 A 变换（缩放 $\det(A)$ 倍），总共缩放 $\det(A) \cdot \det(B)$ 倍。

#### 性质 3：转置不改变行列式

$$
\det(A^T) = \det(A)
$$

#### 性质 4：逆矩阵的行列式

$$
\det(A^{-1}) = \frac{1}{\det(A)}
$$

**为什么？** 因为 $A \cdot A^{-1} = I$，所以 $\det(A) \cdot \det(A^{-1}) = 1$。

---

### 行列式与可逆性

**矩阵可逆 $\Leftrightarrow$ 行列式不为零**

- $\det(A) \neq 0$：矩阵可逆，变换是"一对一"的
- $\det(A) = 0$：矩阵不可逆，空间被压扁了，信息丢失了

**为什么？**

如果 $\det(A) = 0$，说明变换把空间压到了更低维度，从低维度无法"还原"回高维度（就像把 3D 物体压成 2D 照片，无法从照片恢复 3D 形状）。

---

### 旋转矩阵的行列式

任何旋转矩阵的行列式都是 1：

$$
\det(R(\theta)) = 1
$$

**为什么？** 因为旋转不改变面积（体积），只是改变了方向。

---

### 一句话总结

> **行列式 = 面积（体积）的缩放因子。**
>
> - $\det(A) = 0$：空间被压扁，矩阵不可逆
> - $\det(A) < 0$：空间被翻转（镜像）
> - $|\det(A)|$：真正的缩放倍数

---

## 🔄 逆矩阵、列空间、秩和零空间

### 核心问题

> **方程组 $A\vec{x} = \vec{b}$ 什么时候有解？什么时候无解？解是什么？**

---

### 逆矩阵

**逆矩阵**是"撤销变换"的矩阵。

如果矩阵 $A$ 把 $\vec{x}$ 变成了 $\vec{b}$：

$$
A\vec{x} = \vec{b}
$$

那么逆矩阵 $A^{-1}$ 能把 $\vec{b}$ 变回 $\vec{x}$：

$$
A^{-1}\vec{b} = \vec{x}
$$

**性质**：

$$
A^{-1}A = I
$$

**什么时候存在逆矩阵？**

- $\det(A) \neq 0$：存在逆矩阵
- $\det(A) = 0$：不存在逆矩阵（空间被压扁，信息丢失了）

**例子**：

$$
A = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}, \quad
\det(A) = 2 \times 3 - 1 \times 1 = 5 \neq 0
$$

所以 $A$ 可逆。

$$
A^{-1} = \frac{1}{\det(A)} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
= \frac{1}{5} \begin{bmatrix} 3 & -1 \\ -1 & 2 \end{bmatrix}
$$

**验证**：

$$
A \cdot A^{-1} = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}
\cdot \frac{1}{5} \begin{bmatrix} 3 & -1 \\ -1 & 2 \end{bmatrix}
= \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = I
$$

---

### 列空间

**列空间** = 矩阵所有列向量的线性组合构成的集合。

$$
\text{Col}(A) = \text{Span}(\vec{a}_1, \vec{a}_2, \ldots, \vec{a}_n)
$$

**几何直觉**：

- 2×2 矩阵的列空间可能是：
  - 整个二维平面（如果两列不共线）
  - 一条直线（如果两列共线）
  - 原点（如果两列都是零向量）

- 3×3 矩阵的列空间可能是：
  - 整个三维空间
  - 一个平面
  - 一条直线
  - 原点

---

### 方程组 $A\vec{x} = \vec{b}$ 有解的条件

**有解 $\Leftrightarrow$ $\vec{b}$ 在列空间中**

**为什么？**

$$
A\vec{x} = x_1\vec{a}_1 + x_2\vec{a}_2 + \cdots + x_n\vec{a}_n = \vec{b}
$$

这意味着 $\vec{b}$ 可以表示为列向量的线性组合，即 $\vec{b}$ 在列空间中。

**例子**：

$$
A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}
$$

两列共线（第二列是第一列的 2 倍），列空间是一条直线。

如果 $\vec{b} = \begin{bmatrix} 3 \\ 6 \end{bmatrix}$（在这条直线上），方程组有解。

如果 $\vec{b} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$（不在这条直线上），方程组无解。

---

### 秩

**秩** = 列空间的维数

$$
\text{rank}(A) = \dim(\text{Col}(A))
$$

**秩的含义**：

| 秩 | 列空间 | 变换效果 |
|----|--------|----------|
| 秩 = 2（2×2矩阵） | 整个二维平面 | 没有降维 |
| 秩 = 1（2×2矩阵） | 一条直线 | 二维压成一维 |
| 秩 = 0（2×2矩阵） | 原点 | 二维压成原点 |

**秩的性质**：

- $\text{rank}(A) \leq \min(m, n)$（矩阵是 $m \times n$）
- $\text{rank}(A) = n$（列满秩）：列空间是整个空间，方程组一定有解
- $\text{rank}(A) < n$：列空间是子空间，方程组可能无解

---

### 零空间

**零空间** = 所有满足 $A\vec{x} = \vec{0}$ 的向量 $\vec{x}$ 的集合。

$$
\text{Null}(A) = \{ \vec{x} \mid A\vec{x} = \vec{0} \}
$$

**几何直觉**：

零空间是"被变换压成原点的所有向量"。

**例子**：

$$
A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}
$$

求零空间：

$$
\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}
= \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

展开：

$$
\begin{cases}
x_1 + 2x_2 = 0 \\
2x_1 + 4x_2 = 0
\end{cases}
$$

两个方程其实是一样的（第二个是第一个的 2 倍），所以：

$$
x_1 = -2x_2
$$

零空间是所有形如 $\begin{bmatrix} -2t \\ t \end{bmatrix}$ 的向量，其中 $t$ 是任意实数。

**零空间是一条直线**（通过原点）。

---

### 秩与零空间的关系

**秩-零化度定理**：

$$
\text{rank}(A) + \text{nullity}(A) = n
$$

其中：
- $\text{rank}(A)$：列空间的维数
- $\text{nullity}(A)$：零空间的维数
- $n$：矩阵的列数

**直觉**：

- 秩告诉你"输出空间有多大"
- 零化度告诉你"有多少信息被压缩掉了"
- 两者之和等于输入空间的维数

---

### 零空间的维数

零空间的维数 = 零空间中"自由变量"的个数。

**例子**：

$$
A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}
$$

零空间：$x_1 = -2x_2$，只有 $x_2$ 是自由变量。

所以零空间的维数 = 1。

验证：$\text{rank}(A) + \text{nullity}(A) = 1 + 1 = 2 = n$ ✓

---

### 方程组的解

方程组 $A\vec{x} = \vec{b}$ 的解有三种情况：

**情况 1：唯一解**

- $\text{rank}(A) = n$（列满秩）
- 零空间只有零向量
- 逆矩阵存在

**情况 2：无穷多解**

- $\text{rank}(A) < n$
- 零空间有非零向量
- 如果有解，解集是一个"平移的零空间"

**情况 3：无解**

- $\vec{b}$ 不在列空间中
- 方程组无解

---

### 一句话总结

> **逆矩阵撤销变换，列空间是有解的范围，秩是列空间的维数，零空间是被压成原点的向量。**
>
> - 有解 $\Leftrightarrow$ $\vec{b}$ 在列空间中
> - 唯一解 $\Leftrightarrow$ 零空间只有零向量
> - 无穷多解 $\Leftrightarrow$ 零空间有非零向量

---

### 非方阵：不同维度空间之间的线性变换

前面讨论的都是方阵（n×n），它把 n 维空间映射到 n 维空间。

但矩阵也可以是 **m×n**（m ≠ n），它把 **n 维空间映射到 m 维空间**。

---

#### 从低维到高维：m > n

**例子**：3×2 矩阵

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}
$$

这个矩阵把**二维向量**变换成**三维向量**：

$$
A \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}
= x_1 \begin{bmatrix} 1 \\ 3 \\ 5 \end{bmatrix}
+ x_2 \begin{bmatrix} 2 \\ 4 \\ 6 \end{bmatrix}
= \begin{bmatrix} x_1 + 2x_2 \\ 3x_1 + 4x_2 \\ 5x_1 + 6x_2 \end{bmatrix}
$$

**列空间是什么？**

两列是三维向量：

$$
\vec{a}_1 = \begin{bmatrix} 1 \\ 3 \\ 5 \end{bmatrix}, \quad
\vec{a}_2 = \begin{bmatrix} 2 \\ 4 \\ 6 \end{bmatrix}
$$

它们的线性组合是一个**平面**（如果两列不共线）或**直线**（如果两列共线）。

**秩是多少？**

- 如果两列不共线：$\text{rank}(A) = 2$（列空间是二维平面）
- 如果两列共线：$\text{rank}(A) = 1$（列空间是一条直线）

**几何直觉**：

二维空间被"映射"到三维空间中的一个平面上。输入是二维的，输出最多是二维的（不可能填满整个三维空间）。

---

#### 从高维到低维：m < n

**例子**：2×3 矩阵

$$
A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
$$

这个矩阵把**三维向量**变换成**二维向量**：

$$
A \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}
= x_1 \begin{bmatrix} 1 \\ 4 \end{bmatrix}
+ x_2 \begin{bmatrix} 2 \\ 5 \end{bmatrix}
+ x_3 \begin{bmatrix} 3 \\ 6 \end{bmatrix}
= \begin{bmatrix} x_1 + 2x_2 + 3x_3 \\ 4x_1 + 5x_2 + 6x_3 \end{bmatrix}
$$

**列空间是什么？**

三列是二维向量：

$$
\vec{a}_1 = \begin{bmatrix} 1 \\ 4 \end{bmatrix}, \quad
\vec{a}_2 = \begin{bmatrix} 2 \\ 5 \end{bmatrix}, \quad
\vec{a}_3 = \begin{bmatrix} 3 \\ 6 \end{bmatrix}
$$

它们的线性组合是：
- 整个二维平面（如果至少两列不共线）
- 一条直线（如果三列共线）
- 原点（如果三列都是零向量）

**秩是多少？**

- 如果至少两列不共线：$\text{rank}(A) = 2$（列空间是整个二维平面）
- 如果三列共线：$\text{rank}(A) = 1$（列空间是一条直线）

**几何直觉**：

三维空间被"压缩"到二维平面。信息丢失了，所以零空间不会只有零向量。

**零空间是什么？**

$$
\text{Null}(A) = \{ \vec{x} \in \mathbb{R}^3 \mid A\vec{x} = \vec{0} \}
$$

零空间是三维空间中的一个**子空间**（直线、平面或整个空间）。

秩-零化度定理：

$$
\text{rank}(A) + \text{nullity}(A) = 3
$$

- 如果 $\text{rank}(A) = 2$，则 $\text{nullity}(A) = 1$（零空间是一条直线）
- 如果 $\text{rank}(A) = 1$，则 $\text{nullity}(A) = 2$（零空间是一个平面）

---

#### 非方阵的逆矩阵

**非方阵没有逆矩阵**（因为维度不同，无法"撤销"变换）。

但可以定义**伪逆**（Moore-Penrose 伪逆）：

$$
A^+ = (A^TA)^{-1}A^T
$$

伪逆可以用来求**最小二乘解**（当方程组无解时，找最接近的解）。

---

#### 一句话总结

> **非方阵在不同维度空间之间映射。m×n 矩阵把 n 维空间映射到 m 维空间，列空间是输出空间的子空间，零空间是输入空间中被压成原点的向量。**
>
> - m > n：低维到高维，列空间最多是 n 维
> - m < n：高维到低维，信息丢失，零空间非平凡
> - 非方阵没有逆矩阵，但有伪逆

---

## 🎯 点积与对偶性

### 核心问题

> **点积的几何意义是什么？为什么它和投影有关？**

---

### 点积的定义

两个向量的**点积**（内积）定义为对应分量相乘再求和：

$$
\vec{u} \cdot \vec{v} = u_1 v_1 + u_2 v_2 + \cdots + u_n v_n
$$

**例子**：

$$
\vec{u} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}, \quad
\vec{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}
$$

$$
\vec{u} \cdot \vec{v} = 1 \times 3 + 2 \times 4 = 3 + 8 = 11
$$

**注意**：点积的结果是一个**数**，不是向量。

---

### 点积的几何意义

$$
\vec{u} \cdot \vec{v} = |\vec{u}| \cdot |\vec{v}| \cdot \cos\theta
$$

其中：
- $|\vec{u}|$：向量 $\vec{u}$ 的长度
- $|\vec{v}|$：向量 $\vec{v}$ 的长度
- $\theta$：两个向量之间的夹角

**拆解**：

$$
|\vec{v}| \cdot \cos\theta
$$

这是 $\vec{v}$ 在 $\vec{u}$ 方向上的**投影长度**。

所以：

$$
\vec{u} \cdot \vec{v} = |\vec{u}| \times (\text{v 在 u 方向上的投影长度})
$$

**直觉**：点积 = 一个向量的长度 × 另一个向量在它方向上的投影。

---

### 投影的几何意义

**投影** = 把一个向量"垂直落"到另一个向量上。

$$
\text{proj}_{\vec{u}}(\vec{v}) = \frac{\vec{u} \cdot \vec{v}}{|\vec{u}|^2} \vec{u}
$$

**拆解**：

1. $\vec{u} \cdot \vec{v}$：点积
2. $|\vec{u}|^2$：$\vec{u}$ 长度的平方
3. $\frac{\vec{u} \cdot \vec{v}}{|\vec{u}|^2}$：投影的"比例"
4. 乘以 $\vec{u}$：得到投影向量

**投影长度**（标量）：

$$
\text{proj length} = \frac{\vec{u} \cdot \vec{v}}{|\vec{u}|}
$$

---

### 点积的符号

| $\vec{u} \cdot \vec{v}$ | 含义 |
|------------------------|------|
| $> 0$ | 夹角 < 90°（方向大致相同） |
| $= 0$ | 夹角 = 90°（垂直） |
| $< 0$ | 夹角 > 90°（方向大致相反） |

**为什么？**

因为 $\cos\theta$：
- $\theta < 90°$：$\cos\theta > 0$
- $\theta = 90°$：$\cos\theta = 0$
- $\theta > 90°$：$\cos\theta < 0$

---

### 点积与垂直

**两个向量垂直 $\Leftrightarrow$ 点积为零**

$$
\vec{u} \perp \vec{v} \quad \Leftrightarrow \quad \vec{u} \cdot \vec{v} = 0
$$

**例子**：

$$
\vec{u} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
\vec{v} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
$$

$$
\vec{u} \cdot \vec{v} = 1 \times 0 + 0 \times 1 = 0
$$

所以 $\vec{u} \perp \vec{v}$（x 轴和 y 轴垂直）。

---

### 对偶性：点积与线性变换

**核心观点**：点积可以看作是一个**线性变换**。

给定向量 $\vec{u}$，定义函数：

$$
f(\vec{v}) = \vec{u} \cdot \vec{v}
$$

这个函数是**线性**的：

$$
f(\vec{v} + \vec{w}) = \vec{u} \cdot (\vec{v} + \vec{w}) = \vec{u} \cdot \vec{v} + \vec{u} \cdot \vec{w} = f(\vec{v}) + f(\vec{w})
$$

$$
f(c\vec{v}) = \vec{u} \cdot (c\vec{v}) = c(\vec{u} \cdot \vec{v}) = cf(\vec{v})
$$

**几何意义**：

这个函数把向量 $\vec{v}$ 映射到一个数（投影长度）。

---

### 1×n 矩阵：从 n 维到 1 维

一个 $1 \times n$ 矩阵：

$$
A = \begin{bmatrix} a_1 & a_2 & \cdots & a_n \end{bmatrix}
$$

它把 **n 维向量**映射到**1 维**（数）：

$$
A \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix}
= a_1 v_1 + a_2 v_2 + \cdots + a_n v_n
$$

**这和点积是一样的！**

$$
\begin{bmatrix} a_1 & a_2 & \cdots & a_n \end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix}
= \vec{a} \cdot \vec{v}
$$

---

### 对偶性

**对偶性** = 两个看似不同的东西，其实是同一个东西的两种视角。

**视角一：点积**

$$
\vec{u} \cdot \vec{v}
$$

是两个向量的运算，结果是一个数。

**视角二：线性变换**

$$
\begin{bmatrix} u_1 & u_2 \end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \end{bmatrix}
$$

是一个 $1 \times 2$ 矩阵作用于二维向量，结果是一个数。

**它们是同一个东西！**

---

### 对偶性的几何意义

向量 $\vec{u} = \begin{bmatrix} u_1 \\ u_2 \end{bmatrix}$ 可以有两种理解：

**理解一：空间中的一个点/箭头**

$$
\vec{u} = \begin{bmatrix} u_1 \\ u_2 \end{bmatrix}
$$

**理解二：一个线性变换（1×2 矩阵）**

$$
A = \begin{bmatrix} u_1 & u_2 \end{bmatrix}
$$

**对偶性**：每个向量都对应一个线性变换（投影），每个线性变换（1×n 矩阵）都对应一个向量。

---

### 为什么点积和投影有关？

因为点积**就是**投影变换的代数表达。

$$
\vec{u} \cdot \vec{v} = \text{（v 在 u 方向上的投影长度）} \times |\vec{u}|
$$

**从变换的角度**：

1. 把 $\vec{v}$ 投影到 $\vec{u}$ 方向上
2. 投影长度是一个数
3. 这个数就是点积（再除以 $|\vec{u}|$）

---

### 单位向量的点积

如果 $\vec{u}$ 是**单位向量**（$|\vec{u}| = 1$），那么：

$$
\vec{u} \cdot \vec{v} = \text{（v 在 u 方向上的投影长度）}
$$

**例子**：

$$
\vec{u} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
\vec{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}
$$

$$
\vec{u} \cdot \vec{v} = 1 \times 3 + 0 \times 4 = 3
$$

这就是 $\vec{v}$ 在 x 轴上的投影长度。

---

### 一句话总结

> **点积 = 投影。两个向量的点积，就是一个向量在另一个向量方向上的投影长度（再乘以后者的长度）。**
>
> **对偶性：向量和线性变换是同一个东西的两种视角。**

---

## ✖️ 叉积

### 核心问题

> **叉积的几何意义是什么？为什么它只在三维空间中有定义？**

---

### 叉积的定义

两个三维向量的**叉积**（外积）定义为：

$$
\vec{u} \times \vec{v} = \begin{bmatrix} u_2 v_3 - u_3 v_2 \\ u_3 v_1 - u_1 v_3 \\ u_1 v_2 - u_2 v_1 \end{bmatrix}
$$

**注意**：叉积的结果是一个**向量**，不是数。

**例子**：

$$
\vec{u} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}, \quad
\vec{v} = \begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix}
$$

$$
\vec{u} \times \vec{v} = \begin{bmatrix} 2 \times 6 - 3 \times 5 \\ 3 \times 4 - 1 \times 6 \\ 1 \times 5 - 2 \times 4 \end{bmatrix}
= \begin{bmatrix} 12 - 15 \\ 12 - 6 \\ 5 - 8 \end{bmatrix}
= \begin{bmatrix} -3 \\ 6 \\ -3 \end{bmatrix}
$$

---

### 叉积的几何意义

叉积的结果向量有两个重要性质：

#### 1. 方向：垂直于两个输入向量

$$
(\vec{u} \times \vec{v}) \perp \vec{u} \quad \text{且} \quad (\vec{u} \times \vec{v}) \perp \vec{v}
$$

**右手定则**：

1. 四指从 $\vec{u}$ 转向 $\vec{v}$（沿较小的角）
2. 大拇指指向的方向就是 $\vec{u} \times \vec{v}$ 的方向

#### 2. 长度：等于两个向量张成的平行四边形的面积

$$
|\vec{u} \times \vec{v}| = |\vec{u}| \cdot |\vec{v}| \cdot \sin\theta
$$

其中 $\theta$ 是两个向量之间的夹角。

**为什么？**

平行四边形的面积 = 底 × 高

- 底：$|\vec{u}|$
- 高：$|\vec{v}| \cdot \sin\theta$

所以面积 = $|\vec{u}| \cdot |\vec{v}| \cdot \sin\theta$

---

### 叉积与行列式的关系

叉积可以用行列式来记忆：

$$
\vec{u} \times \vec{v} = \det\begin{bmatrix} \hat{i} & u_1 & v_1 \\ \hat{j} & u_2 & v_2 \\ \hat{k} & u_3 & v_3 \end{bmatrix}
$$

其中 $\hat{i}, \hat{j}, \hat{k}$ 是标准基向量：

$$
\hat{i} = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \quad
\hat{j} = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \quad
\hat{k} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}
$$

**展开**：

$$
\vec{u} \times \vec{v} = \hat{i}(u_2 v_3 - u_3 v_2) - \hat{j}(u_1 v_3 - u_3 v_1) + \hat{k}(u_1 v_2 - u_2 v_1)
$$

**注意**：$\hat{j}$ 前面是**负号**。

---

### 叉积的性质

#### 性质 1：反交换律

$$
\vec{u} \times \vec{v} = -(\vec{v} \times \vec{u})
$$

**几何意义**：交换顺序，方向相反（右手定则反过来）。

#### 性质 2：叉积与自身为零

$$
\vec{u} \times \vec{u} = \vec{0}
$$

**为什么？**

- $\sin(0°) = 0$，所以长度为 0
- 方向不确定，所以是零向量

#### 性质 3：叉积与平行

如果 $\vec{u} \parallel \vec{v}$，那么：

$$
\vec{u} \times \vec{v} = \vec{0}
$$

**为什么？**

- $\sin(0°) = 0$ 或 $\sin(180°) = 0$，所以长度为 0

#### 性质 4：分配律

$$
\vec{u} \times (\vec{v} + \vec{w}) = \vec{u} \times \vec{v} + \vec{u} \times \vec{w}
$$

---

### 叉积与点积的对比

| 性质 | 点积 | 叉积 |
|------|------|------|
| 结果 | 数（标量） | 向量 |
| 适用维度 | 任意维度 | 只有三维 |
| 几何意义 | 投影长度 | 面积 + 法向量 |
| 交换律 | $\vec{u} \cdot \vec{v} = \vec{v} \cdot \vec{u}$ | $\vec{u} \times \vec{v} = -(\vec{v} \times \vec{u})$ |
| 自身 | $\vec{u} \cdot \vec{u} = \|\vec{u}\|^2$ | $\vec{u} \times \vec{u} = \vec{0}$ |

---

### 叉积的应用

#### 1. 求法向量

给定一个平面，知道平面上两个向量 $\vec{u}$ 和 $\vec{v}$，那么：

$$
\vec{n} = \vec{u} \times \vec{v}
$$

就是平面的**法向量**（垂直于平面的向量）。

#### 2. 判断方向

三个点 $A, B, C$ 的方向（顺时针还是逆时针）：

$$
\vec{AB} \times \vec{AC}
$$

- 如果 z 分量 > 0：逆时针
- 如果 z 分量 < 0：顺时针
- 如果 z 分量 = 0：共线

#### 3. 计算面积

平行四边形的面积：

$$
\text{Area} = |\vec{u} \times \vec{v}|
$$

三角形的面积：

$$
\text{Area} = \frac{1}{2} |\vec{u} \times \vec{v}|
$$

---

### 为什么叉积只在三维中有定义？

**二维情况**：

两个二维向量的"叉积"可以定义为：

$$
\vec{u} \times \vec{v} = u_1 v_2 - u_2 v_1
$$

结果是一个**数**，表示平行四边形的**有向面积**。

- 正值：$\vec{u}$ 到 $\vec{v}$ 是逆时针
- 负值：$\vec{u}$ 到 $\vec{v}$ 是顺时针

**七维情况**：

叉积在七维空间中也有定义，但性质不同。

**其他维度**：

叉积在其他维度中没有合适的定义，因为无法同时满足：
1. 结果垂直于两个输入向量
2. 长度等于平行四边形面积
3. 满足右手定则

---

### 一句话总结

> **叉积 = 垂直 + 面积。两个三维向量的叉积是一个垂直于它们的向量，长度等于它们张成的平行四边形面积。**
>
> - 方向：右手定则
> - 长度：$|\vec{u}| \cdot |\vec{v}| \cdot \sin\theta$
> - 反交换律：$\vec{u} \times \vec{v} = -(\vec{v} \times \vec{u})$

---

### 以线性变换的眼光看叉积

前面的叉积公式看起来很复杂，有没有更直观的理解方式？

**答案**：用**对偶性**。

---

#### 叉积的本质：一个函数

给定两个向量 $\vec{u}$ 和 $\vec{v}$，定义函数：

$$
f(\vec{w}) = \det\begin{bmatrix} w_1 & u_1 & v_1 \\ w_2 & u_2 & v_2 \\ w_3 & u_3 & v_3 \end{bmatrix}
$$

这个函数输入一个向量 $\vec{w}$，输出一个数（行列式）。

**几何意义**：这个行列式等于 $\vec{u}, \vec{v}, \vec{w}$ 三个向量张成的**平行六面体的有向体积**。

---

#### 这个函数是线性的

函数 $f(\vec{w})$ 是**线性**的：

$$
f(\vec{w} + \vec{x}) = f(\vec{w}) + f(\vec{x})
$$

$$
f(c\vec{w}) = cf(\vec{w})
$$

**为什么？** 因为行列式对每一行都是线性的。

---

#### 对偶性：从函数到向量

根据对偶性，这个线性函数 $f$ 可以表示为一个**向量的点积**：

$$
f(\vec{w}) = \vec{p} \cdot \vec{w}
$$

其中 $\vec{p}$ 是某个向量。

**这个向量 $\vec{p}$ 就是 $\vec{u} \times \vec{v}$！**

---

#### 为什么 $\vec{p}$ 垂直于 $\vec{u}$ 和 $\vec{v}$？

因为：

$$
f(\vec{u}) = \det\begin{bmatrix} u_1 & u_1 & v_1 \\ u_2 & u_2 & v_2 \\ u_3 & u_3 & v_3 \end{bmatrix} = 0
$$

（行列式有两行相同，所以为零）

同理：

$$
f(\vec{v}) = \det\begin{bmatrix} v_1 & u_1 & v_1 \\ v_2 & u_2 & v_2 \\ v_3 & u_3 & v_3 \end{bmatrix} = 0
$$

所以：

$$
\vec{p} \cdot \vec{u} = 0 \quad \text{且} \quad \vec{p} \cdot \vec{v} = 0
$$

即 $\vec{p}$ 垂直于 $\vec{u}$ 和 $\vec{v}$。

---

#### 为什么 $|\vec{p}|$ 等于平行四边形面积？

因为 $\vec{p}$ 的长度等于它在自己方向上的投影长度（因为它是单位方向的倍数）。

取 $\vec{w}$ 垂直于 $\vec{u}$ 和 $\vec{v}$，且 $|\vec{w}| = 1$，那么：

$$
f(\vec{w}) = \det\begin{bmatrix} w_1 & u_1 & v_1 \\ w_2 & u_2 & v_2 \\ w_3 & u_3 & v_3 \end{bmatrix} = \text{平行六面体体积}
$$

平行六面体体积 = 底面积 × 高

- 底面积：$\vec{u}$ 和 $\vec{v}$ 张成的平行四边形面积
- 高：$\vec{w}$ 在垂直方向的投影 = 1（因为 $\vec{w}$ 已经垂直于底面）

所以：

$$
f(\vec{w}) = \text{平行四边形面积}
$$

而：

$$
f(\vec{w}) = \vec{p} \cdot \vec{w} = |\vec{p}| \cdot |\vec{w}| \cdot \cos(0°) = |\vec{p}|
$$

所以 $|\vec{p}|$ = 平行四边形面积。

---

#### 叉积公式的由来

$$
\vec{u} \times \vec{v} = \vec{p} = \begin{bmatrix} u_2 v_3 - u_3 v_2 \\ u_3 v_1 - u_1 v_3 \\ u_1 v_2 - u_2 v_1 \end{bmatrix}
$$

**这个公式是怎么来的？**

把行列式按第一行展开：

$$
\det\begin{bmatrix} w_1 & u_1 & v_1 \\ w_2 & u_2 & v_2 \\ w_3 & u_3 & v_3 \end{bmatrix}
= w_1(u_2 v_3 - u_3 v_2) - w_2(u_1 v_3 - u_3 v_1) + w_3(u_1 v_2 - u_2 v_1)
$$

$$
= \begin{bmatrix} u_2 v_3 - u_3 v_2 \\ -(u_1 v_3 - u_3 v_1) \\ u_1 v_2 - u_2 v_1 \end{bmatrix}
\cdot \begin{bmatrix} w_1 \\ w_2 \\ w_3 \end{bmatrix}
$$

$$
= \begin{bmatrix} u_2 v_3 - u_3 v_2 \\ u_3 v_1 - u_1 v_3 \\ u_1 v_2 - u_2 v_1 \end{bmatrix}
\cdot \vec{w}
$$

所以：

$$
\vec{p} = \begin{bmatrix} u_2 v_3 - u_3 v_2 \\ u_3 v_1 - u_1 v_3 \\ u_1 v_2 - u_2 v_1 \end{bmatrix}
$$

---

#### 一句话总结

> **叉积可以看作是：给定 $\vec{u}$ 和 $\vec{v}$，定义一个线性函数 $f(\vec{w}) = \det[\vec{w}, \vec{u}, \vec{v}]$，这个函数对应一个向量 $\vec{p}$，它就是 $\vec{u} \times \vec{v}$。**
>
> - $\vec{p}$ 垂直于 $\vec{u}$ 和 $\vec{v}$（因为 $f(\vec{u}) = f(\vec{v}) = 0$）
> - $|\vec{p}|$ 等于平行四边形面积（因为 $f$ 在垂直方向的值 = 体积 = 面积）

---

## 🔄 基变换

### 核心问题

> **同一个向量，在不同的基（坐标系）下，坐标不同。如何转换？**

---

### 什么是基？

**基**是一组线性无关的向量，可以张成整个空间。

**标准基**（最常用的基）：

$$
\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
$$

**其他基**：

$$
\vec{b}_1 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}, \quad
\vec{b}_2 = \begin{bmatrix} -1 \\ 1 \end{bmatrix}
$$

这也是二维空间的一组基（因为两个向量不共线）。

---

### 同一个向量，不同的坐标

向量 $\vec{v}$ 在空间中是固定的，但它在不同基下的**坐标**不同。

**例子**：

$$
\vec{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}
$$

在标准基下，$\vec{v}$ 的坐标是 $[3, 2]^T$。

但如果用基 $\vec{b}_1 = [2, 1]^T, \vec{b}_2 = [-1, 1]^T$，$\vec{v}$ 的坐标是 $[a, b]^T$，满足：

$$
a\vec{b}_1 + b\vec{b}_2 = \vec{v}
$$

$$
a\begin{bmatrix} 2 \\ 1 \end{bmatrix} + b\begin{bmatrix} -1 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}
$$

展开：

$$
\begin{cases}
2a - b = 3 \\
a + b = 2
\end{cases}
$$

解得：$a = \frac{5}{3}, b = \frac{1}{3}$

所以 $\vec{v}$ 在新基下的坐标是 $[\frac{5}{3}, \frac{1}{3}]^T$。

---

### 基变换矩阵

**基变换矩阵** $P$ 的列是新基向量在旧基下的坐标。

**例子**：

新基：
$$
\vec{b}_1 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}, \quad
\vec{b}_2 = \begin{bmatrix} -1 \\ 1 \end{bmatrix}
$$

基变换矩阵：
$$
P = \begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}
$$

**作用**：把新基下的坐标转换为旧基下的坐标。

$$
\vec{v}_{\text{旧}} = P \vec{v}_{\text{新}}
$$

**例子**：

$$
\vec{v}_{\text{新}} = \begin{bmatrix} \frac{5}{3} \\ \frac{1}{3} \end{bmatrix}
$$

$$
\vec{v}_{\text{旧}} = P \vec{v}_{\text{新}}
= \begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}
\begin{bmatrix} \frac{5}{3} \\ \frac{1}{3} \end{bmatrix}
= \begin{bmatrix} 2 \times \frac{5}{3} + (-1) \times \frac{1}{3} \\ 1 \times \frac{5}{3} + 1 \times \frac{1}{3} \end{bmatrix}
= \begin{bmatrix} 3 \\ 2 \end{bmatrix}
$$

验证：结果和原来一样 ✓

---

### 逆基变换矩阵

如果想从旧基坐标转换到新基坐标，用 $P^{-1}$：

$$
\vec{v}_{\text{新}} = P^{-1} \vec{v}_{\text{旧}}
$$

**例子**：

$$
P = \begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}, \quad
\det(P) = 2 \times 1 - (-1) \times 1 = 3
$$

$$
P^{-1} = \frac{1}{3} \begin{bmatrix} 1 & 1 \\ -1 & 2 \end{bmatrix}
$$

$$
\vec{v}_{\text{新}} = P^{-1} \vec{v}_{\text{旧}}
= \frac{1}{3} \begin{bmatrix} 1 & 1 \\ -1 & 2 \end{bmatrix}
\begin{bmatrix} 3 \\ 2 \end{bmatrix}
= \frac{1}{3} \begin{bmatrix} 5 \\ 1 \end{bmatrix}
= \begin{bmatrix} \frac{5}{3} \\ \frac{1}{3} \end{bmatrix}
$$

验证：结果和之前算的一样 ✓

---

### 线性变换在不同基下的矩阵

同一个线性变换，在不同基下的**矩阵表示**不同。

**例子**：

在标准基下，旋转 90° 的矩阵是：

$$
R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
$$

如果用新基 $\vec{b}_1 = [2, 1]^T, \vec{b}_2 = [-1, 1]^T$，旋转 90° 的矩阵是什么？

**公式**：

$$
R_{\text{新}} = P^{-1} R P
$$

其中：
- $P$：基变换矩阵（新基在旧基下的坐标）
- $R$：变换在旧基下的矩阵
- $R_{\text{新}}$：变换在新基下的矩阵

**计算**：

$$
R_{\text{新}} = P^{-1} R P
= \frac{1}{3} \begin{bmatrix} 1 & 1 \\ -1 & 2 \end{bmatrix}
\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
\begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}
$$

先算 $RP$：

$$
RP = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
\begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}
= \begin{bmatrix} -1 & -1 \\ 2 & -1 \end{bmatrix}
$$

再算 $P^{-1}(RP)$：

$$
R_{\text{新}} = \frac{1}{3} \begin{bmatrix} 1 & 1 \\ -1 & 2 \end{bmatrix}
\begin{bmatrix} -1 & -1 \\ 2 & -1 \end{bmatrix}
= \frac{1}{3} \begin{bmatrix} 1 & -2 \\ 5 & -1 \end{bmatrix}
$$

---

### 相似矩阵

如果两个矩阵 $A$ 和 $B$ 满足：

$$
B = P^{-1} A P
$$

就称 $A$ 和 $B$ 是**相似矩阵**。

**几何意义**：$A$ 和 $B$ 表示**同一个线性变换**，只是在不同的基下。

**例子**：

$$
R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}, \quad
R_{\text{新}} = \frac{1}{3} \begin{bmatrix} 1 & -2 \\ 5 & -1 \end{bmatrix}
$$

它们是相似矩阵，都表示旋转 90°。

---

### 基变换的应用

#### 1. 对角化

如果矩阵 $A$ 可以相似对角化：

$$
A = P D P^{-1}
$$

其中 $D$ 是对角矩阵。

**好处**：
- 计算 $A^n$ 更容易：$A^n = P D^n P^{-1}$
- 对角矩阵的幂次很容易算

#### 2. 简化问题

有时候，在某个基下，变换的矩阵更简单（比如对角矩阵）。

通过基变换，可以简化计算。

---

### 一句话总结

> **基变换 = 换一个角度看问题。同一个向量、同一个变换，在不同基下有不同的坐标和矩阵表示。**
>
> - $\vec{v}_{\text{旧}} = P \vec{v}_{\text{新}}$
> - $R_{\text{新}} = P^{-1} R P$
> - 相似矩阵表示同一个变换

---

## 🎯 特征向量与特征值

### 核心问题

> **一个线性变换，有没有某些向量，变换后方向不变，只是被拉伸了？**

---

### 特征向量的定义

给定矩阵 $A$，如果存在非零向量 $\vec{v}$ 和数 $\lambda$，使得：

$$
A\vec{v} = \lambda \vec{v}
$$

那么：
- $\vec{v}$ 叫做 $A$ 的**特征向量**
- $\lambda$ 叫做对应的**特征值**

**几何意义**：

- 特征向量 $\vec{v}$：变换后**方向不变**的向量
- 特征值 $\lambda$：变换后被拉伸的**倍数**

**例子**：

$$
A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}
$$

检查 $\vec{v} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ 是不是特征向量：

$$
A\vec{v} = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 2 \\ 0 \end{bmatrix} = 2 \vec{v}
$$

是的！$\vec{v} = [1, 0]^T$ 是特征向量，对应的特征值 $\lambda = 2$。

---

### 为什么特征向量重要？

**1. 简化理解**

特征向量揭示了变换的"本质方向"——哪些方向只被拉伸，没有旋转。

**2. 简化计算**

如果知道所有特征向量和特征值，可以快速计算 $A^n$：

$$
A^n \vec{v} = \lambda^n \vec{v}
$$

**3. 对角化**

如果矩阵有 n 个线性无关的特征向量，可以写成：

$$
A = P D P^{-1}
$$

其中 $D$ 是对角矩阵（对角线是特征值），$P$ 的列是特征向量。

---

### 如何求特征值？

从 $A\vec{v} = \lambda \vec{v}$ 出发：

$$
A\vec{v} - \lambda \vec{v} = \vec{0}
$$

$$
(A - \lambda I)\vec{v} = \vec{0}
$$

如果 $\vec{v} \neq \vec{0}$，那么 $(A - \lambda I)$ 必须是**奇异矩阵**（行列式为零）：

$$
\det(A - \lambda I) = 0
$$

这就是**特征方程**。

**例子**：

$$
A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}
$$

$$
A - \lambda I = \begin{bmatrix} 2 - \lambda & 1 \\ 0 & 3 - \lambda \end{bmatrix}
$$

$$
\det(A - \lambda I) = (2 - \lambda)(3 - \lambda) - 0 = (2 - \lambda)(3 - \lambda)
$$

令行列式为零：

$$
(2 - \lambda)(3 - \lambda) = 0
$$

解得：$\lambda_1 = 2, \lambda_2 = 3$

---

### 如何求特征向量？

对每个特征值 $\lambda$，解方程：

$$
(A - \lambda I)\vec{v} = \vec{0}
$$

**例子**（续上）：

**$\lambda_1 = 2$**：

$$
(A - 2I)\vec{v} = \begin{bmatrix} 0 & 1 \\ 0 & 1 \end{bmatrix} \vec{v} = \vec{0}
$$

展开：$v_2 = 0$，$v_1$ 自由。

所以特征向量：$\vec{v}_1 = t \begin{bmatrix} 1 \\ 0 \end{bmatrix}$（$t$ 是任意非零数）

**$\lambda_2 = 3$**：

$$
(A - 3I)\vec{v} = \begin{bmatrix} -1 & 1 \\ 0 & 0 \end{bmatrix} \vec{v} = \vec{0}
$$

展开：$-v_1 + v_2 = 0$，即 $v_1 = v_2$。

所以特征向量：$\vec{v}_2 = t \begin{bmatrix} 1 \\ 1 \end{bmatrix}$（$t$ 是任意非零数）

---

### 特征值的几何意义

| 特征值 $\lambda$ | 含义 |
|-----------------|------|
| $\lambda > 1$ | 拉伸 |
| $\lambda = 1$ | 不变 |
| $0 < \lambda < 1$ | 压缩 |
| $\lambda = 0$ | 压成原点 |
| $\lambda < 0$ | 反向（翻转） |

**例子**：

- $\lambda = 2$：特征向量方向拉伸 2 倍
- $\lambda = -1$：特征向量方向反转（反射）
- $\lambda = 0$：整个方向被压成原点

---

### 特征多项式

特征方程 $\det(A - \lambda I) = 0$ 是一个关于 $\lambda$ 的多项式，叫做**特征多项式**。

**2×2 矩阵**：

$$
A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}
$$

特征多项式：

$$
\det(A - \lambda I) = (a - \lambda)(d - \lambda) - bc = \lambda^2 - (a+d)\lambda + (ad-bc)
$$

**迹和行列式**：

- $\text{tr}(A) = a + d$（迹 = 对角线元素之和）
- $\det(A) = ad - bc$

特征多项式可以写成：

$$
\lambda^2 - \text{tr}(A)\lambda + \det(A) = 0
$$

**根与系数的关系**（韦达定理）：

$$
\lambda_1 + \lambda_2 = \text{tr}(A)
$$

$$
\lambda_1 \cdot \lambda_2 = \det(A)
$$

---

### 特征值分解（对角化）

如果矩阵 $A$ 有 $n$ 个线性无关的特征向量，可以写成：

$$
A = P D P^{-1}
$$

其中：
- $P$：特征向量组成的矩阵（每列一个特征向量）
- $D$：特征值组成的对角矩阵

**好处**：

$$
A^n = P D^n P^{-1}
$$

对角矩阵的幂次很容易算：

$$
D^n = \begin{bmatrix} \lambda_1^n & 0 \\ 0 & \lambda_2^n \end{bmatrix}
$$

**例子**：

$$
A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}
$$

特征值：$\lambda_1 = 2, \lambda_2 = 3$

特征向量：$\vec{v}_1 = [1, 0]^T, \vec{v}_2 = [1, 1]^T$

$$
P = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}, \quad
D = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}
$$

验证：$A = P D P^{-1}$ ✓

---

### 没有足够特征向量的情况

有些矩阵**没有** $n$ 个线性无关的特征向量。

**例子**：

$$
A = \begin{bmatrix} 2 & 1 \\ 0 & 2 \end{bmatrix}
$$

特征多项式：$(2-\lambda)^2 = 0$，所以 $\lambda = 2$（重根）。

但特征向量只有 $[1, 0]^T$ 这一个方向，无法对角化。

这种情况叫**亏损矩阵**，需要用**若尔当标准型**。

---

### 特征值与稳定性

在动态系统中，特征值决定稳定性：

$$
\vec{x}_{n+1} = A \vec{x}_n
$$

**判断**：

- 所有 $|\lambda| < 1$：系统收敛到原点（稳定）
- 存在 $|\lambda| > 1$：系统发散（不稳定）
- $|\lambda| = 1$：临界状态

---

### 一句话总结

> **特征向量是变换中"方向不变"的向量，特征值是被拉伸的倍数。**
>
> - 求特征值：解 $\det(A - \lambda I) = 0$
> - 求特征向量：解 $(A - \lambda I)\vec{v} = \vec{0}$
> - 对角化：$A = P D P^{-1}$

---

## 🌌 抽象向量空间

### 核心问题

> **向量只能是数组吗？函数、多项式、矩阵算不算向量？**

---

### 从具体到抽象

前面讨论的向量都是**数组**：

$$
\vec{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}
$$

但线性代数的真正威力在于：**只要满足向量的两条规则，任何东西都可以是向量**。

---

### 向量空间的公理

一个**向量空间**是一个集合 $V$，其中的元素叫"向量"，满足以下规则：

#### 加法规则

1. **封闭性**：$\vec{u} + \vec{v} \in V$
2. **交换律**：$\vec{u} + \vec{v} = \vec{v} + \vec{u}$
3. **结合律**：$(\vec{u} + \vec{v}) + \vec{w} = \vec{u} + (\vec{v} + \vec{w})$
4. **零向量**：存在 $\vec{0}$，使得 $\vec{v} + \vec{0} = \vec{v}$
5. **负向量**：对每个 $\vec{v}$，存在 $-\vec{v}$，使得 $\vec{v} + (-\vec{v}) = \vec{0}$

#### 数乘规则

6. **封闭性**：$c\vec{v} \in V$
7. **分配律**：$c(\vec{u} + \vec{v}) = c\vec{u} + c\vec{v}$
8. **分配律**：$(c + d)\vec{v} = c\vec{v} + d\vec{v}$
9. **结合律**：$(cd)\vec{v} = c(d\vec{v})$
10. **单位元**：$1 \cdot \vec{v} = \vec{v}$

**直觉**：只要能做加法和数乘，且结果还在集合内，就是向量空间。

---

### 常见的向量空间

#### 1. $\mathbb{R}^n$：n 维实数组

$$
\mathbb{R}^2 = \left\{ \begin{bmatrix} x \\ y \end{bmatrix} \mid x, y \in \mathbb{R} \right\}
$$

这是最熟悉的向量空间。

#### 2. 多项式空间 $P_n$

所有次数不超过 $n$ 的多项式：

$$
P_n = \{ a_0 + a_1 x + a_2 x^2 + \cdots + a_n x^n \}
$$

**加法**：多项式相加

$$
(1 + 2x) + (3 + 4x) = 4 + 6x
$$

**数乘**：多项式乘以数

$$
3 \cdot (1 + 2x) = 3 + 6x
$$

**零向量**：零多项式 $0$

**维度**：$\dim(P_n) = n + 1$

**基**：$\{1, x, x^2, \ldots, x^n\}$

#### 3. 矩阵空间 $M_{m \times n}$

所有 $m \times n$ 矩阵：

$$
M_{2 \times 2} = \left\{ \begin{bmatrix} a & b \\ c & d \end{bmatrix} \mid a, b, c, d \in \mathbb{R} \right\}
$$

**加法**：矩阵相加

**数乘**：矩阵乘以数

**零向量**：零矩阵

**维度**：$\dim(M_{m \times n}) = m \times n$

#### 4. 函数空间

某些函数的集合也是向量空间。

**例子**：所有连续函数 $C[a, b]$

- **加法**：$(f + g)(x) = f(x) + g(x)$
- **数乘**：$(cf)(x) = c \cdot f(x)$
- **零向量**：零函数 $f(x) = 0$

**这是一个无限维空间！**

---

### 子空间

**子空间**是向量空间的一部分，本身也是向量空间。

**判断**：$W$ 是 $V$ 的子空间，当且仅当：
1. $W$ 非空（包含零向量）
2. 对加法封闭：$\vec{u}, \vec{v} \in W \Rightarrow \vec{u} + \vec{v} \in W$
3. 对数乘封闭：$\vec{v} \in W, c \in \mathbb{R} \Rightarrow c\vec{v} \in W$

**例子**：

$\mathbb{R}^3$ 中，通过原点的平面是子空间。

$$
W = \left\{ \begin{bmatrix} x \\ y \\ z \end{bmatrix} \mid x + y + z = 0 \right\}
$$

- 零向量满足 $0 + 0 + 0 = 0$ ✓
- 如果 $\vec{u}, \vec{v}$ 满足条件，$\vec{u} + \vec{v}$ 也满足 ✓
- 如果 $\vec{v}$ 满足条件，$c\vec{v}$ 也满足 ✓

---

### 线性变换的推广

线性变换可以定义在任何向量空间之间：

$$
T: V \to W
$$

满足：
- $T(\vec{u} + \vec{v}) = T(\vec{u}) + T(\vec{v})$
- $T(c\vec{v}) = cT(\vec{v})$

**例子**：导数是线性变换

$$
T(f) = f'
$$

- $(f + g)' = f' + g'$
- $(cf)' = cf'$

导数把多项式空间 $P_n$ 映射到 $P_{n-1}$。

---

### 同构

如果两个向量空间 $V$ 和 $W$ 之间存在一个**一一对应**的线性变换，就称它们**同构**。

$$
V \cong W
$$

**意义**：同构的向量空间"本质相同"，只是元素的"名字"不同。

**例子**：

- $P_2$（二次多项式空间）$\cong \mathbb{R}^3$

因为 $a + bx + cx^2$ 可以对应 $[a, b, c]^T$。

---

### 抽象的意义

为什么要抽象？

**1. 统一框架**

不同的数学对象（数组、多项式、矩阵、函数）可以用同一套语言描述。

**2. 推广结论**

在 $\mathbb{R}^n$ 中证明的定理，可以直接推广到其他向量空间。

**3. 实际应用**

- 信号处理：函数空间
- 量子力学：希尔伯特空间
- 机器学习：特征空间

---

### 一句话总结

> **向量空间 = 能做加法和数乘的任何集合。数组、多项式、矩阵、函数都可以是向量。**
>
> - 公理：封闭性、交换律、结合律、零向量、负向量
> - 子空间：向量空间的一部分，本身也是向量空间
> - 同构：本质相同的向量空间
