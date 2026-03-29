# Extracted from ch08-mcp.md
# Block #14

class MCPServerQualityEvaluator:
    def __init__(self):
        self.metrics = {
            "context_relevance": ContextRelevanceMetric(),
            "response_latency": ResponseLatencyMetric(),
            "resource_efficiency": ResourceEfficiencyMetric(),
            "error_handling": ErrorHandlingMetric()
        }
    
    def evaluate_server(self, server, test_scenarios):
        results = {}
        
        for scenario in test_scenarios:
            scenario_results = {}
            
            for metric_name, metric in self.metrics.items():
                score = metric.evaluate(server, scenario)
                scenario_results[metric_name] = score
            
            results[scenario.name] = scenario_results
        
        return self.generate_quality_report(results)
    
    def generate_quality_report(self, results):
        report = {
            "overall_score": self.calculate_overall_score(results),
            "strengths": self.identify_strengths(results),
            "improvement_areas": self.identify_improvement_areas(results),
            "recommendations": self.generate_recommendations(results)
        }
        
        return report