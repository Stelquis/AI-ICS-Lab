# ===================================================================
# AnySearch Skill 安装与配置脚本
# ===================================================================
# 功能: 下载、安装并配置 AnySearch Skill，支持多个 AI Agent 平台
#       自动检测运行时环境并写入配置文件
# 参考文档: docs/anysearch-skill.md
#
# 一键运行:
#   bash /workspace/scripts/init-anysearch.sh
# ===================================================================

set -e

# -----------------------------------------------------------------------------
# 用户配置区
# -----------------------------------------------------------------------------

# AnySearch Skill 版本（可指定 release tag，留空用 main 分支）
SKILL_VERSION="main"

# 安装路径: 可选 ~/.claude/skills/、~/.config/opencode/skills/、
#           ~/.agents/skills/、或 <project>/.skills/
INSTALL_DIR="${INSTALL_DIR:-$HOME/.agents/skills/anysearch}"

# AnySearch API Key（默认使用项目共享 Key，如需更换可在 .env 中修改）
# 在 https://anysearch.com/console/api-keys 获取
ANYSEARCH_API_KEY="${ANYSEARCH_API_KEY:-as_sk_eec743dc5f5ceabf489c575c1ecaf646}"

# -----------------------------------------------------------------------------
# 环境检测
# -----------------------------------------------------------------------------

echo "=== AnySearch Skill 安装与配置 ==="
echo ""

detect_runtime() {
    local script_path

    # Python
    script_path="$INSTALL_DIR/scripts/anysearch_cli.py"
    if [ -f "$script_path" ] && command -v python &>/dev/null; then
        if python -c "import requests" &>/dev/null 2>&1; then
            echo "Python"
            echo "python $(realpath "$script_path")"
            return 0
        fi
    fi

    # Python3
    script_path="$INSTALL_DIR/scripts/anysearch_cli.py"
    if [ -f "$script_path" ] && command -v python3 &>/dev/null; then
        if python3 -c "import requests" &>/dev/null 2>&1; then
            echo "Python"
            echo "python3 $(realpath "$script_path")"
            return 0
        fi
    fi

    # Node.js
    script_path="$INSTALL_DIR/scripts/anysearch_cli.js"
    if [ -f "$script_path" ] && command -v node &>/dev/null; then
        echo "Node.js"
        echo "node $(realpath "$script_path")"
        return 0
    fi

    # Bash (Linux/macOS fallback)
    script_path="$INSTALL_DIR/scripts/anysearch_cli.sh"
    if [ -f "$script_path" ]; then
        if [[ "$(uname -s)" == "Linux" ]] || [[ "$(uname -s)" == "Darwin" ]]; then
            echo "Bash"
            echo "bash $(realpath "$script_path")"
            return 0
        fi
    fi

    # PowerShell (Windows fallback)
    script_path="$INSTALL_DIR/scripts/anysearch_cli.ps1"
    if [ -f "$script_path" ] && command -v powershell &>/dev/null; then
        echo "PowerShell"
        echo "powershell -ExecutionPolicy Bypass -File $(realpath "$script_path")"
        return 0
    fi

    echo ""
    echo ""
    return 1
}

# -----------------------------------------------------------------------------
# 下载与安装
# -----------------------------------------------------------------------------

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

DOWNLOAD_URL="https://github.com/anysearch-ai/anysearch-skill/archive/refs/heads/${SKILL_VERSION}.zip"

echo "[1/3] 下载 AnySearch Skill..."
echo "      源: ${DOWNLOAD_URL}"
echo "      目标: ${INSTALL_DIR}"

if command -v curl &>/dev/null; then
    curl -L -s -o "$TEMP_DIR/anysearch.zip" "$DOWNLOAD_URL"
elif command -v wget &>/dev/null; then
    wget -q -O "$TEMP_DIR/anysearch.zip" "$DOWNLOAD_URL"
else
    echo "❌ 错误: 未找到 curl 或 wget，请先安装其中一个"
    exit 1
fi

echo "[2/3] 解压..."

# 优先使用 unzip，不存在则尝试用 python 或 busybox 替代
if command -v unzip &>/dev/null; then
    mkdir -p "$TEMP_DIR/extract"
    unzip -q -o "$TEMP_DIR/anysearch.zip" -d "$TEMP_DIR/extract"
elif command -v python3 &>/dev/null; then
    python3 -c "
import zipfile, sys
with zipfile.ZipFile('$TEMP_DIR/anysearch.zip', 'r') as z:
    z.extractall('$TEMP_DIR/extract')
" 2>/dev/null
elif command -v python &>/dev/null; then
    python -c "
import zipfile, sys
with zipfile.ZipFile('$TEMP_DIR/anysearch.zip', 'r') as z:
    z.extractall('$TEMP_DIR/extract')
" 2>/dev/null
elif command -v bsdtar &>/dev/null; then
    mkdir -p "$TEMP_DIR/extract"
    bsdtar -xf "$TEMP_DIR/anysearch.zip" -C "$TEMP_DIR/extract"
