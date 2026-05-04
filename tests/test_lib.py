import pytest
from todo_lib import (
    create_task, update_task, delete_task, get_task,
    create_update, update_update, delete_update,
    add_artifact, delete_artifact,
    get_tasks_by_urgency,
    list_collections, create_collection, delete_collection,
    get_tasks_due_today, get_tasks_past_due, get_tasks_due_next_week
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

def test_collections(test_agent):
    # List (should have 'default')
    cols = list_collections(test_agent)
    assert "default" in cols
    
    # Create
    assert create_collection(test_agent, "Work") is True
    assert "Work" in list_collections(test_agent)
    
    # Task in collection
    task = create_task(test_agent, "Work Task", collection="Work")
    assert task["collection"] == "Work"
    
    # Report by collection
    work_tasks = get_tasks_by_urgency(test_agent, collection="Work")
    assert len(work_tasks) == 1
    assert work_tasks[0]["title"] == "Work Task"
    
    # Delete collection
    assert delete_collection(test_agent, "Work") is True
    assert "Work" not in list_collections(test_agent)
    
    # Task should move to default
    task_after = get_task(test_agent, task["id"])
    assert task_after["collection"] == "default"

def test_date_reporting(test_agent):
    from datetime import datetime, timedelta
    # Far future
    future = (datetime.now() + timedelta(days=30)).isoformat()
    # Past
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    # Today (end of day to be safe)
    today = datetime.now().replace(hour=23, minute=59, second=59).isoformat()
    
    create_task(test_agent, "Yesterday Task", date_due=yesterday)
    create_task(test_agent, "Today Task", date_due=today)
    create_task(test_agent, "Future Task", date_due=future)
    
    assert len(get_tasks_due_today(test_agent)) == 1
    assert len(get_tasks_past_due(test_agent)) == 1
    assert len(get_tasks_due_next_week(test_agent)) == 1 # Only Today, Future is far away
