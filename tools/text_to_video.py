from tools.base import BaseTool


class TextToVideoTool(BaseTool):
    name = "text_to_video"

    def get_schema(self):
        return {
            "type": "function",
            "function": {
                "name": "text_to_video",
                "description": (
                    "根据用户提供的文本生成视频。"
                    "Supports multiple languages: English, 中文, 日本語, etc. "
                    "Any user message that requests generating/creating/sending a video should trigger this tool." 
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "If the user asks for a video in any language (English, Chinese, Japanese, etc.), call the `text_to_video` tool with the prompt translated to English if needed."
                        },
                        "duration": {
                            "type": "number",
                            "description": "视频时长（秒），默认10秒",
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
            "message": "告知用户现在正在生成视频",
            "task_id": "task_67890",
            # "video_url": f"https://fake-video/{prompt}.mp4"
        }
