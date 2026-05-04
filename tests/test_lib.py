import pytest
from todo_lib import (
    create_task, update_task, delete_task, get_task,
    create_update, update_update, delete_update,
    add_artifact, delete_artifact,
    get_tasks_by_urgency
)

def test_task_lifecycle(test_agent):
    # Create
    task = create_task(test_agent, "Test Task", "Test Desc", priority="high")
    assert task["title"] == "Test Task"
    assert task["priority"] == "high"
    assert task["id"] is not None
    
    # Get
    fetched = get_task(test_agent, task["id"])
    assert fetched["id"] == task["id"]
    assert fetched["title"] == "Test Task"
    
    # Update
    updated = update_task(test_agent, task["id"], title="Updated Task", status="complete")
    assert updated["title"] == "Updated Task"
    assert updated["status"] == "complete"
    assert updated["date_completed"] is not None
    
    # Delete
    assert delete_task(test_agent, task["id"]) is True
    assert get_task(test_agent, task["id"]) is None

def test_updates_and_artifacts(test_agent):
    task = create_task(test_agent, "Task with attachments")
    task_id = task["id"]
    
    # Add Update
    assert create_update(test_agent, task_id, "Initial comment") is True
    
    # Add Artifact
    assert add_artifact(test_agent, task_id, "http://example.com", artifact_type="URL") is True
    
    # Fetch and check
    full_task = get_task(test_agent, task_id)
    assert len(full_task["updates"]) == 1
    assert full_task["updates"][0]["comment"] == "Initial comment"
    assert len(full_task["artifacts"]) == 1
    assert full_task["artifacts"][0]["content"] == "http://example.com"
    
    # Update/Delete update
    update_id = full_task["updates"][0]["id"]
    assert update_update(test_agent, update_id, "Modified comment") is True
    assert delete_update(test_agent, update_id) is True
    
    # Delete artifact
    artifact_id = full_task["artifacts"][0]["id"]
    assert delete_artifact(test_agent, artifact_id) is True
    
    final_task = get_task(test_agent, task_id)
    assert len(final_task["updates"]) == 0
    assert len(final_task["artifacts"]) == 0

def test_urgency_report(test_agent):
    create_task(test_agent, "Low Priority", priority="low", date_due="2026-12-31")
    create_task(test_agent, "Urgent Task", priority="urgent")
    create_task(test_agent, "Medium Priority", priority="medium")
    
    report = get_tasks_by_urgency(test_agent)
    assert len(report) == 3
    assert report[0]["priority"] == "urgent"
    assert report[1]["priority"] == "medium"
    assert report[2]["priority"] == "low"
