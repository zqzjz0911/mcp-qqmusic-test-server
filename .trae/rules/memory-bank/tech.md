# Tech

## 技术栈

| 组件 | 技术/库 | 版本 |
|------|---------|------|
| 语言 | Python | 3.13+ |
| MCP框架 | mcp[cli] | >=1.5.0 |
| HTTP客户端 | httpx | >=0.27.0 |
| JSON处理 | orjson | >=3.10.0 |
| 缓存 | aiocache | >=0.12.3 |
| 类型扩展 | typing_extensions | >=4.10.0 |
| 包管理 | uv | - |

## 开发环境

- 使用 `uv` 作为包管理工具
- 虚拟环境: `.venv`
- 安装依赖: `uv sync`

## 启动方式

```bash
# 方式1: 直接运行
uv run main.py

# 方式2: MCP配置后由AI助手调用
# 配置见 README.md 中的 mcpServers 配置
```

## 依赖来源

- `qqmusic_api` 为本地包，直接在项目目录中实现
- 其他依赖通过 `pyproject.toml` 声明

## MCP配置示例

```json
{
  "mcpServers": {
    "mcp-qqmusic-test-server": {
      "command": "uv",
      "args": [
        "--directory",
        "{本地目录}/mcp-qqmusic-test-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

## MCP工具

1. **search_music**
   - 参数: keyword, page, num
   - 返回: 歌曲列表

2. **search_songs_by_singer**
   - 参数: singer_name, page, num, order
   - 返回: 指定歌手的歌曲列表
