import click
import traceback
from pathlib import Path

from core.command_utils import run_command
from core.config import ProjectConfig
from core.logger import Logger

@click.group()
def cli():
    pass

@cli.command()
@click.option("--root-path", required=True)
@click.option("--solution-name", required=True)
@click.option("--project-name", required=True)
@click.option("--log-path", required=True)
def add_csharp_project(**kwargs):
    try:
        config = ProjectConfig(**kwargs)
        logger = Logger(config.log_path)

        project_path = Path(config.root_path) / f"{config.project_name}"
        if project_path.exists():
            raise Exception(f"Already exist '{config.project_name}' project.")
        
        solution_path = Path(config.root_path) / f"{config.solution_name}.sln"
        if not solution_path.exists():
            raise Exception(f"Cannot found Visual Studio solution : '{config.solution_name}'")
        
        command = f"dotnet new console --language \"C#\" --name {config.project_name}"
        run_command(logger, command)

        command = f"dotnet sln add {config.project_name}"
        run_command(logger, command)

    except FileNotFoundError as e:
        click.echo(f"[ERROR] Invalid log path: {e}")
        traceback.print_exc()
    except NotADirectoryError as e:
        click.echo(f"[ERROR] Log path is not a directory: {e}")
        traceback.print_exc()
    except Exception as e:
        click.echo(f"[ERROR] Unexpected error occurred: {e}")
        traceback.print_exc()

@cli.command()
@click.option("--root-path", required=True)
@click.option("--solution-name", required=True)
@click.option("--project-name", required=True)
@click.option("--log-path", required=True)
def remove_csharp_project(**kwargs):
    try:
        config = ProjectConfig(**kwargs)
        logger = Logger(config.log_path)

        project_path = Path(config.root_path) / f"{config.project_name}"
        if not project_path.exists():
            raise Exception(f"Cannot found '{config.project_name}' project.")
        
        solution_path = Path(config.root_path) / f"{config.solution_name}.sln"
        if not solution_path.exists():
            raise Exception(f"Cannot found Visual Studio solution : '{config.solution_name}'")
        
        command = f"dotnet sln remove {config.project_name}"
        run_command(logger, command)

    except FileNotFoundError as e:
        click.echo(f"[ERROR] Invalid log path: {e}")
        traceback.print_exc()
    except NotADirectoryError as e:
        click.echo(f"[ERROR] Log path is not a directory: {e}")
        traceback.print_exc()
    except Exception as e:
        click.echo(f"[ERROR] Unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    cli()