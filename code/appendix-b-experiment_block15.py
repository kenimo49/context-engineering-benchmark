# Extracted from appendix-b-experiment.md
# Block #15

# monitoring.py
import logging
from datetime import datetime
import psutil
import time

class ExperimentMonitor:
    def __init__(self, log_file: str = "experiment.log"):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.start_time = None
        self.api_calls = 0
        self.errors = 0
        
    def start_experiment(self, experiment_name: str):
        """実験開始"""
        self.start_time = time.time()
        self.logger.info(f"Starting experiment: {experiment_name}")
        self.logger.info(f"System info - CPU: {psutil.cpu_count()}, Memory: {psutil.virtual_memory().total / 1e9:.1f}GB")
    
    def log_api_call(self, model: str, success: bool, response_time: float):
        """API呼び出しのログ"""
        self.api_calls += 1
        if not success:
            self.errors += 1
            
        self.logger.info(f"API call - Model: {model}, Success: {success}, Time: {response_time:.2f}s")
        
        if self.api_calls % 100 == 0:
            self._log_progress()
    
    def _log_progress(self):
        """進捗の記録"""
        elapsed = time.time() - self.start_time
        error_rate = (self.errors / self.api_calls) * 100 if self.api_calls > 0 else 0
        
        self.logger.info(f"Progress - Calls: {self.api_calls}, "
                        f"Elapsed: {elapsed:.1f}s, "
                        f"Error rate: {error_rate:.1f}%")
    
    def finish_experiment(self):
        """実験終了"""
        total_time = time.time() - self.start_time
        self.logger.info(f"Experiment completed in {total_time:.1f}s")
        self.logger.info(f"Total API calls: {self.api_calls}, Errors: {self.errors}")