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
from planner.intent_recognition import recognize_intent


def run_full_pipeline(text, image, audio, api_key=None):
    """
    系统执行主流程：
      1️⃣ 多模态输入解析；
      2️⃣ 基于 GPT-4o 的意图识别；
      3️⃣ 返回标准化输出。
    """
    print("🔹 Step 1: Parsing multimodal input...")
    multimodal_data = parse_multimodal_input(text, image, audio)

    print("🔹 Step 2: Recognizing intent (via GPT-4o)...")
    intent_result = recognize_intent(multimodal_data, api_key=api_key)

    # ⚙️ 预留后续模块
    return {
        "final_summary": intent_result,
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
