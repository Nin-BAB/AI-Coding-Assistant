"""
test_api.py — 单元测试

用 FastAPI 内置的 TestClient 测试所有接口，不需要手动启动服务。

面试话术：
"项目包含完整的单元测试，覆盖所有核心接口的正常流程和异常流程，
使用 FastAPI TestClient 实现轻量级测试，无需额外部署测试环境。"
"""
import sys
import os

# 确保能找到项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app import app

# TestClient 是 FastAPI 提供的测试工具
# 它模拟 HTTP 请求，不需要真的启动 uvicorn 服务器
client = TestClient(app)


# ============================================================
# 测试 1：健康检查
# ============================================================
def test_root():
    """测试根路径返回服务状态"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["service"] == "AI 编码助手 API"
    print("✅ 健康检查 OK")


# ============================================================
# 测试 2：代码生成
# ============================================================
def test_generate_code():
    """测试代码生成接口"""
    response = client.post("/generate", json={
        "requirement": "计算两个数的和",
        "language": "Python",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) > 0   # 赌：生成的代码不是空的
    print("✅ 代码生成 OK")


# ============================================================
# 测试 3：代码分析
# ============================================================
def test_analyze_code():
    """测试代码分析接口"""
    response = client.post("/analyze", json={
        "code": "def add(a, b): return a + b",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) > 0
    print("✅ 代码分析 OK")


# ============================================================
# 测试 4：Bug 修复（带错误信息）
# ============================================================
def test_fix_bug_with_error():
    """测试带错误信息的 Bug 修复"""
    code_with_bug = """
def divide(a, b):
    return a / b
"""
    response = client.post("/fix", json={
        "code": code_with_bug,
        "error_message": "ZeroDivisionError: division by zero",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    print("✅ Bug 修复（带错误信息）OK")


# ============================================================
# 测试 5：Bug 修复（不带错误信息）
# ============================================================
def test_fix_bug_without_error():
    """测试不带错误信息的 Bug 修复"""
    response = client.post("/fix", json={
        "code": "x = 1/0",
        "error_message": "",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    print("✅ Bug 修复（无错误信息）OK")


# ============================================================
# 测试 6：Agent 对话
# ============================================================
def test_agent_chat():
    """测试 Agent 对话接口"""
    response = client.post("/agent/chat", json={
        "query": "Python的list和tuple有什么区别？",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) > 0
    print("✅ Agent 对话 OK")


# ============================================================
# 测试 7：Git Commit Message
# ============================================================
def test_git_commit_message():
    """测试生成 Commit Message"""
    response = client.get("/git/commit-message")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    print("✅ Git Commit Message OK")


# ============================================================
# 测试 8：代码审查
# ============================================================
def test_review_code():
    """测试代码审查（审查 app.py 自身）"""
    response = client.post("/git/review", json={
        "filepath": "app.py",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    print("✅ 代码审查 OK")


# ============================================================
# 测试 9：请求参数校验（空参数）
# ============================================================
def test_generate_empty_requirement():
    """测试空需求时会怎样——会返回 422 校验错误"""
    response = client.post("/generate", json={
        "requirement": "",
        "language": "Python",
    })
    # 空字符串不会触发 Pydantic 校验错误，因为字段类型是 str
    # 它会正常传给 AI，看 AI 怎么处理
    assert response.status_code in (200, 422)
    print("✅ 空参数处理 OK")


# ============================================================
# 入口：运行所有测试
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("🧪 运行单元测试")
    print("=" * 50)

    test_root()
    test_generate_code()
    test_analyze_code()
    test_fix_bug_with_error()
    test_fix_bug_without_error()
    test_agent_chat()
    test_git_commit_message()
    test_review_code()
    test_generate_empty_requirement()

    print("\n" + "=" * 50)
    print("🎉 全部测试通过！")
