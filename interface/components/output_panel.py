# ==========================================
# Module: Output Panel
# File: interface/components/output_panel.py
# ==========================================
# 🧩 模块功能：
#   - 定义输出显示区域；
#   - 包括 JSON结果展示、图片输出和状态栏；
# ==========================================

# 延迟注入不美观，直接用顶层的init函数来直接导入
from interface import gr

def build_output_panel():
    # 解决循环导入的问题，如果放在函数外导入，则和gradio_app中的gradio循环导入了
    # import gradio as gr

    """构建右侧输出区域组件"""
    with gr.Column():
        gr.Markdown("### ✅ Task Decomposition (JSON)")
        tasks_json = gr.JSON(label="Structured Output", value={})

        gr.Markdown("### 🖼️ Visual Outputs")
        visual_gallery = gr.Gallery(
            label="Visual Outputs",
            columns=2,
            height=360
        )

        gr.Markdown("### 📣 Status & Logs")
        status_box = gr.Textbox(label="Status", value="Ready.", interactive=False)

    return tasks_json, visual_gallery, status_box
