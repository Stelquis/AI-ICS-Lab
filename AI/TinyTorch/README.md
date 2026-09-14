<div align="center">

# 🔥 TinyTorch

### 🧱 别只用框架，亲手把它造出来

> 🎓 哈佛大学 **CS249r**（机器学习系统）课程的教学框架
> 📦 用纯 **NumPy** 从零搭一个「能跑起来」的深度学习框架
> 🚀 终点：训练 CNN 做图像分类、跑通 GPT 式语言模型

`User` → `Builder` · 从「会用」到「会造」 · 20 个渐进模块 · 从 Demo 到系统

</div>

---

## 🤔 这到底是什么？

大多数机器学习课程教你**怎么用**框架：

```python
import torch
model.fit(X, y)   # ✨ 魔法发生了——但为什么？
```

TinyTorch 反过来，教你**怎么造**框架：

```python
# 🧱 张量、激活、层、损失、数据加载器
# 🔁 自动求导、优化器、训练循环
# 👁️ 卷积、CNN、注意力、Transformer
# ⚡ 性能剖析、量化、剪枝、加速、基准测试
# —— 每一块都是你自己写的代码
```

它的定位很朴素：**AI 的砖块（AI Bricks）** 🧱

| 🪶 小到能学明白 | 🏗️ 大到能说明问题 |
|:---:|:---:|
| 每一块代码都短小、可读，树莓派上都能跑 | 完整呈现真实框架的架构与取舍 |

> 💡 一句总结：**别人给你鱼，它教你怎么织网。** 甚至——怎么造出一台能出鱼的机器。🐟

---

## 🎯 学完能做出什么

**🌟 北极星目标：从零训练 CNN 做图像分类**
- 在标准基准数据集上做真实的计算机视觉
- 只用 NumPy，不依赖 PyTorch / TensorFlow
- 性能足以和现代框架掰掰手腕

**🎁 附带能力**
- 🤖 GPT 风格的语言模型（注意力机制）
- 📉 现代优化器（SGD / Adam）+ 学习率调度
- ⚡ 性能剖析、优化与竞速基准

---

## 🗂️ 目录结构

> 本 README 位于 `AI/TinyTorch/`，真正的代码全在它下面的 `tinytorch/` 子目录里；
> 下面省略了这个前缀，只展示 `tinytorch/` 内部。

```text
tinytorch/
├── src/                    # 💻 模块源码（20 个模块，唯一「真理源」）
│   ├── 01_tensor/          #    01_tensor.py + module.yaml
│   ├── 02_activations/
│   ├── ...
│   └── 20_capstone/
│
├── modules/                # 📓 学生用的 Notebook（由 tito 现场生成）
│   └── README.md           #    初始只有一个 README —— 这是正常的 ✅
│
├── tinytorch/              # 📦 框架包（由 tito 逐模块导出到这里）
│   └── core/               #    初始只有 __init__.py —— 这是正常的 ✅
│
├── tito/                   # 🎛️ 工作流 CLI（setup / export / test / milestone ...）
├── milestones/             # 🏆 六个「历史里程碑」复现实验
├── datasets/               # 🗃️ 自带 tinydigits / tinytalks，无需额外下载 ✅
├── tests/                  # ✅ 模块测试、CLI 测试、集成测试
├── tools/                  # 🔧 发布校验与参考实现比对脚本
├── quarto/                 # 🌐 课程网站与文档（Quarto）
│   └── install.sh          # ⚠️ 请勿直接执行，见文末说明
│
├── requirements.txt
├── pyproject.toml
├── Makefile
└── README.md
```

📌 **核心工作流一句话**：

```text
src/*.py  ──(tito export)──▶  modules/*.ipynb  ──(你来实现)──▶  tinytorch/*.py
   教材源码                       你的练习本                        你造的框架
```

**目录里的"空"并不代表出错** 🙌

| 现象 | 原因 |
|:---|:---|
| `modules/` 下只有一个 `README.md` | 学生用的 notebook 由 `tito` 现场生成 |
| `tinytorch/core/` 下只有一个 `__init__.py` | 框架包由 `tito` 逐模块导出 |
| `datasets/` 里已有 `tinydigits`、`tinytalks` | 数据已自带，不用再下 |

---

## 🚀 快速上手

> 需要 **Python 3.10 – 3.13**

```bash
cd /workspace/AI/TinyTorch/tinytorch

python3 -m venv .venv
source .venv/bin/activate          # ⚠️ 必须激活！

pip install -r requirements.txt
pip install -e .
tito setup
```

> ⚠️ **`tito` 会强制检查是否处于虚拟环境内**——没激活 venv 会直接报错，这不是 bug。

常用命令：

```bash
make help        # 看所有可用命令
make preflight   # 开工前的快速体检（~1 分钟）
make test        # 跑测试
tito --help      # CLI 全貌
```

---

## 🏗️ 20 个渐进模块

| 部分 | 模块 | 你会造出什么 |
|:---|:---:|:---|
| **I. 地基** | `01`–`08` | 张量、激活、层、损失、数据加载器、自动求导、优化器、训练循环 |
| **II. 视觉** | `09` | `Conv2d`、`MaxPool2d`、CNN 图像分类 |
| **III. 语言** | `10`–`13` | 分词、嵌入、多头注意力、Transformer |
| **IV. 优化** | `14`–`20` | 剖析、量化、压缩、加速、记忆化、基准测试、结课项目 |

每个模块都只问一句话：**「这个能力，我能从零造出来吗？」** 💪

---

## 🏆 顺便复现一遍 ML 历史

沿途会「解锁」六个里程碑实验，用**你自己造的框架**重跑历史：

