# Manim — Python 数学动画引擎

## 概述

**Manim**（Mathematical Animation Engine）是一个基于 Python 的**编程式动画引擎**，专为创建精确、高质量的数学/技术解释视频而生。传统动画工具难以精确表达数学概念——Manim 通过 Python 代码来程序化生成动画，让你能精确控制每一帧的行为。

由 [3Blue1Brown](https://www.3blue1brown.com/) 的 Grant Sanderson 原创开发并开源，其频道上所有精美的数学科普视频均由 Manim 制作。本项目使用的是**社区维护版**（[Manim Community Edition](https://www.manim.community/)），它是从 3b1b/manim 分支出来的独立项目，由社区持续迭代。

> **注意**：Manim 存在两个不兼容的版本：3b1b 原始版（`manimgl`）和社区版（`manim`）。本项目使用社区版。

- 官网：https://www.manim.community/
- 文档：https://docs.manim.community/en/stable/
- 在线体验：https://try.manim.community/
- 源码：https://github.com/ManimCommunity/manim
- 协议：MIT

## 核心概念

Manim 的动画制作围绕三个核心概念展开：

### 1. Scene（场景）

Scene 是所有动画的容器。每个动画脚本就是一个继承自 `Scene` 的类，动画逻辑全部写在 `construct()` 方法中：

```python
from manim import *

class MyAnimation(Scene):
    def construct(self):
        # 所有动画代码写在这里
        pass
```

### 2. Mobject（数学对象）

Mobject 是 Manim 中**可显示在屏幕上的所有对象**的统称——圆形、正方形、文字、数学公式、坐标轴、箭头等都是 Mobject。Mobject 支持丰富的属性设置和变换操作：

```python
circle = Circle()                          # 创建圆形
circle.set_fill(PINK, opacity=0.5)         # 设置颜色和透明度
circle.set_stroke(BLUE, width=2)           # 设置边框
square = Square()                          # 创建正方形
square.next_to(circle, RIGHT, buff=0.5)    # 定位到圆形右侧
```

Mobject 的层次结构：

```
Mobject
├── VMobject（矢量图形）
│   ├── Circle / Square / Triangle / Rectangle / Polygon
│   ├── Line / Arrow / Vector / Arc
│   ├── Text / MarkupText / Paragraph
│   ├── MathTex / Tex / SingleStringMathTex
│   └── SVGMobject / Code
├── ImageMobject（图片）
├── Point（点）
├── ValueTracker（数值追踪器）
├── Axes / NumberLine / NumberPlane（坐标系）
└── Graph / DiGraph（图论）
```

### 3. Animation（动画）

Animation 定义了 Mobject 如何随时间变化。通过 `self.play()` 播放动画：

```python
self.play(Create(circle))                          # 绘制动画
self.play(Transform(square, circle))                # 形状变换
self.play(circle.animate.shift(UP * 2))             # .animate 语法
self.play(FadeOut(circle))                          # 淡出
self.play(Rotate(square, angle=PI / 2))             # 旋转
self.wait(1)                                        # 等待 1 秒
```

#### 常用动画类型

| 类别 | 动画 | 说明 |
|------|------|------|
| **创建/销毁** | `Create` / `Uncreate` / `Write` / `Unwrite` | 绘制/擦除对象 |
| | `FadeIn` / `FadeOut` | 淡入/淡出 |
| | `DrawBorderThenFill` | 先画边框再填充 |
| | `GrowFromCenter` / `GrowFromEdge` | 从中心/边缘生长 |
| **变换** | `Transform` / `ReplacementTransform` | 形状间变换 |
| | `FadeTransform` / `FadeTransformPieces` | 带淡入淡出的变换 |
| | `TransformFromCopy` | 从副本变换 |
| | `TransformMatchingShapes` / `TransformMatchingTex` | 匹配形状/公式变换 |
| **移动** | `shift` / `move_to` / `next_to`（通过 `.animate`） | 位移 |
| | `MoveAlongPath` | 沿路径移动 |
| **旋转** | `Rotate` / `Rotating` | 旋转 |
| **指示** | `Indicate` / `Flash` / `Circumscribe` / `Wiggle` | 高亮/闪烁/圈出/抖动强调 |
| **组合** | `AnimationGroup` / `LaggedStart` / `Succession` | 组合/错开/串联播放 |

#### .animate 语法

`.animate` 是 Manim 最强大的特性之一。在任意修改 Mobject 的方法前加 `.animate`，方法调用就变成了可播放的动画：

```python
# 静态设置（创建时直接应用）
circle = Circle().set_fill(PINK, opacity=0.5)

# 动态动画（在 self.play 中播放变化过程）
self.play(circle.animate.set_fill(BLUE, opacity=0.8).scale(2).shift(UP))
```

> **注意**：`.animate` 是通过对起始状态和结束状态做插值来实现的。当起始和结束状态相同时（如旋转 180° 的正方形），可能产生非预期的结果——此时应使用专门的动画类（如 `Rotate`）。

### 渲染流程

```
Python 脚本 (.py)
       │
       ▼
   Scene.construct()
       │  self.add()     → 创建 Mobject
       │  self.play()    → 执行 Animation
       │  self.wait()    → 暂停
       ▼
   Manim 渲染引擎
       │  Cairo  → 逐帧光栅化
       │  LaTeX  → 数学公式转 PNG
       │  Pango  → 文本渲染
       ▼
   单帧 PNG 序列
       │
       ▼
   FFmpeg 合成
       ▼
   输出 MP4 / GIF / PNG
```

### 数学公式渲染

Manim 通过 LaTeX 实现数学公式渲染。核心类：

```python
# 行内公式
tex = MathTex(r"E = mc^2")

# 多行公式
tex = MathTex(
    r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}",
    r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"
)

# 带颜色的公式
tex = MathTex(r"a^2", "+", r"b^2", "=", r"c^2")
tex.set_color_by_tex("a", RED)
tex.set_color_by_tex("b", GREEN)

# Tex 模板（适合需要自定义 preamble 的场景）
tex = Tex(r"\text{自定义 LaTeX 内容}")
```

## 快速入门

### 最小示例

```python
from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))
```

```bash
manim -pql script.py CreateCircle
```

### 形状变换

```python
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
```

### 坐标系绘图

```python
class PlotGraph(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE}
        )
        graph = axes.plot(lambda x: np.sin(x), color=RED)
        self.play(Create(axes), Create(graph))
```

### 3D 场景

```python
class ThreeDSurface(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
            u_range=[-3, 3], v_range=[-3, 3]
        )
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.play(Create(axes), Create(surface))
```

## 常用技巧

### 项目初始化

```bash
manim init project my-project --default
```

这会创建包含 `main.py` 和 `scene.py` 的项目目录，可直接开始开发。

### 输出质量控制

| 参数 | 分辨率 | 帧率 | 适用场景 |
|------|--------|------|----------|
| `-ql` | 854×480 | 15fps | 快速迭代调试 |
| `-qm` | 1280×720 | 30fps | 日常开发 |
| `-qh` | 1920×1080 | 60fps | 最终成品 |
| `-qk` | 3840×2160 | 60fps | 4K 超高清 |
| `-s` | — | — | 只输出最后一帧图片 |
| `-p` | — | — | 渲染后自动播放 |

### ValueTracker 实现动态更新

```python
class DynamicPlot(Scene):
    def construct(self):
        k = ValueTracker(-3)
        ax = Axes(x_range=[-5, 5], y_range=[-5, 5])
        graph = always_redraw(
            lambda: ax.plot(lambda x: k.get_value() * x, color=YELLOW)
        )
        self.add(ax, graph)
        self.play(k.animate.set_value(3), run_time=3)
```

### 组合动画与时间控制

```python
# 同时播放多个动画
self.play(Create(circle), FadeIn(square), run_time=2)

# 错开播放
self.play(LaggedStart(
    Create(circle), Create(square), Create(triangle),
    lag_ratio=0.5
))

# 串联播放
self.play(Succession(
    Indicate(circle), Indicate(square), Indicate(triangle)
))
```

---

## 附录 A：环境配置

### 安装方式

通过 `bash /workspace/scripts/init-manim.sh` 一键完成环境配置。

### Python 虚拟环境

| 项目 | 值 |
|------|-----|
| 路径 | `/opt/venv` |
| Python | 3.12.3 |
| 策略 | 检测到已有则复用，不存在则创建 |

### 系统依赖

| 包 | 用途 |
|----|------|
| `ffmpeg` | 视频编解码，帧序列合成视频 |
| `texlive-latex-recommended` | LaTeX 核心 + amsmath / amssymb 基础数学宏包 |
| `texlive-fonts-recommended` | 推荐字体集合 |
| `cm-super` | Computer Modern 高分辨率字体（避免渲染模糊） |
| `dvipng` | DVI → PNG 转换，数学公式渲染必需 |
| `pkg-config` | 编译时查找库依赖 |
| `libcairo2-dev` | Cairo 2D 图形库（pycairo 编译需要） |
| `libpango1.0-dev` | Pango 文本渲染（manimpango 编译需要） |

> TeX Live 版本为 **2023**（Ubuntu 24.04 LTS apt 源默认版本），对 Manim 完全够用。

### APT 镜像加速

```bash
APT_MIRROR="" bash /workspace/scripts/init-manim.sh         # 不换源
APT_MIRROR=mirrors.aliyun.com bash /workspace/scripts/init-manim.sh
```

### 环境检测逻辑

脚本通过**实际编译测试**验证 LaTeX 可用性（编译一个带 `amsmath` 的最小 tex 文件），而非仅检查命令是否存在。这能避免残缺安装（如残留二进制）导致的误判。

### 支持的平台

| 系统 | 包管理器 | 状态 |
|------|----------|------|
| Ubuntu / Debian | apt | 主要支持 |
| CentOS / Fedora / RHEL | yum / dnf | 支持 |
| Arch / Manjaro | pacman | 支持 |
| macOS | Homebrew | 支持 |

### 版本锁定

```bash
MANIM_VERSION=0.19.0 bash /workspace/scripts/init-manim.sh
```

---

## 附录 B：常见问题

| 问题 | 解决 |
|------|------|
| LaTeX Error | `apt install texlive-latex-extra` |
| ffmpeg 未找到 | `apt install ffmpeg` |
| 内存溢出 | 降低分辨率 `-ql`，减少画面内图形数量 |
| 中文乱码 | `apt install texlive-lang-chinese` |
| `.animate` 行为异常 | 改用专用动画类（如 `Rotate` 替代 `.animate.rotate`） |
| 渲染速度慢 | 调试阶段使用 `-ql`；拆分大场景为多个小场景 |
