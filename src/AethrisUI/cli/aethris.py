import click
import os
from pathlib import Path

@click.group()
def cli():
    """AethrisUI CLI tool"""
    pass

@cli.command()
@click.argument('name')
def create_project(name):
    """Create a new AethrisUI project"""
    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)
    
    # Create project structure
    (project_dir / "src").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)
    
    # Create initial files
    template_dir = Path(__file__).parent / "templates"
    # Copy templates...

@cli.command()
def dev():
    """Start development server"""
    pass 