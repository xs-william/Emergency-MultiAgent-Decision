# ==========================================
# Module: Model Registry
# File: app/llm_service/model_registry.py
# ==========================================
# 🧩 模块功能：
#   - 注册与动态选择可用的大模型客户端；
#   - 未来可支持多厂商模型（OpenAI, Anthropic, Google, etc）。
# ==========================================

from typing import Dict, Type
from app.llm_service.base_client import BaseLLMClient
from app.llm_service.openai_client import OpenAIClient

# 全局模型注册表
MODEL_REGISTRY: Dict[str, Type[BaseLLMClient]] = {
    "gpt-4o": OpenAIClient,
}

def get_llm_client(model_name: str, api_key: str = None, temperature: float = 0.3) -> BaseLLMClient:
    """根据模型名动态实例化对应客户端"""
    client_cls = MODEL_REGISTRY.get(model_name)
    if not client_cls:
        raise ValueError(f"Unsupported model: {model_name}")
    return client_cls(api_key=api_key, model_name=model_name, temperature=temperature)
