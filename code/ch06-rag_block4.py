def recursive_chunking(text, max_size=1000):
    if len(text) <= max_size:
        return [text]
    
    # 段落で分割を試行
    paragraphs = text.split("\n\n")
    if all(len(p) <= max_size for p in paragraphs):
        return paragraphs
    
    # 文で分割を試行  
    sentences = text.split("。")
    if all(len(s) <= max_size for s in sentences):
        return sentences
    
    # 最後の手段: 固定長分割
    return fixed_length_chunking(text, max_size)

# 利点: 適応的、階層的
# 欠点: 複雑なロジック
