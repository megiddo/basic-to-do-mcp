# Multi-Agent To-Do MCP Tool

A Python-based to-do management system that supports multiple agents, each with their own isolated storage. This tool integrates with the Model Context Protocol (MCP) and provides a command-line interface.

## Features

- Multi-Agent Support: Each agent has their own isolated SQLite database identified by a plaintext keyword.
- Task Management: Create, update, delete, and retrieve tasks.
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
- `get`: Get task details.
- `add-update`: Add a comment to a task.
- `report`: Get tasks ordered by urgency.

### Examples

Create a task for agent "dave":
```bash
python3 todo_cli.py --agent dave create "Buy Groceries" --desc "Milk, Eggs, Bread" --priority high
```

Add an update for agent "bob":
```bash
python3 todo_cli.py --agent bob add-update 1 "Started project alpha"
```

View an urgency report for "dave" in Markdown:
```bash
python3 todo_cli.py --agent dave --format markdown report
```

## MCP Integration

The `todo_mcp.py` script implements a FastMCP server. All tools require an `agent_name` string parameter.

### Available Tools

- `create_todo_task`: Creates a task for an agent.
- `update_todo_task`: Updates task details or status for an agent.
- `delete_todo_task`: Removes a task for an agent.
- `get_todo_task`: Retrieves details for an agent's task.
- `add_todo_update`: Adds a comment to an agent's task.
- `get_urgent_tasks`: Returns an urgency report for an agent.

## Database

The tool creates agent-specific SQLite databases named `todo_<agent_name>.db`. These are initialized automatically on the first call for each agent.
