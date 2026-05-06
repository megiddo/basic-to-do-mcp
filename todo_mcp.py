from mcp.server.fastmcp import FastMCP
import json
from todo_lib import (
    create_task, update_task, delete_task, get_task,
    create_update, update_update, delete_update,
    add_artifact, delete_artifact,
    get_tasks_by_urgency, get_tasks_by_date_range,
    list_collections, create_collection, delete_collection,
    get_tasks_due_today, get_tasks_past_due, get_tasks_due_next_week
)

mcp = FastMCP("Multi-Agent Todo Manager")

@mcp.tool()
def create_todo_task(agent_name: str, title: str, description: str = None, date_due: str = None, priority: str = 'medium', subtask_of: int = None, collection: str = 'default') -> str:
    """Create a new task in the to-do list for a specific agent."""
    task = create_task(agent_name, title, description, date_due, priority, subtask_of, collection)
    return json.dumps(task, indent=2)

@mcp.tool()
def update_todo_task(agent_name: str, task_id: int, title: str = None, description: str = None, status: str = None, priority: str = None, date_due: str = None, collection: str = None) -> str:
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
def update_todo_update(agent_name: str, update_id: int, comment: str) -> str:
    """Update an existing comment or update for a specific agent."""
    update_update(agent_name, update_id, comment)
    return f"Update {update_id} updated for agent {agent_name}."

@mcp.tool()
def delete_todo_update(agent_name: str, update_id: int) -> str:
    """Delete an existing comment or update for a specific agent."""
    delete_update(agent_name, update_id)
    return f"Update {update_id} deleted for agent {agent_name}."

@mcp.tool()
def delete_todo_artifact(agent_name: str, artifact_id: int) -> str:
    """Delete an artifact from a task for a specific agent."""
    delete_artifact(agent_name, artifact_id)
    return f"Artifact {artifact_id} deleted for agent {agent_name}."

@mcp.tool()
def get_urgent_tasks(agent_name: str, collection: str = None) -> str:
    """Get a list of tasks ordered by urgency for a specific agent."""
    tasks = get_tasks_by_urgency(agent_name, collection)
    return json.dumps(tasks, indent=2)

@mcp.tool()
def list_todo_collections(agent_name: str) -> str:
    """List all available collections for a specific agent."""
    cols = list_collections(agent_name)
    return json.dumps(cols, indent=2)

@mcp.tool()
def create_todo_collection(agent_name: str, name: str) -> str:
    """Create a new collection for a specific agent."""
    create_collection(agent_name, name)
    return f"Collection '{name}' created for agent {agent_name}."

@mcp.tool()
def delete_todo_collection(agent_name: str, name: str) -> str:
    """Delete a collection for a specific agent. Tasks in this collection will move to 'default'."""
    if delete_collection(agent_name, name):
        return f"Collection '{name}' deleted for agent {agent_name}."
    return f"Failed to delete collection '{name}' (cannot delete 'default')."

@mcp.tool()
def get_tasks_due_today_tool(agent_name: str, collection: str = None) -> str:
    """Get a list of tasks due today for a specific agent."""
    tasks = get_tasks_due_today(agent_name, collection)
    return json.dumps(tasks, indent=2)

@mcp.tool()
def get_tasks_past_due_tool(agent_name: str, collection: str = None) -> str:
    """Get a list of tasks that are past due for a specific agent."""
    tasks = get_tasks_past_due(agent_name, collection)
    return json.dumps(tasks, indent=2)

@mcp.tool()
def get_tasks_due_next_week_tool(agent_name: str, collection: str = None) -> str:
    """Get a list of tasks due in the next 7 days for a specific agent."""
    tasks = get_tasks_due_next_week(agent_name, collection)
    return json.dumps(tasks, indent=2)

@mcp.tool()
def get_tasks_by_date_range_tool(agent_name: str, start_date: str = None, end_date: str = None, collection: str = None) -> str:
    """Get a list of tasks within a specific date range for a specific agent.
    Dates should be in YYYY-MM-DD format.
    """
    tasks = get_tasks_by_date_range(agent_name, start_date=start_date, end_date=end_date, collection=collection)
    return json.dumps(tasks, indent=2)

if __name__ == "__main__":
    mcp.run()
