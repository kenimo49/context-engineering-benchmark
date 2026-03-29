# main_experiment.py
from dotenv import load_dotenv
import os

load_dotenv()

def run_full_experiment():
    benchmark = ContextEngineeringBenchmark(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    models = [
        "claude-3-haiku-20240307",
        "claude-3-sonnet-20241022"
    ]
    
    all_results = []
    
    for model in models:
        print(f"Testing {model}...")
        
        # ゼロコンテキストテスト
        zero_results = benchmark.run_zero_context_test(model, test_cases)
        all_results.extend(zero_results)
        
        # RAGテスト
        rag_results = benchmark.run_rag_test(model, test_cases, knowledge_base)
        all_results.extend(rag_results)
        
        # 結果の保存
        pd.DataFrame(all_results).to_csv(f'results_{model.replace("-", "_")}.csv')
    
    return all_results

if __name__ == "__main__":
    results = run_full_experiment()
    print("実験完了！")
