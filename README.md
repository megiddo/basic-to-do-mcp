# Multi-Agent To-Do MCP Tool

A Python-based to-do management system that supports multiple agents, isolated storage, and task artifacts. This tool integrates with the Model Context Protocol (MCP) and provides a command-line interface.

## Features

- Multi-Agent Support: Each agent has their own isolated SQLite database identified by a plaintext keyword.
- Task Management: Create, update, delete, and retrieve tasks.
- Task Artifacts: Attach URLs, text notes, and file paths to tasks.
- Detailed Tracking: Title, description, due dates, priority levels, and status tracking.
- Task Updates: Add comments or progress updates to specific tasks.
- Subtasks: Support for hierarchical task relationships.
- Urgency Reporting: View tasks ordered by priority and due date.
- Multiple Output Formats: CLI supports plain text, JSON, and Markdown.
- MCP Integration: Native support for Model Context Protocol tools.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install mcp rich
   ```

## CLI Usage

The `todo_cli.py` script provides a command-line interface. Every command requires an agent name.

### General Options
- `--agent AGENT_NAME`: Required. The name or keyword for the agent's isolated namespace.
- `--format {plain,json,markdown}`: Specify the output format (default: plain).

### Commands
- `create`: Create a new task.
- `update`: Update an existing task.
- `delete`: Delete a task.
- `get`: Get task details (includes updates, subtasks, and artifacts).
- `add-update`: Add a comment to a task.
- `add-artifact`: Add an artifact (URL, Content, or File) to a task.
- `report`: Get tasks ordered by urgency.

### Examples

Add a URL artifact:
```bash
python3 todo_cli.py --agent dave add-artifact 1 "https://docs.google.com/..." --type URL --mimetype "google-doc"
```

Add a text note:
```bash
python3 todo_cli.py --agent dave add-artifact 1 "Note content here" --type Content
```

Add a file reference:
```bash
python3 todo_cli.py --agent dave add-artifact 1 "path/to/image.png" --type File --mimetype "image/png"
```

## MCP Integration

The `todo_mcp.py` script implements a FastMCP server.

### Available Tools

- `create_todo_task`: Creates a task for an agent.
- `update_todo_task`: Updates task details or status.
- `delete_todo_task`: Removes a task.
- `get_todo_task`: Retrieves details including updates and artifacts.
- `add_todo_update`: Adds a comment to a task.
- `add_todo_artifact`: Adds an artifact (URL, Content, or File) to a task.
- `get_urgent_tasks`: Returns an urgency report for an agent.

## Database

The tool creates agent-specific SQLite databases named `todo_<agent_name>.db`. Artifacts are stored in the `artifacts` table linked to tasks.
