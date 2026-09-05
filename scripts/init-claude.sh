# ===================================================================
# Claude Code 配置初始化脚本（接入 DeepSeek）
# ===================================================================
# 功能: 根据环境变量或默认值生成 Claude Code CLI 配置文件
#       使用 DeepSeek Anthropic API 作为后端
# 配置路径: /root/.claude/
#
# 参考文档:
#   https://api-docs.deepseek.com/zh-cn/guides/anthropic_api
#   https://platform.deepseek.com/api_keys （获取 API Key）
#
# 一键运行:
#   bash /workspace/scripts/init-claude.sh
# ===================================================================

set -e

# -----------------------------------------------------------------------------
# 用户配置区（修改此处以自定义默认值）
# -----------------------------------------------------------------------------

# DeepSeek API Key: 在 https://platform.deepseek.com/api_keys 获取
# 留空则运行时交互式输入
MY_API_KEY=""

# DeepSeek Anthropic API 地址
MY_BASE_URL="https://api.deepseek.com/anthropic"

# 主模型: deepseek-v4-pro 对标 claude-opus 级别能力
MY_MODEL="deepseek-v4-pro[1m]"

# 轻量模型: 用于子代理及 haiku 场景，成本更低
MY_LIGHT_MODEL="deepseek-v4-flash"

# 子代理模型: Claude Code 内部 subagent 使用的模型
MY_SUBAGENT_MODEL="${MY_LIGHT_MODEL}"

# 执行力度: max 获得最高质量输出
MY_EFFORT_LEVEL="max"

# -----------------------------------------------------------------------------
# 配置读取逻辑
# -----------------------------------------------------------------------------
# 优先级: 环境变量 > 交互式输入 > 脚本默认值

ANTHROPIC_BASE_URL="${ANTHROPIC_BASE_URL:-$MY_BASE_URL}"
ANTHROPIC_MODEL="${ANTHROPIC_MODEL:-$MY_MODEL}"
ANTHROPIC_DEFAULT_OPUS_MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-$MY_MODEL}"
ANTHROPIC_DEFAULT_SONNET_MODEL="${ANTHROPIC_DEFAULT_SONNET_MODEL:-$MY_MODEL}"
ANTHROPIC_DEFAULT_HAIKU_MODEL="${ANTHROPIC_DEFAULT_HAIKU_MODEL:-$MY_LIGHT_MODEL}"
CLAUDE_CODE_SUBAGENT_MODEL="${CLAUDE_CODE_SUBAGENT_MODEL:-$MY_SUBAGENT_MODEL}"
CLAUDE_CODE_EFFORT_LEVEL="${CLAUDE_CODE_EFFORT_LEVEL:-$MY_EFFORT_LEVEL}"

ROOT_CLAUDE_DIR="/root/.claude"

echo "=== Claude Code 配置初始化（DeepSeek 后端）==="

# 解析 ANTHROPIC_AUTH_TOKEN：环境变量 > 脚本默认值
if [ -n "${ANTHROPIC_AUTH_TOKEN:-}" ]; then
    : # 已有环境变量，直接使用
elif [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_API_KEY}"
elif [ -n "$MY_API_KEY" ]; then
    ANTHROPIC_AUTH_TOKEN="$MY_API_KEY"
else
    # 交互式输入
    echo ""
    echo "   在 https://platform.deepseek.com/api_keys 获取 API Key"
    read -r -p "   请输入 DeepSeek API Key: " ANTHROPIC_AUTH_TOKEN
fi

if [ -z "$ANTHROPIC_AUTH_TOKEN" ]; then
    echo "⚠️  警告: 未提供有效的 API Key，配置未生成"
    echo ""
    echo "   快速配置方法:"
    echo "   1. 在 https://platform.deepseek.com/api_keys 获取 API Key"
    echo "   2. 编辑本脚本: vim /workspace/scripts/init-claude.sh"
    echo "   3. 修改 MY_API_KEY=\"sk-你的DeepSeek-API-Key\""
    echo "   4. 保存并运行: bash /workspace/scripts/init-claude.sh"
    echo ""
    mkdir -p "$ROOT_CLAUDE_DIR"
else
    echo "✅ 检测到 ANTHROPIC_AUTH_TOKEN，正在生成配置文件..."

    mkdir -p "$ROOT_CLAUDE_DIR"

    # 创建 settings.json - Claude Code 环境变量配置
    cat > "$ROOT_CLAUDE_DIR/settings.json" << EOF
{
    "env": {
        "ANTHROPIC_BASE_URL": "${ANTHROPIC_BASE_URL}",
        "ANTHROPIC_AUTH_TOKEN": "${ANTHROPIC_AUTH_TOKEN}",
        "ANTHROPIC_MODEL": "${ANTHROPIC_MODEL}",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "${ANTHROPIC_DEFAULT_OPUS_MODEL}",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "${ANTHROPIC_DEFAULT_SONNET_MODEL}",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "${ANTHROPIC_DEFAULT_HAIKU_MODEL}",
        "CLAUDE_CODE_SUBAGENT_MODEL": "${CLAUDE_CODE_SUBAGENT_MODEL}",
        "CLAUDE_CODE_EFFORT_LEVEL": "${CLAUDE_CODE_EFFORT_LEVEL}"
    },
    "theme": "light-daltonized"
}
EOF

    # 创建 .claude.json - 初始化完成标志
    cat > "$ROOT_CLAUDE_DIR/.claude.json" << EOF
{
    "hasCompletedOnboarding": true
}
EOF

    echo "✅ 已创建 $ROOT_CLAUDE_DIR/settings.json"
    echo "✅ 已创建 $ROOT_CLAUDE_DIR/.claude.json"

    echo ""
    echo "=== Claude Code 配置完成（DeepSeek 后端）==="
    echo "Base URL:    ${ANTHROPIC_BASE_URL}"
    echo "主模型:      ${ANTHROPIC_MODEL}"
    echo "轻量模型:    ${ANTHROPIC_DEFAULT_HAIKU_MODEL}"
    echo "子代理模型:  ${CLAUDE_CODE_SUBAGENT_MODEL}"
    echo "执行力度:    ${CLAUDE_CODE_EFFORT_LEVEL}"
fi