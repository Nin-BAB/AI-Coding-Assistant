"""
gradio_app.py - AI 编码助手 Web 界面

用 Gradio 把项目所有功能打包成好用的 Web 页面。
对比 FastAPI（后端接口）和 Gradio（前端交互），
面试可以聊：
"使用 FastAPI 做服务化封装，Gradio 做前端交互界面，
前后端分离的设计让 API 可以被其他服务调用，
同时 Gradio 提供了零代码门槛的用户交互入口。"
"""
import gradio as gr
import os
import sys

# 确保项目目录在 sys.path 中，这样从任何位置运行都能找到模块
_project_dir = os.path.dirname(os.path.abspath(__file__))
if _project_dir not in sys.path:
    sys.path.insert(0, _project_dir)

# 导入项目功能模块
from ai_coding_assistant import generate_code, analyze_code, fix_bug
from agent_coding import chat_with_agent
from git_workflow import generate_commit_message, review_code


# ============================================================
# Tab 1：Agent 对话 — 最核心的功能
# ============================================================
def agent_chat_fn(message, history):
    """
    Gradio ChatInterface 的回调函数。
    history 是 [(user_msg, ai_msg), ...] 格式的对话历史，
    但我们调 Agent 时只传当前消息，让 Agent 自己决定要不要调工具。

    小笨解释：
    Gradio 的 ChatInterface 会自动维护对话历史显示，
    但我们传参只传最新一条，因为 Agent 有自己的记忆机制
    （当然，这里的 agent 是无状态的，每次都是独立调用）
    """
    response = chat_with_agent(message)
    return response


def build_agent_tab():
    """构建 Agent 对话页面"""
    # ChatInterface = Gradio 提供的开箱即用聊天组件
    # 自动处理输入框 + 对话气泡 + 发送按钮
    # fn 是你要绑定的处理函数
    # type="messages" 是 Gradio 5+ 的新格式
    chatbot = gr.ChatInterface(
        fn=agent_chat_fn,
        title="小笨 AI 编码助手",
        description="和你对话的 AI 编码助手，能帮你写代码、调试、分析文件...",
        examples=[
            "帮我写一个 Python 快速排序算法",
            "现在是几点？",
            "分析一下当前项目里 agent_coding.py 这个文件",
            "写个猜数字游戏",
        ],
    )
    return chatbot


# ============================================================
# Tab 2：代码生成
# ============================================================
def code_generate_fn(requirement, language):
    """调用代码生成功能"""
    if not requirement.strip():
        return "请输入需求描述"
    result = generate_code(requirement, language)
    return result


def build_code_gen_tab():
    """构建代码生成页面"""
    with gr.Column():
        gr.Markdown("## 📝 代码生成")
        gr.Markdown("输入需求描述，AI 自动生成可运行的代码")

        with gr.Row():
            # 需求输入框
            req_input = gr.Textbox(
                label="需求描述",
                placeholder="例如：写一个函数，输入两个列表，返回它们的交集",
                lines=4,
            )
            with gr.Column(scale=1):
                # 语言选择下拉框
                lang_dropdown = gr.Dropdown(
                    choices=["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
                    value="Python",
                    label="编程语言",
                )
                generate_btn = gr.Button("🚀 生成代码", variant="primary")

        # 输出区域
        output = gr.Code(
            label="生成的代码",
            language="python",
            lines=20,
        )

        # 绑定按钮点击事件
        # fn=code_generate_fn — 点击后调哪个函数
        # inputs=[...] — 函数的输入参数
        # outputs=output — 结果显示在哪里
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
    result = analyze_code(code_text)
    return result


def build_analyze_tab():
    """构建代码分析页面"""
    with gr.Column():
        gr.Markdown("## 🔍 代码分析")
        gr.Markdown("粘贴代码，AI 会分析功能逻辑、复杂度、优化建议")

        code_input = gr.Code(
            label="待分析代码",
            language="python",
            lines=12,
        )
        analyze_btn = gr.Button("🔍 开始分析", variant="primary")

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
    result = fix_bug(code_text, error_msg)
    return result


def build_fix_tab():
    """构建 Bug 修复页面"""
    with gr.Column():
        gr.Markdown("## 🐛 Bug 修复")
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
        fix_btn = gr.Button("🔧 开始修复", variant="primary")

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
    """生成 Commit Message"""
    result = generate_commit_message()
    return result


def code_review_fn(filepath):
    """审查代码文件"""
    if not filepath.strip():
        return "请输入文件路径"
    # 支持相对路径和绝对路径
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.getcwd(), filepath)
    result = review_code(filepath)
    return result


