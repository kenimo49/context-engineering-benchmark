# RAG: コード外部保存のリスク
class RAGSecurity:
    def store_code(self):
        risks = [
            "ベクターDB内にコード内容保存",
            "第三者ツール（ChromaDB等）への依存",
            "インデックスファイルの機密性管理",
            "エンベディングサービスへのコード送信"
        ]
        return risks

# Agentic Search: ローカル完結
class AgenticSearchSecurity:
    def search_code(self):
        return "ファイルシステム直接アクセス（外部保存なし）"
