# Extracted from appendix-b-experiment.md
# Block #13

# custom_config.py
class ExperimentConfig:
    def __init__(self, config_file: str = None):
        if config_file:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self._default_config()
    
    def _default_config(self) -> Dict:
        return {
            "models": [
                "claude-3-haiku-20240307",
                "claude-3-sonnet-20241022"
            ],
            "context_strategies": [
                "zero",
                "rag",
                "few_shot",
                "chain_of_thought"
            ],
            "evaluation": {
                "metrics": ["accuracy", "relevance", "completeness"],
                "domain": "general"
            },
            "rag_settings": {
                "chunk_size": 500,
                "chunk_overlap": 50,
                "top_k": 3,
                "embedding_model": "all-MiniLM-L6-v2"
            }
        }
    
    def get_models(self) -> List[str]:
        return self.config["models"]
    
    def get_context_strategies(self) -> List[str]:
        return self.config["context_strategies"]
    
    def save_config(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.config, f, indent=2)

# 使用例
config = ExperimentConfig()
config.config["models"].append("claude-3-opus-20240229")
config.config["evaluation"]["domain"] = "technical"
config.save_config("my_experiment_config.json")