class DynamicContextSelector:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.conversation_tracker = ConversationTracker()
        
    def select_dynamic_context(self, current_query, conversation_history):
        # 会話の進行状況分析
        conversation_state = self.conversation_tracker.analyze_state(
            conversation_history
        )
        
        # 段階に応じたコンテキスト選択
        if conversation_state.stage == "problem_identification":
            return self.select_diagnostic_context(current_query)
        elif conversation_state.stage == "solution_exploration":
            return self.select_solution_context(current_query, conversation_state)
        elif conversation_state.stage == "implementation":
            return self.select_implementation_context(current_query)
        else:
            return self.select_general_context(current_query)
    
    def select_solution_context(self, query, state):
        # 既に特定された問題に基づく解決策検索
        problem_context = state.identified_problems
        
        solution_docs = self.vector_db.search(
            query=f"{query} {problem_context}",
            filter_metadata={"type": "solution", "problem_category": state.category}
        )
        
        # 過去の成功事例も追加
        success_cases = self.memory_manager.get_successful_cases(
            problem_type=state.category
        )
        
        return self.merge_contexts(solution_docs, success_cases)