| 年份 | 里程碑 | 你要做的事 |
|:---:|:---|:---|
| **1958** | Perceptron 🌱 | 用梯度下降做二分类 |
| **1969** | XOR 危机 🧩 | 多层网络解决非线性问题 |
| **1986** | 反向传播 🔁 | 多层网络训练 |
| **1998** | CNN 革命 👁️ | 卷积做图像分类 |
| **2017** | Transformer 时代 🤖 | 自注意力做语言生成 |
| **2018+** | MLPerf ⚡ | 生产级性能优化 |

> 这不是玩具 Demo——是**被历史验证过的成就**，用你自己的代码再走一遍。🧭

---

## 📚 官方资源

| 受众 | 入口 |
|:---|:---|
| 🎓 学生 | [课程网站](https://mlsysbook.ai/tinytorch) · `tinytorch/quarto/getting-started.qmd` |
| 👩‍🏫 教师 | `tinytorch/INSTRUCTOR.md` |
| 🛠️ 贡献者 | `tinytorch/CONTRIBUTING.md` |
| 💬 讨论 | [GitHub Discussions](https://github.com/harvard-edge/cs249r_book/discussions) |

---

## 🔗 相关链接

TinyTorch 不是一座孤岛，它长在下面这个生态里 —— 三条链接，三种不同的"用法"：

| 链接 | 是什么 | 什么时候值得点开 |
|:---|:---|:---|
| 🏛️ **[harvard-edge/cs249r_book](https://github.com/harvard-edge/cs249r_book)** | **上游仓库**。教材、TinyTorch、幻灯片、项目源码都在这个 monorepo 里同仓共管（默认分支 `dev`） | 想翻源码、追 commit、提 issue / PR 时 |
| 📖 **[mlsysbook.ai](https://mlsysbook.ai/)** | **《Machine Learning Systems》官方站**（Harvard · MIT Press 2026）。两卷本：**Vol I · Foundations**、**Vol II · At Scale**，提供 HTML / PDF / EPUB；TinyTorch 的 20 个模块正是它的配套动手部分 | 想系统地学「AI 工程」而不只是跑代码时 |
| 🎓 **[CS249r · Fall 2025 课程站](https://harvard-edge.github.io/cs249r_fall2025/)** | **哈佛 CS249r 研究生研讨课**站点，2025 秋主题 *Architecture 2.0 — Agentic AI for Computer Systems Design*：聊 agentic AI 怎么反向设计与优化整个计算栈（软件 / 编译器 → 体系结构 → 芯片） | 想知道这门课怎么开、看讲义与安排时 |

> 🧭 一句话导航：**想看代码 → GitHub｜想读书 → mlsysbook.ai｜想看课 → CS249r 课程站。**

---

## 🔄 如何更新这个 `tinytorch/` 文件夹

官方仍在维护 `dev` 分支。需要刷新时，重跑一遍**稀疏检出**就好 —— 只下载 `tinytorch/`，不碰仓库其余内容。

> ⚠️ 两个前提：默认分支是 **`dev`**（不是 `main`）；本目录**刻意不带 `.git`**，所以不能直接 `git pull`。
> 当前快照：`dev` 分支 · v0.1.13 · 约 53 MB。

```bash
# 1) 稀疏克隆（只取目录树，不取 blob）
rm -rf /tmp/tt-src /tmp/tt-new
git clone --depth 1 --filter=blob:none --sparse --branch dev \
  https://github.com/harvard-edge/cs249r_book.git /tmp/tt-src
cd /tmp/tt-src && git sparse-checkout set tinytorch

# 2) 取出来，替换旧版本
mv /tmp/tt-src/tinytorch /tmp/tt-new && rm -rf /tmp/tt-src
rm -rf /workspace/AI/TinyTorch/tinytorch
mv /tmp/tt-new /workspace/AI/TinyTorch/tinytorch

# 3) 校验（应约 53M）
du -sh /workspace/AI/TinyTorch/tinytorch
```

<details>
<summary>🔧 若服务端不支持 <code>--filter=blob:none</code>（降级写法）</summary>

```bash
rm -rf /tmp/tt-src /tmp/tt-new
git clone --depth 1 --branch dev \
  https://github.com/harvard-edge/cs249r_book.git /tmp/tt-src
cd /tmp/tt-src && git sparse-checkout init --cone && git sparse-checkout set tinytorch
mv tinytorch /tmp/tt-new && rm -rf /tmp/tt-src
rm -rf /workspace/AI/TinyTorch/tinytorch
mv /tmp/tt-new /workspace/AI/TinyTorch/tinytorch
```

</details>

> 🏷️ 想锁在某个发布版而不是流动的 `dev`？把 `--branch dev` 换成标签即可，如 `tinytorch-v0.1.13`。

**两个提醒**：

- 🚫 别执行 `tinytorch/quarto/install.sh` —— 它默认分支写死 `main`，还会删目录、清空 `modules/` 与 `tinytorch/core/`。
- ✅ 更新后顺手跑一遍：`pip install -r requirements.txt && pip install -e .`，再瞄一眼 `tinytorch/CHANGELOG.md`。

---

<div align="center">

**TinyTorch** · 出自哈佛大学 [Prof. Vijay Janapa Reddi](https://vijay.seas.harvard.edu) 之手
本目录内容取自 [harvard-edge/cs249r_book](https://github.com/harvard-edge/cs249r_book) 的 `dev` 分支 · MIT License

[📖 MLSysBook](https://mlsysbook.ai/) ・ [🏛️ GitHub](https://github.com/harvard-edge/cs249r_book) ・ [🎓 CS249r Fall 2025](https://harvard-edge.github.io/cs249r_fall2025/)

*Start Small. Go Deep. Build ML Systems.* 🔥

</div>
