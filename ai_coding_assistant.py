"""
AI 编码助手 - 核心功能模块

覆盖代码生成、代码解析、Bug修复三大能力。
"""
from openai import OpenAI
from config import API_KEY, API_BASE, MODEL

client = OpenAI(api_key=API_KEY, base_url=API_BASE)


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """
    通用 LLM 调用函数

    Args:
        system_prompt: 系统指令
        user_prompt: 用户输入
        temperature: 生成温度，越低越确定

    Returns:
        AI 回复文本
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content


def generate_code(requirement: str, language: str = "Python") -> str:
    """
    根据需求生成代码

    Args:
        requirement: 业务需求描述
        language: 目标编程语言

    Returns:
        生成的代码
    """
    system_prompt = f"""你是一个资深{language}工程师。
请根据用户的需求，生成完整、可运行的代码。
要求：
1. 代码必须完整，包含必要的 import
2. 添加详细的中文注释说明每段逻辑
3. 包含基本的错误处理（try-except）
4. 代码风格遵循 PEP8（如果是 Python）
5. 输出时用 ``` 代码块包裹
"""
    return call_llm(system_prompt, f"请用{language}实现以下功能：\n{requirement}")


def analyze_code(code: str) -> str:
    """
    分析代码：逐行解释 + 复杂度分析 + 优化建议

    Args:
        code: 待分析的代码

    Returns:
        分析报告
    """
    system_prompt = """你是一个代码审查专家。
请对用户提交的代码进行以下分析：
1. **功能概述**：这段代码是干什么的？
2. **逐行/逐块解释**：关键逻辑说明
3. **复杂度分析**：时间复杂度和空间复杂度（大O表示法）
4. **优化建议**：至少2条具体可操作的优化方案
5. **潜在问题**：可能存在的 bug 或边界情况

按 Markdown 格式组织输出。
"""
    return call_llm(system_prompt, f"请分析以下代码：\n```\n{code}\n```")


def fix_bug(code: str, error_message: str = "") -> str:
    """
    修复代码中的 bug

    Args:
        code: 有 bug 的代码
        error_message: 错误信息（可选）

    Returns:
        修复方案 + 修正后的代码
    """
    system_prompt = """你是一个专业的代码调试专家。
请分析代码中的 bug，给出：
1. **根因分析**：问题出在哪里，为什么
2. **修复方案**：具体怎么改
3. **修正后的完整代码**
4. **预防措施**：以后如何避免这类 bug

输出时用 Markdown 格式，修正后的代码用 ``` 代码块包裹。
"""
    user_content = f"有问题代码：\n```\n{code}\n```\n"
    if error_message:
        user_content += f"错误信息：\n{error_message}\n"
    else:
        user_content += "（无错误信息，请自行分析潜在问题）\n"

    return call_llm(system_prompt, user_content)


def main():
    print("=" * 50)
    print("AI 编码助手 - CLI 版")
    print("=" * 50)
    print("选择功能：")
    print("1. 代码生成 —— 输入需求，生成代码")
    print("2. 代码分析 —— 粘贴代码，获得解析报告")
    print("3. Bug修复 —— 贴代码+报错，获得修复方案")
    print("0. 退出")
    print("=" * 50)

    while True:
        choice = input("\n请输入数字选择功能 (1/2/3/0): ").strip()

        if choice == "1":
            lang = input("目标语言 (默认 Python): ").strip() or "Python"
            req = input("请输入功能需求描述: ").strip()
            print("\n正在生成代码，请稍候...\n")
            result = generate_code(req, lang)
            print(result)

        elif choice == "2":
            print("请输入代码（输入 END 结束）:")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            print("\n正在分析代码，请稍候...\n")
            result = analyze_code(code)
            print(result)

        elif choice == "3":
            print("请输入有 bug 的代码（输入 END 结束）:")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            error = input("\n请输入错误信息（没有直接回车跳过）: ").strip()
            print("\n正在分析并修复 bug，请稍候...\n")
            result = fix_bug(code, error)
            print(result)

        elif choice == "0":
            print("再见！")
            break

        else:
            print("无效输入，请输入 1、2、3 或 0")


if __name__ == "__main__":
    main()
