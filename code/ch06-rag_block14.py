# Extracted from ch06-rag.md
# Block #14

class LinkedInKnowledgeGraphRAG:
    def __init__(self):
        self.knowledge_graph = CustomerServiceKnowledgeGraph()
        self.query_parser = QueryParser()
        
    def answer_customer_query(self, customer_query):
        # クエリの構造解析
        parsed_query = self.query_parser.parse(customer_query)
        
        # 関連するサブグラフ検索
        relevant_subgraphs = self.knowledge_graph.find_relevant_subgraphs(
            entities=parsed_query.entities,
            relations=parsed_query.relations,
            depth=2
        )
        
        # サブグラフの統合・コンテキスト化
        integrated_context = self.integrate_subgraphs(relevant_subgraphs)
        
        return self.generate_answer(customer_query, integrated_context)