import click
import traceback
import subprocess

from config import ProjectConfig
from logger import Logger
from command_utils import run_command

@click.group()
def cli():
    pass

@cli.command()
@click.option("--root-path", required=True)
@click.option("--solution-name", required=True)
@click.option("--project-name", required=True)
@click.option("--log-path", required=True)
def create_csharp_project(**kwargs):
    try:
        config = ProjectConfig(**kwargs)
        logger = Logger(config.log_path)

        command = f"dotnet new console --language \"C#\" --name {config.project_name}"
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