def build_git_tab():
    """构建 Git 工作流页面"""
    with gr.Column():
        gr.Markdown("## 🔧 Git 工作流 AI 工具")
        gr.Markdown("自动生成 Commit Message 和 AI 代码审查")

        with gr.Tab("生成 Commit Message"):
            gr.Markdown("点击按钮，自动分析当前 Git 变更，生成规范的提交信息")
            commit_btn = gr.Button("📋 分析 Git 变更并生成", variant="primary")
            commit_output = gr.Markdown(label="Commit Message")

            commit_btn.click(
                fn=commit_msg_fn,
                inputs=[],
                outputs=commit_output,
            )

        with gr.Tab("AI 代码审查"):
            gr.Markdown("输入文件路径，AI 审查代码质量和潜在问题")
            file_input = gr.Textbox(
                label="文件路径",
                placeholder="例如：agent_coding.py  或  D:/Projects/code.py",
            )
            review_btn = gr.Button("🔍 开始审查", variant="primary")
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
    """构建项目介绍页面"""
    with gr.Column():
        gr.Markdown("""
        # 🐣 AI 编码助手

        ## 项目概述

        基于 **Python + LangChain + DeepSeek API** 构建的 AI 辅助编码工具，
        覆盖研发全流程：代码生成、代码分析、Bug 修复、Git 工作流、Agent 对话。

        ## 技术栈

        | 模块 | 技术 |
        |------|------|
        | AI 模型 | DeepSeek API |
        | Agent 框架 | LangChain (create_agent + @tool) |
        | 服务化 | FastAPI |
        | 前端界面 | Gradio |
        | 版本控制 | Git |

        ## 功能清单

        - 🤖 **Agent 对话** — 思考→调工具→回答的智能助手
        - 📝 **代码生成** — 输入需求，AI 写代码
        - 🔍 **代码分析** — 逐行解释 + 复杂度分析 + 优化建议
        - 🐛 **Bug 修复** — 粘贴问题代码，AI 给修复方案
        - 🔧 **Git 工作流** — 自动生成 Commit Message + 代码审查
        - 🚀 **REST API** — FastAPI 封装，方便集成到其他工具

        ## 项目结构

        ```
        AI-Coding-Assistant/
        ├── ai_coding_assistant.py   # 核心功能（代码生成/分析/修复）
        ├── agent_coding.py          # LangChain Agent 版编程助手
        ├── git_workflow.py          # Git 工作流 AI 工具
        ├── app.py                   # FastAPI 服务入口
        ├── gradio_app.py            # Gradio 界面（当前文件）
        ├── config.py                # 配置加载
        └── .env                     # API Key 配置
        ```
        """)

    return None


# ============================================================
# 主界面组装
# ============================================================
def create_app():
    """
    用 Gradio Blocks 构建多 Tab 界面。

    Blocks 是 Gradio 的高级 API，可以自定义布局和交互。
    对比：
    - gr.Interface → 简单的一输入一输出场景
    - gr.Blocks  → 复杂的多 Tab、多组件交互布局
    - gr.ChatInterface → 专门给聊天场景用的
    """

    # 设置页面标题和主题
    # theme="soft" 是 Gradio 内置主题之一
    # title 显示在浏览器标签页上
    with gr.Blocks(
        title="小笨 AI 编码助手",
    ) as demo:
        # 页面标题
        gr.Markdown(
            "# 小笨 AI 编码助手\n"
            "面向研发流程的 AI 辅助编码工具 -- 代码生成 / 分析 / 修复 / Agent 对话"
        )

        # --- Tab 页导航 ---
        # gr.Tab 创建标签页，label 是显示在导航上的名字
        with gr.Tab("🤖 Agent 对话"):
            build_agent_tab()

        with gr.Tab("📝 代码生成"):
            build_code_gen_tab()

        with gr.Tab("🔍 代码分析"):
            build_analyze_tab()

        with gr.Tab("🐛 Bug 修复"):
            build_fix_tab()

        with gr.Tab("🔧 Git 工作流"):
            build_git_tab()

        with gr.Tab("ℹ️ 关于项目"):
            build_about_tab()

        # 页脚
        gr.Markdown(
            "---\n"
            "🐣 小笨 AI 编码助手 | Powered by DeepSeek + LangChain + Gradio"
        )

    return demo


# ============================================================
# 启动入口
# ============================================================
if __name__ == "__main__":
    # Windows 终端用 GBK 编码，先设置 UTF-8 避免 emoji 报错
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    print("=" * 55)
    print("小笨 AI 编码助手 -- Gradio 界面")
    print("=" * 55)
    print("启动中...")
    print(f"打开浏览器访问: http://localhost:7860")
    print("按 Ctrl+C 停止服务")
    print("=" * 55)

    app = create_app()

    # share=True -> 生成一个临时公网链接（通过 Gradio 的代理）
    # 可以分享给别人访问，但链接 72 小时过期
    # server_port 可以自定义端口
    app.launch(
        share=False,        # 只在本地运行
        server_name="0.0.0.0",   # 局域网内可访问
        server_port=7860,         # Gradio 默认端口
        show_error=True,          # 显示错误详情，调试用
        theme=gr.themes.Soft(),   # Gradio 6.x theme 参数在 launch() 里设置
    )
