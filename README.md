# Multi-Agent To-Do MCP Tool

A robust, Python-based to-do management system designed for multi-agent environments. It supports isolated storage, task artifacts (URLs, notes, files), hierarchical subtasks, and advanced date filtering. Integrated with the Model Context Protocol (MCP) and featuring a powerful CLI.

## Features

-   **Multi-Agent Isolation**: Each agent operates within its own dedicated SQLite namespace.
-   **Rich Task Metadata**: Support for priority (low, medium, high, urgent), status tracking, and hierarchical subtasks.
-   **Task Collections**: Organize tasks into logical groups (e.g., "Work", "Personal").
-   **Task Artifacts**: Attach URLs, text notes, and file paths with optional MIME type tracking.
-   **Progress Tracking**: Add, edit, or delete timestamped updates/comments on tasks.
-   **Intelligent Filtering**: Built-in reporting for tasks due today, past due, or within custom date ranges.
-   **Dual Interface**: Complete feature parity between the Command Line Interface (CLI) and MCP tools.
-   **Normalized Dates**: Robust date comparison logic that correctly handles both date-only strings and full ISO datetimes.

## Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd to-do-mcp
    ```

2.  **Initialize the Environment**:
    Run the `install` command via CLI to set up the default configuration and database directory:
    ```bash
    python3 todo_cli.py install
    ```
    This creates a local `.env` file (or `/etc/mcp/basic_todo/.env` if permissions allow) and ensures the database root directory exists.

3.  **Install Dependencies**:
    ```bash
    pip install mcp rich python-dotenv
    ```

## Configuration

The tool uses environment variables for configuration, loaded from a `.env` file.

-   `AGENTS`: A comma-separated list of authorized agent names (e.g., `alice,bob,dave`).
-   `DB_FILE_ROOT`: The absolute path where agent databases will be stored.

### Configuration Tiering
1.  **System Level**: `/etc/mcp/basic_todo/.env` (Highest priority)
2.  **Local Level**: `./.env` (Current directory)

## CLI Usage

The `todo_cli.py` script provides a full-featured interface. Most commands require the `--agent` flag.

### Global Options
-   `--agent <name>`: The agent keyword to resolve the database namespace.
-   `--format {plain,json,markdown}`: Output formatting (default: `plain`).

### Commands
-   `list-agents`: List all authorized agents.
-   `install`: Initialize the environment.
-   `create [--title] [--desc] [--due] [--priority] [--subtask-of] [--collection]`: Create a task.
-   `update <id> [--title] [--desc] [--due] [--status] [--priority] [--collection]`: Update a task.
-   `delete <id>`: Delete a task.
-   `get <id>`: Retrieve full task details (including updates, artifacts, and subtasks).
-   `add-update <id> <comment>`: Add a new comment to a task.
-   `update-update <id> <comment>`: Edit an existing comment.
-   `delete-update <id>`: Delete a comment.
-   `add-artifact <id> <content> [--type {URL,Content,File}] [--mimetype]`: Add an artifact.
-   `delete-artifact <id>`: Remove an artifact.
-   `collections {list,add,delete}`: Manage task collections.
-   `report [--today] [--past-due] [--next-week] [--start] [--end] [--collection]`: Generate task reports.

### Examples
```bash
# Get tasks due in a custom range
python3 todo_cli.py --agent dave report --start 2026-05-01 --end 2026-05-31 --format markdown

# Update an existing comment
python3 todo_cli.py --agent dave update-update 12 "Revised progress report."
```

## MCP Integration

Expose your to-do list to LLMs using the `todo_mcp.py` script.

### Available Tools
-   `list_todo_agents`: Lists all authorized agents.
-   `create_todo_task`, `update_todo_task`, `delete_todo_task`, `get_todo_task`
-   `add_todo_update`, `update_todo_update`, `delete_todo_update`
-   `add_todo_artifact`, `delete_todo_artifact`
-   `list_todo_collections`, `create_todo_collection`, `delete_todo_collection`
-   `get_urgent_tasks`, `get_tasks_due_today_tool`, `get_tasks_past_due_tool`, `get_tasks_due_next_week_tool`
-   `get_tasks_by_date_range_tool`: Advanced filtering by custom dates.

## Testing

Run the comprehensive test suite using `pytest`:
```bash
PYTHONPATH=. pytest tests/
```
The suite covers all library functions, CLI commands, and MCP tools, ensuring 100% feature reliability.
