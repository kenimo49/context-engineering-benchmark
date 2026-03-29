# Extracted from appendix-b-experiment.md
# Block #14

# parallel_experiment.py
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time

class ParallelBenchmark:
    def __init__(self, api_key: str, max_concurrent: int = 5):
        self.api_key = api_key
        self.max_concurrent = max_concurrent
        
    async def run_parallel_experiment(self, test_cases: List[Dict]) -> List[Dict]:
        """非同期並列実行"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def bounded_request(test_case):
            async with semaphore:
                return await self._async_api_call(test_case)
        
        tasks = [bounded_request(case) for case in test_cases]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # エラーハンドリング
        valid_results = [r for r in results if not isinstance(r, Exception)]
        errors = [r for r in results if isinstance(r, Exception)]
        
        if errors:
            print(f"Encountered {len(errors)} errors during execution")
        
        return valid_results
    
    async def _async_api_call(self, test_case: Dict) -> Dict:
        """非同期API呼び出し"""
        # Anthropic SDKは現在async未対応のため、
        # 実際の実装では ThreadPoolExecutor を使用
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, self._sync_api_call, test_case
            )
        return result
    
    def _sync_api_call(self, test_case: Dict) -> Dict:
        """同期API呼び出し（実際の処理）"""
        # レート制限対応
        time.sleep(0.1)  # 100ms間隔
        
        # 実際のAPI呼び出し処理
        # （ここで ContextEngineeringBenchmark を使用）
        pass