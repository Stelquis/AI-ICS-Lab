# ===================================================================
# Dockerfile
# ===================================================================

# -----------------------------------------------------------------------------
# 基础镜像与环境变量
# -----------------------------------------------------------------------------

# 使用 Ubuntu 24.04 LTS 作为基础镜像
FROM ubuntu:24.04

# 环境变量配置
#   DEBIAN_FRONTEND=noninteractive: 禁用交互式提示, 避免安装时卡住
ENV DEBIAN_FRONTEND=noninteractive

# 配置国内镜像源
# 说明: 使用腾讯云镜像加速 apt 下载
RUN . /etc/os-release 2>/dev/null || VERSION_CODENAME="noble" && \
    echo "deb https://mirrors.cloud.tencent.com/ubuntu/ ${VERSION_CODENAME} main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb https://mirrors.cloud.tencent.com/ubuntu/ ${VERSION_CODENAME}-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.cloud.tencent.com/ubuntu/ ${VERSION_CODENAME}-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.cloud.tencent.com/ubuntu/ ${VERSION_CODENAME}-security main restricted universe multiverse" >> /etc/apt/sources.list

# -----------------------------------------------------------------------------
# 系统工具安装
# -----------------------------------------------------------------------------

# 安装基础开发工具与编译依赖
# 说明: 合并安装减少镜像层数, --no-install-recommends 避免安装不必要的包
#   git:                版本控制工具
#   git-lfs:            Git 大文件扩展(拉取模型权重 / 数据集)
#   curl:               命令行下载工具
#   procps:             ps / top / kill 等进程查看与管理命令
#   ca-certificates:    CA 根证书(HTTPS 下载时校验服务器证书)
#   gpg:                密钥管理(导入 / 校验软件源签名)
#   python-is-python3:  提供 python 命令别名, 指向 python3
#   python3.12-dev:     Python 头文件与静态库(编译 C 扩展时需要)
#   build-essential:    GCC / G++ / make 编译工具链
#   libssl-dev:         OpenSSL 开发库(编译 cryptography 等包)
#   zlib1g-dev:         zlib 压缩库开发包(编译 Pillow 等包)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        git-lfs \
        curl \
        procps \
        ca-certificates \
        gpg \
        python-is-python3 \
        python3.12-dev \
        build-essential \
        libssl-dev \
        zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装 OpenCV 运行时依赖库
# 说明: opencv-python 等 CV 库导入时需要以下 X11 / GL / OpenMP 系统库
#   libgl1:           OpenGL 运行时库(提供 libGL.so.1, import cv2 必需)
#   libglx-mesa0:     Mesa 实现的 OpenGL GLX 运行时
#   libglib2.0-0:     GLib 基础库
#   libsm6:           X11 会话管理(Session Management)库
#   libxext6:         X11 扩展库
#   libxrender-dev:   X Rendering Extension 渲染扩展
#   libgomp1:         GCC OpenMP 运行时(多线程并行加速)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 \
        libglx-mesa0 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Python 库
# -----------------------------------------------------------------------------

# 安装 UV - 极速 Python 包管理器
# 说明: 比 pip 快 10-100 倍, 支持并行安装, 与系统 Python 3.12 完美兼容
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 添加 UV 到 PATH
ENV PATH="/root/.local/bin:$PATH"

# 创建虚拟环境
RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 安装计算机视觉基础库
# 说明: 走 PyPI 官方源
#   numpy:          多维数组与矩阵运算基础库
#   pandas:         表格数据处理与统计分析
#   opencv-python:  OpenCV 图像处理 / 视频读写 / 特征算子
#   scikit-learn:   传统机器学习算法(分类 / 回归 / 聚类 / 降维)
#   matplotlib:     数据可视化绘图
#   tqdm:           循环与训练进度条
RUN uv pip install --python /opt/venv/bin/python \
        numpy>=1.26.0 \
        pandas>=2.0.0 \
        opencv-python>=4.8.0 \
        scikit-learn>=1.3.0 \
        matplotlib>=3.7.0 \
        tqdm>=4.66.0

