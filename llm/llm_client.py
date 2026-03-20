# llm/llm_client.py

from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME, OPENROUTER_API_KEY, OPENROUTER_MODEL_NAME

# client = OpenAI(api_key=OPENAI_API_KEY)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def call_llm_with_tools(messages, tools):
    """
    调用LLM并处理工具调用
    
    Args:
        messages: 消息列表
        tools: 工具列表
        
    Returns:
        response.choices[0].message: LLM响应消息
    """
    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto"  # 让模型自动决定是否调用工具
        )

        # print("LLM Response:", response.choices[0].message)
        return response.choices[0].message
        
    except Exception as e:
        print(f"LLM调用错误: {e}")
        # 返回一个模拟的响应，避免程序崩溃
        class MockMessage:
            def __init__(self):
                self.content = "抱歉，我现在无法处理您的请求。"
                self.tool_calls = None
        
        return MockMessage()


def call_llm(messages):
    """
    调用LLM（不带工具）
    
    Args:
        messages: 消息列表
        
    Returns:
        response.choices[0].message: LLM响应消息
    """
    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL_NAME,
            messages=messages
        )

        return response.choices[0].message
        
    except Exception as e:
        print(f"LLM调用错误: {e}")
        class MockMessage:
            def __init__(self):
                self.content = "抱歉，我现在无法处理您的请求。"
        
        return MockMessage()
