class ContextEngine:
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.retrieval_system = RAGSystem()
        self.tool_orchestrator = ToolOrchestrator()
        
    def process_query(self, user_query, user_context):
        # 動的コンテキスト構築
        context = self.build_dynamic_context(
            user_query, 
            user_context,
            self.memory_manager.get_relevant_history(),
            self.retrieval_system.search(user_query, user_context),
            self.tool_orchestrator.get_available_tools(user_context)
        )
        
        # 構造化出力生成
        return self.generate_structured_response(context)
