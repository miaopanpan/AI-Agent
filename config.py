# config.py

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL_NAME = os.getenv("OPENROUTER_MODEL_NAME", "deepseek/deepseek-chat-v3-0324")