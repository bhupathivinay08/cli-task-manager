from datetime import datetime
import json

class Task:
    """Base task model"""
    def __init__(self, task_id, title, description="", completed=False, created_at=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "type": "task"
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Task from dictionary"""
        return cls(
            data["id"],
            data["title"],
            data["description"],
            data["completed"],
            data["created_at"]
        )
    
    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.id}. {self.title}"


class PriorityTask(Task):
    """Priority task that inherits from Task"""
    def __init__(self, task_id, title, priority="medium", description="", completed=False, created_at=None):
        super().__init__(task_id, title, description, completed, created_at)
        self.priority = priority
    
    def to_dict(self):
        """Override to include priority"""
        data = super().to_dict()
        data["priority"] = self.priority
        data["type"] = "priority_task"
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create PriorityTask from dictionary"""
        return cls(
            data["id"],
            data["title"],
            data["priority"],
            data["description"],
            data["completed"],
            data["created_at"]
        )
    
    def __str__(self):
        status = "✓" if self.completed else "✗"
        priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        icon = priority_icons.get(self.priority, "⚪")
        return f"[{status}] {self.id}. {icon} {self.title} (Priority: {self.priority})"