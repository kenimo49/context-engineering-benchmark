# data_preprocessor.py
import json
from pathlib import Path
from typing import Union, List, Dict

class DataPreprocessor:
    def __init__(self):
        self.supported_formats = ['.txt', '.json', '.csv', '.md']
    
    def load_documents(self, data_path: Union[str, Path]) -> List[str]:
        """様々な形式の文書を読み込み"""
        path = Path(data_path)
        documents = []
        
        if path.is_file():
            documents = self._load_single_file(path)
        elif path.is_dir():
            for file_path in path.rglob('*'):
                if file_path.suffix in self.supported_formats:
                    documents.extend(self._load_single_file(file_path))
        
        return documents
    
    def _load_single_file(self, file_path: Path) -> List[str]:
        """単一ファイルの読み込み"""
        try:
            if file_path.suffix == '.json':
                return self._load_json(file_path)
            elif file_path.suffix == '.csv':
                return self._load_csv(file_path)
            else:
                return self._load_text(file_path)
        except Exception as e:
            print(f"Failed to load {file_path}: {e}")
            return []
    
    def _load_json(self, file_path: Path) -> List[str]:
        """JSON形式の処理"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            return [str(item) for item in data]
        elif isinstance(data, dict):
            return [f"{k}: {v}" for k, v in data.items()]
        else:
            return [str(data)]
    
    def create_test_cases(self, questions_file: str, expected_file: str) -> List[Dict]:
        """自社のQ&Aデータからテストケース作成"""
        with open(questions_file, 'r', encoding='utf-8') as f:
            questions = [line.strip() for line in f.readlines()]
            
        with open(expected_file, 'r', encoding='utf-8') as f:
            expected_answers = [line.strip() for line in f.readlines()]
        
        test_cases = []
        for i, (q, a) in enumerate(zip(questions, expected_answers)):
            test_cases.append({
                'id': f'custom_{i:03d}',
                'prompt': q,
                'expected': {'answer': a},
                'domain': 'custom'
            })
        
        return test_cases