# 安装 PyTorch CPU 版本
# 说明: 走 PyTorch 官方 CPU wheel 通道, 该通道只发布 +cpu 构建, 不会拉入 nvidia-* GPU 依赖
#       官方源偶发 503, 故保留重试机制提高可靠性
#   torch:        PyTorch 深度学习框架(张量计算 / 自动求导)
#   torchvision: 视觉数据集 / 预训练模型 / 图像变换
RUN for attempt in 1 2 3; do \
    uv pip install --python /opt/venv/bin/python \
        --index-url https://download.pytorch.org/whl/cpu \
        torch>=2.0.0 \
        torchvision>=0.15.0 \
    && break || sleep 5; \
    if [ $attempt -eq 3 ]; then echo "PyTorch install failed after 3 retries"; exit 1; fi; \
    done && \
    rm -rf /root/.cache/uv

# -----------------------------------------------------------------------------
# LaTeX 编译环境 (XeLaTeX) 安装
# -----------------------------------------------------------------------------

# 安装 TeX Live 核心包 + 常用扩展, 支持 XeLaTeX 编译 .tex 生成 PDF
# 说明: 核心包保证基础编译, 扩展包补齐绘图 / 理工 / 西文字体, 体积仍远小于 texlive-full
#   texlive-xetex:             XeLaTeX 引擎 + fontspec
#   texlive-latex-base:        LaTeX 基础格式与文档类(核心, 含 bibtex 程序)
#   texlive-latex-recommended: 常用宏包(recommended 级, 含 natbib)
#   texlive-latex-extra:       更全的常用宏包
#   texlive-fonts-recommended: 推荐西文字体(Latin Modern / TeX Gyre 等)
#   texlive-lang-chinese:      中文支持(ctex / xeCJK / Fandol 中文字体)
#   texlive-pictures:          TikZ / PGF 绘图(网络结构图 / 流程图)
#   texlive-science:           algorithm2e / siunitx 等理工科宏包
#   latexmk:                   自动多轮编译工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        texlive-xetex \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-fonts-recommended \
        texlive-lang-chinese \
        texlive-pictures \
        texlive-science \
        latexmk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* && \
    xelatex --version

# -----------------------------------------------------------------------------
# code-server 与 VS Code 扩展
# -----------------------------------------------------------------------------

# 安装 code-server - 浏览器版 VS Code
RUN curl -fsSL https://code-server.dev/install.sh | sh

# 安装 VS Code 扩展
# 说明: 末尾 || true 保证单个扩展安装失败不会中断整个镜像构建
#   tencent-cloud.coding-copilot: 腾讯云 AI 代码助手(代码补全 / Chat 对话)
#   ms-python.python:             Python 语言支持(语法高亮 / 智能提示 / 调试 / Jupyter)
#   james-yu.latex-workshop:      LaTeX 编辑与编译(调用 XeLaTeX 生成 PDF, 支持正反向搜索)
#   cweijan.vscode-office:        Office 文档预览(直接查看 docx / xlsx / pptx)
#   oderwat.indent-rainbow:       缩进层级彩色高亮, 便于阅读 Python 代码块
#   mhutchie.git-graph:           Git 提交历史图谱可视化
#   redhat.vscode-yaml:           YAML 语言支持(语法校验 / 格式化, 用于 CI 配置文件)
#   mechatroner.rainbow-csv:      CSV / TSV 按列着色与表格预览
#   cnbcool.cnb-welcome:          CNB 平台欢迎页与上手引导
RUN code-server --install-extension tencent-cloud.coding-copilot && \
    code-server --install-extension ms-python.python && \
    code-server --install-extension james-yu.latex-workshop && \
    code-server --install-extension cweijan.vscode-office && \
    code-server --install-extension oderwat.indent-rainbow && \
    code-server --install-extension mhutchie.git-graph && \
    code-server --install-extension redhat.vscode-yaml && \
    code-server --install-extension mechatroner.rainbow-csv && \
    code-server --install-extension cnbcool.cnb-welcome || true

# -----------------------------------------------------------------------------
# 配置文件复制
# -----------------------------------------------------------------------------

# 复制 VS Code 设置和脚本目录
COPY .vscode/settings.json /root/.local/share/code-server/Machine/settings.json
COPY scripts/ /workspace/scripts/

# -----------------------------------------------------------------------------
# 环境变量与系统配置
# -----------------------------------------------------------------------------

# 字符集配置
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

# 容器默认工作目录
WORKDIR /workspace

# 容器默认启动命令
CMD ["/bin/bash"]