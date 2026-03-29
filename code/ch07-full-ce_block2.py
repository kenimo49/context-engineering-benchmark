class ContextCompressor:
    def __init__(self, summarization_llm):
        self.summarizer = summarization_llm
        
    def compress_context(self, retrieved_docs, target_length=2000):
        if self.estimate_total_tokens(retrieved_docs) <= target_length:
            return retrieved_docs
            
        # 長い文書を優先的に圧縮
        compressed_docs = []
        for doc in retrieved_docs:
            if len(doc.content) > 1000:
                compressed_content = self.summarizer.summarize(
                    doc.content,
                    max_length=500,
                    preserve_key_facts=True
                )
                compressed_docs.append(
                    Document(content=compressed_content, metadata=doc.metadata)
                )
            else:
                compressed_docs.append(doc)
                
        return compressed_docs
    
    def hierarchical_compression(self, documents):
        """階層的圧縮: 詳細→要点→エッセンス"""
        # Level 1: 不要な詳細の除去
        level1 = [self.remove_redundancy(doc) for doc in documents]
        
        # Level 2: 要点の抽出
        level2 = [self.extract_key_points(doc) for doc in level1]
        
        # Level 3: エッセンスの凝縮
        level3 = self.merge_related_points(level2)
        
        return level3
