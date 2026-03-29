# Extracted from appendix-b-experiment.md
# Block #8

# test_dataset.py
test_cases = [
    {
        'id': 'tech_001',
        'prompt': 'Pythonのリスト内包表記について説明してください',
        'expected': {
            'keywords': ['リスト', '内包表記', 'for', '効率的', 'Pythonic'],
            'required_elements': ['構文', '例', '利点']
        },
        'domain': 'programming'
    },
    {
        'id': 'biz_001', 
        'prompt': 'スタートアップが資金調達する際の注意点は？',
        'expected': {
            'keywords': ['バリュエーション', '株式', '投資家', 'デューデリジェンス'],
            'required_elements': ['準備', 'リスク', '戦略']
        },
        'domain': 'business'
    },
    # 実際には50-100件程度のテストケースを用意
]

knowledge_base = [
    "Pythonのリスト内包表記は、既存のリストから新しいリストを効率的に作成する構文です...",
    "スタートアップの資金調達では、適切なバリュエーション設定が重要です...",
    # ドメイン知識を含む文書群
]