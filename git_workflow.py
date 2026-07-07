"""
git_workflow.py — Git 工作流 AI 辅助工具

功能：
1. 自动生成 Git Commit Message（读 git diff → AI 写提交说明）
2. AI 代码审查（读代码文件 → AI 给优化建议）
"""
import subprocess
from openai import OpenAI
from config import API_KEY, API_BASE, MODEL

client = OpenAI(api_key=API_KEY, base_url=API_BASE)


# ============================================================
# 功能 1：生成 Commit Message
# ============================================================
def get_git_diff() -> str:
    """获取当前 Git 仓库的变更内容。"""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout

        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout

        return "（没有检测到变更）"
    except Exception as e:
        return f"获取 Git 变更失败: {e}"


def generate_commit_message() -> str:
    """读取代码变更 → AI 生成规范的 Commit Message"""
    diff_content = get_git_diff()

    system_prompt = """你是一个 Git 提交信息生成器。
根据代码 diff，生成规范的 Commit Message。

格式要求（Conventional Commits）：
第一行：type(scope): 简短描述（50字以内）
空一行
正文：详细说明变更内容和原因

type 类型：
feat - 新功能
fix - Bug修复
docs - 文档
style - 格式
refactor - 重构
test - 测试
chore - 杂项/配置

要求：
1. 用中文写描述
2. 第一行不超过 50 字
3. 不要废话，直接输出 Commit Message
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请根据以下 diff 生成提交信息：\n\n{diff_content}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


# ============================================================
# 功能 2：AI 代码审查
# ============================================================
def review_code(filepath: str) -> str:
    """审查指定代码文件，给出优化建议。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return f"文件读取失败: {e}"

    system_prompt = """你是一个代码审查专家。
请从以下维度审查代码，给出具体可操作的建议：

1. **代码规范**：命名是否合理、格式是否规范
2. **潜在风险**：可能的 bug 或边界情况
3. **性能优化**：可以改进的性能瓶颈
4. **可读性**：注释是否足够、逻辑是否清晰

输出用 Markdown 格式，每一条建议都要有"问题行"和"修改建议"。
如果代码没问题，说清楚即可。
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请审查以下代码：\n\n```python\n{code}\n```"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


# ============================================================
# 交互入口
# ============================================================
def main():
    print("=" * 55)
    print("Git 工作流 AI 工具")
    print("=" * 55)
    print("1. 生成 Commit Message")
    print("2. AI 代码审查")
    print("0. 返回")
    print("=" * 55)

    while True:
        choice = input("\n请输入 (1/2/0): ").strip()

        if choice == "1":
            print("\n正在分析 Git 变更...\n")
            msg = generate_commit_message()
            print(f"\n{'-' * 40}")
            print(msg)
            print(f"{'-' * 40}")

        elif choice == "2":
            path = input("请输入要审查的文件路径: ").strip()
            print(f"\n正在审查 {path}...\n")
            result = review_code(path)
            print(result)

        elif choice == "0":
            print("再见！")
            break

        else:
            print("无效输入，请输入 1、2 或 0")


if __name__ == "__main__":
    main()
