chunking_decision_tree = {
    "technical_docs": {
        "strategy": "recursive",
        "reason": "コードブロックと説明の分離が重要"
    },
    "legal_documents": {
        "strategy": "semantic", 
        "reason": "条項の意味的一貫性が重要"
    },
    "news_articles": {
        "strategy": "fixed_length",
        "reason": "均一な処理速度が重要"
    },
    "conversation_logs": {
        "strategy": "semantic",
        "reason": "話題の切れ目での分割が重要"
    }
}
