"""Test fixtures for TermWave."""

import pytest
import os
import sys
import tempfile
from pathlib import Path

# Add the project root to the path so imports work during testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the application
from src.app import AIChatApp
from src.db.database import ChatDatabase


@pytest.fixture
def temp_db_path():
    """Create a temporary database file path for testing."""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_chat_history.db"
    yield db_path
    # Clean up
    if db_path.exists():
        os.unlink(db_path)
    os.rmdir(temp_dir)


@pytest.fixture
def test_app(monkeypatch, temp_db_path):
    """Create a test app instance with a temporary database."""
    # Create an app instance
    app = AIChatApp()
    
    # Create a test database
    db = ChatDatabase(db_path=temp_db_path)
    
    # Override the app's database
    monkeypatch.setattr(app, "db", db)
    
    return app
