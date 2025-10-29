# ==========================================
# Module: Layout Manager
# File: interface/components/layout_manager.py
# ==========================================
# 🧩 模块功能：
#   - 定义界面布局（两栏结构）；
#   - 可扩展为Tabs或多页布局；
# ==========================================

# 延迟注入不美观，直接用顶层的init函数来直接导入
from interface import gr

def create_layout():
    # 解决循环导入的问题，如果放在函数外导入，则和gradio_app中的gradio循环导入了
    # import gradio as gr

    """创建页面两栏布局"""
    with gr.Row():
        left_col = gr.Column(scale=5, min_width=400)
        right_col = gr.Column(scale=7, min_width=500)
        return left_col, right_col
