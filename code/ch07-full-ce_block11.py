class TokenCostOptimizer:
    def __init__(self, cost_per_token=0.00002):  # GPT-4価格例
        self.cost_per_token = cost_per_token
        self.quality_threshold = 0.85
        
    def optimize_context_for_cost(self, context_elements, budget_limit=1000):
        # 各要素の品質貢献度計算
        element_values = []
        for element in context_elements:
            quality_contribution = self.estimate_quality_contribution(element)
            token_cost = self.estimate_token_count(element) * self.cost_per_token
            value_ratio = quality_contribution / token_cost
            
            element_values.append((element, value_ratio, token_cost))
        
        # 価値比率順でソート
        sorted_elements = sorted(element_values, key=lambda x: x[1], reverse=True)
        
        # 予算内での最適選択
        selected_elements = []
        total_cost = 0
        
        for element, value_ratio, cost in sorted_elements:
            if total_cost + cost <= budget_limit:
                selected_elements.append(element)
                total_cost += cost
            
            # 品質閾値チェック
            current_quality = self.estimate_combined_quality(selected_elements)
            if current_quality >= self.quality_threshold:
                break
        
        return selected_elements, total_cost
