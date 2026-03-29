# Claude Code内部で試されたRAGアプローチ
class TraditionalRAGApproach:
    def __init__(self):
        self.voyage_embeddings = VoyageEmbeddings()
        self.vector_db = ChromaDB()
        self.semantic_search = SemanticSearchEngine()
        
    def setup_codebase_index(self, codebase_path: str):
        """コードベース事前インデックス"""
        # 全ファイルをベクトル化
        for file_path in glob.glob(f"{codebase_path}/**/*", recursive=True):
            content = read_file(file_path)
            embedding = self.voyage_embeddings.embed(content)
            self.vector_db.store(file_path, embedding, content)
            
    def search_codebase(self, query: str):
        """意味検索によるコード検索"""
        query_embedding = self.voyage_embeddings.embed(query)
        similar_files = self.vector_db.similarity_search(
            query_embedding, 
            top_k=10
        )
        return similar_files

# 採用されたAgentic Search（grep/glob）アプローチ  
class AgenticSearchApproach:
    def __init__(self):
        self.llm = ClaudeModel()
        self.file_system = FileSystemInterface()
        
    def search_codebase(self, query: str, project_context: str):
        """エージェント主導検索"""
        
        # LLMが検索戦略を立案
        search_plan = self.llm.plan_search_strategy(
            query=query,
            context=project_context,
            available_tools=["grep", "find", "ls", "cat"]
        )
        
        results = []
        for step in search_plan.steps:
            if step.tool == "grep":
                # パターン検索
                matches = self.file_system.grep(
                    pattern=step.pattern,
                    directories=step.directories,
                    file_types=step.file_types
                )
                results.extend(matches)
                
            elif step.tool == "find":
                # ファイル名検索  
                files = self.file_system.find(
                    pattern=step.filename_pattern,
                    path=step.search_path
                )
                results.extend(files)
                
            elif step.tool == "cat":
                # 特定ファイル内容取得
                content = self.file_system.read_file(step.file_path)
                results.append({"file": step.file_path, "content": content})
        
        # 結果をLLMで統合・解析
        synthesized = self.llm.synthesize_search_results(
            query=query,
            raw_results=results
        )
        
        return synthesized
