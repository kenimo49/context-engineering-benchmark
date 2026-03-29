import hashlib
from functools import lru_cache

class RAGCache:
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self.local_cache = {}
    
    def cache_key(self, query, doc_version):
        content = f"{query}:{doc_version}"
        return hashlib.md5(content.encode()).hexdigest()
    
    @lru_cache(maxsize=1000)  
    def cached_similarity_search(self, query_hash, doc_version):
        # ローカルキャッシュ確認
        cache_key = self.cache_key(query_hash, doc_version)
        
        if self.redis_client:
            # Redis キャッシュ確認
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        
        # キャッシュミス: 実際の検索実行
        results = self.vector_db.similarity_search(query_hash)
        
        # キャッシュに保存
        if self.redis_client:
            self.redis_client.setex(
                cache_key, 
                3600,  # 1時間TTL
                json.dumps(results)
            )
        
        return results
