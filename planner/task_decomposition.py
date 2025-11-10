# ==========================================
# Module: Task Decomposition (LLM-based)
# ==========================================
# 🧩 功能概述：
#   - 基于 GPT-4o 的任务规划与分解；
#   - 自动生成结构化 JSON 任务表；
#   - 输出任务 ID、目标、输入、输出标准等；
#   - 供调用器模块执行多模型调度。
# ==========================================

from typing import Dict, Any
import json, os
from app.llm_service.model_registry import get_llm_client


class TaskDecomposer:
    """基于 LLM 的任务分解器"""

    def __init__(self, api_key: str = None, model_name: str = "gpt-4o", temperature: float = 0.4):
        self.client = get_llm_client(model_name=model_name, api_key=api_key, temperature=temperature)

    def _build_prompt(self, multimodal_data: Dict[str, Any]) -> str:
        """构建任务分解 Prompt"""
        text_input = multimodal_data.get("text", {}).get("text_content", "")
        has_image = multimodal_data.get("image", {}).get("image_valid", False)
        has_audio = multimodal_data.get("audio", {}).get("audio_valid", False)

        return f"""
        You are an emergency multi-agent planner.

        The user is describing a potential emergency scenario.
        Your goal is to **analyze the situation** and **decompose it into specific, actionable sub-tasks**
        that different AI modules can perform collaboratively.

        Consider:
        - Visual perception (for analyzing environment or objects)
        - Audio recognition (for identifying distress sounds, alarms, or human voices)
        - Text reasoning (for understanding user descriptions or requests)
        - Decision-making (for proposing response actions)

        Each sub-task must include:
        1. task_id: unique incremental ID (T1, T2, ...)
        2. task_goal: what this task tries to achieve
        3. task_input: what information is needed for this task
        4. expected_output: what result or data this task should produce
        5. priority: "high" / "medium" / "low"
        6. dependencies: list of task_ids that must complete before this one

        Return STRICT JSON ONLY, like this:
        {{
            "overall_goal": "Summarize the user’s emergency need and general objective.",
            "tasks": [
                {{
                    "task_id": "T1",
                    "task_goal": "Identify fire location from visual input",
                    "task_input": "image_data",
                    "expected_output": "coordinates or bounding boxes of fire sources",
                    "priority": "high",
                    "dependencies": []
                }},
                {{
                    "task_id": "T2",
                    "task_goal": "Detect human distress signals from audio",
                    "task_input": "audio_data",
                    "expected_output": "transcript and classification of distress type",
                    "priority": "medium",
                    "dependencies": ["T1"]
                }}
            ]
        }}

        [User Text]: {text_input or "N/A"}
        [Image Provided]: {has_image}
        [Audio Provided]: {has_audio}
        """

    def generate_plan(self, multimodal_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务分解"""
        prompt = self._build_prompt(multimodal_data)
        try:
            raw_text = self.client.send_request(prompt)
            parsed = self.client.safe_json_parse(raw_text)
        except Exception as e:
            print(f"[ERROR] Task decomposition failed: {e}")
            parsed = self._default_result()

        os.makedirs("output/logs", exist_ok=True)
        with open("output/logs/last_task_plan.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        return parsed

    @staticmethod
    def _default_result() -> Dict[str, Any]:
        """默认返回结构"""
        return {
            "overall_goal": "unknown",
            "tasks": [
                {
                    "task_id": "T1",
                    "task_goal": "undefined",
                    "task_input": "N/A",
                    "expected_output": "N/A",
                    "priority": "medium",
                    "dependencies": []
                }
            ]
        }


def generate_task_plan(multimodal_data: Dict[str, Any], api_key: str = None) -> Dict[str, Any]:
    """统一接口"""
    decomposer = TaskDecomposer(api_key=api_key)
    result = decomposer.generate_plan(multimodal_data)
    result["input_summary"] = multimodal_data.get("input_summary", "")
    return result
