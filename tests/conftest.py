import pytest
import os
from todo_lib.db import get_db_path

@pytest.fixture
def test_agent():
    agent_name = "test_agent_internal"
    db_path = get_db_path(agent_name)
    if os.path.exists(db_path):
        os.remove(db_path)
    
    yield agent_name
    
    if os.path.exists(db_path):
        os.remove(db_path)
