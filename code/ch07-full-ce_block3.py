class HierarchicalLayoutManager:
    def __init__(self):
        self.importance_weights = {
            "critical": 1.0,
            "important": 0.8,
            "supporting": 0.6,
            "background": 0.4
        }
    
    def structure_context(self, documents, query):
        # 重要度スコアリング
        scored_docs = []
        for doc in documents:
            importance = self.calculate_importance(doc, query)
            scored_docs.append((doc, importance))
        
        # 階層化レイアウト生成
        return self.create_hierarchical_layout(scored_docs)
    
    def create_hierarchical_layout(self, scored_docs):
        layout = {
            "primary_context": [],
            "supporting_context": [],
            "background_context": []
        }
        
        for doc, score in scored_docs:
            if score > 0.8:
                layout["primary_context"].append(doc)
            elif score > 0.5:
                layout["supporting_context"].append(doc)
            else:
                layout["background_context"].append(doc)
        
        return self.format_hierarchical_prompt(layout)
    
    def format_hierarchical_prompt(self, layout):
        prompt = "# PRIMARY CONTEXT (Most Relevant)\n"
        for i, doc in enumerate(layout["primary_context"], 1):
            prompt += f"## Source {i}: {doc.metadata.get('title', 'Document')}\n"
            prompt += f"{doc.content}\n\n"
        
        if layout["supporting_context"]:
            prompt += "# SUPPORTING CONTEXT (Additional Details)\n"
            for doc in layout["supporting_context"]:
                prompt += f"- {doc.content[:200]}...\n"
        
        if layout["background_context"]:
            prompt += "# BACKGROUND CONTEXT (Reference Only)\n"
            for doc in layout["background_context"]:
                prompt += f"- {doc.metadata.get('title', 'Reference')}\n"
        
        return prompt
