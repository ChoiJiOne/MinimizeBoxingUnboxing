from pathlib import Path

def is_directory(path):
    target_path = Path(path)
    return target_path.exists() and target_path.is_dir()

def is_file(path):
    target_path = Path(path)
    return target_path.exists() and target_path.is_file()