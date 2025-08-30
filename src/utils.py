from datetime import datetime, timedelta
from typing import List, Optional
import re

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from .models import Task, Priority


console = Console()


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None

    date_str = date_str.lower().strip()
    now = datetime.now()

    # Handle relative dates
    if date_str == "today":
        return now.replace(hour=23, minute=59, second=59, microsecond=0)
    elif date_str == "tomorrow":
        return (now + timedelta(days=1)).replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    elif date_str == "yesterday":
        return (now - timedelta(days=1)).replace(
            hour=23, minute=59, second=59, microsecond=0
        )

    # Handle "in X days" format
    days_match = re.match(r"in (\d+) days?", date_str)
    if days_match:
        days = int(days_match.group(1))
        return (now + timedelta(days=days)).replace(
            hour=23, minute=59, second=59, microsecond=0
        )

    # Handle ISO date format (YYYY-MM-DD)
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    except ValueError:
        pass

    # Handle MM/DD/YYYY format
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    except ValueError:
        pass

    # Handle DD-MM-YYYY format
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    except ValueError:
        pass

    return None


def format_task_list(tasks: List[Task]) -> None:
    if not tasks:
        console.print("No tasks found", style="dim")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Status", width=8)
    table.add_column("Priority", width=8)
    table.add_column("Description", min_width=20)
    table.add_column("Due Date", width=12)
    table.add_column("Tags", width=15)

    for task in tasks:
        # Status column
        if task.completed:
            status = Text("Done", style="green")
        elif task.is_overdue:
            status = Text("Late", style="red")
        else:
            status = Text("Todo", style="yellow")

        # Priority column with colors
        priority_colors = {
            Priority.HIGH: "red",
            Priority.MEDIUM: "yellow",
            Priority.LOW: "green",
        }
        priority_text = Text(
            task.priority.value.title(), style=priority_colors[task.priority]
        )

        # Due date formatting
        due_date_str = ""
        if task.due_date:
            if task.due_date.date() == datetime.now().date():
                due_date_str = "Today"
            elif task.due_date.date() == (datetime.now() + timedelta(days=1)).date():
                due_date_str = "Tomorrow"
            else:
                due_date_str = task.due_date.strftime("%Y-%m-%d")

        # Tags formatting
        tags_str = ", ".join(task.tags) if task.tags else ""

        table.add_row(
            str(task.id),
            status,
            priority_text,
            task.description,
            due_date_str,
            tags_str,
        )

    console.print(table)
    console.print(f"\nTotal: {len(tasks)} tasks")


def format_priority_color(priority: Priority) -> str:
    colors = {Priority.HIGH: "red", Priority.MEDIUM: "yellow", Priority.LOW: "green"}
    return colors.get(priority, "white")


def validate_priority(priority_str: str) -> bool:
    try:
        Priority(priority_str.lower())
        return True
    except ValueError:
        return False
