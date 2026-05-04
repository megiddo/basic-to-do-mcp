import pytest
import json
import sys
from io import StringIO
from todo_cli import main

def test_cli_create_and_report(test_agent, capsys, monkeypatch):
    # Create task using CLI
    args = ["todo_cli.py", "--agent", test_agent, "create", "--title", "CLI Task", "--desc", "From CLI"]
    monkeypatch.setattr(sys, 'argv', args)
    main()
    
    out, err = capsys.readouterr()
    assert "{'id': 1, 'title': 'CLI Task'" in out
    
    # Report using CLI (JSON format)
    args = ["todo_cli.py", "--agent", test_agent, "report", "--format", "json"]
    monkeypatch.setattr(sys, 'argv', args)
    main()
    
    out, err = capsys.readouterr()
    data = json.loads(out)
    assert len(data) == 1
    assert data[0]["title"] == "CLI Task"

def test_cli_markdown_format(test_agent, capsys, monkeypatch):
    from todo_lib import create_task
    create_task(test_agent, "MD Task")
    
    args = ["todo_cli.py", "--agent", test_agent, "report", "--format", "markdown"]
    monkeypatch.setattr(sys, 'argv', args)
    main()
    
    out, err = capsys.readouterr()
    assert "| id | title |" in out
    assert "| MD Task |" in out

def test_cli_get_task(test_agent, capsys, monkeypatch):
    from todo_lib import create_task
    create_task(test_agent, "Get Me")
    
    args = ["todo_cli.py", "--agent", test_agent, "get", "1"]
    monkeypatch.setattr(sys, 'argv', args)
    main()
    
    out, err = capsys.readouterr()
    assert "'title': 'Get Me'" in out

def test_cli_collections(test_agent, capsys, monkeypatch):
    # Add collection
    args = ["todo_cli.py", "--agent", test_agent, "collections", "add", "Personal"]
    monkeypatch.setattr(sys, 'argv', args)
    main()
    capsys.readouterr() # Clear output
    
    # List collections
    args = ["todo_cli.py", "--agent", test_agent, "collections", "list"]
    monkeypatch.setattr(sys, 'argv', args)
    main()
    
    out, err = capsys.readouterr()
    assert "Personal" in out
    assert "default" in out
