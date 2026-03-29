# Extracted from ch05-few-shot.md
# Block #10

# ❌ バイアスのあるexample
examples = [
    {"user": "田中", "response": "丁寧語で対応"},
    {"user": "Smith", "response": "簡潔に対応"},
    {"user": "佐藤", "response": "丁寧語で対応"}
]

# ✅ 公平なexample
examples = [
    {"inquiry_type": "技術相談", "response": "専門的説明"},
    {"inquiry_type": "一般質問", "response": "分かりやすい説明"},  
    {"inquiry_type": "緊急対応", "response": "迅速な案内"}
]