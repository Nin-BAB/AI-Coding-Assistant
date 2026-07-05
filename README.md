# 🤖 AI 编码助手

面向研发流程的 AI 辅助编码工具，覆盖代码生成、代码分析、Bug 修复三大核心能力，帮助提升研发交付效率。

## 功能

| 功能 | 说明 |
|------|------|
| **代码生成** | 输入业务需求 + 目标语言，自动生成完整可运行代码 |
| **代码分析** | 粘贴代码，获得逐行解释 + 时空复杂度分析 + 优化建议 |
| **Bug 修复** | 输入有问题的代码 + 错误信息，自动定位根因并给出修复方案 |

## 技术栈

- Python 3.12
- LangChain / OpenAI SDK
- DeepSeek API
- FastAPI
- Git

## 快速开始

```bash
# 1. 安装依赖
pip install openai langchain langchain-community fastapi uvicorn python-dotenv

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的 DeepSeek API Key

# 3. 运行
python ai_coding_assistant.py
```

## 项目结构

```
├── ai_coding_assistant.py   # 主程序：三个核心功能模块
├── config.py                # 配置文件：读取 API Key 和环境变量
├── .env                     # 环境变量（已加入 .gitignore，不提交）
└── .gitignore               # Git 忽略规则
```

## 安全说明

- API Key 存储在 `.env` 文件中，已加入 `.gitignore`
- 严禁将 API Key 提交到公开仓库
