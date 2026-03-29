# Extracted from ch05-few-shot.md
# Block #6

# ❌ 単調なexample
examples = [
    {"input": "商品Aについて", "output": "商品Aは..."},
    {"input": "商品Bについて", "output": "商品Bは..."},
    {"input": "商品Cについて", "output": "商品Cは..."}
]

# ✅ 多様なexample  
examples = [
    {"input": "商品Aの価格は？", "output": "申し訳ございませんが、最新の価格情報については公式サイトをご確認ください。"},
    {"input": "返品方法を教えて", "output": "返品手順：1. カスタマーサービス連絡 2. 返品番号取得 3. 指定住所へ発送"},
    {"input": "新商品の発売予定は？", "output": "具体的な発売日程についてはお答えできませんが、メルマガ登録で最新情報をお受け取りいただけます。"}
]