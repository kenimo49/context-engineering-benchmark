# simple_agentic_rag.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import glob
import subprocess
import re

class AgentState(TypedDict):
    query: str
    search_results: List[str]
    iteration_count: int
    final_answer: str

def search_local_files(state: AgentState) -> AgentState:
    """ローカルファイル検索（grep/globベース）"""
    query = state["query"]
    
    # シンプルなgrep検索
    try:
        # Pythonファイルから関連コード検索
        result = subprocess.run(
            ["grep", "-r", "--include=*.py", query, "."],
            capture_output=True, 
            text=True
        )
        
        matches = result.stdout.split('\n')[:5]  # 上位5件
        
        state["search_results"] = [match for match in matches if match.strip()]
        state["iteration_count"] = state["iteration_count"] + 1
        
    except Exception as e:
        state["search_results"] = [f"検索エラー: {str(e)}"]
        
    return state

def should_continue(state: AgentState) -> str:
    """継続判定"""
    if state["search_results"] and state["iteration_count"] < 3:
        if len(state["search_results"]) > 2:  # 十分な結果
            return "synthesize"
        else:
            return "search"  # 追加検索
    else:
        return "synthesize"

def synthesize_answer(state: AgentState) -> AgentState:
    """回答統合（簡易版）"""
    results = state["search_results"]
    
    # 簡易統合ロジック
    if results:
        state["final_answer"] = f"""
        検索クエリ: {state["query"]}
        
        発見された関連情報:
        {chr(10).join(f"- {result}" for result in results[:3])}
        
        検索戦略: grep検索によるローカルファイル調査
        反復回数: {state["iteration_count"]}
        """
    else:
        state["final_answer"] = "関連情報が見つかりませんでした。"
        
    return state

# グラフ構築
def create_simple_agentic_rag():
    workflow = StateGraph(AgentState)
    
    # ノード追加
    workflow.add_node("search", search_local_files)
    workflow.add_node("synthesize", synthesize_answer)
    
    # エントリポイント
    workflow.set_entry_point("search")
    
    # 条件分岐
    workflow.add_conditional_edges(
        "search",
        should_continue,
        {
            "search": "search",      # 追加検索
            "synthesize": "synthesize"  # 回答生成
        }
    )
    
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()

# 実行例
def run_tutorial():
    app = create_simple_agentic_rag()
    
    initial_state = {
        "query": "def",  # Python関数定義を検索
        "search_results": [],
        "iteration_count": 0,
        "final_answer": ""
    }
    
    result = app.invoke(initial_state)
    print(result["final_answer"])

if __name__ == "__main__":
    run_tutorial()
