# ===================================================================
# Dockerfile
# ===================================================================

# -----------------------------------------------------------------------------
# 第一部分: 基础镜像与环境变量
# -----------------------------------------------------------------------------

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    PATH="/root/.local/bin:/usr/local/bin:$PATH" \
    LD_LIBRARY_PATH="/usr/lib:/usr/local/lib"

# -----------------------------------------------------------------------------
# 第二部分: 系统工具安装
# -----------------------------------------------------------------------------

# 安装基础开发工具和系统依赖
# 说明: 合并安装减少镜像层数，--no-install-recommends 避免安装不必要的包
#
# 工具说明:
#   git:                版本控制系统，代码管理必备
#   curl:               命令行 HTTP 客户端，用于下载文件
#   wget:               另一个下载工具，某些脚本依赖
#   procps:             进程管理工具(ps, top等)
#   ca-certificates:    HTTPS 证书，确保 SSL 连接安全
#   build-essential:    GCC/G++ 编译工具，部分 Python 包需要编译
#   software-properties-common: 软件源管理工具
#
# 清理: apt-get clean + rm -rf 删除缓存，减小镜像体积
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git curl wget procps \
        ca-certificates build-essential software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# 第三部分: Python 3.12 环境
# -----------------------------------------------------------------------------

# 安装 Python 3.12 及开发依赖
# 说明: Ubuntu 24.04 内置 Python 3.12，无需从源码编译
#
# 包说明:
#   python3.12:         Python 解释器主程序
#   python3.12-venv:    虚拟环境支持模块
#   python3.12-dev:     开发头文件，编译 C 扩展时需要
#   python3-pip:        Python 包管理器(备用，主要用 uv)
#   libssl-dev:         OpenSSL 开发库，HTTPS 相关包需要
#   zlib1g-dev:         压缩库开发文件，部分包编译依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.12 python3.12-venv python3.12-dev python3-pip \
        libssl-dev zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# 第三部分续: OpenCV 依赖库
# -----------------------------------------------------------------------------

# Python opencv-python 包依赖的 C 语言库
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libglx-mesa0 libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# 第四部分: Node.js 环境
# -----------------------------------------------------------------------------

# Claude Code CLI 等 AI 工具需要 Node.js 22+
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl && \
    update-ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_22.x -o /tmp/nodesource_setup.sh && \
    bash /tmp/nodesource_setup.sh && \
    rm /tmp/nodesource_setup.sh && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# 第五部分: uv 包管理器与 Python 依赖
# -----------------------------------------------------------------------------

# 安装 uv - 高性能 Python 包管理器
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
RUN python3 -m venv /opt/venv

# 配置环境变量
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 预装计算机视觉相关库
# 说明: 先从 PyPI 安装非 PyTorch 包，再从 PyTorch CPU 源安装 PyTorch 相关包
#       分开安装可避免 PyTorch 源不稳定导致全部依赖安装失败
RUN uv pip install --python /opt/venv \
    --index-url https://pypi.org/simple \
    numpy>=1.26.0 \
    pandas>=2.0.0 \
    opencv-python>=4.8.0 \
    scikit-learn>=1.3.0 \
    matplotlib>=3.7.0 \
    jupyter>=1.0.0 \
    ipykernel>=6.25.0 \
    tqdm>=4.66.0

# 安装 PyTorch CPU 版本（单独安装，避免源不稳定阻塞其它包）
# 说明: PyTorch CPU wheel 源偶尔 503，增加重试机制提高可靠性
RUN for attempt in 1 2 3; do \
    uv pip install --python /opt/venv \
    --index-url https://download.pytorch.org/whl/cpu \
    torch>=2.0.0 \
    torchvision>=0.15.0 \
    && break || sleep 5; \
    if [ $attempt -eq 3 ]; then echo "PyTorch install failed after 3 retries"; exit 1; fi; \
    done

# -----------------------------------------------------------------------------
# 第六部分: code-server 与 VS Code 扩展
# -----------------------------------------------------------------------------

# 安装 code-server - 浏览器版 VS Code
# 扩展: Python 支持, Git 图形化, AI 辅助编程, YAML 支持, 缩进彩虹, CSV 高亮
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    code-server --install-extension tencent-cloud.coding-copilot && \
    code-server --install-extension ms-python.python && \
    code-server --install-extension mhutchie.git-graph && \
    code-server --install-extension redhat.vscode-yaml && \
    code-server --install-extension oderwat.indent-rainbow && \
    code-server --install-extension mechatroner.rainbow-csv && \
    code-server --install-extension cweijan.vscode-office && \
    code-server --install-extension cnbcool.cnb-welcome && \
    code-server --install-extension anthropic.claude-code && \
    code-server --install-extension openai.chatgpt || true

# -----------------------------------------------------------------------------
# 第七部分: CodeX CLI 配置
# -----------------------------------------------------------------------------

# 复制 CodeX 初始化脚本
COPY scripts/init-codex.sh /usr/local/bin/init-codex.sh
RUN chmod +x /usr/local/bin/init-codex.sh

# -----------------------------------------------------------------------------
# 第八部分: Claude Code CLI 配置 + 汉化包
# -----------------------------------------------------------------------------

# 安装 Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# 复制 Claude Code 初始化脚本
COPY scripts/init-claude.sh /usr/local/bin/init-claude.sh
RUN chmod +x /usr/local/bin/init-claude.sh

# 安装 Claude Code 汉化包（非官方社区扩展）
RUN node --version && \
    npm --version && \
    git clone --depth 1 https://github.com/zstings/claude-code-zh-cn.git /tmp/claude-code-zh-cn && \
    cd /tmp/claude-code-zh-cn && \
    npm install && \
    npx vsce package --no-dependencies --allow-star-activation && \
    code-server --install-extension ./claude-code-zhcn-*.vsix && \
    rm -rf /tmp/claude-code-zh-cn

# -----------------------------------------------------------------------------
# 第九部分: 配置文件复制
# -----------------------------------------------------------------------------

# 复制 VS Code 设置和脚本目录
COPY settings.json /root/.local/share/code-server/Machine/settings.json
COPY scripts/ /workspace/scripts/

# -----------------------------------------------------------------------------
# 第九部分: 环境变量配置
# -----------------------------------------------------------------------------

ENV PYTHONPATH=/workspace \
    PYTHONUNBUFFERED=1

# 设置容器工作目录
# 说明: 容器启动后默认进入 /workspace，与 CNB 平台挂载点一致
WORKDIR /workspace

# 容器默认启动命令
# 说明: 启动 bash shell，实际运行由 .cnb.yml 配置文件控制
#       CNB 平台会覆盖此命令以启动 code-server 服务
CMD ["/bin/bash"]