# middleware/tool_selector.py

import json
from llm.llm_client import call_llm_with_tools
from tools.dynamic_prompt import generate_interaction_guidance


class LLMToolSelectorMiddleware:

    def __init__(self, tools: list):
        self.tools = {tool.name: tool for tool in tools}

    def get_tool_schemas(self):
        return [tool.get_schema() for tool in self.tools.values()]

    def run(self, user_input: str, role_info: dict = None, chat_history: list = None):

        try:
            # ===============================
            # 1️⃣ 让 AI 决定是否生成动态提示词
            # ===============================
            system_prompt = "你是一个智能助手，可以调用工具帮助用户。"

            if role_info and chat_history:
                agent_input = {
                    **role_info,
                    "messages": chat_history
                }

                dynamic_prompt = generate_interaction_guidance(agent_input)

                # 如果 AI 生成了完整 system prompt
                if dynamic_prompt:
                    system_prompt = dynamic_prompt

            # ===============================
            # 2️⃣ 构建消息（不再拼接角色字段）
            # ===============================
            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # 历史对话
            if chat_history:
                for msg in chat_history[-5:]:
                    messages.append({
                        "role": msg.get("speaker", "user"),
                        "content": msg.get("message", "")
                    })

            # 当前输入
            messages.append({
                "role": "user",
                "content": user_input
            })

            # ===============================
            # 3️⃣ 交给 LLM 决定是否调用工具
            # ===============================
            response_message = call_llm_with_tools(
                messages,
                self.get_tool_schemas()
            )

            # ===============================
            # 4️⃣ 工具处理
            # ===============================
            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                tool = self.tools.get(tool_name)

                if not tool:
                    return {"type": "error", "content": "工具不存在"}

                result = tool.run(**arguments)

                return {
                    "type": "tool_result",
                    "data": result
                }

            # ===============================
            # 5️⃣ 普通聊天回复
            # ===============================
            return {
                "type": "chat",
                "content": getattr(response_message, "content", "无法处理请求")
            }

        except Exception as e:
            print(f"中间件运行错误: {e}")
            return {
                "type": "error",
                "content": f"处理请求时发生错误: {str(e)}"
            }