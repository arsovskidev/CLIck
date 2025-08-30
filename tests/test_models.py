"""
Tests for CLIck models
"""

import pytest
from datetime import datetime
from src.models import Task, Priority


def test_task_creation():
    """Test basic task creation"""
    task = Task(description="Test task")
    assert task.description == "Test task"
    assert task.priority == Priority.MEDIUM
    assert task.completed is False
    assert task.tags == []
    assert isinstance(task.created_at, datetime)


def test_task_with_priority():
    """Test task creation with priority"""
    task = Task(description="High priority task", priority=Priority.HIGH)
    assert task.priority == Priority.HIGH


def test_task_is_overdue():
    """Test overdue task detection"""
    past_date = datetime(2020, 1, 1)
    task = Task(description="Overdue task", due_date=past_date)
    assert task.is_overdue is True

    # Completed tasks are never overdue
    task.completed = True
    assert task.is_overdue is False


def test_task_to_dict():
    """Test task serialization to dictionary"""
    task = Task(
        description="Test task", priority=Priority.HIGH, tags=["work", "urgent"]
    )
    task.id = 1

    data = task.to_dict()
    assert data["description"] == "Test task"
    assert data["priority"] == "high"
    assert data["tags"] == "work,urgent"


def test_task_from_dict():
    """Test task deserialization from dictionary"""
    data = {
        "id": 1,
        "description": "Test task",
        "priority": "high",
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "due_date": None,
        "tags": "work,urgent",
    }

    task = Task.from_dict(data)
    assert task.description == "Test task"
    assert task.priority == Priority.HIGH
    assert task.tags == ["work", "urgent"]
