"""
app.py — FastAPI 服务入口

把所有功能封装成 HTTP 接口，模拟后端服务。

面试话术：
"使用 FastAPI 对 AI 编码助手进行了服务化封装，
将 Agent 能力、代码分析、Git 工作流等模块统一暴露为 REST API，
采用模块化路由设计，方便后续微服务拆分。"
"""
import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# ============================================================
# 1. 创建 FastAPI 应用
# ============================================================
# FastAPI() → 创建 Web 应用实例
# 后面所有路由、中间件都注册在这个 app 上
app = FastAPI(
    title="AI 编码助手 API",
    description="面向研发流程的 AI 辅助编码工具后端服务",
    version="2.0.0",
)


# ============================================================
# 2. 配置日志系统
# ============================================================
# 日志级别：DEBUG < INFO < WARNING < ERROR
# 生产环境一般用 INFO，开发调式用 DEBUG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),                          # 输出到控制台
        logging.FileHandler("api_server.log", encoding="utf-8"),  # 写入文件
    ],
)
logger = logging.getLogger("ai_coding_api")


# ============================================================
# 3. 定义请求/响应数据模型（Pydantic）
# ============================================================
# Pydantic 是做数据校验的——前端传过来的数据对不对，它自动检查
# 继承 BaseModel 就是定义"这个接口要收什么数据"

class CodeGenerateRequest(BaseModel):
    """代码生成请求模型"""
    requirement: str          # 业务需求
    language: str = "Python"  # 目标语言，默认 Python


class CodeAnalyzeRequest(BaseModel):
    """代码分析请求模型"""
    code: str                 # 待分析代码


class BugFixRequest(BaseModel):
    """Bug 修复请求模型"""
    code: str                 # 有 bug 的代码
    error_message: str = ""   # 错误信息，可选


class ChatRequest(BaseModel):
    """Agent 对话请求模型"""
    query: str                # 用户输入


class ReviewRequest(BaseModel):
    """代码审查请求模型"""
    filepath: str             # 文件路径


class ApiResponse(BaseModel):
    """统一响应格式"""
    success: bool
    data: str = ""
    message: str = ""


# ============================================================
# 4. 注册路由（API 接口）
# ============================================================
# 先把第一天的功能也接进来，面试展示完整度

# -----------------------------------------------------------
# 4.1 根路径 — 服务健康检查
# -----------------------------------------------------------
@app.get("/")
def root():
    """服务状态检测，面试常问：你服务怎么保证可用的？"""
    return {
        "service": "AI 编码助手 API",
        "version": "2.0.0",
        "status": "running",
    }


# -----------------------------------------------------------
# 4.2 代码生成
# -----------------------------------------------------------
@app.post("/generate", response_model=ApiResponse)
def generate_code(request: CodeGenerateRequest):
    """
    代码生成接口。
    输入：需求描述 + 编程语言
    输出：生成的代码
    """
    try:
        from ai_coding_assistant import generate_code as _generate
        logger.info(f"代码生成请求: lang={request.language}, req={request.requirement[:50]}...")
        result = _generate(request.requirement, request.language)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"代码生成失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 4.3 代码分析
# -----------------------------------------------------------
@app.post("/analyze", response_model=ApiResponse)
def analyze_code(request: CodeAnalyzeRequest):
    """
    代码分析接口。
    输入：代码
    输出：逐行解释 + 复杂度分析 + 优化建议
    """
    try:
        from ai_coding_assistant import analyze_code as _analyze
        logger.info(f"代码分析请求: code_len={len(request.code)}")
        result = _analyze(request.code)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"代码分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 4.4 Bug 修复
# -----------------------------------------------------------
@app.post("/fix", response_model=ApiResponse)
def fix_bug(request: BugFixRequest):
    """
    Bug 修复接口。
    输入：有 bug 的代码 + 错误信息（可选）
    输出：根因分析 + 修复方案 + 修正后代码
    """
    try:
        from ai_coding_assistant import fix_bug as _fix
        logger.info(f"Bug 修复请求: code_len={len(request.code)}, has_error={bool(request.error_message)}")
        result = _fix(request.code, request.error_message)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Bug 修复失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 4.5 Agent 对话
# -----------------------------------------------------------
@app.post("/agent/chat", response_model=ApiResponse)
def agent_chat(request: ChatRequest):
    """
    Agent 对话接口。
    输入：用户问题
    输出：Agent 回答（会自动调用工具）
    """
    try:
        from agent_coding import chat_with_agent
        logger.info(f"Agent 对话请求: query={request.query[:50]}...")
        result = chat_with_agent(request.query)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Agent 执行失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 4.6 生成 Commit Message
# -----------------------------------------------------------
@app.get("/git/commit-message", response_model=ApiResponse)
def generate_commit_message():
    """
    自动生成 Git Commit Message。
    分析当前 Git 变更 → AI 生成规范提交信息
    """
    try:
        from git_workflow import generate_commit_message as _gen_commit
        logger.info("生成 Commit Message 请求")
        result = _gen_commit()
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"生成 Commit Message 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 4.7 代码审查
# -----------------------------------------------------------
@app.post("/git/review", response_model=ApiResponse)
def review_code(request: ReviewRequest):
    """
    AI 代码审查接口。
    输入：文件路径
    输出：代码规范、潜在问题、优化建议
    """
    try:
        from git_workflow import review_code as _review
        logger.info(f"代码审查请求: filepath={request.filepath}")
        result = _review(request.filepath)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"代码审查失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 5. 启动入口
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("🚀 AI 编码助手 API 服务启动中...")
    print(f"文档地址: http://localhost:8000/docs")
    print(f"接口地址: http://localhost:8000/")
    print("=" * 55)
    # host="0.0.0.0" 表示监听所有网络接口
    # 这样同一局域网内的设备也能访问
    uvicorn.run(app, host="0.0.0.0", port=8000)
