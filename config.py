import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent

# Database configuration
DATABASE_PATH = PROJECT_ROOT / 'market.db'
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"