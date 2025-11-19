# ==========================================
# Module: Decomposition Parser
# File: executor/decomp_parser.py
# ==========================================
# 🧩 功能概述：
#   - 从任务分解结果中提取结构化任务信息；
#   - 支持任务 ID、目标、输入、输出标准等字段解析；
#   - 为调用器模块提供清晰的任务调度数据。
# ==========================================

from typing import Dict, Any, List


class DecompositionParser:
    """任务分解结果解析器"""

    def __init__(self, decomposition_results: Dict[str, Any]):
        self.decomposition_results = decomposition_results

    def parse_tasks(self) -> List[Dict[str, Any]]:
        """提取并返回结构化任务列表"""
        tasks = self.decomposition_results.get("tasks", [])
        structured_tasks = []

        for task in tasks:
            structured_task = {
                "task_id": task.get("task_id", ""),
                "task_goal": task.get("task_goal", ""),
                "task_input": task.get("task_input", ""),
                "expected_output": task.get("expected_output", ""),
                "priority": task.get("priority", "medium"),
                "dependencies": task.get("dependencies", [])
            }
            structured_tasks.append(structured_task)

        return structured_tasks


def extract_tasks(decomposition_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """统一接口：提取任务列表"""
    parser = DecompositionParser(decomposition_results)
    return parser.parse_tasks()


if __name__ == '__main__':
    # 测试用例
    sample_decomposition = {
        "overall_goal": "Rescue operation planning",
        "tasks": [
            {
                "task_id": "T1",
                "task_goal": "Identify fire locations from image",
                "task_input": "image_data",
                "expected_output": "coordinates or bounding boxes of fire sources",
                "priority": "high",
                "dependencies": []
            },
            {
                "task_id": "T2",
                "task_goal": "Detect human distress signals from audio",
                "task_input": "audio_data",
                "expected_output": "transcript and classification of distress type",
                "priority": "medium",
                "dependencies": ["T1"]
            }
        ]
    }

    parser = DecompositionParser(sample_decomposition)
    tasks = parser.parse_tasks()
    print(tasks)
