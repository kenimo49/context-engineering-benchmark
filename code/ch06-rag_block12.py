# Extracted from ch06-rag.md
# Block #12

def filtered_search(vector_db, query, filters=None):
    base_results = vector_db.similarity_search(query, k=50)
    
    if not filters:
        return base_results[:5]
    
    filtered_results = []
    for doc in base_results:
        if matches_filters(doc.metadata, filters):
            filtered_results.append(doc)
        
        if len(filtered_results) >= 5:
            break
    
    return filtered_results

def matches_filters(metadata, filters):
    for key, value in filters.items():
        if key == "date_range":
            if not (value["start"] <= metadata["date"] <= value["end"]):
                return False
        elif key == "category":
            if metadata.get("category") != value:
                return False
        elif key == "language":
            if metadata.get("language") != value:
                return False
    
    return True

# 使用例
filters = {
    "category": "technical",
    "language": "ja", 
    "date_range": {"start": "2024-01-01", "end": "2024-12-31"}
}
results = filtered_search(vector_db, "RAGの実装方法", filters)