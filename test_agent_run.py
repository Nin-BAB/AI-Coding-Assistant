from agent_coding import chat_with_agent

# 测试 1: 简单问题
print("=== 测试 1: 普通知识问答 ===")
r = chat_with_agent("Python的list和tuple有什么区别？")
print(r[:200])

# 测试 2: 代码执行
print("\n=== 测试 2: 执行代码 ===")
r = chat_with_agent("请帮我计算 1+2+...+100 的和，并用Python验证")
print(r[:300])
