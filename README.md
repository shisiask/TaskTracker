# Task Tracker CLI

A simple command-line interface (CLI) application for tracking and managing your tasks. This project helps you organize what you need to do, what you're currently working on, and what you've completed.

**Project URL:** https://roadmap.sh/projects/task-tracker

## Features

- **Add tasks** - Create new tasks with descriptions
- **Update tasks** - Modify existing task descriptions
- **Delete tasks** - Remove tasks you no longer need
- **Track progress** - Mark tasks as todo, in-progress, or done
- **List tasks** - View all tasks or filter by status
- **Persistent storage** - Tasks are saved in a JSON file

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd TaskTracker
```

2. Make the CLI executable:
```bash
chmod +x task-cli
```

3. (Optional) Add to your PATH for global access:
```bash
# Add this line to your ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/TaskTracker"
```

## Usage

### Basic Commands

#### Add a new task
```bash
./task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)
```

#### Update a task
```bash
./task-cli update 1 "Buy groceries and cook dinner"
# Output: Task 1 updated successfully
```

#### Delete a task
```bash
./task-cli delete 1
# Output: Task 1 deleted successfully
```

#### Mark a task as in progress
```bash
./task-cli mark-in-progress 1
# Output: Task 1 marked as in progress
```

#### Mark a task as done
```bash
./task-cli mark-done 1
# Output: Task 1 marked as done
```

### Listing Tasks

#### List all tasks
```bash
./task-cli list
```

#### List tasks by status
```bash
# List only todo tasks
./task-cli list todo

# List only in-progress tasks
./task-cli list in-progress

# List only completed tasks
./task-cli list done
```

## Task Properties

Each task in the system has the following properties:

- **id**: A unique identifier for the task (auto-generated)
- **description**: A short description of the task
- **status**: The current status of the task (`todo`, `in-progress`, or `done`)
- **createdAt**: The date and time when the task was created (ISO format)
- **updatedAt**: The date and time when the task was last updated (ISO format)

## Data Storage

Tasks are stored in a `tasks.json` file in the current directory. The file is automatically created when you add your first task.

Example `tasks.json` structure:
```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "status": "todo",
    "createdAt": "2025-11-03T10:30:00.000000",
    "updatedAt": "2025-11-03T10:30:00.000000"
  },
  {
    "id": 2,
    "description": "Write documentation",
    "status": "in-progress",
    "createdAt": "2025-11-03T11:00:00.000000",
    "updatedAt": "2025-11-03T11:15:00.000000"
  }
]
```

## Error Handling

The application includes comprehensive error handling:

- **Invalid task IDs**: Non-numeric or non-existent task IDs are rejected with clear error messages
- **Empty descriptions**: Tasks must have non-empty descriptions
- **Invalid commands**: Unknown commands display the usage information
- **Invalid status filters**: Only valid status values are accepted (todo, in-progress, done)
- **JSON file errors**: Corrupted JSON files are handled gracefully

## Examples

Here's a typical workflow:

```bash
# Add some tasks
./task-cli add "Prepare presentation for meeting"
./task-cli add "Review pull requests"
./task-cli add "Update project documentation"

# Start working on a task
./task-cli mark-in-progress 1

# Complete a task
./task-cli mark-done 2

# Update a task description
./task-cli update 3 "Update project documentation and README"

# View all in-progress tasks
./task-cli list in-progress

# View all completed tasks
./task-cli list done

# Delete a task
./task-cli delete 1
```

## Project Structure

```
TaskTracker/
├── task-cli.py       # Main Python application
├── task-cli          # Bash wrapper script for easy execution
├── tasks.json        # Task data storage (created automatically)
└── README.md         # This file
```

## Implementation Details

- **Language**: Python 3
- **Storage**: JSON file using native `json` module
- **Date/Time**: ISO 8601 format using `datetime` module
- **File I/O**: Native `pathlib` and built-in file operations
- **CLI Arguments**: Native `sys.argv` parsing
- **No external dependencies**: Uses only Python standard library

## Testing

The application has been tested with:

- Adding, updating, and deleting tasks
- Marking tasks with different statuses
- Listing tasks with and without status filters
- Various error conditions (invalid IDs, missing arguments, etc.)
- Edge cases (empty task list, corrupted JSON, etc.)

## License

This project is open source and available for educational purposes.

## Acknowledgments

This project is based on the [Task Tracker](https://roadmap.sh/projects/task-tracker) project from [roadmap.sh](https://roadmap.sh/)
