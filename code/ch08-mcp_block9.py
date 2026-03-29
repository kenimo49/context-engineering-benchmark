# Extracted from ch08-mcp.md
# Block #9

class EnterpriseContextAggregatorMCP:
    """エンタープライズ環境の統合コンテキストサーバー"""
    
    def __init__(self):
        self.connectors = {
            "jira": JiraConnector(),
            "confluence": ConfluenceConnector(),
            "github": GitHubConnector(),
            "slack": SlackConnector()
        }
        
    def register_tools(self):
        return [
            Tool(
                name="get_project_context",
                description="Gather comprehensive project context from multiple sources (Jira, GitHub, Confluence)",
                input_schema={
                    "type": "object", 
                    "properties": {
                        "project_key": {"type": "string"},
                        "include_sources": {
                            "type": "array",
                            "items": {"enum": ["jira", "github", "confluence", "slack"]},
                            "default": ["jira", "github"]
                        }
                    }
                }
            )
        ]
    
    async def get_project_context(self, project_key, include_sources):
        """マルチドメイン プロジェクトコンテキスト統合"""
        context_parts = {}
        
        # 並列でコンテキスト取得
        tasks = []
        for source in include_sources:
            if source in self.connectors:
                tasks.append(
                    self.get_source_context(source, project_key)
                )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 結果統合
        for source, result in zip(include_sources, results):
            if isinstance(result, Exception):
                context_parts[source] = {"error": str(result)}
            else:
                context_parts[source] = result
        
        # 統合コンテキストの構造化
        integrated_context = self.integrate_multi_source_context(
            project_key, context_parts
        )
        
        return integrated_context
    
    def integrate_multi_source_context(self, project_key, context_parts):
        """マルチソースコンテキストの知的統合"""
        integrated = {
            "project": project_key,
            "summary": self.generate_project_summary(context_parts),
            "current_status": self.extract_current_status(context_parts),
            "key_contributors": self.identify_key_contributors(context_parts),
            "recent_activity": self.aggregate_recent_activity(context_parts),
            "blockers_and_issues": self.identify_blockers(context_parts)
        }
        
        return integrated