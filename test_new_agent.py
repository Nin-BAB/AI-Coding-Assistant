"""测试新 LangChain create_agent API"""
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from config import API_KEY, API_BASE, MODEL


@tool
def ping() -> str:
    """Return ping result."""
    return "pong"


llm = ChatOpenAI(
    model=MODEL,
    openai_api_key=API_KEY,
    openai_api_base=API_BASE,
    temperature=0,
)

graph = create_agent(
    model=llm,
    tools=[ping],
    system_prompt="You are a helpful assistant. Reply concisely.",
)
print(f"Graph type: {type(graph).__name__}")

# 测试调用
result = graph.invoke({"messages": [{"role": "user", "content": "call ping tool"}]})
print(f"Result keys: {result.keys()}")

msgs = result["messages"]
for i, m in enumerate(msgs):
    role = type(m).__name__
    content = str(m.content)[:120] if m.content else "(empty)"
    print(f"  [{i}] {role}: {content}")
    if hasattr(m, "tool_calls") and m.tool_calls:
        for tc in m.tool_calls:
            print(f"       -> tool: {tc['name']} args={tc['args']}")
