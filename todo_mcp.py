from mcp.server.fastmcp import FastMCP
import json
from todo_lib import (
    create_task, update_task, delete_task, get_task,
    create_update, update_update, delete_update,
    add_artifact, delete_artifact,
    get_tasks_by_urgency
)

mcp = FastMCP("Multi-Agent Todo Manager")

@mcp.tool()
def create_todo_task(agent_name: str, title: str, description: str = None, date_due: str = None, priority: str = 'medium', subtask_of: int = None) -> str:
    """Create a new task in the to-do list for a specific agent."""
    task = create_task(agent_name, title, description, date_due, priority, subtask_of)
    return json.dumps(task, indent=2)

@mcp.tool()
def update_todo_task(agent_name: str, task_id: int, title: str = None, description: str = None, status: str = None, priority: str = None, date_due: str = None) -> str:
    """Update an existing task for a specific agent."""
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ['task_id', 'agent_name']}
    task = update_task(agent_name, task_id, **kwargs)
    return json.dumps(task, indent=2)

@mcp.tool()
def delete_todo_task(agent_name: str, task_id: int) -> str:
    """Delete a task for a specific agent."""
    delete_task(agent_name, task_id)
    return f"Task {task_id} deleted for agent {agent_name}."

@mcp.tool()
def get_todo_task(agent_name: str, task_id: int) -> str:
    """Get details of a specific task including its updates and artifacts for a specific agent."""
    task = get_task(agent_name, task_id)
    if not task:
        return f"Task {task_id} not found for agent {agent_name}."
    return json.dumps(task, indent=2)

@mcp.tool()
def add_todo_update(agent_name: str, task_id: int, comment: str) -> str:
    """Add a comment or update to a specific task for a specific agent."""
    create_update(agent_name, task_id, comment)
    return f"Update added to task {task_id} for agent {agent_name}."

@mcp.tool()
def add_todo_artifact(agent_name: str, task_id: int, content: str, artifact_type: str = 'Content', mimetype: str = None) -> str:
    """Add an artifact (URL, text note, or file path) to a specific task for a specific agent.
    artifact_type should be one of 'URL', 'Content', or 'File'.
    """
    add_artifact(agent_name, task_id, content, mimetype, artifact_type)
    return f"Artifact added to task {task_id} for agent {agent_name}."

@mcp.tool()
def get_urgent_tasks(agent_name: str) -> str:
    """Get a list of tasks ordered by urgency for a specific agent."""
    tasks = get_tasks_by_urgency(agent_name)
    return json.dumps(tasks, indent=2)

if __name__ == "__main__":
    mcp.run()
