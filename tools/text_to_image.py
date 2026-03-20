from tools.base import BaseTool


class TextToImageTool(BaseTool):
    name = "text_to_image"

    def get_schema(self):
        return {
            "type": "function",
            "function": {
                "name": "text_to_image",
               "description": (
                    "根据用户提供的文本生成图片。"
                    "Supports multiple languages: English, 中文, 日本語, etc. "
                    "Any user message that requests generating/creating/sending an image/photo should trigger this tool."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "If the user asks for an image in any language (English, Chinese, Japanese, etc.), call the `text_to_image` tool with the prompt translated to English if needed."
                        }
                    },
                    "required": ["prompt"]
                }
            }
        }

    def run(self, prompt: str):
        print(f"【工具调用】text_to_image，提示: {prompt}")
        return {
            "tool": self.name,
            "message": "告知用户现在正在生成图片",
            "task_id": "task_12345",
            # "image_url": f"https://fake-image/{prompt}.png"
        }