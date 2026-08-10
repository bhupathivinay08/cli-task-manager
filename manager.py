import json
import os
from models import Task, PriorityTask

class TaskManager:
    """Manages tasks with JSON persistence"""
    
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load()
    
    def load(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = []
                    for task_data in data:
                        if task_data["type"] == "priority_task":
                            task = PriorityTask.from_dict(task_data)
                        else:
                            task = Task.from_dict(task_data)
                        self.tasks.append(task)
                        if task.id >= self.next_id:
                            self.next_id = task.id + 1
            except (json.JSONDecodeError, KeyError):
                print("⚠️  Error loading tasks. Starting fresh.")
                self.tasks = []
                self.next_id = 1
    
    def save(self):
        """Save tasks to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
        except Exception as e:
            print(f"❌ Error saving tasks: {e}")
    
    def add_task(self, title, description=""):
        """Add a standard task"""
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        self.save()
        return task
    
    def add_priority_task(self, title, priority="medium", description=""):
        """Add a priority task"""
        task = PriorityTask(self.next_id, title, priority, description)
        self.tasks.append(task)
        self.next_id += 1
        self.save()
        return task
    
    def list_tasks(self, show_all=False):
        """Return list of tasks"""
        if show_all:
            return self.tasks
        return [t for t in self.tasks if not t.completed]
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        task = self.get_task(task_id)
        if task:
            task.completed = True
            self.save()
            return True
        return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save()
            return True
        return False
    
    def get_task(self, task_id):
        """Find a task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None