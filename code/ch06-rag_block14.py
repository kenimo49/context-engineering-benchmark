def conflict_aware_rag(query, retrieved_docs):
    # 文書の新しさでスコアリング
    scored_docs = []
    for doc in retrieved_docs:
        freshness_score = calculate_freshness_score(doc.metadata['date'])
        relevance_score = doc.similarity_score
        combined_score = relevance_score * 0.7 + freshness_score * 0.3
        scored_docs.append((doc, combined_score))
    
    # スコア順にソート
    sorted_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)
    
    # 矛盾検出と解決
    resolved_context = resolve_contradictions([doc for doc, _ in sorted_docs[:5]])
    
    return generate_response_with_confidence(query, resolved_context)
