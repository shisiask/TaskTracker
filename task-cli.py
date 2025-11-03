#!/usr/bin/env python3
"""
Task Tracker CLI - A simple command-line task management application
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class TaskTracker:
    """Manages tasks stored in a JSON file"""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.filepath = Path(filename)
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        """Load tasks from JSON file or create empty list if file doesn't exist"""
        if not self.filepath.exists():
            return []

        try:
            with open(self.filepath, 'r') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.filename}. Starting with empty task list.")
            return []
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []

    def _save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
            sys.exit(1)

    def _get_next_id(self):
        """Get the next available task ID"""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1

    def _find_task(self, task_id):
        """Find a task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def add(self, description):
        """Add a new task"""
        if not description or not description.strip():
            print("Error: Task description cannot be empty")
            sys.exit(1)

        task_id = self._get_next_id()
        now = datetime.now().isoformat()

        task = {
            'id': task_id,
            'description': description,
            'status': 'todo',
            'createdAt': now,
            'updatedAt': now
        }

        self.tasks.append(task)
        self._save_tasks()
        print(f"Task added successfully (ID: {task_id})")

    def update(self, task_id, description):
        """Update a task's description"""
        if not description or not description.strip():
            print("Error: Task description cannot be empty")
            sys.exit(1)

        task = self._find_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found")
            sys.exit(1)

        task['description'] = description
        task['updatedAt'] = datetime.now().isoformat()
        self._save_tasks()
        print(f"Task {task_id} updated successfully")

    def delete(self, task_id):
        """Delete a task"""
        task = self._find_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found")
            sys.exit(1)

        self.tasks.remove(task)
        self._save_tasks()
        print(f"Task {task_id} deleted successfully")

    def mark_in_progress(self, task_id):
        """Mark a task as in progress"""
        task = self._find_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found")
            sys.exit(1)

        task['status'] = 'in-progress'
        task['updatedAt'] = datetime.now().isoformat()
        self._save_tasks()
        print(f"Task {task_id} marked as in progress")

    def mark_done(self, task_id):
        """Mark a task as done"""
        task = self._find_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found")
            sys.exit(1)

        task['status'] = 'done'
        task['updatedAt'] = datetime.now().isoformat()
        self._save_tasks()
        print(f"Task {task_id} marked as done")

    def list_tasks(self, status_filter=None):
        """List tasks, optionally filtered by status"""
        filtered_tasks = self.tasks

        if status_filter:
            valid_statuses = ['todo', 'in-progress', 'done']
            if status_filter not in valid_statuses:
                print(f"Error: Invalid status '{status_filter}'. Valid statuses: {', '.join(valid_statuses)}")
                sys.exit(1)
            filtered_tasks = [task for task in self.tasks if task['status'] == status_filter]

        if not filtered_tasks:
            if status_filter:
                print(f"No tasks with status '{status_filter}'")
            else:
                print("No tasks found")
            return

        # Print header
        print("\n" + "=" * 80)
        if status_filter:
            print(f"Tasks - Status: {status_filter}")
        else:
            print("All Tasks")
        print("=" * 80)

        for task in filtered_tasks:
            status_display = f"[{task['status'].upper()}]"
            print(f"\nID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {status_display}")
            print(f"Created: {self._format_datetime(task['createdAt'])}")
            print(f"Updated: {self._format_datetime(task['updatedAt'])}")
            print("-" * 80)

    def _format_datetime(self, iso_string):
        """Format ISO datetime string for display"""
        try:
            dt = datetime.fromisoformat(iso_string)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return iso_string


def print_usage():
    """Print usage information"""
    usage = """
Task Tracker CLI - Usage:

  task-cli add <description>              Add a new task
  task-cli update <id> <description>      Update a task's description
  task-cli delete <id>                    Delete a task
  task-cli mark-in-progress <id>          Mark a task as in progress
  task-cli mark-done <id>                 Mark a task as done
  task-cli list                           List all tasks
  task-cli list todo                      List all todo tasks
  task-cli list in-progress               List all in-progress tasks
  task-cli list done                      List all done tasks

Examples:
  task-cli add "Buy groceries"
  task-cli update 1 "Buy groceries and cook dinner"
  task-cli mark-in-progress 1
  task-cli mark-done 1
  task-cli delete 1
  task-cli list
  task-cli list done
"""
    print(usage)


def main():
    """Main entry point for the CLI"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]
    tracker = TaskTracker()

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Error: Missing task description")
                print("Usage: task-cli add <description>")
                sys.exit(1)
            description = " ".join(sys.argv[2:])
            tracker.add(description)

        elif command == "update":
            if len(sys.argv) < 4:
                print("Error: Missing task ID or description")
                print("Usage: task-cli update <id> <description>")
                sys.exit(1)
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: Invalid task ID '{sys.argv[2]}'. ID must be a number")
                sys.exit(1)
            description = " ".join(sys.argv[3:])
            tracker.update(task_id, description)

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Missing task ID")
                print("Usage: task-cli delete <id>")
                sys.exit(1)
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: Invalid task ID '{sys.argv[2]}'. ID must be a number")
                sys.exit(1)
            tracker.delete(task_id)

        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Error: Missing task ID")
                print("Usage: task-cli mark-in-progress <id>")
                sys.exit(1)
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: Invalid task ID '{sys.argv[2]}'. ID must be a number")
                sys.exit(1)
            tracker.mark_in_progress(task_id)

        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Error: Missing task ID")
                print("Usage: task-cli mark-done <id>")
                sys.exit(1)
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: Invalid task ID '{sys.argv[2]}'. ID must be a number")
                sys.exit(1)
            tracker.mark_done(task_id)

        elif command == "list":
            status_filter = None
            if len(sys.argv) >= 3:
                status_filter = sys.argv[2]
            tracker.list_tasks(status_filter)

        else:
            print(f"Error: Unknown command '{command}'")
            print_usage()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
