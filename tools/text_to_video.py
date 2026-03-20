from tools.base import BaseTool


class TextToVideoTool(BaseTool):
    name = "text_to_video"

    def get_schema(self):
        return {
            "type": "function",
            "function": {
                "name": "text_to_video",
                "description": "根据用户提供的文本生成视频",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "生成视频的描述文本"
                        },
                        "duration": {
                            "type": "number",
                            "description": "视频时长（秒）",
                            "default": 10
                        }
                    },
                    "required": ["prompt"]
                }
            }
        }

    def run(self, prompt: str, duration: int = 10):
        print(f"【工具调用】text_to_video，提示: {prompt}，时长: {duration}秒")
        return {
            "tool": self.name,
            "task_id": "task_67890",
            "video_url": f"https://fake-video/{prompt}.mp4",
            "duration": duration
        }
