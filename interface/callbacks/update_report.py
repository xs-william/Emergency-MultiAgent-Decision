# ==========================================
# Module: Update & Utility Callbacks
# File: interface/callbacks/update_report.py
# ==========================================
# 🧩 模块功能：
#   - 提供界面状态管理（清空、加载示例）；
#   - 辅助主回调模块；
# ==========================================

from typing import Dict, Any, List, Tuple

def handle_clear() -> Tuple[str, None, None, Dict[str, Any], List[Any], str]:
    """清空输入与输出"""
    return "", None, None, {}, [], "🧹 Cleared."

def handle_load_example(example_id: int) -> Tuple[str, None, None]:
    """加载预设示例文本"""
    examples = {
        1: "Fire detected in east building. Analyze and plan evacuation routes.",
        2: "Flood warning in district A. Assess affected areas and coordinate rescue.",
        3: "Chemical leak in lab B. Provide containment and safety guidance."
    }
    text = examples.get(example_id, "")
    return text, None, None
