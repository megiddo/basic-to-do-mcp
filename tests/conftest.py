import pytest
import os
from todo_lib.db import get_db_path

@pytest.fixture
def test_agent(monkeypatch):
    agent_name = "testagent"
    from todo_lib import config
    monkeypatch.setattr(config, "AGENT_LIST", config.AGENT_LIST + [agent_name])
    
    db_path = get_db_path(agent_name)
    if os.path.exists(db_path):
        os.remove(db_path)
    
    yield agent_name
    
    if os.path.exists(db_path):
        os.remove(db_path)
