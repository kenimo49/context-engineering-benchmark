# Extracted from ch11b-agentic-rag-impl.md
# Block #8

class SearchSystemEvolution:
    def stage_1_simple(self):
        return "grep/glob + LLM統合"
        
    def stage_2_hybrid(self):
        return "Agentic Search + 必要時RAG補完"
        
    def stage_3_full_rag(self):
        return "複雑性が正当化される場合のみRAG導入"
        
    def decision_criteria(self):
        return {
            "データ量": "10万ファイル超でRAG検討",
            "検索複雑性": "意味検索が頻繁に必要",
            "運用体制": "インデックス管理の人的リソース確保",
            "セキュリティ": "外部保存許可の組織ポリシー"
        }