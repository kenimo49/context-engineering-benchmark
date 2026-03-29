from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class RAGSystem:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = None
    
    def build_knowledge_base(self, documents: List[str], collection_name: str = "knowledge"):
        """知識ベースの構築"""
        # コレクション作成
        self.collection = self.chroma_client.create_collection(name=collection_name)
        
        # 文書の埋め込み生成とインデックス化
        for i, doc in enumerate(documents):
            embedding = self.embedding_model.encode(doc).tolist()
            self.collection.add(
                embeddings=[embedding],
                documents=[doc],
                ids=[f"doc_{i}"]
            )
    
    def search(self, query: str, top_k: int = 3) -> List[str]:
        """セマンティック検索"""
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results['documents'][0]
    
    def build_context(self, relevant_docs: List[str]) -> str:
        """検索結果からコンテキストを構築"""
        context = "参考情報:\n"
        for i, doc in enumerate(relevant_docs, 1):
            context += f"{i}. {doc}\n\n"
        context += "上記の情報を参考にして、以下の質問に答えてください。\n"
        return context
