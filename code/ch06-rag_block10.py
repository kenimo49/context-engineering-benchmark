# Extracted from ch06-rag.md
# Block #10

class HybridRetriever:
    def __init__(self, vector_db, keyword_index):
        self.vector_db = vector_db
        self.keyword_index = keyword_index
        
    def retrieve(self, query, top_k=5):
        # ベクトル検索
        vector_results = self.vector_db.similarity_search(query, k=top_k)
        
        # キーワード検索  
        keyword_results = self.keyword_index.search(query, k=top_k)
        
        # 結果の融合（RRF: Reciprocal Rank Fusion）
        return self.merge_results(vector_results, keyword_results)
    
    def merge_results(self, vector_results, keyword_results):
        score_dict = {}
        
        # ベクトル検索スコア
        for rank, doc in enumerate(vector_results):
            score_dict[doc.id] = score_dict.get(doc.id, 0) + 1 / (rank + 1)
        
        # キーワード検索スコア
        for rank, doc in enumerate(keyword_results):  
            score_dict[doc.id] = score_dict.get(doc.id, 0) + 1 / (rank + 1)
        
        # スコア順ソート
        return sorted(score_dict.items(), key=lambda x: x[1], reverse=True)