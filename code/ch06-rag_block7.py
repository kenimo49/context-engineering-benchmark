# Extracted from ch06-rag.md
# Block #7

def semantic_chunking(text, embedding_model):
    sentences = split_into_sentences(text)
    embeddings = [embedding_model.encode(s) for s in sentences]
    
    chunks = []
    current_chunk = []
    
    for i, sentence in enumerate(sentences):
        if should_start_new_chunk(embeddings[i-1], embeddings[i]):
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
        else:
            current_chunk.append(sentence)
    
    return chunks

# 利点: 意味的一貫性、自然な境界
# 欠点: 処理コスト高、サイズ不均一