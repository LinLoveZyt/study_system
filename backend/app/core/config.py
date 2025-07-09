# app/core/config.py
import os
from pathlib import Path

# 项目根目录
# 使用 Path(__file__).resolve() 来获取当前文件的绝对路径
# .parent.parent 将我们带到 app 目录的父目录，即 backend 目录
BACKEND_ROOT = Path(__file__).resolve().parent.parent

# 数据存储目录
DATA_DIR = BACKEND_ROOT / "data"
USER_PROFILES_DIR = DATA_DIR / "user_profiles"
LEARNING_MATERIALS_DIR = DATA_DIR / "learning_materials"

# LLM 配置
# 请确保您已通过 Ollama 下载并运行了此模型
OLLAMA_MODEL_NAME = "qwen2:7b" # 您可以换成您的模型，例如 "qwen3:8b-q8_0"
LLM_JSON_RETRY_ATTEMPTS = 3
OLLAMA_TIMEOUT = 300 # 设置更长的超时时间，以防模型生成内容耗时过长

# 确保目录存在
USER_PROFILES_DIR.mkdir(parents=True, exist_ok=True)
LEARNING_MATERIALS_DIR.mkdir(parents=True, exist_ok=True)
