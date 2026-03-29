# Extracted from appendix-b-experiment.md
# Block #12

# domain_evaluator.py
class DomainSpecificEvaluator:
    def __init__(self, domain: str):
        self.domain = domain
        self.evaluation_methods = {
            'legal': self._evaluate_legal,
            'medical': self._evaluate_medical,
            'technical': self._evaluate_technical,
            'financial': self._evaluate_financial
        }
    
    def evaluate(self, response: str, expected: Dict) -> Dict[str, float]:
        """ドメイン特化評価"""
        evaluator = self.evaluation_methods.get(
            self.domain, self._evaluate_general
        )
        return evaluator(response, expected)
    
    def _evaluate_legal(self, response: str, expected: Dict) -> Dict[str, float]:
        """法務文書用評価"""
        scores = {}
        
        # 法的精度（条文、判例の正確性）
        if 'legal_references' in expected:
            refs = expected['legal_references']
            correct_refs = sum(1 for ref in refs if ref in response)
            scores['legal_accuracy'] = correct_refs / len(refs) if refs else 0
        
        # リスク言及の適切性
        risk_keywords = ['リスク', '注意', '但し', 'ただし', '例外']
        risk_mentioned = any(kw in response for kw in risk_keywords)
        scores['risk_awareness'] = 1.0 if risk_mentioned else 0.0
        
        return scores
    
    def _evaluate_technical(self, response: str, expected: Dict) -> Dict[str, float]:
        """技術文書用評価"""
        scores = {}
        
        # コード例の正確性
        if 'code_elements' in expected:
            elements = expected['code_elements']
            present = sum(1 for elem in elements if elem in response)
            scores['code_accuracy'] = present / len(elements) if elements else 0
        
        # 技術用語の適切性
        if 'technical_terms' in expected:
            terms = expected['technical_terms']
            used_correctly = sum(1 for term in terms if term in response)
            scores['terminology'] = used_correctly / len(terms) if terms else 0
        
        return scores
    
    def _evaluate_general(self, response: str, expected: Dict) -> Dict[str, float]:
        """一般的な評価"""
        return {
            'relevance': self._calculate_relevance(response, expected),
            'completeness': self._calculate_completeness(response, expected)
        }