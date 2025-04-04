from pathlib import Path
import logging

def setup_global_logging(log_path: str):
    path = Path(log_path)