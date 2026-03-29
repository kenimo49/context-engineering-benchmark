import re

def detect_and_mask_pii(content: str) -> dict:
    """個人情報を検出してマスキングする"""
    patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}-\d{4}-\d{4}\b',
        'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    }
    
    found_pii = []
    masked = content
    
    for pii_type, pattern in patterns.items():
        for match in re.finditer(pattern, content):
            found_pii.append({'type': pii_type, 'text': match.group()})
            masked = masked.replace(match.group(), '*' * len(match.group()))
    
    return {'found': len(found_pii) > 0, 'masked_content': masked, 'items': found_pii}

# テスト
test = "お問い合わせは user@example.com または 090-1234-5678 まで"
result = detect_and_mask_pii(test)
print(result['masked_content'])
# → お問い合わせは **************** または *************  まで
