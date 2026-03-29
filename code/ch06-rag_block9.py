class DoorDashRAGSystem:
    def __init__(self):
        self.knowledge_base = self.load_support_articles()
        self.conversation_summarizer = ConversationSummarizer()
        self.vector_db = VectorDatabase()
        
    def answer_dasher_question(self, conversation_history, current_question):
        # Step 1: 会話要約
        context_summary = self.conversation_summarizer.summarize(
            conversation_history
        )
        
        # Step 2: 関連記事検索
        relevant_articles = self.vector_db.search(
            query=f"{context_summary} {current_question}",
            collection="support_articles",
            top_k=3
        )
        
        # Step 3: 過去の解決事例検索
        similar_cases = self.vector_db.search(
            query=current_question,
            collection="resolved_cases", 
            top_k=2
        )
        
        # Step 4: コンテキスト統合
        context = self.build_context(relevant_articles, similar_cases)
        
        return self.generate_response(current_question, context)
