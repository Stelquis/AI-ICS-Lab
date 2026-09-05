# EdgeOne Makers 接入与使用文档

> **EdgeOne Makers** 是基于 Tencent EdgeOne 基础设施打造的 Web 与 Agent 开发部署平台，覆盖前端页面、动态 API、Cloud Functions 到 AI Agent 的一站式托管。
>
> 本文记录在 CodeBuddy / 本仓库环境下接入 Makers 的全部可行路径、配置细节与排障要点。

---

## 目录

- [一、四种接入路径对比](#一四种接入路径对比)
- [二、环境实测结论](#二环境实测结论)
- [三、方式一：MCP HTTP 模式（免登录）](#三方式一mcp-http-模式免登录)
- [四、方式二：MCP stdio 模式（全栈部署）](#四方式二mcp-stdio-模式全栈部署)
- [五、方式三：CodeBuddy IDE 部署插件（零配置）](#五方式三codebuddy-ide-部署插件零配置)
- [六、方式四：EdgeOne CLI（脚本化 / CI）](#六方式四edgeone-cli脚本化--ci)
- [七、站点区域选择](#七站点区域选择)
- [八、验证接入是否生效](#八验证接入是否生效)
- [九、排障指南](#九排障指南)
- [十、参考链接](#十参考链接)

---

## 一、四种接入路径对比

| 路径 | 能力范围 | 前置条件 | 是否需改配置 | 适用场景 |
|---|---|---|---|---|
| **MCP HTTP 模式** | 分享 HTML 内容，生成公网链接 | 无（免登录） | 改 `mcp.json` | 快速分享单页 / 演示稿 |
| **MCP stdio 模式** | 部署全栈项目（前端 + API + Agent） | Node 运行时 + 登录态 | 改 `mcp.json` | 用自然语言持续开发并部署完整项目 |
| **CodeBuddy IDE 插件** | 一键构建部署 | 腾讯云账号授权 | 无需改配置 | GUI 操作，最省事 |
| **EdgeOne CLI** | 完整项目管理 | Node 运行时 | 无 | 命令行 / CI 流水线 |

选择建议：**先试 CodeBuddy IDE 插件**（零配置、有 GUI 反馈）；需要在对话里让 AI 自主部署时再配 MCP。

---

## 二、环境实测结论

本文档编写时对本机（`AI-ICS-Lab` 开发容器）的实测结果：

| 检查项 | 结果 |
|---|---|
| MCP 配置文件 | `/root/.codebuddy/mcp.json`，内容 `{"mcpServers": {}}`（尚未配置任何 MCP 服务） |
| Node / npx | 未安装 —— stdio 模式与 CLI 需先装 Node |
| 托管 MCP 端点连通性 | `https://mcp-on-edge.edgeone.app/mcp-server` 返回 `405` |

`405` 是**正常**的：MCP Streamable HTTP 端点不接受裸 GET，不代表故障，仅说明服务在线。

---

## 三、方式一：MCP HTTP 模式（免登录）

无需登录即可把 HTML 内容部署到 Makers，秒级生成公网访问链接。底层基于边缘无服务器 + KV 存储。

### 配置

编辑 `/root/.codebuddy/mcp.json`：

```json
{
  "mcpServers": {
    "edgeone-makers-mcp-server": {
      "url": "https://mcp-on-edge.edgeone.app/mcp-server"
    }
  }
}
```

### 生效

改完后**必须重启 CodeBuddy 或重载 MCP 服务**，新工具才会出现在可用工具列表中，会话内不会热更新。

### 使用

配置生效后直接用自然语言：

```
把这个页面部署到 EdgeOne Makers，给我公网链接
```

---

## 四、方式二：MCP stdio 模式（全栈部署）

功能完整，可部署前端、后端 API 与 Agent 项目。

### 4.1 安装 Node

本机当前无 Node，stdio 模式依赖 `npx`。任选其一：

```bash
# 方式 A：通过 CodeBuddy 安装（版本可控，推荐）
# 让 AI 助手调用 install_binary 安装 Node 20+

# 方式 B：系统包管理器
apt-get update && apt-get install -y nodejs npm

# 验证
node --version && npx --version
```

### 4.2 配置

编辑 `/root/.codebuddy/mcp.json`：

```json
{
  "mcpServers": {
    "edgeone-makers-mcp-server": {
      "command": "npx",
      "args": ["@edgeone/makers-mcp@latest"]
    }
  }
}
```

### 4.3 让 AI 生成合规代码（强烈建议）

全栈项目部署前，配置 Makers 提供的 AI 上下文文件 `pages-llms.mdc`，让生成的项目结构符合平台规范（构建命令、输出目录等）。

---

## 五、方式三：CodeBuddy IDE 部署插件（零配置）

官方推荐路径，**不需要修改 `mcp.json`**。

1. 在 CodeBuddy IDE 中单击 **Deploy**。
2. 选择 **EdgeOne Makers** 进行连接。
3. 单击 **Manage**，跳转腾讯云，登录并完成账号授权。
4. （全栈项目强烈建议）配置 Rules 文件 `pages-llms.mdc`。
5. 用自然语言开发项目，随时通过对话或 **Deploy** 按钮触发构建部署。
6. 选择部署目标：
   - 新建项目；或
   - 选择已有项目 —— **仅限通过「直接上传」方式创建的项目**。
7. 部署完成后在 CodeBuddy 中查看预览地址，或到腾讯云控制台管理（自定义域名、项目设置等）。

---

## 六、方式四：EdgeOne CLI（脚本化 / CI）

适合命令行与 CI/CD 流水线。

```bash
# 1. 安装
npm install -g edgeone

# 2. 登录
edgeone login

# 3. 部署
edgeone makers deploy -n <project-name>

# 示例
edgeone makers deploy -n vite-react-demo
```

部署成功后 Console 会输出构建信息与访问 URL（形如 `https://vite-react-demo.edgeone.app`）。

若不想全局安装，可用 `npx edgeone ...` 替代。

---

## 七、站点区域选择

Makers 区分**国际站**与**腾讯云中国站**。

| 目标站点 | stdio 模式参数 |
|---|---|
| 国际站（默认） | `["@edgeone/makers-mcp@latest"]` |
| 腾讯云中国站 | `["@edgeone/makers-mcp@latest", "--region", "china"]` |

中国站完整配置：

```json
{
  "mcpServers": {
    "edgeone-makers-mcp-server": {
      "command": "npx",
      "args": ["@edgeone/makers-mcp@latest", "--region", "china"]
    }
  }
}
```

HTTP 模式与 CLI 的区域选择以控制台登录站点为准。

---

## 八、验证接入是否生效

### 8.1 确认配置已加载

重启 CodeBuddy 后，工具列表中应出现 EdgeOne Makers 相关工具（名称以 `mcp__` 前缀开头）。若没有，说明配置未被加载。

### 8.2 端点连通性自检

```bash
# 返回 405 即服务在线（正常）
curl -s -o /dev/null -w "%{http_code}\n" https://mcp-on-edge.edgeone.app/mcp-server
```

### 8.3 配置文件语法自检

```bash
cat /root/.codebuddy/mcp.json | python3 -m json.tool
```

JSON 解析失败会直接导致 MCP 服务整体无法加载。

---

## 九、排障指南

### 9.1 改了 `mcp.json` 但工具没出现

MCP 服务在 CodeBuddy 启动时加载，**改配置后必须重启或重载**。仅保存文件不会热更新。

### 9.2 `spawn npx ENOENT` / `command not found: npx`

本机无 Node 运行时。回到 [4.1 安装 Node](#41-安装-node)。

### 9.3 配置多个 MCP 时全部失效

`mcp.json` 是**整体生效**的：任意一个 server 配置出错（JSON 语法、缺字段）会导致整个文件加载失败。用 `python3 -m json.tool` 校验语法，或先只保留一个 server 逐个排查。

### 9.4 部署到中国站提示区域不匹配

stdio 模式需显式加 `--region china`，见 [第七节](#七站点区域选择)。

### 9.5 选择已有项目时列表为空

CodeBuddy IDE 插件仅支持选择通过「直接上传」方式创建的项目，其他方式（Git 导入、模板创建）的项目不在可选列表内。

### 9.6 HTTP 模式只能部署静态 HTML

这是设计限制，不是故障。HTTP 模式底层是 KV 存储单页内容，全栈能力请使用 stdio 模式或 CLI。

---

## 十、参考链接

| 资源 | 地址 |
|---|---|
| EdgeOne Makers MCP 文档 | https://makers.edgeone.link/document/mcp |
| 使用 CodeBuddy IDE 部署 | https://pages.edgeone.ai/zh/document/using-codebuddy-ide |
| 腾讯云 EdgeOne Makers 产品页 | https://cloud.tencent.com/product/makers |
| 腾讯云 EO MCP 文档 | https://cloud.tencent.com/document/product/1552/127424 |
| EdgeOne CLI 快速开始 | https://cloud.tencent.com/document/product/1552/132786 |

### 附：自托管 MCP Server

Makers 提供 `Self Hosted Makers MCP` 模板，可部署为自己的项目以使用自定义域名：

```bash
curl -X POST https://<你的自定义域名>/kv/set \
  -H "Content-Type: application/json" \
  -d '{"value": "<html><body><h1>Hello, World!</h1></body></html>"}'
```

前置条件：

1. 配置 KV 存储，**绑定变量名必须为 `my_kv`**，绑定后需重新部署项目。
2. 绑定自定义域名。
