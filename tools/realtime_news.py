from tools.base import BaseTool


class RealtimeNewsTool(BaseTool):
    name = "realtime_news"

    def get_schema(self):
        return {
            "type": "function",
            "function": {
                "name": "realtime_news",
                "description": "【世界新闻记者角色】当用户询问新闻、热点事件、最新消息时调用此工具。作为世界新闻记者，你必须以'作为一名世界新闻记者，我为您报道...'为开头，用专业记者的口吻回复用户。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "用户想了解的新闻关键词（可选）"
                        }
                    },
                    "required": []
                }
            }
        }

    def run(self, keywords: str = None):
        # 不需要返回实际数据，LLM会根据上下文自动以记者身份回复
        print(f"【工具调用】realtime_news，关键词: {keywords}")
        return {
            "status": "ready",
            "message": "请以世界新闻记者身份回复"
        }
