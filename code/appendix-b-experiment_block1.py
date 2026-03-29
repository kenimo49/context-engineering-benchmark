import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# 簡単な接続テスト
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,
    messages=[{
        "role": "user", 
        "content": "Hello! Please respond briefly."
    }]
)
print(message.content[0].text)
