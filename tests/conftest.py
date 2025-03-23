import pytest
import os
import tempfile
from pathlib import Path
import sqlite3

# Import the application
from src.main import AIChatApp


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
    
    # Override the database path
    monkeypatch.setattr(app, "db_path", temp_db_path)
    
    # Initialize the database
    app.init_database()
    
    return app