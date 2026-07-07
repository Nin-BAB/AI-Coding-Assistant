"""
agent_coding.py — LangChain Agent 版 AI 编程助手

从手动 ReAct 循环升级到 LangChain Agent 框架。
- 手动解析 AI 输出 → LangChain 自动工具调用
- create_react_agent → create_agent（基于 LangGraph）
- @tool 装饰器定义工具
"""

from datetime import datetime
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from config import API_KEY, API_BASE, MODEL


# ============================================================
# 工具定义
# ============================================================

@tool
def python_executor(code: str) -> str:
    """执行 Python 代码并返回执行结果。
    当你需要验证代码逻辑、运行测试、或调试时使用。
    注意：不支持 input() 交互输入，数据要在代码中写好。"""
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return str(local_vars)
    except Exception as e:
        return f"执行错误: {e}"


@tool
def current_time() -> str:
    """获取当前的日期和时间。当用户询问时间或需要时间戳时使用。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def file_reader(filepath: str) -> str:
    """读取指定文件的内容（UTF-8 编码）。
    当你需要查看源代码、配置文件或其他文本文件时使用。
    输入参数为文件的路径字符串。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"文件读取失败: {e}"


tools = [python_executor, current_time, file_reader]


# ============================================================
# 初始化 LLM
# ============================================================
llm = ChatOpenAI(
    model=MODEL,
    openai_api_key=API_KEY,
    openai_api_base=API_BASE,
    temperature=0,
)


# ============================================================
# 创建 Agent
# ============================================================
agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "你是一个 AI 编程助手，拥有执行代码、读取文件、获取时间的能力。\n\n"
        "工作流程：\n"
        "1. 分析用户问题 → 决定是否需要工具\n"
        "2. 如果需要工具 → 调用工具获取信息\n"
        "3. 拿到结果后继续推理 → 如果还不够，继续调工具\n"
        "4. 问题解决 → 给出完整清晰的答案\n\n"
        "规则：\n"
        "- 不要编造结果，使用工具获取真实信息\n"
        "- 如果工具出错，分析原因并尝试修复\n"
        "- 最终答案要包含清晰的解释和正确的代码\n"
        "- 使用中文回答"
    ),
)


# ============================================================
# 5. 使用 Agent
# ============================================================
def chat_with_agent(query: str) -> str:
    """向 Agent 发送消息并返回回复。"""
    try:
        result = agent_graph.invoke({"messages": [{"role": "user", "content": query}]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Agent 执行出错: {e}"


def main():
    print("=" * 55)
    print("🐣 小笨的 AI 编码助手 v2.0 — LangChain Agent 版")
    print("=" * 55)
    print("输入你的问题，我来帮你写代码、调试、分析...")
    print("输入 'exit' 退出")
    print("=" * 55)

    while True:
        query = input("\n🙋 你: ").strip()

        if query.lower() in ("exit", "quit", "q"):
            print("👋 再见！下次继续")
            break

        if not query:
            continue

        print("\n🤔 小笨思考中...\n")
        result = chat_with_agent(query)
        print(f"\n🐣 小笨: {result}")


if __name__ == "__main__":
    main()
