# claude_code_agentic_search.py

import os
import subprocess
from typing import List, Dict

class ClaudeCodeAgenticSearch:
    def __init__(self, project_root: str):
        self.project_root = project_root
        
    def search_claude_md(self, query: str) -> Dict:
        """CLAUDE.md検索"""
        claude_files = []
        
        # CLAUDE.mdファイル発見
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.upper() == "CLAUDE.MD":
                    claude_files.append(os.path.join(root, file))
        
        results = []
        for file_path in claude_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        results.append({
                            "file": file_path,
                            "content_preview": content[:200] + "..."
                        })
            except Exception as e:
                continue
                
        return {
            "query": query,
            "claude_md_results": results,
            "search_strategy": "CLAUDE.md contextual search"
        }
    
    def search_code_with_context(self, query: str) -> Dict:
        """コンテキスト考慮コード検索"""
        
        # 1. CLAUDE.mdから技術スタック情報取得
        context = self.search_claude_md("技術スタック")
        
        # 2. コンテキスト情報を基にgrep検索戦略調整
        file_patterns = ["*.py", "*.js", "*.ts", "*.jsx", "*.tsx"]
        if "React" in str(context):
            file_patterns.extend(["*.jsx", "*.tsx"])
        if "Python" in str(context):
            file_patterns.extend(["*.py"])
            
        # 3. 戦略的grep実行
        all_results = []
        for pattern in file_patterns:
            try:
                result = subprocess.run([
                    "find", self.project_root, "-name", pattern, 
                    "-exec", "grep", "-l", query, "{}", "+"
                ], capture_output=True, text=True)
                
                if result.stdout:
                    files = result.stdout.strip().split('\n')
                    all_results.extend(files)
                    
            except Exception:
                continue
                
        return {
            "query": query,
            "context_info": context,
            "matching_files": all_results[:10],
            "search_strategy": "context-aware grep search"
        }

# 使用例
if __name__ == "__main__":
    searcher = ClaudeCodeAgenticSearch(".")
    
    # CLAUDE.md検索
    claude_result = searcher.search_claude_md("コーディング規約")
    print("=== CLAUDE.md検索結果 ===")
    print(claude_result)
    
    # コンテキスト考慮検索
    code_result = searcher.search_code_with_context("function")
    print("\n=== コンテキスト考慮検索結果 ===") 
    print(code_result)
