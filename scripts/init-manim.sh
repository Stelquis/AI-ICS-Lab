# ===================================================================
# Manim
# ===================================================================
# 一键运行:
#   bash /workspace/scripts/init-manim.sh
# ===================================================================

set -e

# -----------------------------------------------------------------------------
# 用户配置区
# -----------------------------------------------------------------------------

# Python 虚拟环境路径（复用 Dockerfile 中已创建的 /opt/venv）
VENV_DIR="${VENV_DIR:-/opt/venv}"

# -----------------------------------------------------------------------------
# 环境检测函数
# -----------------------------------------------------------------------------

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ "$(uname -s)" = "Darwin" ]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

check_command() { command -v "$1" &>/dev/null; }

OS_ID=$(detect_os)

echo "=== Manim 安装与配置 ==="
echo "  系统: ${OS_ID} / $(uname -m) / $(nproc) 核 / $(free -h | awk '/^Mem:/ {print $2}')"
echo ""

# -----------------------------------------------------------------------------
# 检测已有环境
# -----------------------------------------------------------------------------

echo "--- 环境检测 ---"

PYTHON_OK=false
FFMPEG_OK=false
LATEX_OK=false

# Python（>= 3.10）
_check_python_ver() {
    local ver=$("$1" --version 2>&1 | grep -oP '\d+\.\d+')
    local major=$(echo "$ver" | cut -d. -f1)
    local minor=$(echo "$ver" | cut -d. -f2)
    [ "$major" -ge 3 ] && { [ "$major" -gt 3 ] || [ "$minor" -ge 10 ]; }
}

PYTHON_CMD=""
for candidate in python3.12 python3 python; do
    if check_command "$candidate" && _check_python_ver "$candidate"; then
        PYTHON_CMD="$candidate"
        break
    fi
done

if [ -n "$PYTHON_CMD" ]; then
    echo "✅ Python:    $($PYTHON_CMD --version 2>&1)"
    PYTHON_OK=true
else
    echo "❌ Python:    未找到或版本 < 3.10"
fi

# FFmpeg
if check_command ffmpeg; then
    echo "✅ FFmpeg:    $(ffmpeg -version 2>&1 | head -1)"
    FFMPEG_OK=true
else
    echo "⚠️  FFmpeg:   未安装"
fi

# LaTeX（实际编译测试，避免残缺安装导致的误判）
LATEX_OK=false
_check_latex() {
    local tmpdir
    tmpdir=$(mktemp -d)
    cat > "$tmpdir/test.tex" << 'TEXEOF'
\documentclass{article}
\usepackage{amsmath}
\begin{document}
$E=mc^2$
\end{document}
TEXEOF
    if (cd "$tmpdir" && pdflatex -interaction=nonstopmode test.tex >/dev/null 2>&1); then
        rm -rf "$tmpdir"
        return 0
    else
        rm -rf "$tmpdir"
        return 1
    fi
}

if _check_latex; then
    LATEX_VER=$(pdflatex --version 2>&1 | head -1)
    echo "✅ LaTeX:     ${LATEX_VER}"
    LATEX_OK=true
else
    echo "⚠️  LaTeX:    未安装或不可用"
fi

echo ""

# -----------------------------------------------------------------------------
# 安装系统依赖
# -----------------------------------------------------------------------------

# 仅支持 apt: 基础镜像已固定为 Ubuntu 24.04，镜像源由 Dockerfile 统一配置
install_sys_deps() {
    apt-get update

    if ! $FFMPEG_OK; then
        echo "  → 安装 FFmpeg..."
        apt-get install -y ffmpeg
    fi

    if ! $LATEX_OK; then
        echo "  → 安装 LaTeX（texlive 核心包）..."
        apt-get install -y \
            texlive-latex-recommended \
            texlive-latex-extra \
            texlive-fonts-recommended \
            texlive-science
    fi

    # dvipng / cm-super 为 Manim 渲染公式所必需，Dockerfile 未包含，需无条件补装
    echo "  → 安装编译依赖（Cairo / Pango / dvipng）..."
    apt-get install -y pkg-config libcairo2-dev libpango1.0-dev cm-super dvipng
}

echo "--- 安装系统依赖 ---"
install_sys_deps
echo ""

# 重新检测
check_command ffmpeg && FFMPEG_OK=true
_check_latex && LATEX_OK=true

# 最终检查
for dep in "FFmpeg:$FFMPEG_OK" "LaTeX:$LATEX_OK" "Python:$PYTHON_OK"; do
    name="${dep%%:*}" ok="${dep##*:}"
    if ! $ok; then
        echo "❌ ${name} 安装失败，请手动安装后重试。"
        exit 1
    fi
done

# -----------------------------------------------------------------------------
# 虚拟环境 & 安装 Manim
# -----------------------------------------------------------------------------

echo "--- Python 虚拟环境 ---"
echo "  路径: ${VENV_DIR}"

if [ ! -d "$VENV_DIR" ]; then
    "$PYTHON_CMD" -m venv "$VENV_DIR"
    echo "  → 已创建"
elif [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "❌ 路径存在但不是有效的虚拟环境: ${VENV_DIR}"
    exit 1
else
    echo "  → 复用已有"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

echo ""
echo "--- 安装 Manim ---"
uv pip install manim -q

MANIM_VERSION_INSTALLED=$(uv pip show manim | awk '/^Version:/ {print $2}')
echo "✅ Manim ${MANIM_VERSION_INSTALLED}"

# -----------------------------------------------------------------------------
# 写入配置文件
# -----------------------------------------------------------------------------

cat > "$VENV_DIR/manim.conf" << EOF
# Manim 环境配置（$(date)）
VENV_DIR="${VENV_DIR}"
MANIM_VERSION="${MANIM_VERSION_INSTALLED}"
# source ${VENV_DIR}/bin/activate
EOF

# -----------------------------------------------------------------------------
# 功能验证
# -----------------------------------------------------------------------------

echo ""
echo "--- 功能验证 ---"

TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

cat > "$TEST_DIR/test_manim.py" << 'PYEOF'
from manim import *

class TestSetup(Scene):
    def construct(self):
        formula = MathTex(r"f'(x)=\lim_{\Delta x \to 0}\frac{f(x+\Delta x)-f(x)}{\Delta x}")
        self.add(formula)
        self.wait(0.1)

if __name__ == "__main__":
    TestSetup().render()
PYEOF

MANIM_OUTPUT=$(cd "$TEST_DIR" && python test_manim.py 2>&1) && MANIM_OK=true || MANIM_OK=false

if $MANIM_OK; then
    echo "✅ 渲染测试通过"
else
    echo "⚠️  渲染测试未通过"
    echo "$MANIM_OUTPUT" | grep -i "error" | tail -3 | while read -r line; do echo "    $line"; done
fi

deactivate 2>/dev/null || true

# -----------------------------------------------------------------------------
# 安装摘要
# -----------------------------------------------------------------------------

echo ""
echo "=== 安装摘要 ==="
echo "  Python:    $($PYTHON_CMD --version 2>&1)"
echo "  Manim:     ${MANIM_VERSION_INSTALLED}"
echo "  FFmpeg:    $(ffmpeg -version 2>&1 | head -1)"
echo "  LaTeX:     $(pdflatex --version 2>&1 | head -1)"
echo "  虚拟环境:  ${VENV_DIR}"
echo ""

echo "✅ Manim 环境配置完成！"