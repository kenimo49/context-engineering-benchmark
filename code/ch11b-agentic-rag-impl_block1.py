# Extracted from ch11b-agentic-rag-impl.md
# Block #1

from tavily import TavilyClient
import os

def agentic_search(query: str, trusted_domains: list = None) -> dict:
    """Tavily APIを使ったAgentic検索の基本実装"""
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    
    response = client.search(
        query=query,
        search_depth="advanced",
        include_domains=trusted_domains or [],
        max_results=10
    )
    
    results = []
    for r in response["results"]:
        results.append({
            "title": r["title"],
            "url": r["url"],
            "content": r["content"],
            "score": r.get("score", 0),
        })
    
    return {"query": query, "results": results}

# 使用例
results = agentic_search(
    "Claude Code CLAUDE.md 最適化",
    trusted_domains=["anthropic.com", "github.com"]
)
for r in results["results"][:3]:
    print(f"[{r['score']:.2f}] {r['title']}")
    print(f"  {r['url']}")