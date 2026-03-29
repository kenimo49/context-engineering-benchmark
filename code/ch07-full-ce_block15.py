# Extracted from ch07-full-ce.md
# Block #15

class ContextQualityMetrics:
    def __init__(self):
        self.relevance_weight = 0.4
        self.completeness_weight = 0.3
        self.coherence_weight = 0.2
        self.freshness_weight = 0.1
        
    def calculate_context_quality(self, context, query, expected_answer=None):
        metrics = {
            "relevance": self.calculate_relevance(context, query),
            "completeness": self.calculate_completeness(context, query),
            "coherence": self.calculate_coherence(context),
            "freshness": self.calculate_freshness(context)
        }
        
        # 重み付き総合スコア
        total_score = (
            metrics["relevance"] * self.relevance_weight +
            metrics["completeness"] * self.completeness_weight +
            metrics["coherence"] * self.coherence_weight +
            metrics["freshness"] * self.freshness_weight
        )
        
        return {
            "total_score": total_score,
            "metrics": metrics,
            "recommendation": self.get_improvement_recommendation(metrics)
        }
    
    def get_improvement_recommendation(self, metrics):
        recommendations = []
        
        if metrics["relevance"] < 0.7:
            recommendations.append("改善推奨: より関連性の高い文書を選択")
        if metrics["completeness"] < 0.6:
            recommendations.append("改善推奨: 不足している情報の追加")
        if metrics["coherence"] < 0.7:
            recommendations.append("改善推奨: 階層的レイアウトの見直し")
        if metrics["freshness"] < 0.5:
            recommendations.append("改善推奨: より新しい情報源の使用")
        
        return recommendations