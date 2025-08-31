import click
from typing import Optional
from datetime import datetime

from .storage import TaskStorage
from .models import Task, Priority
from .utils import format_task_list, parse_date, print_success_message, print_error_message


@click.command()
@click.argument("description")
@click.option("--due", help="Due date (e.g., tomorrow, 2024-01-15)")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    default="medium",
    help="Task priority",
)
@click.option("--tags", help="Comma-separated tags")
def add_task(
    description: str, due: Optional[str], priority: str, tags: Optional[str]
) -> None:
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
    print_success_message(f"Task added successfully with ID: {task_id}")

    tasks = storage.get_tasks()
    format_task_list(tasks)


@click.command("list")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    help="Filter by priority",
)
@click.option("--due", help="Filter by due date")
@click.option("--tags", help="Filter by tags (comma-separated)")
@click.option("--completed", is_flag=True, help="Show completed tasks")
def list_tasks(
    priority: Optional[str], due: Optional[str], tags: Optional[str], completed: bool
) -> None:
    storage = TaskStorage()
    tasks = storage.get_tasks(
        priority=Priority(priority) if priority else None,
        due_date=parse_date(due) if due else None,
        tags=[tag.strip() for tag in tags.split(",")] if tags else None,
        completed=completed,
    )

    format_task_list(tasks)


@click.command()
@click.argument("task_id", type=int)
def complete_task(task_id: int) -> None:
    storage = TaskStorage()
    if storage.complete_task(task_id):
        print_success_message(f"Task {task_id} marked as completed!")
    else:
        print_error_message(f"Task {task_id} not found.")

    tasks = storage.get_tasks()
    format_task_list(tasks)


@click.command()
@click.argument("task_id", type=int)
def delete_task(task_id: int) -> None:
    storage = TaskStorage()
    if storage.delete_task(task_id):
        print_success_message(f"Task {task_id} deleted successfully!")
    else:
        print_error_message(f"Task {task_id} not found.")

    tasks = storage.get_tasks()
    format_task_list(tasks)


@click.command("complete-all")
@click.confirmation_option(prompt="Are you sure you want to complete all tasks?")
def complete_all_tasks() -> None:
    storage = TaskStorage()
    count = storage.complete_all_tasks()
    print_success_message(f"Completed {count} tasks!")

    tasks = storage.get_tasks()
    format_task_list(tasks)


@click.command("delete-all")
@click.confirmation_option(prompt="Are you sure you want to delete all tasks?")
def delete_all_tasks() -> None:
    storage = TaskStorage()
    count = storage.delete_all_tasks()
    print_success_message(f"Deleted {count} tasks!")

    tasks = storage.get_tasks()
    format_task_list(tasks)
