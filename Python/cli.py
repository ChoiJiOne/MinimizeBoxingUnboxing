import click
import logging

from config import ProjectConfig
from logging import setup_global_logging

@click.group()
def cli():
    pass

@cli.command()
@click.option("--root-path", required=True)
@click.option("--solution-name", required=True)
@click.option("--project-name", required=True)
@click.option("--log-path", required=True)
def create_csharp_project(**kwargs):
    config = ProjectConfig(**kwargs)
    setup_global_logging(config.log_path)
    
if __name__ == "__main__":
    cli()