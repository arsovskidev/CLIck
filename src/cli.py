import click
from typing import Optional
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage import TaskStorage
from models import Task, Priority
from utils import format_task_list, parse_date


@click.group()
@click.version_option(version="0.1.0", prog_name="click")
def cli() -> None:
    pass


@cli.command()
@click.argument("description")
@click.option("--due", help="Due date (e.g., tomorrow, 2024-01-15)")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    default="medium",
    help="Task priority",
)
@click.option("--tags", help="Comma-separated tags")
def add(
    description: str, due: Optional[str], priority: str, tags: Optional[str]
) -> None:
    """Add a new task"""
    storage = TaskStorage()

    due_date = parse_date(due) if due else None
    task_tags = [tag.strip() for tag in tags.split(",")] if tags else []

    task = Task(
        description=description,
        due_date=due_date,
        priority=Priority(priority),
        tags=task_tags,
    )

    task_id = storage.add_task(task)
    click.echo(f"Task added successfully with ID: {task_id}")


@cli.command()
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    help="Filter by priority",
)
@click.option("--due", help="Filter by due date")
@click.option("--tags", help="Filter by tags (comma-separated)")
@click.option("--completed", is_flag=True, help="Show completed tasks")
def list(
    priority: Optional[str], due: Optional[str], tags: Optional[str], completed: bool
) -> None:
    """List tasks"""
    storage = TaskStorage()
    tasks = storage.get_tasks(
        priority=Priority(priority) if priority else None,
        due_date=parse_date(due) if due else None,
        tags=[tag.strip() for tag in tags.split(",")] if tags else None,
        completed=completed,
    )

    if not tasks:
        click.echo("No tasks found.")
        return

    format_task_list(tasks)


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Mark a task as complete"""
    storage = TaskStorage()
    if storage.complete_task(task_id):
        click.echo(f"Task {task_id} marked as completed!")
    else:
        click.echo(f"Task {task_id} not found.")


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id: int) -> None:
    storage = TaskStorage()
    if storage.delete_task(task_id):
        click.echo(f"Task {task_id} deleted successfully!")
    else:
        click.echo(f"Task {task_id} not found.")


if __name__ == "__main__":
    cli()
