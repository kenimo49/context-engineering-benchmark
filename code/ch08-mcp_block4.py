# Extracted from ch08-mcp.md
# Block #4

class CodeRepositoryMCPServer:
    """コードリポジトリ専用MCPサーバー"""
    
    def __init__(self, repository_path):
        self.repo_path = repository_path
        self.code_analyzer = CodeStructureAnalyzer()
        self.git_analyzer = GitHistoryAnalyzer()
        
    async def handle_resource_request(self, resource_uri):
        if resource_uri.startswith("code://"):
            return await self.get_code_context(resource_uri)
        elif resource_uri.startswith("git://"):
            return await self.get_git_context(resource_uri)
        else:
            raise ValueError(f"Unsupported resource URI: {resource_uri}")
    
    async def get_code_context(self, resource_uri):
        # パスの解析
        file_path = resource_uri.replace("code://", "")
        full_path = os.path.join(self.repo_path, file_path)
        
        if os.path.isfile(full_path):
            return await self.get_file_context(full_path)
        elif os.path.isdir(full_path):
            return await self.get_directory_context(full_path)
        else:
            raise FileNotFoundError(f"Path not found: {file_path}")
    
    async def get_file_context(self, file_path):
        """ファイルのContext Engineering最適化"""
        # ファイル分析
        analysis = self.code_analyzer.analyze_file(file_path)
        
        context = {
            "file_path": file_path,
            "language": analysis.language,
            "summary": analysis.summary,
            "key_functions": analysis.key_functions[:5],  # 重要な関数のみ
            "dependencies": analysis.dependencies,
            "recent_changes": await self.git_analyzer.get_recent_changes(
                file_path, days=7
            )
        }
        
        # Context用に最適化されたファイル内容
        if analysis.estimated_tokens > 2000:
            context["content"] = self.summarize_code_file(file_path)
        else:
            context["content"] = self.read_file_with_line_numbers(file_path)
        
        return context