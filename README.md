# AI-Agent

这是一个基于 FastAPI 的 AI 代理服务，集成了多种工具和动态提示词功能。

## 功能特性

- **多工具集成**: 支持文本转图片、天气查询、文本转视频等多种工具
- **动态提示词**: 基于角色数据和聊天历史生成动态系统提示词
- **LLM 工具选择器**: 智能选择合适的工具处理用户请求
- **FastAPI 服务**: 提供 RESTful API 接口

## 项目结构

```
AI-Agent/
├── main.py                    # FastAPI 应用入口
├── config.py                  # 配置文件
├── llm/                       # LLM 客户端
│   └── llm_client.py
├── middleware/                  # 中间件
│   └── tool_selector.py       # LLM 工具选择器中间件
├── prompt_agent_env/          # 动态提示词环境
├── tools/                     # 工具模块
│   ├── base.py               # 工具基类
│   ├── dynamic_prompt.py     # 动态提示词生成
│   ├── text_to_image.py      # 文本转图片工具
│   ├── text_to_video.py      # 文本转视频工具
│   └── weather.py            # 天气查询工具
└── README.md
```

## 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install fastapi uvicorn pydantic openai python-dotenv
```

## 配置

### 环境变量配置

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入实际的 API 密钥：
```bash
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL_NAME=deepseek/deepseek-chat-v3-0324
```

### 配置文件说明

- `config.py`: 配置文件，会自动从 `.env` 文件加载环境变量
- `.env`: 包含敏感信息的环境变量文件（已添加到 .gitignore）
- `.env.example`: 环境变量示例文件，用于参考

## 运行服务

```bash
python main.py
```

服务将在 `http://0.0.0.0:8000` 启动。

## API 接口

### POST /chat

接收用户输入的文本，返回处理结果。

**请求体格式:**
```json
{
  "message": "用户输入的文本",
  "character_data": {
    // 角色数据（可选）
  },
  "chat_history": [
    // 聊天历史（可选）
  ]
}
```

**响应格式:**
```json
{
  "message": "处理结果",
  "dynamic_prompt_used": "使用的动态提示词（如果有）",
  "success": true
}
```

## 工具说明

### 文本转图片工具 (TextToImageTool)
- 功能: 将文本描述转换为图片
- 触发条件: 用户请求生成图片

### 天气查询工具 (WeatherTool)
- 功能: 查询指定城市的天气信息
- 触发条件: 用户询问天气相关问题

### 文本转视频工具 (TextToVideoTool)
- 功能: 将文本描述转换为视频
- 触发条件: 用户请求生成视频

### 动态提示词生成 (DynamicPrompt)
- 功能: 基于角色数据和聊天历史生成动态系统提示词
- 触发条件: 提供了角色数据和聊天历史

## 使用示例

### 基本聊天
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

### 带角色数据的聊天
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "请生成一张图片",
    "character_data": {
      "name": "AI助手",
      "personality": "友好"
    },
    "chat_history": [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "你好！"}
    ]
  }'
```

## 开发

### 添加新工具

1. 在 `tools/` 目录下创建新的工具文件
2. 继承 `tools.base.Tool` 基类
3. 实现 `can_handle` 和 `run` 方法
4. 在 `main.py` 中注册新工具

### 修改动态提示词逻辑

编辑 `tools/dynamic_prompt.py` 文件中的 `generate_dynamic_prompt` 函数。

## 许可证

MIT License
