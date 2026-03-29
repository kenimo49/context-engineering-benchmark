# Extracted from ch07-full-ce.md
# Block #19

# DoorDashパターン: 段階的品質チェック
class DoorDashStyleContextOrchestrator:
    def orchestrate_context(self, user_query, conversation_history):
        # Stage 1: 会話要約
        conversation_summary = self.summarize_conversation(conversation_history)
        
        # Stage 2: 関連記事・事例検索  
        relevant_content = self.multi_source_retrieval(
            query=user_query,
            context=conversation_summary
        )
        
        # Stage 3: LLMガードレール品質チェック
        quality_check = self.quality_validator.validate(relevant_content)
        
        if quality_check.passed:
            return self.generate_response(user_query, relevant_content)
        else:
            return self.fallback_response()

# LinkedInパターン: 知識グラフ統合
class LinkedInStyleKnowledgeGraphCE:
    def integrate_structured_knowledge(self, query):
        # 知識グラフからのサブグラフ抽出
        relevant_subgraphs = self.knowledge_graph.extract_subgraphs(query)
        
        # テキスト文書との統合
        text_documents = self.vector_db.similarity_search(query)
        
        # 構造化知識 + 非構造化知識の統合
        integrated_context = self.merge_structured_unstructured(
            relevant_subgraphs, text_documents
        )
        
        return integrated_context