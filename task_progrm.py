# ============================================
# WEEK 1: CLI TASK MANAGER
# SkillAudit.ai Python Development Internship
# ============================================

from manager import TaskManager


class TaskCLI:
    """Command-line interface for Task Manager"""

    def __init__(self):
        """Initialize the CLI with a TaskManager instance"""
        self.manager = TaskManager()

    def display_menu(self):
        """Show the main menu options to the user"""
        print("\n" + "=" * 40)
        print("📋 TASK MANAGER")
        print("=" * 40)
        print("1. Add Task")
        print("2. Add Priority Task")
        print("3. List All Tasks")
        print("4. Complete Task")
        print("5. Delete Task")
        print("6. Exit")
        print("=" * 40)

    def run(self):
        """Main loop - keeps showing menu until user exits"""
        while True:
            self.display_menu()
            choice = input("\n👉 Choose an option: ").strip()

            # Route to appropriate method based on user choice
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.add_priority_task()
            elif choice == "3":
                self.list_tasks()
            elif choice == "4":
                self.complete_task()
            elif choice == "5":
                self.delete_task()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")

    def add_task(self):
        """Add a standard task (no priority)"""
        title = input("📌 Task title: ").strip()
        if not title:
            print("❌ Title cannot be empty.")
            return

        description = input("📝 Description (optional): ").strip()
        task = self.manager.add_task(title, description)
        print(f"✅ Task added with ID: {task.id}")

    def add_priority_task(self):
        """Add a task with priority level (high/medium/low)"""
        title = input("📌 Task title: ").strip()
        if not title:
            print("❌ Title cannot be empty.")
            return

        # Get priority with default value 'medium'
        priority = input("🔴 Priority (high/medium/low) [medium]: ").strip().lower()
        if priority not in ["high", "medium", "low"]:
            priority = "medium"

        description = input("📝 Description (optional): ").strip()
        task = self.manager.add_priority_task(title, priority, description)
        print(f"✅ Priority task added with ID: {task.id}")

    def list_tasks(self):
        """Display all tasks (both completed and pending)"""
        tasks = self.manager.list_tasks(show_all=True)

        if not tasks:
            print("📭 No tasks found.")
            return

        print("\n📋 Your Tasks:")
        print("-" * 40)
        for task in tasks:
            print(task)
        print("-" * 40)

    def complete_task(self):
        """Mark a task as completed by its ID"""
        task_id = self.get_task_id("complete")
        if task_id is None:
            return

        if self.manager.complete_task(task_id):
            print(f"✅ Task {task_id} marked as completed!")
        else:
            print(f"❌ Task {task_id} not found.")

    def delete_task(self):
        """Delete a task by its ID"""
        task_id = self.get_task_id("delete")
        if task_id is None:
            return

        if self.manager.delete_task(task_id):
            print(f"🗑️  Task {task_id} deleted.")
        else:
            print(f"❌ Task {task_id} not found.")

    def get_task_id(self, action):
        """Helper method to get and validate a task ID from user"""
        try:
            return int(input(f"🔢 Enter task ID to {action}: ").strip())
        except ValueError:
            print("❌ Please enter a valid number.")
            return None


# ============================================
# PROGRAM STARTS HERE
# ============================================
if __name__ == "__main__":
    app = TaskCLI()
    app.run()
