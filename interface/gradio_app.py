# ==========================================
# Module: Gradio Application Entrypoint
# File: interface/gradio_app.py
# ==========================================
# 🧩 模块功能：
#   - 整合所有界面组件与回调逻辑；
#   - 提供项目交互式可视化入口；
#   - 负责界面布局与逻辑绑定；
# ==========================================

import gradio as gr
import sys, os

# 将项目根目录加入 sys.path（自动推断，无需修改）
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from interface.components.input_panel import build_input_panel
from interface.components.output_panel import build_output_panel
from interface.components.layout_manager import create_layout
from interface.callbacks.run_pipeline import handle_run
from interface.callbacks.update_report import handle_clear, handle_load_example


def launch_ui():
    """构建完整的 Gradio 应急多智能体系统界面"""
    with gr.Blocks(title="Emergency Multi-Agent Decision System") as demo:
        gr.Markdown(
            """
            ## 🚨 Multi-Agent Intent Understanding & Decision System  
            Provide **Text / Image / Audio** and your **OpenAI API Key**  
            to run multimodal reasoning and collaborative decision-making.
            """
        )

        # ========== 页面布局 ==========
        left_col, right_col = create_layout()
        with left_col:
            api_key, user_text, user_image, user_audio, run_btn, clear_btn, examples = build_input_panel()
        with right_col:
            summary_json, visual_gallery, status_box = build_output_panel()

        # ========== 绑定交互 ==========
        run_btn.click(
            fn=handle_run,
            inputs=[api_key, user_text, user_image, user_audio],
            outputs=[summary_json, visual_gallery, status_box],
        )

        clear_btn.click(
            fn=handle_clear,
            inputs=[],
            outputs=[user_text, user_image, user_audio, summary_json, visual_gallery, status_box],
        )

        for i, btn in enumerate(examples, start=1):
            btn.click(
                fn=lambda x=i: handle_load_example(x),
                inputs=[],
                outputs=[user_text, user_image, user_audio],
            )

        gr.Markdown(
            "<div style='text-align:center; color:gray;'>"
            "© 2025 Emergency Multi-Agent Decision System • Gradio Frontend v1.0"
            "</div>"
        )

    return demo


if __name__ == "__main__":
    print("✅ Launching Gradio UI ...")
    ui = launch_ui()
    ui.launch(server_name="localhost", server_port=7860, share=True)
    print("✅ Gradio UI started successfully.")
