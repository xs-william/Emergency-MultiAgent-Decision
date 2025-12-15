import json
import os
import sys
from typing import Dict, Any

# ==========================================
# 💡 兼容性设计：本地开发环境加载
# ==========================================
# 这里使用 try-except 结构：
# 1. 如果你在本地安装了 python-dotenv，它会加载 .env 文件中的 Key。
# 2. 如果队友没装这个库（或者在服务器运行），这几行代码会自动跳过，
#    直接使用系统环境变量（符合队友 config_loader.py 的逻辑）。
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # 队友没装 python-dotenv 也没关系，静默跳过

# ==========================================
# 路径配置与模块导入
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# 导入队友编写的标准模块
from app.llm_service.openai_client import OpenAIClient
# (可选) 导入配置加载器用于检查，或者直接信赖 OpenAIClient 内部的检查
from app.config_loader import load_api_key 

class Aggregator:
    """
    总结器模块：负责读取日志，整合信息，生成最终决策报告。
    """
    
    def __init__(self):
        # 初始化路径
        self.log_dir = os.path.join(project_root, "output", "logs")
        self.input_log = os.path.join(self.log_dir, "last_input.json")
        self.result_log = os.path.join(self.log_dir, "last_executor_result.json")
        self.report_path = os.path.join(self.log_dir, "final_decision_report.txt")

        # 初始化 LLM 客户端
        # 这里我们直接实例化，让 OpenAIClient 内部去调用 config_loader 找 Key
        # 如果找不到 Key，它会抛出 EnvironmentError，我们在下面捕获它
        try:
            # 这一步会自动去读 os.environ['OPENAI_API_KEY']
            self.llm_client = OpenAIClient()
            print("✅ [Aggregator] LLM 服务连接成功")
        except Exception as e:
            print(f"❌ [Aggregator] 初始化失败: {e}")
            print("💡 提示: 请检查环境变量 OPENAI_API_KEY 是否配置正确。")
            # 这里不阻断程序，防止导入时直接崩溃，但在生成时会再次检查
            self.llm_client = None

    def load_context_from_logs(self) -> Dict[str, Any]:
        """读取 last_input.json 和 last_executor_result.json"""
        print(f"🚀 [任务11] 正在读取日志文件...")
        context = { "user_query": "", "task_results": [] }

        # 1. 读取用户输入
        if os.path.exists(self.input_log):
            try:
                with open(self.input_log, 'r', encoding='utf-8') as f:
                    input_data = json.load(f)
                    # 兼容不同格式：优先取 text_content，否则转字符串
                    if isinstance(input_data, dict) and "text" in input_data:
                        context["user_query"] = input_data["text"].get("text_content", str(input_data))
                    else:
                        context["user_query"] = str(input_data)
            except Exception as e:
                print(f"⚠️ 读取输入日志出错: {e}")
        
        # 2. 读取执行结果
        if os.path.exists(self.result_log):
            try:
                with open(self.result_log, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                    if "results" in result_data:
                        context["task_results"] = result_data["results"]
            except Exception as e:
                print(f"⚠️ 读取结果日志出错: {e}")
                
        return context

    def construct_prompt(self, context: Dict[str, Any]) -> str:
        """构建 Prompt"""
        print(f"🚀 [任务12] 正在构建提示词...")
        user_query = context.get("user_query", "无用户输入")
        task_results = context.get("task_results", [])

        # 格式化任务结果
        results_str = ""
        for task in task_results:
            t_id = task.get("task_id", "未知ID")
            t_out = task.get("task_output", "无结果")
            results_str += f"- 步骤 {t_id} 执行结果: {t_out}\n"

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

请直接输出报告内容。
"""
        return prompt

    def generate_decision(self) -> str:
        """核心流程：生成决策报告"""
        if not self.llm_client:
            print("❌ 无法执行：LLM 客户端未成功初始化（缺少 API Key）")
            return "初始化失败"

        # 执行任务流
        context = self.load_context_from_logs()
        prompt = self.construct_prompt(context)
        
        print(f"🚀 [任务13] 正在请求大模型...")
        try:
            # 调用 OpenAIClient 的标准方法
            response = self.llm_client.send_request(prompt)
            
            print("\n" + "="*30)
            print("📄 最终决策报告")
            print("="*30)
            print(response)
            print("="*30 + "\n")
            
            # 保存报告
            with open(self.report_path, 'w', encoding='utf-8') as f:
                f.write(response)
            print(f"✅ 报告已保存至: {self.report_path}")
            return response
            
        except Exception as e:
            print(f"❌ [任务13] 调用失败: {e}")
            return "生成报告失败"

# ==========================================
# 测试入口
# ==========================================
if __name__ == "__main__":
    agg = Aggregator()
    agg.generate_decision()