#!/usr/bin/env python3
"""
Context Engineering本のコードブロック抽出ツール

全章からコードブロックを抽出し、言語別に分類して保存する。
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def extract_code_blocks(markdown_content: str, filename: str) -> List[Dict]:
    """
    Markdownファイルからコードブロックを抽出
    """
    # コードブロックの正規表現（```で囲まれた部分）
    pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    
    code_blocks = []
    for i, (language, code) in enumerate(matches):
        if not language:  # 言語が指定されていない場合
            language = detect_language(code)
        
        code_block = {
            'chapter': filename,
            'index': i + 1,
            'language': language,
            'code': code.strip(),
            'line_count': len(code.strip().split('\n'))
        }
        code_blocks.append(code_block)
    
    return code_blocks

def detect_language(code: str) -> str:
    """
    コードの内容から言語を推測
    """
    code_lower = code.lower().strip()
    
    # Python
    if any(keyword in code_lower for keyword in ['def ', 'import ', 'from ', 'class ', 'if __name__']):
        return 'python'
    
    # Shell/Bash
    if code_lower.startswith(('#!', 'pip install', 'conda ', 'git ', 'mkdir ', 'cd ')):
        return 'bash'
    
    # JavaScript/TypeScript
    if any(keyword in code_lower for keyword in ['function ', 'const ', 'let ', 'var ', 'npm ']):
        return 'javascript'
    
    # YAML
    if ':' in code and code_lower.startswith(('---', 'version:', 'name:')):
        return 'yaml'
    
    # JSON
    if code.strip().startswith(('{', '[')):
        return 'json'
    
    # Markdown
    if code.strip().startswith('#'):
        return 'markdown'
    
    return 'text'

def main():
    """メイン処理"""
    # Context Engineering本のパス
    book_path = Path.home() / 'repos' / 'zenn-content' / 'books' / 'context-engineering'
    output_dir = Path.home() / 'repos' / 'iris-lab' / '014-context-engineering-code-check'
    
    # 対象ファイルのリスト
    target_files = [
        'ch01-five-answers.md',
        'ch02-llm-lies.md', 
        'ch03-context-engineering-begins.md',
        'ch04-first-step.md',
        'ch05-few-shot.md',
        'ch06-rag.md',
        'ch07-full-ce.md',
        'ch08-mcp.md',
        'ch09-memory.md',
        'ch10-claude-code.md',
        'ch11a-agentic-rag-concept.md',
        'ch11b-agentic-rag-impl.md',
        'ch12a-enterprise-cases.md',
        'ch12b-enterprise-eval.md',
        'ch13-small-model-philosophy.md',
        'appendix-a-checklist.md',
        'appendix-b-experiment.md'
    ]
    
    all_code_blocks = []
    summary = {}
    
    for filename in target_files:
        file_path = book_path / filename
        
        if not file_path.exists():
            print(f"❌ ファイルが見つかりません: {filename}")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            code_blocks = extract_code_blocks(content, filename)
            all_code_blocks.extend(code_blocks)
            
            summary[filename] = {
                'total_blocks': len(code_blocks),
                'languages': {}
            }
            
            for block in code_blocks:
                lang = block['language']
                if lang in summary[filename]['languages']:
                    summary[filename]['languages'][lang] += 1
                else:
                    summary[filename]['languages'][lang] = 1
            
            print(f"✅ {filename}: {len(code_blocks)}個のコードブロック")
            
        except Exception as e:
            print(f"❌ {filename}の処理中にエラー: {str(e)}")
    
    # 言語別にコードブロックを分類
    languages = {}
    for block in all_code_blocks:
        lang = block['language']
        if lang not in languages:
            languages[lang] = []
        languages[lang].append(block)
    
    # 言語別にファイルを保存
    for lang, blocks in languages.items():
        if lang == 'text':  # テキストファイルは除外
            continue
            
        lang_dir = output_dir / lang
        lang_dir.mkdir(exist_ok=True)
        
        for block in blocks:
            chapter = block['chapter'].replace('.md', '')
            filename = f"{chapter}_block{block['index']}.{get_extension(lang)}"
            filepath = lang_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Extracted from {block['chapter']}\n")
                f.write(f"# Block #{block['index']}\n\n")
                f.write(block['code'])
    
    # サマリーレポートを生成
    generate_summary_report(output_dir, summary, languages)

def get_extension(language: str) -> str:
    """言語に応じた拡張子を返す"""
    extensions = {
        'python': 'py',
        'javascript': 'js',
        'typescript': 'ts',
        'bash': 'sh',
        'shell': 'sh',
        'yaml': 'yml',
        'json': 'json',
        'markdown': 'md'
    }
    return extensions.get(language, 'txt')

def generate_summary_report(output_dir: Path, summary: Dict, languages: Dict):
    """サマリーレポートを生成"""
    
    total_blocks = sum(info['total_blocks'] for info in summary.values())
    
    with open(output_dir / 'extraction_summary.md', 'w', encoding='utf-8') as f:
        f.write("# Context Engineering本 コードブロック抽出結果\n\n")
        
        f.write("## 全体サマリー\n")
        f.write(f"- **総コードブロック数**: {total_blocks}個\n")
        f.write(f"- **確認対象章**: {len(summary)}章\n\n")
        
        f.write("## 言語別分布\n")
        for lang, blocks in sorted(languages.items()):
            f.write(f"- **{lang}**: {len(blocks)}個\n")
        f.write("\n")
        
        f.write("## 章別詳細\n")
        for filename, info in summary.items():
            f.write(f"### {filename}\n")
            f.write(f"- 総ブロック数: {info['total_blocks']}個\n")
            
            if info['languages']:
                f.write("- 言語内訳:\n")
                for lang, count in sorted(info['languages'].items()):
                    f.write(f"  - {lang}: {count}個\n")
            else:
                f.write("- コードブロックなし\n")
            f.write("\n")
        
        f.write("## 注意事項\n")
        f.write("- 多くのコードは「設計パターンの説明用」として書かれています\n")
        f.write("- 実際に動作させることを想定していないコードが含まれています\n")
        f.write("- API呼び出しが必要なコードは適切なキーが必要です\n")
        f.write("- 依存関係のインストールが必要な場合があります\n")

if __name__ == "__main__":
    main()