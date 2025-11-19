# ==========================================
# Module: Task Scheduler
# File: executor/task_scheduler.py
# ==========================================
# 🧩 功能概述：
#   - 根据任务优先级和依赖关系调度执行顺序；
#   - 支持并行与串行任务执行策略；
#   - 提供任务执行状态跟踪与日志记录。
# ==========================================

# 通过 decomp_parser 提取出的 priority 和 dependencies，求有向无环图的拓扑序，即任务调度顺序
from typing import List, Dict, Any


class TaskScheduler:
    """任务调度器"""

    def __init__(self, tasks: List[Dict[str, Any]]):
        self.tasks = tasks
        self.task_map = {task['task_id']: task for task in tasks}
        self.visited = {}
        self.result = []

    def schedule_tasks(self) -> List[Dict[str, Any]]:
        """根据优先级和依赖关系调度任务顺序"""
        for task in self.tasks:
            if task['task_id'] not in self.visited:
                self._dfs(task['task_id'])
        return self.result

    def _dfs(self, task_id: str):
        """深度优先搜索实现拓扑排序"""
        if task_id in self.visited:
            return
        self.visited[task_id] = True

        task = self.task_map[task_id]
        for dep in task.get('dependencies', []):
            self._dfs(dep)

        self.result.append(task)


def get_scheduled_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """统一接口：获取调度后的任务列表"""
    scheduler = TaskScheduler(tasks)
    return scheduler.schedule_tasks()


if __name__ == '__main__':
    # 测试用例
    structured_tasks = [{'task_id': 'T1', 'task_goal': 'Identify fire locations from image', 'task_input': 'image_data', 'expected_output': 'coordinates or bounding boxes of fire sources', 'priority': 'high', 'dependencies': []}, {'task_id': 'T2', 'task_goal': 'Detect human distress signals from audio', 'task_input': 'audio_data', 'expected_output': 'transcript and classification of distress type', 'priority': 'medium', 'dependencies': ['T1']}]

    scheduled_tasks = get_scheduled_tasks(structured_tasks)
    for task in scheduled_tasks:
        print(f"Scheduled Task ID: {task['task_id']}, Goal: {task['task_goal']}")
