from datetime import datetime, timedelta
from typing import List, Optional
import re

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from rich.panel import Panel
from rich.align import Align

from .models import Task, Priority


console = Console()


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None

    date_str = date_str.lower().strip()
    now = datetime.now()

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

    days_match = re.match(r"in (\d+) days?", date_str)
    if days_match:
        days = int(days_match.group(1))
        return (now + timedelta(days=days)).replace(
            hour=23, minute=59, second=59, microsecond=0
        )

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, "%m/%d/%Y").replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, "%d-%m-%Y").replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    except ValueError:
        pass

    return None


def format_task_list(tasks: List[Task]) -> None:
    if not tasks:
        empty_panel = Panel(
            Align.center("[dim white]No tasks found[/dim white]"),
            title="[bold white]📋 Tasks[/bold white]",
            border_style="white",
            box=box.ROUNDED,
        )
        console.print(empty_panel)
        return

    table = Table(
        show_header=True,
        header_style="bold white",
        border_style="white",
        box=box.ROUNDED,
        title="[bold white]📋 Your Tasks[/bold white]",
        title_style="bold white",
    )
    table.add_column("ID", style="dim white", width=4, justify="center")
    table.add_column("Status", width=10, justify="center")
    table.add_column("Priority", width=10, justify="center")
    table.add_column("Description", min_width=25, style="white")
    table.add_column("Due Date", width=12, justify="center")
    table.add_column("Tags", width=20, style="dim white")

    for task in tasks:
        if task.completed:
            status = Text("✅ Done", style="white")
        elif task.is_overdue:
            status = Text("⚠️ Late", style="bright_white")
        else:
            status = Text("📝 Todo", style="dim white")

        priority_colors = {
            Priority.HIGH: "bright_white",
            Priority.MEDIUM: "white",
            Priority.LOW: "dim white",
        }
        priority_icons = {
            Priority.HIGH: "🔥",
            Priority.MEDIUM: "⭐",
            Priority.LOW: "💙",
        }
        priority_text = Text(
            f"{priority_icons[task.priority]} {task.priority.value.title()}",
            style=priority_colors[task.priority],
        )

        due_date_text = ""
        if task.due_date:
            if task.due_date.date() == datetime.now().date():
                due_date_text = Text("📅 Today", style="bright_white")
            elif task.due_date.date() == (datetime.now() + timedelta(days=1)).date():
                due_date_text = Text("📅 Tomorrow", style="white")
            else:
                due_date_text = Text(
                    f"📅 {task.due_date.strftime('%m-%d')}", style="dim white"
                )
        else:
            due_date_text = Text("-", style="dim")

        if task.tags:
            tags_text = Text(f"🏷️ {', '.join(task.tags)}", style="white")
        else:
            tags_text = Text("-", style="dim")

        table.add_row(
            str(task.id),
            status,
            priority_text,
            task.description,
            due_date_text,
            tags_text,
        )

    console.print(table)

    summary_text = f"[bold white]Total: {len(tasks)} tasks[/bold white]"
    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = len(tasks) - completed_count

    if completed_count > 0 or pending_count > 0:
        summary_text += f"\n[white]✅ Completed: {completed_count}[/white] | [dim white]📝 Pending: {pending_count}[/dim white]"

    summary_panel = Panel(
        Align.center(summary_text), border_style="white", box=box.ROUNDED
    )
    console.print(summary_panel)


def format_priority_color(priority: Priority) -> str:
    colors = {Priority.HIGH: "red", Priority.MEDIUM: "yellow", Priority.LOW: "green"}
    return colors.get(priority, "white")


def validate_priority(priority_str: str) -> bool:
    try:
        Priority(priority_str.lower())
        return True
    except ValueError:
        return False


def print_success_message(message: str) -> None:
    panel = Panel(
        f"[bold white]✅ {message}[/bold white]", border_style="white", box=box.ROUNDED
    )
    console.print(panel)


def print_error_message(message: str) -> None:
    panel = Panel(
        f"[bold white]❌ {message}[/bold white]", border_style="white", box=box.ROUNDED
    )
    console.print(panel)


def print_info_message(message: str) -> None:
    panel = Panel(
        f"[bold white]ℹ️ {message}[/bold white]", border_style="white", box=box.ROUNDED
    )
    console.print(panel)
