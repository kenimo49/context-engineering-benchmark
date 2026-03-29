# Extracted from ch11a-agentic-rag-concept.md
# Block #1

# 従来のRAG（静的検索）
class TraditionalRAG:
    def __init__(self):
        self.vector_db = VectorDatabase()  # 事前インデックス必須
        self.embedder = EmbeddingModel()
        
    def query(self, user_question: str):
        # 1. 質問をベクトル化
        query_vector = self.embedder.embed(user_question)
        
        # 2. 類似検索（固定戦略）
        similar_docs = self.vector_db.similarity_search(query_vector, k=5)
        
        # 3. LLM生成
        return self.llm.generate(user_question, similar_docs)

# Agentic RAG（動的検索戦略）
class AgenticRAG:
    def __init__(self):
        self.search_tools = [
            SemanticSearch(),
            KeywordSearch(), 
            GraphSearch(),
            TimeSeriesSearch(),
            WebSearch()
        ]
        self.planning_agent = PlanningAgent()
        
    def query(self, user_question: str):
        # 1. エージェントが検索戦略を立案
        search_plan = self.planning_agent.create_plan(user_question)
        
        # 2. 複数検索手法を組み合わせ実行
        all_results = []
        for step in search_plan.steps:
            tool = self.get_tool(step.tool_name)
            results = tool.search(step.query, step.parameters)
            all_results.extend(results)
            
            # 3. 中間結果を基に戦略調整
            if step.needs_refinement(results):
                refined_plan = self.planning_agent.refine_plan(
                    original_plan=search_plan,
                    current_results=results
                )
                search_plan.update(refined_plan)
        
        # 4. 統合回答生成
        return self.synthesize_response(user_question, all_results)