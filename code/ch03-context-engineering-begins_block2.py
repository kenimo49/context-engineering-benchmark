# Extracted from ch03-context-engineering-begins.md
# Block #2

prompt = f"""
あなたは{role}です。以下のルールに従ってください：
{rules}

質問：{user_question}
"""

response = llm.generate(prompt)