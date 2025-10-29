# ==========================================
# Module: Base LLM Client
# File: app/llm_service/base_client.py
# ==========================================
# 🧩 模块功能：
#   - 提供统一的大模型客户端抽象；
#   - 所有模型适配器需继承此类并实现 send_request。
# ==========================================

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLLMClient(ABC):
    """统一大模型调用接口"""

    def __init__(self, api_key: str = None, temperature: float = 0.3):
        self.api_key = api_key
        self.temperature = temperature

    @abstractmethod
    def send_request(self, prompt: str) -> str:
        """发送请求到 LLM 并返回原始响应文本"""
        pass

    @staticmethod
    def safe_json_parse(text: str) -> Dict[str, Any]:
        """通用 JSON 解析工具"""
        import json, re
        try:
            return json.loads(text)
        except Exception:
            match = re.search(r"\{[\s\S]*\}", text)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    pass
        return {"error": "Invalid JSON response"}
