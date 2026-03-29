# CLI Implementation（114,000トークン）
class TraditionalCLIApproach:
    def automate_web_task(self, task_description):
        # Step 1: タスクを細かいCLIコマンドに分解
        cli_commands = self.decompose_to_cli_commands(task_description)
        
        # Step 2: 各コマンドの説明をコンテキストに含める
        context = "Available CLI commands:\n"
        context += self.generate_cli_documentation()  # 巨大なドキュメント
        
        # Step 3: 実行例とエラーハンドリングもコンテキストに含める
        context += self.generate_cli_examples()
        context += self.generate_error_handling_docs()
        
        # 結果: 114,000トークンの巨大コンテキスト
        return self.llm_with_massive_context(task_description, context)

# MCP Implementation（27,000トークン）  
class MCPPlaywrightApproach:
    def automate_web_task(self, task_description):
        # Step 1: 高レベルなPlaywright MCPツールを使用
        available_tools = [
            "playwright_navigate(url)",
            "playwright_click(selector)",
            "playwright_type(selector, text)",
            "playwright_screenshot()",
            "playwright_extract_text(selector)"
        ]
        
        # Step 2: 簡潔なツール説明のみコンテキストに含める
        context = self.generate_concise_tool_descriptions(available_tools)
        
        # Step 3: MCPサーバーが詳細な実装を処理
        return self.llm_with_optimized_context(task_description, context)
    
    def generate_concise_tool_descriptions(self, tools):
        """MCP用の最適化されたツール説明"""
        descriptions = []
        
        for tool in tools:
            # 必要最小限の情報のみ
            desc = {
                "name": tool.split("(")[0],
                "purpose": self.get_tool_purpose(tool),
                "when_to_use": self.get_usage_pattern(tool)
            }
            descriptions.append(desc)
        
        return json.dumps(descriptions, indent=2)  # 簡潔なJSON形式
