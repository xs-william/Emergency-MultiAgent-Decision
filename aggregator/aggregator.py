# ==========================================
# Module: Aggregator
# File: aggregator/aggregator.py
# ==========================================
# 🧩🧩🧩 功能概述：
#   - 整合Executor任务结果和用户意图，生成决策报告；
#   - 使用LLM进行多模态结果融合与推理；
#   - 输出结构化JSON报告和可视化文件。
# ==========================================

import json
import os
from typing import Dict, Any, List
from app.llm_service.model_registry import get_llm_client

class Aggregator:
    """总结器：聚合任务结果，生成决策报告"""
    
    def __init__(self, api_key: str = None, model_name: str = "gpt-4o"):
        self.llm_client = get_llm_client(model_name=model_name, api_key=api_key)
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def merge_inputs(self, executor_results: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """
        输入整合模块：收集任务结果和用户意图
        :param executor_results: Executor输出，包含任务结果和共享意图变量
        :param user_query: 用户原始查询
        :return: 统一上下文字典
        """
        tasks_summary = []
        visual_assets = []
        
        # 提取任务摘要和文件路径
        for task_result in executor_results.get("results", []):
            tasks_summary.append(f"Task {task_result['task_id']}: {task_result.get('summary', '')}")
            visual_assets.extend(task_result.get("output_files", []))
        
        # 构建统一上下文
        merged_context = {
            "context_text": " ".join(tasks_summary),
            "context_files": visual_assets,
            "shared_intent": executor_results.get("intent_context", {}),
            "user_query": user_query
        }
        return merged_context
    
    def rebuild_intent(self, merged_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        用户意图分析模块：重构高层目标
        :param merged_context: 整合后的上下文
        :return: 意图目标字典
        """
        user_query = merged_context["user_query"]
        shared_intent = merged_context["shared_intent"]
        
        # 简单规则提取关键目标（可扩展为LLM解析）
        goal = "生成应急决策报告"
        if "救援" in user_query:
            goal = "优化救援方案"
        elif "评估" in user_query:
            goal = "风险评估"
        
        return {
            "user_goal": goal,
            "expected_output": "包含态势总结和行动建议的结构化报告",
            "style": shared_intent.get("style", "正式汇报")
        }
    
    def build_decision_prompt(self, merged_context: Dict[str, Any], intent_info: Dict[str, Any]) -> str:
        """
        决策Prompt构建器：生成LLM提示
        :param merged_context: 统一上下文
        :param intent_info: 意图信息
        :return: 格式化Prompt字符串
        """
        shared_intent = merged_context["shared_intent"]
        context_text = merged_context["context_text"]
        user_query = merged_context["user_query"]
        
        prompt = f"""
你是一个应急指挥智能体，负责生成综合决策报告。

[用户目标]
{intent_info['user_goal']}

[系统上下文]
地点：{shared_intent.get('location', '未知')}
风险等级：{shared_intent.get('risk_level', '未知')}
任务优先级：{shared_intent.get('priority', ['安全', '效率'])}

[任务结果汇总]
{context_text}

[用户需求]
{user_query}

[输出要求]
请基于以上信息生成：
1. 统一的态势总结（situation_overview）；
2. 明确的行动决策建议（recommended_actions），列表形式；
3. 风险评估（risk_assessment），包括火势强度和疏散风险；
4. 语气正式，面向应急指挥汇报。

返回严格JSON格式：
{{
    "situation_overview": "总结文本",
    "recommended_actions": ["行动1", "行动2"],
    "risk_assessment": {{
        "fire_intensity": "High/Medium/Low",
        "evacuation_risk": "High/Medium/Low"
    }}
}}
"""
        return prompt
    
    def generate_report(self, executor_results: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """
        LLM汇总与生成模块：执行决策生成
        :param executor_results: Executor输出
        :param user_query: 用户原始查询
        :return: 结构化报告字典
        """
        # 步骤1：输入整合
        merged_context = self.merge_inputs(executor_results, user_query)
        
        # 步骤2：意图重构
        intent_info = self.rebuild_intent(merged_context)
        
        # 步骤3：构建Prompt并调用LLM
        prompt = self.build_decision_prompt(merged_context, intent_info)
        llm_response = self.llm_client.send_request(prompt)
        
        # 解析LLM响应
        try:
            decision_data = json.loads(llm_response)
        except json.JSONDecodeError:
            decision_data = {
                "situation_overview": "无法解析决策数据",
                "recommended_actions": [],
                "risk_assessment": {"fire_intensity": "Unknown", "evacuation_risk": "Unknown"}
            }
        
        # 步骤4：输出结构化
        report = {
            "final_summary": {
                "situation_overview": decision_data.get("situation_overview", ""),
                "recommended_actions": decision_data.get("recommended_actions", []),
                "risk_assessment": decision_data.get("risk_assessment", {})
            },
            "visual_outputs": merged_context["context_files"],
            "report_file": os.path.join(self.output_dir, "final_report.txt"),
            "generated_at": json.dumps(os.path.getctime(__file__))  # 伪时间戳
        }
        
        # 保存文本报告
        with open(report["report_file"], "w", encoding="utf-8") as f:
            f.write(f"态势总结：{report['final_summary']['situation_overview']}\n")
            f.write("行动建议：\n")
            for action in report['final_summary']['recommended_actions']:
                f.write(f"- {action}\n")
        
        # 日志记录
        os.makedirs("output/logs", exist_ok=True)
        with open("output/logs/last_aggregator_result.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report

def run_aggregator(executor_results: Dict[str, Any], user_query: str, api_key: str = None) -> Dict[str, Any]:
    """统一接口：运行Aggregator生成报告"""
    aggregator = Aggregator(api_key=api_key)
    return aggregator.generate_report(executor_results, user_query)

if __name__ == "__main__":
    # 测试用例
    sample_executor_results = {
        "results": [
            {
                "task_id": "T1",
                "summary": "火源位于南区A栋东侧，热度高风险区域半径约20米。",
                "output_files": ["output/fire_heatmap.png"]
            },
            {
                "task_id": "T2",
                "summary": "安全区在西北角，路径规划推荐北门出入口。",
                "output_files": ["output/route.json"]
            }
        ],
        "intent_context": {
            "goal": "优化救援路径",
            "location": "南区A栋",
            "risk_level": "high"
        }
    }
    user_query = "请生成救援决策报告。"
    
    report = run_aggregator(sample_executor_results, user_query)
    print(json.dumps(report, indent=2, ensure_ascii=False))