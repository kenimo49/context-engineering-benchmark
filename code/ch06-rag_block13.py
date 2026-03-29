def hallucination_resistant_rag(query, retrieved_docs):
    # 情報源の明示
    context_with_sources = []
    for i, doc in enumerate(retrieved_docs):
        context_with_sources.append(f"Source {i+1} ({doc.source}): {doc.content}")
    
    prompt = f"""
    Based ONLY on the following sources, answer the question.
    If the answer is not in the sources, say "I don't have enough information."

    Sources:
    {chr(10).join(context_with_sources)}

    Question: {query}
    Answer:
    """
    
    return llm.generate(prompt)
