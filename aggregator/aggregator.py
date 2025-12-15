# ==========================================
# Module: Decision Aggregator
# File: aggregator/aggregator.py
# ==========================================
# 🧩 模块功能：
#   - 负责读取并整合“用户输入”与“执行器结果”；
#   - 构建结构化的 Prompt 提示词；
#   - 调用 LLM 生成最终的决策建议报告；
#   - 支持本地开发 (.env) 与系统集成 (Pipeline) 两种启动方式。
# ==========================================

import json
import os
import sys
from typing import Dict, Any

# ==========================================
# 1. 环境与路径配置
# ==========================================
# 尝试加载本地开发环境的 .env 文件 (兼容性设计)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # 如果未安装 python-dotenv，静默跳过

# 将项目根目录添加到系统路径，确保能导入 app 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# 导入项目内部模块
from app.llm_service.openai_client import OpenAIClient
from app.config_loader import load_api_key 


class Aggregator:
    """
    决策总结器 (Aggregator)
    -----------------------
    核心职责：作为系统的“大脑”，负责综合多源信息并生成最终行动指令。
    """
    
    def __init__(self, api_key: str = None):
        """
        初始化总结器
        :param api_key: (可选) 优先使用传入的 Key，否则自动读取环境变量
        """
        # 定义日志与报告的文件路径
        self.log_dir = os.path.join(project_root, "output", "logs")
        self.input_log = os.path.join(self.log_dir, "last_input.json")
        self.result_log = os.path.join(self.log_dir, "last_executor_result.json")
        self.report_path = os.path.join(self.log_dir, "final_decision_report.txt")

        # 初始化大模型客户端
        try:
            # 逻辑：优先使用 pipeline 传来的 key，若无则自动回退到环境变量
            self.llm_client = OpenAIClient(api_key=api_key)
            print("✅ [Aggregator] LLM 服务连接成功")
        except Exception as e:
            print(f"❌ [Aggregator] 初始化失败: {e}")
            self.llm_client = None

    # ==========================
    # 🟢 任务 11：多源信息读取与整合
    # ==========================
    def load_context_from_logs(self) -> Dict[str, Any]:
        """
        从日志文件中读取上下文信息
        :return: 包含 user_query 和 task_results 的字典
        """
        print(f"🚀 [任务11] 正在读取日志文件...")
        context = { "user_query": "", "task_results": [] }

        # 1. 读取用户原始意图
        if os.path.exists(self.input_log):
            try:
                with open(self.input_log, 'r', encoding='utf-8') as f:
                    input_data = json.load(f)
                    # 兼容性处理：提取嵌套的 text_content 或直接转换
                    if isinstance(input_data, dict) and "text" in input_data:
                        context["user_query"] = input_data["text"].get("text_content", str(input_data))
                    else:
                        context["user_query"] = str(input_data)
            except Exception as e:
                print(f"⚠️ [Warn] 读取输入日志出错: {e}")
        
        # 2. 读取执行器的执行结果
        if os.path.exists(self.result_log):
            try:
                with open(self.result_log, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                    if "results" in result_data:
                        context["task_results"] = result_data["results"]
            except Exception as e:
                print(f"⚠️ [Warn] 读取结果日志出错: {e}")
                
        return context

    # ==========================
    # 🟡 任务 12：决策提示词构建
    # ==========================
    def construct_prompt(self, context: Dict[str, Any]) -> str:
        """
        根据上下文构建 LLM 提示词 (Prompt Engineering)
        """
        print(f"🚀 [任务12] 正在构建提示词...")
        user_query = context.get("user_query", "无用户输入")
        task_results = context.get("task_results", [])

        # 格式化任务执行结果
        results_str = ""
        for task in task_results:
            t_id = task.get("task_id", "未知ID")
            t_out = task.get("task_output", "无结果")
            results_str += f"- [步骤 {t_id}] 执行结果: {t_out}\n"

        # 组装最终 Prompt
        prompt = f"""
你是一个专业的应急决策辅助专家。请根据以下信息生成一份详细的决策建议报告。

【用户原始需求】：
{user_query}

【现场排查与系统执行结果】：
{results_str}

请基于上述信息：
1. 【态势总结】：简要概括当前现场的关键情况。
2. 【风险研判】：分析当前存在的潜在风险。
3. 【决策建议】：给出具体的下一步行动指令建议。

请直接输出报告内容，保持专业、客观。
"""
        return prompt

    # ==========================
    # 🔴 任务 13：生成并输出决策报告
    # ==========================
    def generate_decision(self) -> str:
        """
        执行完整的决策生成流程
        :return: 生成的决策报告文本
        """
        if not self.llm_client:
            return "❌ 错误：API Key 未配置，无法调用模型。"

        # 1. 加载上下文
        context = self.load_context_from_logs()
        
        # 2. 构建 Prompt
        prompt = self.construct_prompt(context)
        
        # 3. 调用大模型
        print(f"🚀 [任务13] 正在请求大模型生成决策...")
        try:
            response = self.llm_client.send_request(prompt)
            
            # 控制台输出报告预览
            print("\n" + "="*40)
            print("📄 最终决策报告 (Final Decision Report)")
            print("="*40)
            print(response)
            print("="*40 + "\n")
            
            # 持久化保存报告
            with open(self.report_path, 'w', encoding='utf-8') as f:
                f.write(response)
            print(f"✅ 报告已保存至: {self.report_path}")
            
            return response
            
        except Exception as e:
            print(f"❌ [任务13] 调用失败: {e}")
            return "生成报告失败"


# ==========================================
# 🛠️ 模块测试入口
# ==========================================
if __name__ == "__main__":
    # 本地直接运行时，不传参，自动加载 .env 配置
    print("🔧 正在启动 Aggregator 模块测试...")
    agg = Aggregator()
    agg.generate_decision()
