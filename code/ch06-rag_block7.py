class CrossEncoderReranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query, candidates, top_k=3):
        # Query-Document ペアのスコア計算
        pairs = [(query, doc.content) for doc in candidates]
        scores = self.model.predict(pairs)
        
        # スコア順でソート
        ranked_docs = sorted(
            zip(candidates, scores), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [doc for doc, score in ranked_docs[:top_k]]
