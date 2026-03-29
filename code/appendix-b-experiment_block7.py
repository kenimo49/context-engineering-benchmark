# analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_results(results_file: str):
    df = pd.read_csv(results_file)
    
    # 基本統計
    summary = df.groupby(['model', 'context_type'])['score'].agg([
        'mean', 'std', 'count'
    ]).round(3)
    print("実験結果サマリー:")
    print(summary)
    
    # 改善率の計算
    pivot = df.pivot_table(
        values='score', 
        index='model', 
        columns='context_type', 
        aggfunc='mean'
    )
    
    if 'rag' in pivot.columns and 'zero' in pivot.columns:
        pivot['improvement'] = (pivot['rag'] - pivot['zero']) / pivot['zero'] * 100
        print("\nRAG適用による改善率:")
        print(pivot[['zero', 'rag', 'improvement']])
    
    # 可視化
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='model', y='score', hue='context_type')
    plt.title('モデル別・コンテキスト別性能比較')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('experiment_results.png', dpi=300)
    plt.show()

# コスト分析
def cost_analysis(df: pd.DataFrame):
    # 概算トークン数（実際はAPIレスポンスから取得）
    df['estimated_input_tokens'] = df['prompt'].str.len() * 0.75  # 概算
    df['estimated_output_tokens'] = df['response'].str.len() * 0.75
    
    # Anthropic料金体系（2024年12月時点）
    pricing = {
        'claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
        'claude-3-sonnet-20241022': {'input': 3.0, 'output': 15.0}
    }
    
    df['cost'] = df.apply(lambda row: 
        (row['estimated_input_tokens'] / 1_000_000 * pricing[row['model']]['input'] +
         row['estimated_output_tokens'] / 1_000_000 * pricing[row['model']]['output']), 
        axis=1
    )
    
    cost_summary = df.groupby(['model', 'context_type']).agg({
        'cost': ['mean', 'sum'],
        'score': 'mean'
    }).round(4)
    
    print("コスト分析:")
    print(cost_summary)
    
    # ROI計算
    df['roi'] = df['score'] / df['cost']
    roi_summary = df.groupby(['model', 'context_type'])['roi'].mean().round(2)
    print("\nROI (Performance/Cost):")
    print(roi_summary)

if __name__ == "__main__":
    analyze_results('experiment_results.csv')
