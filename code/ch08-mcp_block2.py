# Extracted from ch08-mcp.md
# Block #2

class MCPContextOrchestrator:
    """Host: コンテキストオーケストレーター"""
    
    def __init__(self):
        self.clients = {}  # 各MCPサーバーへのクライアント接続
        self.context_manager = ContextManager()
        self.security_manager = SecurityManager()
    
    def orchestrate_context(self, user_query):
        # Step 1: クエリ分析 - 必要なコンテキスト源の特定
        required_contexts = self.analyze_context_requirements(user_query)
        
        # Step 2: 並列コンテキスト取得
        context_tasks = []
        for context_type in required_contexts:
            if context_type == "files":
                context_tasks.append(self.get_file_context(user_query))
            elif context_type == "database":  
                context_tasks.append(self.get_database_context(user_query))
            elif context_type == "apis":
                context_tasks.append(self.get_api_context(user_query))
        
        # Step 3: コンテキスト統合・最適化
        gathered_contexts = await asyncio.gather(*context_tasks)
        integrated_context = self.context_manager.integrate_contexts(
            gathered_contexts
        )
        
        return integrated_context
    
    async def get_file_context(self, query):
        """ファイルシステムMCPサーバーからのコンテキスト取得"""
        file_client = self.clients["file_system"]
        
        # 関連ファイル検索
        relevant_files = await file_client.search_resources(
            query=query,
            resource_type="file"
        )
        
        # ファイル内容の取得・要約
        file_contents = []
        for file_resource in relevant_files:
            content = await file_client.read_resource(file_resource.uri)
            summarized = self.context_manager.summarize_for_context(
                content, max_tokens=1000
            )
            file_contents.append({
                "source": file_resource.name,
                "content": summarized,
                "type": "file_context"
            })
        
        return file_contents