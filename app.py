"""
app.py — FastAPI 服务入口

将所有功能封装为 REST API 接口。
"""
import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


# ============================================================
# 创建 FastAPI 应用
# ============================================================
app = FastAPI(
    title="AI 编码助手 API",
    description="面向研发流程的 AI 辅助编码工具后端服务",
    version="2.0.0",
)


# ============================================================
# 日志配置
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api_server.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("ai_coding_api")


# ============================================================
# 请求/响应数据模型
# ============================================================

class CodeGenerateRequest(BaseModel):
    """代码生成请求"""
    requirement: str
    language: str = "Python"


class CodeAnalyzeRequest(BaseModel):
    """代码分析请求"""
    code: str


class BugFixRequest(BaseModel):
    """Bug 修复请求"""
    code: str
    error_message: str = ""


class ChatRequest(BaseModel):
    """Agent 对话请求"""
    query: str


class ReviewRequest(BaseModel):
    """代码审查请求"""
    filepath: str


class ApiResponse(BaseModel):
    """统一响应格式"""
    success: bool
    data: str = ""
    message: str = ""


# ============================================================
# 路由注册
# ============================================================

# -----------------------------------------------------------
# 根路径 — 健康检查
# -----------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "AI 编码助手 API",
        "version": "2.0.0",
        "status": "running",
    }


# -----------------------------------------------------------
# 代码生成
# -----------------------------------------------------------
@app.post("/generate", response_model=ApiResponse)
def generate_code(request: CodeGenerateRequest):
    try:
        from ai_coding_assistant import generate_code as _generate
        logger.info(f"代码生成请求: lang={request.language}, req={request.requirement[:50]}...")
        result = _generate(request.requirement, request.language)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"代码生成失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 代码分析
# -----------------------------------------------------------
@app.post("/analyze", response_model=ApiResponse)
def analyze_code(request: CodeAnalyzeRequest):
    try:
        from ai_coding_assistant import analyze_code as _analyze
        logger.info(f"代码分析请求: code_len={len(request.code)}")
        result = _analyze(request.code)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"代码分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# Bug 修复
# -----------------------------------------------------------
@app.post("/fix", response_model=ApiResponse)
def fix_bug(request: BugFixRequest):
    try:
        from ai_coding_assistant import fix_bug as _fix
        logger.info(f"Bug 修复请求: code_len={len(request.code)}, has_error={bool(request.error_message)}")
        result = _fix(request.code, request.error_message)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Bug 修复失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# Agent 对话
# -----------------------------------------------------------
@app.post("/agent/chat", response_model=ApiResponse)
def agent_chat(request: ChatRequest):
    try:
        from agent_coding import chat_with_agent
        logger.info(f"Agent 对话请求: query={request.query[:50]}...")
        result = chat_with_agent(request.query)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Agent 执行失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 生成 Commit Message
# -----------------------------------------------------------
@app.get("/git/commit-message", response_model=ApiResponse)
def generate_commit_message():
    try:
        from git_workflow import generate_commit_message as _gen_commit
        logger.info("生成 Commit Message 请求")
        result = _gen_commit()
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"生成 Commit Message 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------
# 代码审查
# -----------------------------------------------------------
@app.post("/git/review", response_model=ApiResponse)
def review_code(request: ReviewRequest):
    try:
        from git_workflow import review_code as _review
        logger.info(f"代码审查请求: filepath={request.filepath}")
        result = _review(request.filepath)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"代码审查失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 启动入口
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("AI 编码助手 API 服务启动中...")
    print(f"文档地址: http://localhost:8000/docs")
    print(f"接口地址: http://localhost:8000/")
    print("=" * 55)
    uvicorn.run(app, host="0.0.0.0", port=8000)
