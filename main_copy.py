# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from tools.text_to_image import TextToImageTool
from tools.weather import WeatherTool
from tools.text_to_video import TextToVideoTool
from middleware.tool_selector import LLMToolSelectorMiddleware

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: object
    # tool_used: str = None
    # tool_result: Dict[str, Any] = None
    success: bool = True

# 注册工具
tools = [
    TextToImageTool(),
    WeatherTool(),
    TextToVideoTool()
]

middleware = LLMToolSelectorMiddleware(tools)

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    接收用户输入的文本，返回处理结果
    
    - **message**: 用户输入的文本
    """
    try:
        result = middleware.run(request.message)
        
        # 解析结果，判断是否使用了工具
        tool_used = None
        tool_result = None
        
        if isinstance(result, dict):
            if "tool" in result:
                tool_used = result["tool"]
                tool_result = result
            else:
                # 如果返回的是字典但不是工具结果，转换为字符串
                result = str(result)
        elif hasattr(result, 'tool'):
            tool_used = result.tool
            tool_result = result.__dict__
        
        return ChatResponse(
            # message=str(result),
            message=result,
            tool_used=tool_used,
            tool_result=tool_result,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理请求时发生错误: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
