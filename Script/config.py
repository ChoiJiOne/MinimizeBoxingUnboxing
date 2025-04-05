from dataclasses import dataclass

@dataclass
class ProjectConfig:
    root_path: str
    solution_name: str
    project_name: str
    log_path: str