# ==========================================
# Module: Run Pipeline Callback
# File: interface/callbacks/run_pipeline.py
# ==========================================
# 🧩 模块功能：
#   - 执行 pipeline 并返回结果；
#   - 校验输入、捕获异常；
#   - 提供执行状态与安全提示。
# ==========================================

from app.pipeline import run_full_pipeline
from typing import Dict, Any, List, Tuple
import traceback

# 延迟注入不美观，直接用顶层的init函数来直接导入
from interface import gr

def handle_run(api_key: str,
               user_text: str,
               user_image: Any,
               user_audio: Any
                    ) -> Tuple[Dict[str, Any], List[Any], str]:
    # 解决循环导入的问题，如果放在函数外导入，则和gradio_app中的gradio循环导入了
    # import gradio as gr

    """运行主流程"""
    try:
        if not api_key:
            return {"error": "Missing API Key."}, [], "❌ Please input your OpenAI API Key."
        if not (user_text or user_image or user_audio):
            return {"error": "No valid input."}, [], "❌ Provide at least one input."

        # ✅ 执行主流程
        result = run_full_pipeline(text=user_text, image=user_image, audio=user_audio, api_key=api_key)

        summary = result.get("final_summary", {})
        visuals = result.get("visual_outputs", [])
        return summary, visuals, "✅ Analysis complete."

    except Exception as e:
        import traceback
        tb = traceback.format_exc(limit=2)
        return {"error": str(e), "trace": tb}, [], "❌ Pipeline execution failed."
