# Architecture

## 系统架构

MCP QQ音乐测试服务器采用分层架构：

```
┌─────────────────────────────┐
│    MCP Client (AI)         │
│  (Claude/Cursor)           │
└─────────────┬───────────────┘
              │ stdio
              ▼
┌─────────────────────────────┐
│   FastMCP Server           │
│   main.py                  │
│  - search_music()          │
│  - search_songs_by_singer()│
└─────────────┬───────────────┘
              │ async calls
              ▼
┌─────────────────────────────┐
│   qqmusic_api package      │
│  - search.py               │
│  - singer.py               │
│  - song.py                 │
│  - album.py                │
│  - playlist.py             │
└─────────────┬───────────────┘
              │ HTTP requests
              ▼
┌─────────────────────────────┐
│   QQ Music Backend API     │
└─────────────────────────────┘
```

## 源码结构

```
mcp-qqmusic-test-server/
├── main.py                  # FastMCP服务器入口，定义MCP工具
├── qqmusic_api/             # QQ音乐API封装包
│   ├── __init__.py
│   ├── search.py           # 搜索API (SearchType枚举)
│   ├── singer.py           # 歌手相关API
│   ├── song.py             # 歌曲相关API
│   ├── album.py            # 专辑相关API
│   ├── playlist.py         # 歌单相关API
│   └── utils/              # 工具模块
│       ├── network.py      # 网络请求处理 (ApiRequest)
│       ├── session.py      # 会话管理
│       ├── credential.py   # 凭证管理
│       └── common.py      # 通用工具
├── test_api.py             # API测试脚本
└── test_direct.py          # 直接测试脚本
```

## 核心组件

1. **FastMCP Server** (`main.py`)
   - 使用 `mcp.server.fastmcp.FastMCP` 创建
   - 定义两个 `@mcp.tool()` 装饰的异步函数
   - 通过 stdio 传输协议与客户端通信

2. **QQMusic API** (`qqmusic_api/`)
   - 封装QQ音乐后端API调用
   - 使用装饰器模式 (`@api_request`) 定义API
   - 支持响应缓存 (aiocache)
   - 内置签名和凭证处理

## 数据流

1. MCP客户端发送JSON-RPC请求
2. FastMCP解析请求，调用对应工具函数
3. 工具函数调用 `qqmusic_api` 模块
4. `qqmusic_api` 发起HTTP请求到QQ音乐后端
5. 响应经过处理后返回给MCP客户端
