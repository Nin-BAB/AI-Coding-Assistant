"""
gradio_app.py — AI 编码助手 Web 界面

用 Gradio 将项目功能打包为交互式 Web 界面。
"""
import gradio as gr
import os
import sys

_project_dir = os.path.dirname(os.path.abspath(__file__))
if _project_dir not in sys.path:
    sys.path.insert(0, _project_dir)

from ai_coding_assistant import generate_code, analyze_code, fix_bug
from agent_coding import chat_with_agent
from git_workflow import generate_commit_message, review_code


# ============================================================
# Tab 1：Agent 对话
# ============================================================
def agent_chat_fn(message, history):
    response = chat_with_agent(message)
    return response


def build_agent_tab():
    chatbot = gr.ChatInterface(
        fn=agent_chat_fn,
        title="AI 编码助手",
        description="AI 编码助手，支持代码编写、调试、文件分析等功能",
        examples=[
            "帮我写一个 Python 快速排序算法",
            "现在是几点？",
            "分析一下 agent_coding.py 这个文件",
            "写个猜数字游戏",
        ],
    )
    return chatbot


# ============================================================
# Tab 2：代码生成
# ============================================================
def code_generate_fn(requirement, language):
    if not requirement.strip():
        return "请输入需求描述"
    return generate_code(requirement, language)


def build_code_gen_tab():
    with gr.Column():
        gr.Markdown("## 代码生成")
        gr.Markdown("输入需求描述，AI 自动生成可运行的代码")

        with gr.Row():
            req_input = gr.Textbox(
                label="需求描述",
                placeholder="例如：写一个函数，输入两个列表，返回它们的交集",
                lines=4,
            )
            with gr.Column(scale=1):
                lang_dropdown = gr.Dropdown(
                    choices=["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
                    value="Python",
                    label="编程语言",
                )
                generate_btn = gr.Button("生成代码", variant="primary")

        output = gr.Code(
            label="生成的代码",
            language="python",
            lines=20,
        )

        generate_btn.click(
            fn=code_generate_fn,
            inputs=[req_input, lang_dropdown],
            outputs=output,
        )
    return req_input, lang_dropdown, generate_btn, output


# ============================================================
# Tab 3：代码分析
# ============================================================
def code_analyze_fn(code_text):
    if not code_text.strip():
        return "请粘贴要分析的代码"
    return analyze_code(code_text)


def build_analyze_tab():
    with gr.Column():
        gr.Markdown("## 代码分析")
        gr.Markdown("粘贴代码，AI 分析功能逻辑、复杂度及优化建议")

        code_input = gr.Code(
            label="待分析代码",
            language="python",
            lines=12,
        )
        analyze_btn = gr.Button("开始分析", variant="primary")
        output = gr.Markdown(label="分析报告")

        analyze_btn.click(
            fn=code_analyze_fn,
            inputs=code_input,
            outputs=output,
        )
    return code_input, analyze_btn, output


# ============================================================
# Tab 4：Bug 修复
# ============================================================
def bug_fix_fn(code_text, error_msg):
    if not code_text.strip():
        return "请粘贴有 bug 的代码"
    return fix_bug(code_text, error_msg)


def build_fix_tab():
    with gr.Column():
        gr.Markdown("## Bug 修复")
        gr.Markdown("粘贴有问题的代码（可附带错误信息），AI 分析并给出修复方案")

        code_input = gr.Code(
            label="有 bug 的代码",
            language="python",
            lines=10,
        )
        error_input = gr.Textbox(
            label="错误信息（可选）",
            placeholder="粘贴报错信息，没有则留空",
            lines=3,
        )
        fix_btn = gr.Button("开始修复", variant="primary")
        output = gr.Markdown(label="修复方案")

        fix_btn.click(
            fn=bug_fix_fn,
            inputs=[code_input, error_input],
            outputs=output,
        )
    return code_input, error_input, fix_btn, output


# ============================================================
# Tab 5：Git 工作流
# ============================================================
def commit_msg_fn():
    return generate_commit_message()


def code_review_fn(filepath):
    if not filepath.strip():
        return "请输入文件路径"
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.getcwd(), filepath)
    return review_code(filepath)


