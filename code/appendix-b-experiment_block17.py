# Extracted from appendix-b-experiment.md
# Block #17

def process_in_batches(data: List, batch_size: int = 10):
    """大量データのバッチ処理"""
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        yield batch

# 使用例
for batch in process_in_batches(large_test_cases, batch_size=20):
    results = process_batch(batch)
    save_intermediate_results(results)