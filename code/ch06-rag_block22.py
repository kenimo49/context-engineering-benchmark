# Extracted from ch06-rag.md
# Block #22

# 最小限のRAGシステム
class MinimalRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma()
        self.llm = ChatOpenAI()
        
    def add_documents(self, documents):
        # シンプルなチャンキング
        chunks = [doc[i:i+1000] for doc in documents 
                 for i in range(0, len(doc), 800)]
        
        # 埋め込み・保存
        self.vector_store.add_texts(chunks)
    
    def query(self, question):
        # 検索・生成
        docs = self.vector_store.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        
        prompt = f"Question: {question}\nContext: {context}\nAnswer:"
        return self.llm.invoke(prompt)