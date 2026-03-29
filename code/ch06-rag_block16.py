# Extracted from ch06-rag.md
# Block #16

# ❌ 問題のあるRAG実装
def naive_rag(query, vector_db):
    # 大量の文書を無差別取得
    docs = vector_db.similarity_search(query, k=20)
    
    # 全てをコンテキストに詰め込み
    context = "\n".join([doc.content for doc in docs])
    
    return llm.generate(f"Question: {query}\n\nContext: {context}")

# ✅ 改善されたRAG実装  
def optimized_rag(query, vector_db):
    # 関連性スコアでフィルタリング
    docs = vector_db.similarity_search_with_score(query, k=10)
    relevant_docs = [doc for doc, score in docs if score > 0.7]
    
    # トークン制限内で最適化
    context = self.optimize_context_for_tokens(relevant_docs, max_tokens=8000)
    
    return llm.generate(f"Question: {query}\n\nContext: {context}")