# ==========================================
# Module: Interface Initialization
# File: interface/__init__.py
# ==========================================
# 🧩 模块功能：
#   - 集中导入Gradio并提供全局引用；
#   - 防止循环导入问题；
#   - 支持未来框架替换（如Streamlit、Flask）；
# ==========================================

import gradio as _gr

# 🔄 全局依赖注册（依赖注入）
# 所有子模块均通过此文件访问 Gradio，而不单独 import gradio
gr = _gr

__all__ = ["gr"]
