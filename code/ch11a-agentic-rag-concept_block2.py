class SingleAgentRAG:
    def __init__(self):
        self.agent = AutonomousAgent(
            tools=[
                VectorSearch(),
                KeywordSearch(), 
                WebSearch(),
                DocumentParser()
            ],
            llm=ClaudeHaiku(),  # コスト効率重視
            max_iterations=5
        )
        
    def process_query(self, query: str, context: dict = None):
        """単一エージェントによる自律検索"""
        
        # Step 1: 初期分析
        analysis = self.agent.analyze_query(query, context)
        
        # Step 2: 検索戦略立案
        search_strategy = self.agent.plan_search(analysis)
        
        # Step 3: 反復検索・改良
        results = []
        for iteration in range(self.agent.max_iterations):
            # 検索実行
            current_results = self.agent.execute_search(search_strategy)
            results.extend(current_results)
            
            # 結果評価
            evaluation = self.agent.evaluate_results(current_results, query)
            
            # 十分な情報が得られた場合は終了
            if evaluation.sufficient:
                break
                
            # 戦略修正
            search_strategy = self.agent.refine_strategy(
                current_strategy=search_strategy,
                results=current_results,
                evaluation=evaluation
            )
        
        # Step 4: 統合回答生成
        return self.agent.synthesize_response(query, results)

# 実装例：技術ドキュメント検索システム
class TechnicalDocRAG(SingleAgentRAG):
    def __init__(self):
        super().__init__()
        self.agent.add_tools([
            GitHubCodeSearch(),
            StackOverflowSearch(),
            OfficialDocsSearch(),
            TutorialSearch()
        ])
        
    def search_implementation_guide(self, tech_query: str):
        """技術実装ガイド検索"""
        context = {
            "domain": "software_engineering",
            "priority": ["official_docs", "github_examples", "tutorials"],
            "recency": "prefer_recent"
        }
        
        return self.process_query(tech_query, context)
