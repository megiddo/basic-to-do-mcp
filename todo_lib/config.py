import os
import re
from pathlib import Path
from dotenv import load_dotenv

class InvalidAgent(Exception):
    pass

class InvalidConfiguration(Exception):
    pass

# Determine paths
LIB_DIR = Path(__file__).parent.parent.absolute()
DOTENV_LIB = LIB_DIR / ".env"
DOTENV_ETC = Path("/etc/mcp/basic_todo/.env")

# Check for conflict
if DOTENV_LIB.exists() and DOTENV_ETC.exists():
    raise InvalidConfiguration(
        f"Conflict: Both {DOTENV_ETC} and {DOTENV_LIB} exist. "
        "Please use either the system-wide configuration or the local one, but not both."
    )

# Load configuration
if DOTENV_ETC.exists():
    load_dotenv(DOTENV_ETC)
elif DOTENV_LIB.exists():
    load_dotenv(DOTENV_LIB)

# Environment variables
AGENTS_RAW = os.getenv("AGENTS", "")
DB_FILE_ROOT = os.getenv("DB_FILE_ROOT", str(LIB_DIR))

# Parse agents
AGENT_LIST = [a.strip() for a in AGENTS_RAW.split(",") if a.strip()]

def is_valid_agent_name(name):
    """Validate that the agent name is alphanumeric and starts with a letter."""
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", name))

# Validate names in config
for agent in AGENT_LIST:
    if not is_valid_agent_name(agent):
        # We'll just ignore invalid names in the config or should we raise error?
        # Let's keep them but they might fail validation later if we are strict.
        # Actually, let's keep only valid ones.
        pass

def validate_agent(agent_name):
    """Check if the agent is authorized (case-insensitive)."""
    if not agent_name:
        raise InvalidAgent("Agent name cannot be empty.")
    
    if not is_valid_agent_name(agent_name):
        raise InvalidAgent(f"Invalid agent name format: '{agent_name}'. Names must be alphanumeric and start with a letter.")

    authorized_lower = [a.lower() for a in AGENT_LIST]
    if agent_name.lower() not in authorized_lower:
        raise InvalidAgent(f"Agent '{agent_name}' is not authorized.")

def get_agents():
    """Return the list of authorized agents."""
    return AGENT_LIST

def get_db_root():
    """Return the database file root directory."""
    return DB_FILE_ROOT
