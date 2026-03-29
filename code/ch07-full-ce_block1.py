class SelectiveRetriever:
    def __init__(self, vector_db, relevance_threshold=0.7):
        self.vector_db = vector_db
        self.relevance_threshold = relevance_threshold
        
    def selective_retrieve(self, query, context_budget=8000):
        # 初期候補の取得
        candidates = self.vector_db.similarity_search_with_score(
            query, k=20
        )
        
        # 関連性フィルタリング
        relevant_candidates = [
            (doc, score) for doc, score in candidates 
            if score > self.relevance_threshold
        ]
        
        # トークン予算内での最適選択
        selected_docs = self.optimize_for_token_budget(
            relevant_candidates, context_budget
        )
        
        return selected_docs
    
    def optimize_for_token_budget(self, candidates, budget):
        selected = []
        total_tokens = 0
        
        # 関連性スコア順で選択
        for doc, score in sorted(candidates, key=lambda x: x[1], reverse=True):
            doc_tokens = self.estimate_tokens(doc.content)
            
            if total_tokens + doc_tokens <= budget:
                selected.append(doc)
                total_tokens += doc_tokens
            else:
                break
                
        return selected
