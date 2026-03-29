#!/usr/bin/env python3
"""
Context Engineering本コードブロックの動作確認ツール

抽出されたコードの品質をチェックし、レポートを生成する。
"""

import os
import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import importlib.util
import re

class CodeQualityChecker:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.results = []
        self.stats = {
            'total_checked': 0,
            'syntax_ok': 0,
            'syntax_error': 0,
            'import_error': 0,
            'executable': 0,
            'design_pattern': 0,
            'pseudo_code': 0,
        }
    
    def check_python_files(self):
        """Pythonファイルを全てチェック"""
        python_dir = self.base_dir / 'python'
        
        if not python_dir.exists():
            print("❌ pythonディレクトリが見つかりません")
            return
        
        python_files = list(python_dir.glob('*.py'))
        print(f"📋 {len(python_files)}個のPythonファイルをチェックします\n")
        
        for py_file in python_files:
            self.check_single_file(py_file)
        
        self.generate_report()
    
    def check_single_file(self, file_path: Path):
        """単一ファイルのチェック"""
        filename = file_path.name
        self.stats['total_checked'] += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result = {
                'file': filename,
                'syntax_ok': False,
                'error': f"読み込みエラー: {str(e)}",
                'category': 'file_error',
                'executable': False,
                'imports': []
            }
            self.results.append(result)
            return
        
        result = {
            'file': filename,
            'content': content,
            'syntax_ok': False,
            'error': None,
            'category': 'unknown',
            'executable': False,
            'imports': [],
            'missing_imports': [],
            'design_hints': []
        }
        
        # 設計パターン・擬似コードの検出
        result['category'], result['design_hints'] = self.categorize_code(content)
        if result['category'] in ['design_pattern', 'pseudo_code']:
            if result['category'] == 'design_pattern':
                self.stats['design_pattern'] += 1
            else:
                self.stats['pseudo_code'] += 1
        
        # 構文チェック
        try:
            ast.parse(content)
            result['syntax_ok'] = True
            self.stats['syntax_ok'] += 1
            
            # import文の抽出
            result['imports'] = self.extract_imports(content)
            
            # import存在確認
            missing_imports = self.check_imports(result['imports'])
            result['missing_imports'] = missing_imports
            
            if missing_imports:
                result['executable'] = False
                result['error'] = f"存在しないモジュール: {', '.join(missing_imports)}"
                self.stats['import_error'] += 1
            else:
                result['executable'] = True
                self.stats['executable'] += 1
                
        except SyntaxError as e:
            result['syntax_ok'] = False
            result['error'] = f"構文エラー: {str(e)}"
            self.stats['syntax_error'] += 1
        except Exception as e:
            result['syntax_ok'] = False
            result['error'] = f"予期しないエラー: {str(e)}"
        
        self.results.append(result)
        
        # 進捗表示
        status = "✅" if result['syntax_ok'] else "❌"
        category_icon = self.get_category_icon(result['category'])
        print(f"{status} {category_icon} {filename}")
        if result['error']:
            print(f"   └─ {result['error']}")
    
    def categorize_code(self, content: str) -> Tuple[str, List[str]]:
        """コードの分類"""
        content_lower = content.lower()
        hints = []
        
        # 設計パターン説明用の明示的な言及
        if '設計パターンの説明' in content:
            hints.append("「設計パターンの説明」と明記")
            return 'design_pattern', hints
        
        if '擬似コード' in content:
            hints.append("「擬似コード」と明記")
            return 'pseudo_code', hints
        
        if 'extracted from' in content_lower and ('説明' in content or 'example' in content_lower):
            hints.append("抽出コメントに説明的表現")
            return 'design_pattern', hints
        
        # クラス名から推測
        design_pattern_classes = [
            'ContextEngine', 'AgenticRAG', 'MCPServer', 'RAGSystem',
            'ContextOrchestrator', 'EnterpriseRAG', 'Benchmark'
        ]
        
        for class_name in design_pattern_classes:
            if class_name in content:
                hints.append(f"設計パターンクラス名: {class_name}")
                return 'design_pattern', hints
        
        # pass文やNotImplementedが多い
        pass_count = content_lower.count('pass')
        not_implemented_count = content_lower.count('notimplemented')
        
        if pass_count > 2 or not_implemented_count > 0:
            hints.append(f"未実装箇所: pass={pass_count}, NotImplemented={not_implemented_count}")
            return 'pseudo_code', hints
        
        # コメントで実装を説明している
        if '# 実装は省略' in content or '# （実装は省略）' in content:
            hints.append("実装省略のコメント")
            return 'pseudo_code', hints
        
        return 'implementation', hints
    
    def get_category_icon(self, category: str) -> str:
        """カテゴリアイコン"""
        icons = {
            'design_pattern': '🏗️',
            'pseudo_code': '📝',
            'implementation': '⚙️',
            'unknown': '❓',
            'file_error': '💥'
        }
        return icons.get(category, '❓')
    
    def extract_imports(self, content: str) -> List[str]:
        """import文を抽出"""
        imports = []
        
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except:
            # 構文エラーの場合は正規表現で抽出
            import_lines = re.findall(r'^\s*(?:from|import)\s+([^\s]+)', content, re.MULTILINE)
            imports.extend(import_lines)
        
        return list(set(imports))  # 重複除去
    
    def check_imports(self, imports: List[str]) -> List[str]:
        """importの存在確認"""
        missing = []
        
        # 標準ライブラリとよく知られるパッケージ
        known_modules = {
            'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'typing',
            'asyncio', 'subprocess', 'collections', 'functools', 're',
            'math', 'random', 'hashlib', 'base64', 'uuid', 'logging',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'requests',
            'anthropic', 'openai', 'langchain', 'langgraph', 'chromadb',
            'pinecone', 'weaviate', 'sentence_transformers', 'torch',
            'transformers', 'sklearn', 'scipy'
        }
        
        for module in imports:
            base_module = module.split('.')[0]  # サブモジュールは除く
            
            if base_module in known_modules:
                continue
            
            try:
                importlib.util.find_spec(base_module)
            except (ImportError, ModuleNotFoundError, ValueError):
                missing.append(base_module)
        
        return missing
    
    def generate_report(self):
        """レポート生成"""
        report_path = self.base_dir / 'README.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Context Engineering本 コード動作確認レポート\n\n")
            
            # サマリー
            f.write("## サマリー\n")
            f.write(f"- 確認コードブロック数: {self.stats['total_checked']}個\n")
            f.write(f"- 構文OK: {self.stats['syntax_ok']}個\n")
            f.write(f"- 構文エラー: {self.stats['syntax_error']}個\n")
            f.write(f"- import不足: {self.stats['import_error']}個\n")
            f.write(f"- 実行可能: {self.stats['executable']}個\n")
            f.write(f"- 設計パターン説明用: {self.stats['design_pattern']}個\n")
            f.write(f"- 擬似コード: {self.stats['pseudo_code']}個\n\n")
            
            # カテゴリ別結果
            self.write_category_results(f)
            
            # 詳細リスト
            f.write("## 詳細結果\n\n")
            
            for result in sorted(self.results, key=lambda x: x['file']):
                f.write(f"### {result['file']}\n")
                f.write(f"- **カテゴリ**: {result['category']} {self.get_category_icon(result['category'])}\n")
                f.write(f"- **構文チェック**: {'✅' if result['syntax_ok'] else '❌'}\n")
                f.write(f"- **実行可能性**: {'✅' if result['executable'] else '❌'}\n")
                
                if result['error']:
                    f.write(f"- **エラー**: {result['error']}\n")
                
                if result.get('imports'):
                    f.write(f"- **import文**: {', '.join(result['imports'])}\n")
                
                if result.get('missing_imports'):
                    f.write(f"- **不足モジュール**: {', '.join(result['missing_imports'])}\n")
                
                if result.get('design_hints'):
                    f.write(f"- **設計ヒント**: {'; '.join(result['design_hints'])}\n")
                
                f.write("\n")
            
            # 推奨事項
            f.write("## 推奨事項\n\n")
            f.write("### 実行可能コード\n")
            executable_files = [r for r in self.results if r['executable']]
            if executable_files:
                f.write("以下のファイルは構文的に正しく、依存関係も解決されているため実行可能です：\n")
                for result in executable_files:
                    f.write(f"- {result['file']}\n")
            else:
                f.write("実行可能なコードはありませんでした。\n")
            
            f.write("\n### 設計パターン理解用コード\n")
            design_files = [r for r in self.results if r['category'] == 'design_pattern']
            if design_files:
                f.write("以下は設計パターンの説明用コードです。実行よりも理解を目的としています：\n")
                for result in design_files[:10]:  # 最初の10個のみ表示
                    f.write(f"- {result['file']}\n")
                if len(design_files) > 10:
                    f.write(f"- （他{len(design_files)-10}個）\n")
            
            f.write("\n### 注意事項\n")
            f.write("- 多くのコードは教育目的の設計パターン説明用です\n")
            f.write("- API呼び出しには有効なAPIキーが必要です\n")
            f.write("- 一部のモジュールは `pip install` での追加インストールが必要です\n")
            f.write("- 実際の動作には、適切な設定ファイルや環境変数が必要な場合があります\n")
    
    def write_category_results(self, f):
        """カテゴリ別結果を記述"""
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'count': 0, 'syntax_ok': 0, 'executable': 0}
            categories[cat]['count'] += 1
            if result['syntax_ok']:
                categories[cat]['syntax_ok'] += 1
            if result['executable']:
                categories[cat]['executable'] += 1
        
        f.write("## カテゴリ別結果\n\n")
        f.write("| カテゴリ | 総数 | 構文OK | 実行可能 | 説明 |\n")
        f.write("|----------|------|--------|----------|------|\n")
        
        category_descriptions = {
            'design_pattern': '設計パターンの説明用コード',
            'pseudo_code': '擬似コード（学習用）',
            'implementation': '実装を意図したコード',
            'unknown': '分類不明',
            'file_error': 'ファイル読み込みエラー'
        }
        
        for cat, stats in sorted(categories.items()):
            icon = self.get_category_icon(cat)
            desc = category_descriptions.get(cat, '不明')
            f.write(f"| {icon} {cat} | {stats['count']} | {stats['syntax_ok']} | {stats['executable']} | {desc} |\n")
        
        f.write("\n")

def main():
    """メイン処理"""
    base_dir = Path.home() / 'repos' / 'iris-lab' / '014-context-engineering-code-check'
    
    if not base_dir.exists():
        print("❌ 作業ディレクトリが見つかりません")
        return
    
    checker = CodeQualityChecker(base_dir)
    checker.check_python_files()
    
    print(f"\n📊 レポートが生成されました: {base_dir}/README.md")

if __name__ == "__main__":
    main()