else
    # 最后尝试安装 unzip
    if command -v apt-get &>/dev/null; then
        echo "  → 未找到 unzip，正在安装..."
        apt-get update -qq && apt-get install -y -qq unzip
        mkdir -p "$TEMP_DIR/extract"
        unzip -q -o "$TEMP_DIR/anysearch.zip" -d "$TEMP_DIR/extract"
    elif command -v yum &>/dev/null; then
        echo "  → 未找到 unzip，正在安装..."
        yum install -y -q unzip
        mkdir -p "$TEMP_DIR/extract"
        unzip -q -o "$TEMP_DIR/anysearch.zip" -d "$TEMP_DIR/extract"
    else
        echo "❌ 错误: 未找到 unzip，请手动安装: apt install unzip"
        exit 1
    fi
fi

# 找到解压后的目录（通常带有分支名后缀）
EXTRACTED_DIR=$(find "$TEMP_DIR/extract" -maxdepth 1 -type d | tail -1)

# 创建目标目录（清理旧版）
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# 复制文件
cp -r "$EXTRACTED_DIR"/* "$INSTALL_DIR/"

echo "✅ 安装完成: ${INSTALL_DIR}"

# 创建到 Claude Code 技能目录的软链接（如果存在 .claude 目录）
CLAUDE_SKILL_DIR="$HOME/.claude/skills"
if [ -d "$(dirname "$CLAUDE_SKILL_DIR")" ]; then
    mkdir -p "$CLAUDE_SKILL_DIR"
    ln -sf "$INSTALL_DIR" "$CLAUDE_SKILL_DIR/anysearch"
    echo "  → 已创建软链接: $CLAUDE_SKILL_DIR/anysearch"
fi

# -----------------------------------------------------------------------------
# 运行时检测
# -----------------------------------------------------------------------------

echo ""
echo "[3/3] 检测运行时环境..."

if ! RUNTIME_INFO=$(detect_runtime); then
    echo "⚠️  未检测到支持的运行时环境"
    echo "   请安装 Python 3.6+（推荐）或 Node.js 12+"
    echo "   Python 需要 requests 库: pip install requests"
    exit 1
fi

RUNTIME_NAME=$(echo "$RUNTIME_INFO" | head -1)
RUNTIME_CMD=$(echo "$RUNTIME_INFO" | tail -1)

echo "      运行时: ${RUNTIME_NAME}"
echo "      命令:   ${RUNTIME_CMD}"

# 写入 runtime.conf
cat > "$INSTALL_DIR/runtime.conf" << EOF
Runtime: ${RUNTIME_NAME}
Command: ${RUNTIME_CMD}
EOF

echo "✅ 运行时配置已写入: ${INSTALL_DIR}/runtime.conf"

# -----------------------------------------------------------------------------
# API Key 配置
# -----------------------------------------------------------------------------

# 写入 .env（环境变量 > 脚本默认值）
cat > "$INSTALL_DIR/.env" << EOF
ANYSEARCH_API_KEY=${ANYSEARCH_API_KEY}
EOF
echo "✅ API Key 已配置"

# -----------------------------------------------------------------------------
# 功能验证
# -----------------------------------------------------------------------------

echo ""
echo "=== 安装摘要 ==="
echo "  安装路径:  ${INSTALL_DIR}"
echo "  运行时:    ${RUNTIME_NAME}"
echo "  命令:      ${RUNTIME_CMD}"
echo "  API Key:   ${ANYSEARCH_API_KEY:0:16}..."
echo ""

echo "=== 运行入口测试 ==="

RUNTEST_OUTPUT=$(eval "${RUNTIME_CMD} doc" 2>&1) && RUNTEST_OK=true || RUNTEST_OK=false

# 检测是否生成了自动 API Key（当前 Key 失效时 AnySearch 会自动分配新 Key）
AUTO_KEY=$(echo "$RUNTEST_OUTPUT" | grep -o 'api_key: [a-z0-9_]*' | head -1 | cut -d' ' -f2)
if [ -n "$AUTO_KEY" ] && [ "$AUTO_KEY" != "$ANYSEARCH_API_KEY" ]; then
    echo "$RUNTEST_OUTPUT" | head -20
    echo ""
    echo "🔑 检测到新的自动生成 API Key，更新 .env..."
    echo "ANYSEARCH_API_KEY=${AUTO_KEY}" > "$INSTALL_DIR/.env"
    echo "✅ 已更新 Key"
    echo ""
    echo "=== 再次运行入口测试验证 ==="
    eval "${RUNTIME_CMD} doc" 2>&1 | head -10
    echo ""
elif $RUNTEST_OK; then
    echo "$RUNTEST_OUTPUT" | head -20
else
    echo "$RUNTEST_OUTPUT" | head -20
    echo ""
    echo "⚠️  入口测试未通过，请检查运行时环境"
    exit 1
fi

echo ""
echo "✅ AnySearch Skill 安装成功，随时可用！"
echo ""
echo "💡 提示: 重启 Claude Code 会话后，AnySearch 技能会自动加载。"
echo "   在此之前可以通过 bash 直接调 CLI 使用。"
