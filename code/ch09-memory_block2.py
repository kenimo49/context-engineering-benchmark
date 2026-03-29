# Extracted from ch09-memory.md
# Block #2

# 設計パターン説明用の擬似コード（そのまま動作するコードではありません）

class SummaryMemory:
    def __init__(self, llm, summary_interval=10):
        self.llm = llm
        self.summary_interval = summary_interval
        self.current_summary = ""          # 過去の会話の要約
        self.recent_buffer = deque(maxlen=5)  # 直近の詳細な履歴
        self.interaction_count = 0

    def add_interaction(self, user_input, assistant_response):
        self.recent_buffer.append({"user": user_input, "assistant": assistant_response})
        self.interaction_count += 1
        if self.interaction_count % self.summary_interval == 0:
            self._update_summary()

    def _update_summary(self):
        """既存サマリー + 最近の会話 → LLMで新サマリー生成"""
        prompt = f"""
以下を簡潔に要約してください。重要な決定事項、継続中のタスク、
ユーザーの嗜好や背景情報を中心にまとめてください。

既存のサマリー: {self.current_summary}
最近の会話: {format_recent(self.recent_buffer)}
"""
        self.current_summary = self.llm.generate(prompt)
        # 古い詳細を破棄し、最新2件だけ残す
        keep = list(self.recent_buffer)[-2:]
        self.recent_buffer.clear()
        self.recent_buffer.extend(keep)

    def get_context_for_llm(self):
        """LLMに渡すコンテキスト = サマリー + 直近の詳細"""
        parts = []
        if self.current_summary:
            parts.append(f"=== 会話サマリー ===\n{self.current_summary}")
        if self.recent_buffer:
            parts.append("=== 最近の会話 ===")
            parts.extend(format_interaction(i) for i in self.recent_buffer)
        return "\n".join(parts)