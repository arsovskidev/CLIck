"""
Data models for CLIck task manager
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    """Task priority levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Task data model"""
    description: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    id: Optional[int] = None
    
    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tags is None:
            self.tags = []

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.due_date is None or self.completed:
            return False
        return datetime.now() > self.due_date

    def to_dict(self) -> dict:
        """Convert task to dictionary for storage"""
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority.value,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else datetime.now().isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": ",".join(self.tags) if self.tags else "",
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task from dictionary"""
        return cls(
            id=data["id"],
            description=data["description"],
            priority=Priority(data["priority"]),
            completed=bool(data["completed"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            due_date=(
                datetime.fromisoformat(data["due_date"]) if data["due_date"] else None
            ),
            tags=data["tags"].split(",") if data["tags"] else [],
        )
