# Extracted from ch06-rag.md
# Block #21

class RAGEvaluator:
    def __init__(self):
        self.retrieval_metrics = RetrievalEvaluator()
        self.generation_metrics = GenerationEvaluator()
        
    def evaluate_system(self, test_queries, ground_truth):
        results = {
            "retrieval": {},
            "generation": {},
            "end_to_end": {}
        }
        
        for query, expected in zip(test_queries, ground_truth):
            # 検索品質評価
            retrieved_docs = self.rag_system.retrieve(query)
            results["retrieval"] = self.retrieval_metrics.evaluate(
                retrieved_docs, expected.relevant_docs
            )
            
            # 生成品質評価
            generated_answer = self.rag_system.generate(query, retrieved_docs)
            results["generation"] = self.generation_metrics.evaluate(
                generated_answer, expected.answer
            )
            
            # エンドツーエンド評価
            results["end_to_end"] = self.evaluate_end_to_end(
                generated_answer, expected.answer
            )
        
        return results

class RetrievalEvaluator:
    def evaluate(self, retrieved_docs, relevant_docs):
        return {
            "precision": self.calculate_precision(retrieved_docs, relevant_docs),
            "recall": self.calculate_recall(retrieved_docs, relevant_docs),
            "f1_score": self.calculate_f1(retrieved_docs, relevant_docs),
            "mrr": self.calculate_mrr(retrieved_docs, relevant_docs)  # Mean Reciprocal Rank
        }

class GenerationEvaluator:
    def evaluate(self, generated, expected):
        return {
            "bleu_score": self.calculate_bleu(generated, expected),
            "rouge_score": self.calculate_rouge(generated, expected),
            "semantic_similarity": self.calculate_semantic_similarity(generated, expected),
            "factual_accuracy": self.check_factual_accuracy(generated, expected)
        }