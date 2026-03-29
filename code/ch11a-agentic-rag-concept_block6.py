from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.agent import OpenAIAgent
from llama_index.core.agent import AgentRunner

class LlamaIndexAgenticRAG:
    def __init__(self):
        # 複数データソースのインデックス構築
        self.indexes = {
            "documentation": self._build_documentation_index(),
            "code_examples": self._build_code_index(), 
            "community": self._build_community_index(),
            "official": self._build_official_index()
        }
        
        # 各インデックスをツール化
        self.tools = self._create_query_tools()
        
        # エージェント初期化
        self.agent = self._setup_agent()
        
    def _build_documentation_index(self):
        """技術ドキュメントインデックス"""
        from llama_index.core import SimpleDirectoryReader
        
        docs = SimpleDirectoryReader("./docs").load_data()
        return VectorStoreIndex.from_documents(docs)
        
    def _build_code_index(self):
        """コード例インデックス"""
        from llama_index.readers.github import GithubRepositoryReader
        
        # GitHub リポジトリから直接読み込み
        reader = GithubRepositoryReader(
            owner="anthropics",
            repo="claude-code-examples"
        )
        docs = reader.load_data()
        return VectorStoreIndex.from_documents(docs)
        
    def _build_community_index(self):
        """コミュニティQ&Aインデックス"""
        # Stack Overflow, Reddit, Discord等からデータ収集
        # （実装は省略）
        pass
        
    def _create_query_tools(self):
        """各インデックスをツール化"""
        tools = []
        
        for name, index in self.indexes.items():
            query_engine = index.as_query_engine(
                similarity_top_k=5,
                response_mode="compact"
            )
            
            tool = QueryEngineTool.from_defaults(
                query_engine=query_engine,
                name=f"{name}_search",
                description=f"Search {name} for relevant information"
            )
            tools.append(tool)
            
        return tools
        
    def _setup_agent(self):
        """エージェント設定"""
        return OpenAIAgent.from_tools(
            tools=self.tools,
            verbose=True,
            system_prompt="""
            あなたはClaude Code専門のエージェントです。
            ユーザーの質問に対して、複数の情報源を活用して
            包括的で実践的な回答を提供してください。
            
            検索戦略：
            1. まず公式ドキュメントを確認
            2. 具体的実装例が必要な場合はコード例を検索
            3. 複雑な問題の場合はコミュニティの知見を参照
            4. 最新情報が必要な場合は複数ソースをクロスチェック
            """
        )
    
    def query(self, question: str):
        """Agentic RAGクエリ実行"""
        response = self.agent.chat(question)
        return response

# 実装例：Claude Code専門検索システム
class ClaudeCodeAgenticRAG(LlamaIndexAgenticRAG):
    def __init__(self):
        super().__init__()
        
        # Claude Code特化ツール追加
        self.agent.add_tools([
            self._create_config_tool(),
            self._create_workflow_tool(),
            self._create_troubleshooting_tool()
        ])
    
    def _create_config_tool(self):
        """設定関連専門ツール"""
        from llama_index.core.tools import FunctionTool
        
        def search_config_patterns(query: str):
            """Claude Code設定パターン検索"""
            # CLAUDE.md、設定ファイルパターンから検索
            pass
            
        return FunctionTool.from_defaults(
            fn=search_config_patterns,
            name="config_search",
            description="Search for Claude Code configuration patterns"
        )
    
    def search_implementation_help(self, coding_question: str):
        """実装支援検索"""
        structured_query = f"""
        技術的実装質問: {coding_question}
        
        以下の観点で検索・回答してください：
        1. 公式推奨方法
        2. 実装例・コードサンプル
        3. よくある問題・解決方法
        4. パフォーマンス・セキュリティ考慮事項
        """
        
        return self.query(structured_query)
