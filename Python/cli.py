import click
import traceback

from config import ProjectConfig
from logger import Logger

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