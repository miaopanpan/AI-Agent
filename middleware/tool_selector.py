# middleware/tool_selector.py

import json
from llm.llm_client import call_llm_with_tools, call_llm
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
            # 4️⃣ 工具处理 - 支持多Agent并行调用
            # ===============================
            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                results = []
                tool_calls = []
                has_async_task = False  # 标记是否有异步任务
                async_tasks = []  # 存储异步任务信息
                
                # 遍历所有工具调用（支持多Agent并行）
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    tool = self.tools.get(tool_name)

                    # 记录工具调用信息
                    tool_calls.append({
                        "id": tool_call.id,
                        "function": tool_call.function.name,
                        "arguments": arguments
                    })

                    if not tool:
                        results.append({
                            "tool": tool_name,
                            "status": "error",
                            "error": "工具不存在"
                        })
                        continue

                    # 执行工具
                    try:
                        result = tool.run(**arguments)
                        
                        # 检查是否是异步任务（有task_id）
                        if isinstance(result, dict) and result.get("task_id"):
                            has_async_task = True
                            async_tasks.append({
                                "tool": tool_name,
                                "task_id": result.get("task_id"),
                                "message": result.get("message", "任务正在处理中")
                            })
                        
                        results.append({
                            "tool": tool_name,
                            "status": "success",
                            "data": result
                        })
                    except Exception as e:
                        results.append({
                            "tool": tool_name,
                            "status": "error",
                            "error": str(e)
                        })

                # ===============================
                # 5️⃣ 如果有异步任务，直接返回task_id给客户端
                # ===============================
                if has_async_task:
                    return {
                        "type": "async_task",
                        "async_tasks": async_tasks,
                        "message": "任务已提交，请使用task_id查询结果"
                    }

                # ===============================
                # 6️⃣ 同步任务：工具执行后，再次调用LLM生成最终回复
                # ===============================
                # 构建包含工具结果的新消息
                messages_with_tools = messages.copy()
                
                # 添加助手的消息（包含工具调用）
                assistant_msg = {
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in response_message.tool_calls
                    ]
                }
                messages_with_tools.append(assistant_msg)

                # 添加工具结果
                for i, result in enumerate(results):
                    messages_with_tools.append({
                        "role": "tool",
                        "tool_call_id": tool_calls[i].get("id", f"call_{i}"),
                        "content": json.dumps(result)
                    })

                # 再次调用LLM生成最终回复
                final_response = call_llm(messages_with_tools)
                
                return {
                    "type": "chat",
                    "content": getattr(final_response, "content", "无法处理请求")
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
