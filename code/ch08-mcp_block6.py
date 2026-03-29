# Extracted from ch08-mcp.md
# Block #6

class DynamicToolSelector:
    def __init__(self, available_tools):
        self.available_tools = available_tools
        self.usage_analyzer = ToolUsageAnalyzer()
        
    def select_relevant_tools(self, user_query, context_budget=5000):
        """クエリに基づく関連ツールの動的選択"""
        # Step 1: クエリ分析
        query_intent = self.analyze_query_intent(user_query)
        
        # Step 2: 各ツールの関連性スコアリング  
        tool_scores = []
        for tool in self.available_tools:
            relevance_score = self.calculate_tool_relevance(
                tool, query_intent
            )
            tool_scores.append((tool, relevance_score))
        
        # Step 3: トークン予算内での最適選択
        sorted_tools = sorted(tool_scores, key=lambda x: x[1], reverse=True)
        selected_tools = self.optimize_for_token_budget(
            sorted_tools, context_budget
        )
        
        return selected_tools
    
    def calculate_tool_relevance(self, tool, query_intent):
        """ツールとクエリ意図の関連性スコア"""
        # セマンティック類似度
        semantic_score = self.calculate_semantic_similarity(
            tool.description, query_intent.description
        )
        
        # 過去の使用パターン
        usage_score = self.usage_analyzer.get_usage_probability(
            tool.name, query_intent.category
        )
        
        # カテゴリマッチング
        category_score = self.calculate_category_match(
            tool.context_hints.get('categories', []),
            query_intent.categories
        )
        
        # 重み付き合計
        total_score = (
            semantic_score * 0.5 +
            usage_score * 0.3 +
            category_score * 0.2
        )
        
        return total_score