import anthropic
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import time
import json

class ContextEngineeringBenchmark:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.results = []
    
    def run_zero_context_test(self, model: str, test_cases: List[Dict]) -> List[Dict]:
        """ゼロコンテキストでのベースライン測定"""
        results = []
        for case in test_cases:
            response = self._call_model(
                model=model,
                prompt=case['prompt'],
                context=""
            )
            score = self._evaluate_response(response, case['expected'])
            results.append({
                'model': model,
                'context_type': 'zero',
                'prompt_id': case['id'],
                'response': response,
                'score': score,
                'expected': case['expected']
            })
        return results
    
    def run_rag_test(self, model: str, test_cases: List[Dict], 
                     knowledge_base: List[str]) -> List[Dict]:
        """RAG適用での測定"""
        # ベクトルデータベース構築
        vector_db = self._build_vector_db(knowledge_base)
        
        results = []
        for case in test_cases:
            # 関連文書の検索
            relevant_docs = self._search_relevant_docs(
                vector_db, case['prompt'], top_k=3
            )
            
            # コンテキスト構築
            context = self._build_context(relevant_docs)
            
            response = self._call_model(
                model=model,
                prompt=case['prompt'],
                context=context
            )
            score = self._evaluate_response(response, case['expected'])
            results.append({
                'model': model,
                'context_type': 'rag',
                'prompt_id': case['id'],
                'response': response,
                'score': score,
                'context_length': len(context.split()),
                'relevant_docs': len(relevant_docs)
            })
        return results
    
    def _call_model(self, model: str, prompt: str, context: str) -> str:
        """モデル呼び出し（エラーハンドリング付き）"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            message = self.client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": full_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"API call failed: {e}")
            return f"ERROR: {str(e)}"
    
    def _evaluate_response(self, response: str, expected: Dict) -> float:
        """レスポンス評価（カスタマイズ可能）"""
        # 簡単な例: キーワード一致ベースのスコア
        if 'keywords' in expected:
            keywords = expected['keywords']
            matches = sum(1 for kw in keywords if kw.lower() in response.lower())
            return matches / len(keywords)
        return 0.0
