# tools/base.py

class BaseTool:
    name: str
    description: str

    def run(self, input_text: str):
        raise NotImplementedError