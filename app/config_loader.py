# ==========================================
# Module: Configuration Loader
# File: app/config_loader.py
# ==========================================
# 🧩 功能概述：
#   - 动态、安全地加载 OpenAI API Key；
#   - 支持用户输入与系统环境变量两种方式；
#   - 确保 key 仅存储于内存环境中，不写入磁盘。
# ==========================================

import os

def load_api_key(user_key: str = None) -> str:
    """
    加载 OpenAI API Key。
    优先使用用户输入，其次使用环境变量。
    """
    if user_key:
        os.environ["OPENAI_API_KEY"] = user_key
        print("[INFO] Using user-provided OpenAI API key.")
        return user_key

    if "OPENAI_API_KEY" in os.environ:
        print("[INFO] Using system environment API key.")
        return os.environ["OPENAI_API_KEY"]

    raise EnvironmentError("❌ Missing OpenAI API Key. Please input or set environment variable.")
