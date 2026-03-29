# Extracted from ch06-rag.md
# Block #6

def fixed_length_chunking(text, chunk_size=1000, overlap=200):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

# 利点: シンプル、一定サイズ
# 欠点: 文脈無視、文章途中で切断