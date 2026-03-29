class AdvancedMemoryManager:
    def __init__(self):
        self.short_term_memory = ConversationBuffer(max_size=10)
        self.long_term_memory = PersistentMemoryStore()
        self.memory_scorer = MemoryRelevanceScorer()
        
    def manage_context_memory(self, current_query, max_memory_tokens=4000):
        # 短期記憶からの関連情報
        recent_relevant = self.select_relevant_short_term_memory(
            current_query, 
            self.short_term_memory.get_recent(5)
        )
        
        # 長期記憶からの関連情報
        long_term_relevant = self.select_relevant_long_term_memory(
            current_query,
            lookback_days=30
        )
        
        # メモリ統合・最適化
        optimized_memory = self.optimize_memory_context(
            recent_relevant, 
            long_term_relevant, 
            max_memory_tokens
        )
        
        return optimized_memory
    
    def select_relevant_long_term_memory(self, query, lookback_days=30):
        # 時間減衰を考慮したスコアリング
        memories = self.long_term_memory.search(
            query=query,
            time_range=f"last_{lookback_days}_days"
        )
        
        scored_memories = []
        for memory in memories:
            relevance_score = self.memory_scorer.calculate_relevance(query, memory)
            freshness_score = self.memory_scorer.calculate_freshness(memory.timestamp)
            importance_score = self.memory_scorer.calculate_importance(memory)
            
            combined_score = (
                relevance_score * 0.5 + 
                freshness_score * 0.3 + 
                importance_score * 0.2
            )
            
            scored_memories.append((memory, combined_score))
        
        # スコア順ソート
        return sorted(scored_memories, key=lambda x: x[1], reverse=True)[:5]
