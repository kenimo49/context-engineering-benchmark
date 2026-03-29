# Extracted from ch06-rag.md
# Block #19

import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelEmbeddingProcessor:
    def __init__(self, embedding_model, batch_size=32):
        self.embedding_model = embedding_model
        self.batch_size = batch_size
        
    async def process_documents(self, documents):
        # 文書をチャンクに分割
        chunks = []
        for doc in documents:
            doc_chunks = self.chunk_document(doc)
            chunks.extend(doc_chunks)
        
        # バッチ処理で埋め込み生成
        embeddings = await self.embed_chunks_parallel(chunks)
        
        return list(zip(chunks, embeddings))
    
    async def embed_chunks_parallel(self, chunks):
        batches = [chunks[i:i + self.batch_size] 
                  for i in range(0, len(chunks), self.batch_size)]
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            tasks = [
                asyncio.get_event_loop().run_in_executor(
                    executor, 
                    self.embedding_model.encode, 
                    batch
                ) for batch in batches
            ]
            
            results = await asyncio.gather(*tasks)
        
        # バッチ結果の統合
        return [embedding for batch in results for embedding in batch]