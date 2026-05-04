import pytest
import json
from todo_mcp import (
    create_todo_task, update_todo_task, delete_todo_task,
    get_todo_task, add_todo_update, add_todo_artifact,
    get_urgent_tasks
)

def test_mcp_tools(test_agent):
    # Create
    resp = create_todo_task(test_agent, "MCP Task", priority="urgent")
    task = json.loads(resp)
    assert task["title"] == "MCP Task"
    task_id = task["id"]
    
    # Update
    resp = update_todo_task(test_agent, task_id, status="in-progress")
    task = json.loads(resp)
    assert task["status"] == "in-progress"
    
    # Add Update
    resp = add_todo_update(test_agent, task_id, "MCP Update")
    assert "Update added" in resp
    
    # Get
    resp = get_todo_task(test_agent, task_id)
    task = json.loads(resp)
    assert task["updates"][0]["comment"] == "MCP Update"
    
    # Urgency
    resp = get_urgent_tasks(test_agent)
    tasks = json.loads(resp)
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    
    # Delete
    resp = delete_todo_task(test_agent, task_id)
    assert "deleted" in resp
    
    # Verify deletion
    resp = get_todo_task(test_agent, task_id)
    assert "not found" in resp
