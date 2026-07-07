# AI 编码助手

面向研发流程的 AI 辅助编码工具，覆盖代码生成、代码分析、Bug 修复、Agent 对话、Git 工作流全流程，提供 CLI / REST API / Web UI 三种使用方式。

## 功能一览

| 功能 | 说明 | 访问方式 |
|------|------|---------|
| **代码生成** | 输入业务需求 + 目标语言，AI 自动生成完整可运行代码 | CLI / API / UI |
| **代码分析** | 粘贴代码，获得逐行解释 + 时空复杂度 + 优化建议 | CLI / API / UI |
| **Bug 修复** | 输入问题代码 + 错误信息，定位根因并给出修复方案 | CLI / API / UI |
| **Agent 对话** | LangChain Agent 驱动的智能对话，自动调用工具（执行代码、读文件、查时间）| CLI / API / UI |
| **Git Commit 生成** | 读取 git diff，AI 自动生成规范的 Conventional Commit 信息 | CLI / API / UI |
| **AI 代码审查** | 审查指定代码文件，从规范/性能/安全多维度给建议 | CLI / API / UI |

## 技术栈

| 模块 | 技术 |
|------|------|
| AI 模型 | DeepSeek API（Chat 模型） |
| Agent 框架 | LangChain（create_agent + @tool 装饰器） |
| REST API | FastAPI + Pydantic + Uvicorn |
| Web 界面 | Gradio（多 Tab 交互式 UI） |
| 版本控制 | Git + 自动 Commit Message 生成 |
| 运行环境 | Python 3.12 + Windows |

## 项目演进路线

```
Day 1  CLI 版基础功能（代码生成/分析/修复）+ 手动 ReAct Agent 演示
Day 2  LangChain Agent 升级 + Git 工作流联动 + FastAPI 服务化封装
Day 3  Gradio Web 界面 + 项目完善 + 面试准备
```

## 快速开始

```bash
# 1. 安装依赖
pip install openai langchain langchain-community langchain-openai fastapi uvicorn python-dotenv gradio

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，将 DEEPSEEK_API_KEY 替换为你的真实 Key

# 3. 启动方式（任选其一）
python ai_coding_assistant.py   # CLI 交互模式
uvicorn app:app                 # FastAPI 服务（http://localhost:8000/docs）
python gradio_app.py            # Web 界面（http://localhost:7860）
```

## 项目结构

```
D:\Projects\AI-Coding-Assistant\
├── ai_coding_assistant.py   # Day 1: 核心功能模块（生成/分析/修复）
├── agent_demo.py            # Day 1: 手动 ReAct 循环 Agent 演示
├── agent_coding.py          # Day 2: LangChain Agent（@tool + create_agent）
├── git_workflow.py          # Day 2: Git Commit 生成 + 代码审查
├── app.py                   # Day 2: FastAPI 服务化封装
├── gradio_app.py            # Day 3: Gradio Web 界面
├── config.py                # 配置加载（.env -> 环境变量）
├── test_api.py              # API 接口测试脚本
├── test_agent_run.py        # Agent 功能测试
├── .env                     # API Key 配置（不提交）
├── .env.example             # 环境变量模板
├── .gitignore               # Git 忽略规则
└── README.md                # 项目说明文档
```

## 面试亮点

> 构建了一个面向研发流程的 AI 辅助编码工具，采用三层架构设计：
> - **CLI 层** — 快速验证 AI 能力，支持代码生成/分析/Bug 修复
> - **服务层** — FastAPI 封装为 REST API，支持跨服务调用
> - **展示层** — Gradio 搭建 Web 界面，降低使用门槛
>
> 核心创新点在于用 LangChain 的 create_agent + @tool 构建了可自主调用工具的编码 Agent，
> 同时打通 Git 工作流（自动生成 Commit Message + AI 代码审查），实现了 AI 工具与研发流程的衔接。

## 安全说明

- API Key 存储在 `.env` 文件中，已加入 `.gitignore`
- 严禁将 API Key 提交到公开仓库

## License

MIT
