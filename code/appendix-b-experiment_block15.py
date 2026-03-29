class CheckpointManager:
    def __init__(self, checkpoint_file: str):
        self.checkpoint_file = checkpoint_file
        
    def save_checkpoint(self, results: List[Dict], processed_count: int):
        """チェックポイントの保存"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'processed_count': processed_count,
            'results': results
        }
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)
    
    def load_checkpoint(self) -> Dict:
        """チェックポイントの読み込み"""
        try:
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'processed_count': 0, 'results': []}
