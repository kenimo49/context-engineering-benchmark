# Extracted from appendix-b-experiment.md
# Block #7

class EvaluationMetrics:
    @staticmethod
    def semantic_similarity(response: str, expected: str) -> float:
        """セマンティック類似度"""
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        response_emb = model.encode(response)
        expected_emb = model.encode(expected)
        
        # コサイン類似度
        similarity = np.dot(response_emb, expected_emb) / (
            np.linalg.norm(response_emb) * np.linalg.norm(expected_emb)
        )
        return float(similarity)
    
    @staticmethod
    def fact_accuracy(response: str, facts: List[str]) -> float:
        """事実精度（簡易版）"""
        correct_facts = 0
        for fact in facts:
            if fact.lower() in response.lower():
                correct_facts += 1
        return correct_facts / len(facts) if facts else 0.0
    
    @staticmethod
    def response_completeness(response: str, required_elements: List[str]) -> float:
        """回答完全性"""
        present_elements = 0
        for element in required_elements:
            if element.lower() in response.lower():
                present_elements += 1
        return present_elements / len(required_elements) if required_elements else 0.0