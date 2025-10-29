# ==========================================
# Module: Input Panel
# File: interface/components/input_panel.py
# ==========================================
# 🧩 模块功能：
#   - 定义输入区域组件；
#   - 包括 API Key、文本、图像、音频输入；
#   - 附带示例加载与清空按钮。
# ==========================================

# 延迟注入不美观，直接用顶层的init函数来直接导入
from interface import gr

def build_input_panel():
    # 解决循环导入的问题，如果放在函数外导入，则和gradio_app中的gradio循环导入了
    # import gradio as gr
    
    """构建左侧输入区域组件"""
    with gr.Column():
        gr.Markdown("### 🔑 OpenAI API Key")
        api_key = gr.Textbox(
            label="API Key",
            placeholder="sk-xxxxxxxxxxxxxxxx",
            type="password",
            info="Your key will not be saved; used only for current session."
        )
        
        gr.Markdown("### 🧾 User Inputs")
        user_text = gr.Textbox(
            label="Text Input",
            placeholder="Describe the emergency scenario or request...",
            lines=6
            )

        with gr.Row():
                user_image = gr.Image(label="Image Input (optional)")
                user_audio = gr.Audio(label="Audio Input (optional)", type="filepath")

        with gr.Row():
            run_btn = gr.Button("Run Analysis 🚀", variant="primary")
            clear_btn = gr.Button("Clear 🧹", variant="secondary")

        with gr.Row():
            ex1 = gr.Button("Example 1")
            ex2 = gr.Button("Example 2")
            ex3 = gr.Button("Example 3")

    return api_key, user_text, user_image, user_audio, run_btn, clear_btn, (ex1, ex2, ex3)
