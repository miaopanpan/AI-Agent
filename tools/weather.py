from tools.base import BaseTool


class WeatherTool(BaseTool):
    name = "get_weather"

    def get_schema(self):
        return {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的天气情况",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称"
                        }
                    },
                    "required": ["city"]
                }
            }
        }

    def run(self, city: str):
        print(f"调用天气工具，查询城市：{city}")
        return {
            "tool": self.name,
            "city": city,
            "weather": "晴天",
            "temperature": "25°C"
        }