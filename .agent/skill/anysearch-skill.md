# AnySearch Skill — AI Agent 统一搜索引擎

> **版本:** v1.0 | **适用平台:** Claude Code, CodeX, Cursor, Windsurf, OpenClaw 等 AI Agent

## 概述

AnySearch 是一个面向 AI Agent 的统一实时搜索引擎 Skill。它提供了**通用网页搜索**、**垂直领域搜索**、**并行批量搜索**和**网页内容提取**等能力，帮助 AI 助手高效获取和处理互联网信息。

### 核心优势

| 能力 | 说明 |
|------|------|
| **实时搜索** | 获取最新网络信息，突破模型知识截止日期 |
| **批量并行** | 一次提交多个搜索请求，大幅提升信息收集效率 |
| **内容提取** | 将网页自动转为 Markdown 结构化文本，便于后续处理 |
| **多运行时** | 同时支持 Python、Node.js、Bash、PowerShell |
| **Key 注入** | 脚本变量 / 环境变量 / 交互式输入，三种方式任选 |

## 安装

### 前置条件

支持以下任一运行时（按优先级排序）：

1. **Python 3.6+**（推荐）— 需安装 `requests` 库
2. **Node.js 12+**
3. **Bash 4+**（Linux/macOS）
4. **PowerShell 5.1+**（Windows）

### 快速安装

使用项目提供的安装脚本一键完成：

```bash
bash /workspace/scripts/init-anysearch.sh
```

该脚本会自动完成：下载 → 解压 → 运行时检测 → API Key 配置 → 功能验证。API Key 需由你提供，支持脚本变量、环境变量、运行时交互式输入三种方式（详见下方「配置」）。

### 手动安装

```bash
# 下载
curl -L -o anysearch.zip https://github.com/anysearch-ai/anysearch-skill/archive/refs/heads/main.zip

# 解压到技能目录（按你的平台选择）
unzip anysearch.zip
mv anysearch-skill-main ~/.agents/skills/anysearch     # 通用共享
# 或: mv anysearch-skill-main ~/.claude/skills/anysearch  # Claude Code
# 或: mv anysearch-skill-main ~/.config/opencode/skills/anysearch  # OpenCode
```

## 配置

将 API Key 填入 [scripts/init-anysearch.sh](scripts/init-anysearch.sh) 的 `MY_API_KEY` 变量，安装时自动写入 `.env` 文件。

如需更换自己的 Key，可通过环境变量覆盖：

```bash
export ANYSEARCH_API_KEY=<your_key>
bash /workspace/scripts/init-anysearch.sh
```

Key 在 [AnySearch Console](https://anysearch.com/console/api-keys) 免费获取。

## 使用指南

安装完成后，运行时信息存储在 `runtime.conf` 中。假设检测到的命令为 `<CMD>`，基础用法如下：

### 1. 网页搜索

```bash
<CMD> search "your search query" --max_results 10
```

参数说明：
- `search` — 搜索子命令
- `--max_results` — 返回结果数量（默认 5，建议 1-20）
- `--source` — 指定搜索源（默认为 web）

### 2. 并行批量搜索

```bash
<CMD> batch_search --queries '[
  {"query": "Python async programming", "max_results": 5},
  {"query": "Rust concurrency patterns", "max_results": 5},
  {"query": "Go goroutine best practices", "max_results": 5}
]'
```

### 3. 网页内容提取

```bash
<CMD> extract "https://example.com/article"
# 或
<CMD> extract --url "https://example.com/article"
```

> **注意：** extract 输出已是 Markdown 格式，无需额外转换。

### 4. 查看帮助

```bash
<CMD> --help          # 全局帮助
<CMD> search --help   # 搜索子命令帮助
<CMD> doc             # 完整文档
```

## AI Agent 平台配置

### Claude Code

安装到 `~/.claude/skills/anysearch`，Claude Code 启动时会自动加载。

### 通用共享路径

推荐安装到 `~/.agents/skills/anysearch`，多个 AI 工具（Codex、Cursor、OpenClaw）若能读取同一技能目录，可共用此路径。

### 项目级安装

在多项目环境中，也可安装到单个项目的 `.skills/` 目录下：

```bash
mv anysearch-skill <your-project>/.skills/anysearch
```

## 使用场景

### 场景一：深度研究（与 deep-research 技能配合）

AnySearch 适合作为信息收集层，收集原始素材后交由 deep-research 技能进行综合分析和引用验证。

```
AnySearch:  批量搜索 + 内容提取 → 原始素材
deep-research: 综合分析 + 事实核查 → 结构化报告
```

### 场景二：技术调研

同时搜索多个技术方案进行比较：

```bash
<CMD> batch_search --queries '[
  {"query": "LangChain vs LlamaIndex comparison 2026"},
  {"query": "AI agent framework comparison latest"}
]'
```

### 场景三：实时数据获取

追踪最新的新闻、公告或市场数据：

```bash
<CMD> search "Claude API latest updates" --max_results 5
<CMD> extract "https://docs.anthropic.com/claude/reference"
```

## 工作原理

```
用户提问
   │
   ▼
AI Agent
   │   ┌── AnySearch Skill ──┐
   ├──→│  search / batch     │──→ AnySearch API ──→ 搜索引擎
   │   │  extract / doc      │←── 结构化结果返回
   │   └──────────────────────┘
   │
   ▼
  回答用户
```

Agent 调用 AnySearch CLI，CLI 请求 AnySearch API，API 聚合搜索引擎结果并以 JSON 结构返回，Agent 解析后呈现给用户。

## 常见问题

### Q: 没有 API Key 能用吗？
脚本内置了共享 API Key，安装即用。如果 Key 失效，运行脚本时会自动检测并更新。

### Q: 提示 `requests` 库找不到？
```bash
pip install requests  # Python 3
# 或
pip3 install requests # macOS
```

### Q: 如何切换运行时？
编辑 `runtime.conf`，修改 `Command:` 行指向其他运行时 CLI 即可。

### Q: 搜索返回结果太少？
使用 `--max_results 10` 或更大值控制返回数量。

### Q: 脚本安装失败怎么办？
参考[手动安装](#手动安装)部分进行手动部署。

## 相关链接

- [GitHub 仓库](https://github.com/anysearch-ai/anysearch-skill)
- [API Key 申请](https://anysearch.com/console/api-keys)
- [Claude Code Skills 文档](https://claude.ai/docs/claude-code/skills)