def build_git_tab():
    with gr.Column():
        gr.Markdown("## Git 工作流 AI 工具")
        gr.Markdown("自动生成 Commit Message 和 AI 代码审查")

        with gr.Tab("生成 Commit Message"):
            gr.Markdown("自动分析当前 Git 变更，生成规范的提交信息")
            commit_btn = gr.Button("分析 Git 变更并生成", variant="primary")
            commit_output = gr.Markdown(label="Commit Message")

            commit_btn.click(
                fn=commit_msg_fn,
                inputs=[],
                outputs=commit_output,
            )

        with gr.Tab("AI 代码审查"):
            gr.Markdown("输入文件路径，AI 审查代码质量")
            file_input = gr.Textbox(
                label="文件路径",
                placeholder="例如：agent_coding.py",
            )
            review_btn = gr.Button("开始审查", variant="primary")
            review_output = gr.Markdown(label="审查报告")

            review_btn.click(
                fn=code_review_fn,
                inputs=file_input,
                outputs=review_output,
            )
    return commit_btn, file_input, review_btn


# ============================================================
# Tab 6：关于项目
# ============================================================
def build_about_tab():
    with gr.Column():
        gr.Markdown("""
        # AI 编码助手

        ## 项目概述

        基于 **Python + LangChain + DeepSeek API** 的 AI 辅助编码工具，
        覆盖代码生成、代码分析、Bug 修复、Git 工作流、Agent 对话。

        ## 技术栈

        | 模块 | 技术 |
        |------|------|
        | AI 模型 | DeepSeek API |
        | Agent 框架 | LangChain (create_agent + @tool) |
        | 服务化 | FastAPI |
        | 前端界面 | Gradio |
        | 版本控制 | Git |

        ## 功能清单

        - **Agent 对话** — 思考→调工具→回答的智能助手
        - **代码生成** — 输入需求，AI 写代码
        - **代码分析** — 逐行解释 + 复杂度分析 + 优化建议
        - **Bug 修复** — 粘贴问题代码，AI 给修复方案
        - **Git 工作流** — 自动生成 Commit Message + 代码审查
        - **REST API** — FastAPI 封装，方便集成到其他工具

        ## 项目结构

        ```
        AI-Coding-Assistant/
        ├── ai_coding_assistant.py   # 核心功能（代码生成/分析/修复）
        ├── agent_coding.py          # LangChain Agent
        ├── agent_demo.py            # 手动 ReAct Agent 演示
        ├── git_workflow.py          # Git 工作流 AI 工具
        ├── app.py                   # FastAPI 服务入口
        ├── gradio_app.py            # Gradio 界面
        ├── config.py                # 配置加载
        └── .env                     # API Key 配置
        ```
        """)

    return None


# ============================================================
# 主界面
# ============================================================
def create_app():
    with gr.Blocks(
        title="AI 编码助手",
    ) as demo:
        gr.Markdown(
            "# AI 编码助手\n"
            "面向研发流程的 AI 辅助编码工具 -- 代码生成 / 分析 / 修复 / Agent 对话"
        )

        with gr.Tab("Agent 对话"):
            build_agent_tab()

        with gr.Tab("代码生成"):
            build_code_gen_tab()

        with gr.Tab("代码分析"):
            build_analyze_tab()

        with gr.Tab("Bug 修复"):
            build_fix_tab()

        with gr.Tab("Git 工作流"):
            build_git_tab()

        with gr.Tab("关于项目"):
            build_about_tab()

        gr.Markdown(
            "---\n"
            "AI 编码助手 | Powered by DeepSeek + LangChain + Gradio"
        )

    return demo


# ============================================================
# 启动入口
# ============================================================
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    print("=" * 55)
    print("AI 编码助手 -- Gradio 界面")
    print("=" * 55)
    print("启动中...")
    print(f"打开浏览器访问: http://localhost:7860")
    print("按 Ctrl+C 停止服务")
    print("=" * 55)

    app = create_app()

    app.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        theme=gr.themes.Soft(),
    )
