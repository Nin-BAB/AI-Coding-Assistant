"""
Agent 入门演示 —— 最小可运行版本

Agent = LLM + Tools + 循环（思考→行动→观察）

当前已实现 2 个工具：
1. 执行 Python 代码
2. 查询当前时间
"""
from openai import OpenAI
from config import API_KEY, API_BASE, MODEL

client = OpenAI(api_key=API_KEY, base_url=API_BASE)


def run_python_code(code: str) -> str:
    """执行 Python 代码并返回结果"""
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return str(local_vars)
    except Exception as e:
        return f"执行错误: {e}"


def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


TOOLS_DESCRIPTION = """
你是一个 AI 编程助手，你可以使用以下工具来帮助用户：

工具 1：run_python_code
- 功能：执行 Python 代码并返回结果
- 用法：当你需要运行代码验证时使用
- 输入：Python 代码字符串（不要包含 input()，无法交互）

工具 2：get_current_time
- 功能：获取当前时间
- 用法：当用户问时间相关问题时使用
- 输入：无

=== 输出格式规则 ===

情况 A：如果需要使用工具：
TOOL: 工具名
ARGS: 参数

例如：用户说"帮我算 1+1"
TOOL: run_python_code
ARGS: print(1+1)

情况 B：如果可以直接回答：
ANSWER: 你的回答

=== 规则 ===
1. 每次只能调用一个工具
2. 不要编造结果，必须调用工具获取真实结果
3. 调用工具后，我会把结果发给你，由你决定下一步
"""


def run_agent(user_query: str, max_steps: int = 5) -> str:
    """
    Agent 主循环：思考 → 决定调用工具或直接回答 → 执行 → 观察 → 继续

    Args:
        user_query: 用户输入
        max_steps: 最大思考轮数

    Returns:
        最终回答
    """
    messages = [
        {"role": "system", "content": TOOLS_DESCRIPTION},
        {"role": "user", "content": user_query}
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3,
        )
        reply = response.choices[0].message.content

        if reply.startswith("TOOL:"):
            lines = reply.strip().split("\n")
            tool_name = lines[0].replace("TOOL:", "").strip()
            args_lines = [l for l in lines[1:] if l.startswith("ARGS:")]
            args_str = args_lines[0].replace("ARGS:", "").strip() if args_lines else ""

            if tool_name == "run_python_code":
                result = run_python_code(args_str)
            elif tool_name == "get_current_time":
                result = get_current_time()
            else:
                result = f"错误：未知工具 {tool_name}"

            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content": f"工具返回结果：{result}\n请根据这个结果继续分析并给出最终答案。"})

        elif reply.startswith("ANSWER:"):
            return reply.replace("ANSWER:", "").strip()

        else:
            return reply

    return "步骤超限，复杂任务需要更多步骤。"


if __name__ == "__main__":
    print("=" * 50)
    print("Agent 演示")
    print("=" * 50)

    print("\n测试 1: 计算斐波那契数列前 10 项")
    result = run_agent("请帮我计算斐波那契数列的前10项，并用Python验证结果，然后告诉我当前时间")
    print(f"\n最终回答:\n{result}")

    print("\n测试 2: 普通知识问题")
    result = run_agent("Python的list和tuple有什么区别？")
    print(f"\n最终回答:\n{result}")
