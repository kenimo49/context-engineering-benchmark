class DatabaseMCPClient:
    """データベースコンテキスト専用クライアント"""
    
    def __init__(self, connection_string):
        self.connection = DatabaseConnection(connection_string)
        self.schema_analyzer = SchemaAnalyzer()
        
    async def get_contextual_data(self, query, context_scope):
        # Step 1: クエリからデータベース検索意図を抽出
        search_intent = self.extract_search_intent(query)
        
        # Step 2: 関連テーブル・カラム特定
        relevant_schema = self.schema_analyzer.find_relevant_schema(
            search_intent
        )
        
        # Step 3: Context Engineering最適化クエリ生成
        optimized_query = self.generate_context_optimized_query(
            search_intent,
            relevant_schema,
            max_rows=100  # コンテキスト制限
        )
        
        # Step 4: データ取得・構造化
        raw_results = await self.connection.execute(optimized_query)
        structured_context = self.format_for_context(raw_results)
        
        return structured_context
    
    def format_for_context(self, raw_results):
        """データベース結果をLLMコンテキスト用に最適化"""
        if len(raw_results) == 0:
            return "No relevant data found in database."
        
        # サンプリング + 要約戦略
        if len(raw_results) > 20:
            sample_results = random.sample(raw_results, 10)
            summary = f"Found {len(raw_results)} records. Sample of 10 shown below:"
        else:
            sample_results = raw_results
            summary = f"Found {len(raw_results)} records:"
        
        formatted = f"Database Results: {summary}\n"
        for i, record in enumerate(sample_results, 1):
            formatted += f"{i}. {self.format_record_summary(record)}\n"
        
        return formatted
