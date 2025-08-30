import sqlite3
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from models import Task, Priority


class TaskStorage:

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            home_dir = Path.home()
            self.db_path = home_dir / ".click_tasks.db"
        else:
            self.db_path = Path(db_path)

        self._init_database()

    def _init_database(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT NOT NULL DEFAULT 'medium',
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    due_date TEXT,
                    tags TEXT
                )
            """
            )
            conn.commit()

    def add_task(self, task: Task) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO tasks (description, priority, completed, created_at, due_date, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    task.description,
                    task.priority.value,
                    task.completed,
                    (
                        task.created_at.isoformat()
                        if task.created_at
                        else datetime.now().isoformat()
                    ),
                    task.due_date.isoformat() if task.due_date else None,
                    ",".join(task.tags) if task.tags else "",
                ),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def get_tasks(
        self,
        priority: Optional[Priority] = None,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        completed: bool = False,
    ) -> List[Task]:
        query = "SELECT * FROM tasks WHERE completed = ?"
        params: List[str] = [str(int(completed))]

        if priority:
            query += " AND priority = ?"
            params.append(priority.value)

        if due_date:
            query += " AND date(due_date) = date(?)"
            params.append(due_date.isoformat())

        if tags:
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
            query += " AND (" + " OR ".join(tag_conditions) + ")"

        query += " ORDER BY created_at DESC"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

            tasks = []
            for row in rows:
                task_data = dict(row)
                tasks.append(Task.from_dict(task_data))

            return tasks

    def complete_task(self, task_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if row:
                return Task.from_dict(dict(row))
            return None
