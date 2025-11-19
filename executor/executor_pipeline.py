# ==========================================
# Module: Executor Pipeline
# File: executor/executor_pipeline.py
# ==========================================
# 🧩 功能概述：
#   - 执行器模块的局部主流程控制；
#   - 减少模块间耦合，提升代码复用性；
#   - 省钱且高效的调试手段。
# ==========================================

from typing import Dict, Any, List
import json, os, sys
import numpy as np
from PIL import Image
import requests

if __name__ == '__main__':
    # 将项目根目录加入 sys.path（自动推断，无需修改）
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)

from executor.decomp_parser import extract_tasks
from executor.task_scheduler import get_scheduled_tasks
from executor.task_executor import run_tasks_execution
from executor.SAM_preprocessor import sam2_image_preprocess


def run_executor_pipeline(decomposition_results: Dict[str, Any], image, audio, api_key=None) -> List[Dict[str, Any]]:
    """
    执行器模块主流程：
      1️⃣ 解析任务分解结果，提取结构化任务列表；
      2️⃣ 根据任务优先级和依赖关系调度执行顺序。
    """
    print("🔹🔹 Step 1: Extracting structured tasks from decomposition results...")
    structured_tasks = extract_tasks(decomposition_results)

    print("🔹🔹 Step 2: Scheduling tasks based on priority and dependencies...")
    scheduled_tasks = get_scheduled_tasks(structured_tasks)

    print("🔹🔹 Step 3: Preparing data for task execution...")
    image_data = None
    if type(image) == str:
        with open(image, "rb") as img_file:
            image_data = img_file.read()
            image_data = Image.open(image).convert("RGB")
    elif image is not None:
        image_data = Image.fromarray(np.array(image)).convert("RGB")
    # 等比例裁剪到最大 128x128
    image_clipped = None
    if image_data is not None:
        width, height = image_data.size
        max_size = 128
        if width > max_size or height > max_size:
            scaling_factor = min(max_size / width, max_size / height)
            new_width = int(width * scaling_factor)
            new_height = int(height * scaling_factor)
            image_clipped = image_data.resize((new_width, new_height), Image.LANCZOS)
        else:
            image_clipped = image_data.copy()

    sam2_result = sam2_image_preprocess(image_data)

    print("🔹 Step 4: Executing scheduled tasks...")
    tasks_results = run_tasks_execution(scheduled_tasks, None, None, api_key=api_key) #image_clipped

    execution_results = {"sam2_result": sam2_result, "tasks_execution": tasks_results}

    os.makedirs("output/logs", exist_ok=True)
    with open("output/logs/last_executor_result.json", "w", encoding="utf-8") as f:
        json.dump(tasks_results, f, ensure_ascii=False, indent=2)

    # print(execution_results)

    return execution_results


if __name__ == "__main__":
    # 测试用例，从 output/logs 加载
    file = open("output/logs/last_task_plan.json", "r", encoding="utf-8")
    sample_decomposition = json.load(file)
    file.close()

    executor_result = run_executor_pipeline(sample_decomposition, "test/example1/image1.png", "test/example1/voice.mp3", api_key=None)
    print(executor_result)
