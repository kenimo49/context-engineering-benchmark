from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    search_results: List[dict]
    current_strategy: str
    iteration_count: int
    confidence_score: float

def create_agentic_rag_graph():
    # ツール定義
    tools = [
        VectorSearchTool(),
        WebSearchTool(), 
        DatabaseQueryTool(),
        DocumentParseTool()
    ]
    tool_executor = ToolExecutor(tools)
    
    # 状態グラフ構築
    workflow = StateGraph(AgentState)
    
    # ノード定義
    workflow.add_node("analyzer", query_analyzer_node)
    workflow.add_node("planner", search_planner_node)
    workflow.add_node("searcher", search_executor_node)
    workflow.add_node("evaluator", result_evaluator_node)
    workflow.add_node("synthesizer", response_synthesizer_node)
    
    # エッジ定義（制御フロー）
    workflow.set_entry_point("analyzer")
    
    workflow.add_edge("analyzer", "planner")
    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "evaluator")
    
    # 条件分岐：十分な結果が得られた場合は終了、否則再検索
    workflow.add_conditional_edges(
        "evaluator",
        should_continue,
        {
            "continue": "planner",  # 戦略修正して再検索
            "synthesize": "synthesizer"  # 回答生成へ
        }
    )
    
    workflow.add_edge("synthesizer", END)
    
    return workflow.compile()

# ノード実装例
def query_analyzer_node(state: AgentState) -> AgentState:
    """クエリ分析ノード"""
    query = state["query"]
    
    # 意図分析、複雑性評価、必要情報特定
    analysis = analyze_query_intent(query)
    
    return {
        **state,
        "current_strategy": analysis.recommended_strategy,
        "iteration_count": 0,
        "confidence_score": 0.0
    }

def search_planner_node(state: AgentState) -> AgentState:
    """検索戦略立案ノード"""
    query = state["query"]
    current_strategy = state["current_strategy"]
    previous_results = state.get("search_results", [])
    
    # 前回結果を基に戦略調整
    plan = create_search_plan(
        query=query,
        strategy=current_strategy,
        previous_results=previous_results,
        iteration=state["iteration_count"]
    )
    
    return {
        **state,
        "current_strategy": plan.strategy_name
    }

def search_executor_node(state: AgentState) -> AgentState:
    """検索実行ノード"""
    # 戦略に基づくツール選択・実行
    tools_to_use = select_tools_for_strategy(state["current_strategy"])
    
    new_results = []
    for tool in tools_to_use:
        results = tool.search(
            query=state["query"],
            parameters=extract_tool_parameters(state)
        )
        new_results.extend(results)
    
    all_results = state.get("search_results", []) + new_results
    
    return {
        **state,
        "search_results": all_results,
        "iteration_count": state["iteration_count"] + 1
    }

def should_continue(state: AgentState) -> str:
    """継続判定"""
    confidence = evaluate_result_confidence(state["search_results"])
    max_iterations = 3
    
    if confidence > 0.8 or state["iteration_count"] >= max_iterations:
        return "synthesize"
    else:
        return "continue"

# 使用例
def run_langgraph_agentic_rag():
    graph = create_agentic_rag_graph()
    
    initial_state = {
        "query": "Claude Codeでマルチファイル編集を効率化する方法",
        "search_results": [],
        "current_strategy": "",
        "iteration_count": 0,
        "confidence_score": 0.0
    }
    
    result = graph.invoke(initial_state)
    return result["synthesized_response"]
