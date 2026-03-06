# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from tools.text_to_image import TextToImageTool
from tools.weather import WeatherTool
from tools.text_to_video import TextToVideoTool
from middleware.tool_selector import LLMToolSelectorMiddleware
from tools.dynamic_prompt import generate_interaction_guidance

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    character_data: Optional[Dict[str, Any]] = None  # 👈 角色数据
    chat_history: Optional[list] = None              # 👈 聊天历史


class ChatResponse(BaseModel):
    message: object
    dynamic_prompt_used: Optional[str] = None
    success: bool = True


# 注册工具
tools = [
    TextToImageTool(),
    WeatherTool(),
    TextToVideoTool()
]

middleware = LLMToolSelectorMiddleware(tools)


# @app.post("/chat")
# async def chat(request: ChatRequest):
#     """
#     接收用户输入的文本，返回处理结果
#     """

#     try:
#         dynamic_prompt = None

#         # ==============================
#         # Step 1: 动态提示词 Agent 判断
#         # ==============================
#         if request.character_data and request.chat_history:
#             print(123456)
#             agent_input = {
#                 **request.character_data,
#                 "messages": request.chat_history
#             }

#             dynamic_prompt = generate_dynamic_prompt(agent_input)

#         # ==============================
#         # Step 2: 调用主处理流程
#         # ==============================
#         if dynamic_prompt:
#             # 如果生成了动态prompt，传入middleware
#             result = middleware.run(
#                 request.message,
#                 # system_prompt_override=dynamic_prompt
#             )
#         else:
#             result = middleware.run(request.message)

#         return ChatResponse(
#             message=result,
#             dynamic_prompt_used=dynamic_prompt,
#             success=True
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"处理请求时发生错误: {str(e)}"
#         )

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    接收用户输入的文本，返回处理结果
    """

    try:
        dynamic_prompt = None
        result = None  # 先不生成消息

        # ==============================
        # Step 1: 动态提示词 Agent 判断
        # ==============================
        if request.character_data and request.chat_history:
            agent_input = {
                **request.character_data,
                "messages": request.chat_history
            }

            dynamic_prompt = generate_interaction_guidance(agent_input)
            print(f"生成的动态提示词: {dynamic_prompt}")

        # ==============================
        # Step 2: 调用主处理流程
        # ==============================
        # if dynamic_prompt:
            # print("=== 使用动态提示词调用 middleware ===")
            # result = middleware.run(
            #     request.message,
            #     # system_prompt_override=dynamic_prompt
            # )
        # else:
            # print("=== 使用默认提示词调用 middleware ===")
            # result = middleware.run(request.message)

        return ChatResponse(
            message=result,  # 如果不生成消息则为 None
            dynamic_prompt_used=dynamic_prompt,
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