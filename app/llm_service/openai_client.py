# ==========================================
# Module: OpenAI GPT Client
# File: app/llm_service/openai_client.py
# ==========================================
# 🧩 模块功能：
#   - 负责 GPT 系列模型（包括 GPT-4o）调用；
#   - 兼容 openai==0.28.0；
#   - 支持自定义 API Base（如 Nuwa API）。
# ==========================================

import openai
from typing import Dict, Any
from app.llm_service.base_client import BaseLLMClient
from app.config_loader import load_api_key


class OpenAIClient(BaseLLMClient):
    """基于 openai==0.28.0 的 GPT 调用实现"""

    def __init__(self, api_key: str = None, model_name: str = "gpt-4o", temperature: float = 0.3):
        super().__init__(api_key, temperature)
        openai.api_key = load_api_key(api_key)
        openai.api_base = "https://api.nuwaapi.com/v1"
        self.model_name = model_name

    def send_request(self, prompt: str) -> str:
        """发送 prompt 并返回原始模型响应文本"""
        response = openai.ChatCompletion.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": "You are an intelligent reasoning agent for emergency tasks."},
                {"role": "user", "content": prompt},
            ],
        )
        return response["choices"][0]["message"]["content"].strip()
