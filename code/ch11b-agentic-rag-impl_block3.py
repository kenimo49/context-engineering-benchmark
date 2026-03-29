# RAG: 意味類似度による検索（しばしば的外れ）
query = "認証エラーの修正方法"
rag_results = [
    "user_authentication.py",      # 適切
    "error_handling.py",           # 適切
    "email_validation.py",         # 関連性低い（意味的類似による誤抽出）
    "password_hashing.py"          # 関連性低い
]

# Agentic Search: モデルが文脈理解して検索
query = "認証エラーの修正方法" 
agentic_plan = {
    "step1": "grep -r 'AuthenticationError' src/",
    "step2": "grep -r 'authentication.*error' src/",  
    "step3": "find src/ -name '*auth*' -name '*.py'",
    "step4": "grep -A 5 -B 5 'def handle_auth_error' src/"
}
# → より的確な結果
