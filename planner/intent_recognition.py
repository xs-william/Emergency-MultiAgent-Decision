# ==========================================
# Module: Intent Recognition (LLM-based)
# File: planner/intent_recognition.py
# ==========================================
# 🧩 功能概述：
#   - 基于独立 LLM Service 模块实现显式/隐式意图识别；
#   - 通过 Model Registry 动态选择模型；
#   - 输出结构化 JSON。
# ==========================================

from typing import Dict, Any
import json, os
from app.llm_service.model_registry import get_llm_client


class IntentRecognition:
    """多模态意图识别器"""

    def __init__(self, api_key: str = None, model_name: str = "gpt-4o", temperature: float = 0.3):
        self.client = get_llm_client(model_name=model_name, api_key=api_key, temperature=temperature)

    def _build_prompt(self, multimodal_data: Dict[str, Any]) -> str:
        """构建 Prompt"""
        text_input = multimodal_data.get("text", {}).get("text_content", "")
        has_image = multimodal_data.get("image", {}).get("image_valid", False)
        has_audio = multimodal_data.get("audio", {}).get("audio_valid", False)
        return f"""
        You are an emergency intent-understanding agent.
        Given the multimodal inputs, identify:
        1. explicit_intent (direct user goal)
        2. implicit_intent (hidden motivation)
        3. environment_context (key scene info)

        Return STRICT JSON only:
        {{
            "explicit_intent": "",
            "implicit_intent": "",
            "environment_context": "",
            "intent_confidence": 0.0
        }}

        [User Text]: {text_input or "N/A"}
        [Image Provided]: {has_image}
        [Audio Provided]: {has_audio}
        """

    def recognize(self, multimodal_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行意图识别"""
        prompt = self._build_prompt(multimodal_data)
        try:
            raw_text = self.client.send_request(prompt)
            parsed = self.client.safe_json_parse(raw_text)
        except Exception as e:
            print(f"[ERROR] Intent recognition failed: {e}")
            parsed = self._default_result()

        os.makedirs("output/logs", exist_ok=True)
        with open("output/logs/last_intent.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        return parsed

    @staticmethod
    def _default_result() -> Dict[str, Any]:
        return {
            "explicit_intent": "unknown",
            "implicit_intent": "unknown",
            "environment_context": "unknown",
            "intent_confidence": 0.0
        }


def recognize_intent(multimodal_data: Dict[str, Any], api_key: str = None) -> Dict[str, Any]:
    """统一模块接口"""
    recognizer = IntentRecognition(api_key=api_key)
    result = recognizer.recognize(multimodal_data)
    result["input_summary"] = multimodal_data.get("input_summary", "")
    return result
