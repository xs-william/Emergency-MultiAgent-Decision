# ==========================================
# Module: Task Executor
# File: executor/task_executor.py
# ==========================================
# 🧩 功能概述：
#   - 执行具体任务的调用器模块；
#   - 支持多种任务类型的处理逻辑；
#   - 提供统一的任务执行接口。
# ==========================================

from typing import Dict, Any
import json, os
from app.llm_service.model_registry import get_llm_client
import base64


class TaskExecutor:
    """任务执行器"""

    def __init__(self, image, audio_path, llm_model="gpt-4o", api_key: str = None):
        self.llm_client = get_llm_client(model_name=llm_model, api_key=api_key)
        self.image = image # ndarray
        self.audio_path = audio_path
        # ndarray to base64
        self.image_base64 = base64.b64encode(self.image.tobytes()).decode("utf-8") if self.image is not None else None
        self.audio_base64 = base64.b64encode(open(audio_path, "rb").read()).decode("utf-8") if audio_path else None

    def prompt_for_task(self, task: Dict[str, Any]) -> str:
        """根据任务类型生成对应的 prompt"""
        task_goal = task.get("task_goal", "")
        task_input = task.get("task_input", "")
        task_expected_output = task.get("expected_output", "")
        text = f"""
        You are an emergency multi-agent planner.

        The user is describing a potential emergency scenario.
        Your goal is to **analyze the situation** and **decompose it into specific, actionable sub-tasks**
        that different AI modules can perform collaboratively.
        If none of the provided input data is relevant to your task goal, imagine a fire in department store scenario to complete your task.

        Your goals may be:
        - Visual perception (for analyzing environment or objects)
        - Audio recognition (for identifying distress sounds, alarms, or human voices)
        - Text reasoning (for understanding user descriptions or requests)
        - Decision-making (for proposing response actions)

        Your Task Goal Is To {task_goal}
        Your Task Input Is {task_input}
        Your Task Mission Is To Produce {task_expected_output}

        Your result must include:
        1. task_id: unique incremental ID (T1, T2, ...)
        2. task_output: what result or data this task should produce

        Return STRICT JSON ONLY, like this:
        {{
            "task_output": "the fire source is in the north-west corner of the image, which is kitchen area"
        }}
        """
        res = [{"type": "text", "text": text}]
        if task_input == "image_data":
            res = [{"type": "text", "text": text}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{self.image_base64}"}}]
        elif task_input == "audio_data":
            res = [{"type": "text", "text": text}, {"type": "audio_url", "audio_url": {"url": f"data:audio/mp3;base64,{self.audio_base64}"}}]
        return json.dumps(res)

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个任务并返回结果"""
        prompt = self.prompt_for_task(task)

        print(f"🔸 Executing Task ID: {task.get('task_id', '')}")
        response = self.llm_client.send_request(prompt)
        parsed_response = self.llm_client.safe_json_parse(response)

        return {
            "task_id": task.get("task_id", ""),
            "task_output": parsed_response.get("task_output", "")
        }


def run_tasks_execution(tasks: Dict[str, Any], image, audio, api_key: str = None) -> Dict[str, Any]:
    """统一接口：执行任务列表"""
    executor = TaskExecutor(image, audio, api_key=api_key)
    results = []
    for task in tasks:
        result = executor.execute_task(task)
        results.append(result)

    tasks_results = {"results": results}

    return tasks_results
