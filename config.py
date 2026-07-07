"""配置文件 — 读取 .env 中的 API 配置"""
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

if not API_KEY or API_KEY == "sk-你的key粘贴在这里":
    raise ValueError(
        "\n还没配置 API Key！\n"
        "请打开项目下的 .env 文件，把 DEEPSEEK_API_KEY 替换成你的真实 Key\n"
        "例如：DEEPSEEK_API_KEY=sk-abc123def456\n"
    )
