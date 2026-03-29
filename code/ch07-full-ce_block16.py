# Extracted from ch07-full-ce.md
# Block #16

class ContextEngineeringOrchestrator:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.compression_service = CompressionService()
        self.layout_service = LayoutService()
        self.memory_service = MemoryService()
        
    async def orchestrate_context_engineering(self, query, user_context):
        # 並列実行可能なサービス
        retrieval_task = asyncio.create_task(
            self.retrieval_service.selective_retrieve(query)
        )
        memory_task = asyncio.create_task(
            self.memory_service.get_relevant_memory(query, user_context)
        )
        
        # 並列実行完了待ち
        retrieved_docs, relevant_memory = await asyncio.gather(
            retrieval_task, memory_task
        )
        
        # 順次実行が必要なサービス
        compressed_context = await self.compression_service.compress(
            retrieved_docs
        )
        
        structured_context = await self.layout_service.create_hierarchical_layout(
            compressed_context, relevant_memory
        )
        
        return structured_context