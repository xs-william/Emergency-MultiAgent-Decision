# ==========================================
# Module: Pipeline Controller
# File: app/pipeline.py
# ==========================================
# 🧩 功能概述：
#   - 串联系统主执行流程；
#   - 负责模块间数据传递与日志；
#   - 提供给可视化界面的统一调用入口。
# ==========================================

from planner.multimodal_input import parse_multimodal_input
from planner.task_decomposition import generate_task_plan
from executor.executor_pipeline import run_executor_pipeline


def run_full_pipeline(text, image, audio, api_key=None):
    """
    系统执行主流程：
      1️⃣ 多模态输入解析；
      2️⃣ 基于 GPT-4o 的任务分解；
      3️⃣ 返回标准化输出。
    """
    print("🔹 Step 1: Parsing multimodal input...")
    multimodal_data = parse_multimodal_input(text, image, audio)

    print("🔹 Step 2: Decomposite tasks (via GPT-4o)...")
    task_decomposition_results = generate_task_plan(multimodal_data, api_key=api_key)

    print("🔹 Step 3: Calling executors to handle subtasks...")
    executor_results = run_executor_pipeline(task_decomposition_results, image, audio, api_key=api_key)

    # ⚙️ 预留后续模块
    return {
        "final_decomposition_results": task_decomposition_results,
        "visual_outputs": []  # aggregator 接口占位
    }


if __name__ == "__main__":
    demo = run_full_pipeline(
        text="Fire detected in east building, analyze danger and plan rescue.",
        image="./examples/demo_input/fire_scene.jpg",
        audio=None,
        api_key=None
    )
    print(demo)
