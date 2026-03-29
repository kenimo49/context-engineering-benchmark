# Extracted from ch09-memory.md
# Block #3

# 設計パターン説明用の擬似コード（そのまま動作するコードではありません）

# デフォルトの予算配分
budget_ratios = {
    "recent_buffer":        0.4,  # 40% - 最新の対話（常に最重要）
    "conversation_summary":  0.3,  # 30% - 過去の要約
    "relevant_entities":     0.2,  # 20% - 関連エンティティ
    "knowledge_graph":       0.1,  # 10% - 詳細な関係性（必要時のみ）
}

# 実際の配分は「関連性スコア × 優先度」で動的に調整
# 例: エンティティの関連性が高い質問では、エンティティ枠を拡大