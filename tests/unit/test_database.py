"""Tests for database functionality."""

import os
import sqlite3
import tempfile
import pytest
from pathlib import Path

# Import the database module
from src.db.database import ChatDatabase


class TestDatabase:
    """Tests for database functionality."""

    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database file for testing."""
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test_chat_history.db"
        yield db_path
        # Clean up
        if db_path.exists():
            os.unlink(db_path)
        os.rmdir(temp_dir)

    @pytest.fixture
    def db(self, temp_db_path):
        """Create a database instance with a test database."""
        return ChatDatabase(db_path=temp_db_path)

    def test_init_database(self, db, temp_db_path):
        """Test that database initialization creates the expected tables."""
        # Connect to the database
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chats'")
        assert cursor.fetchone() is not None, "Chats table not created"
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        assert cursor.fetchone() is not None, "Messages table not created"
        
        # Check chats table schema
        cursor.execute("PRAGMA table_info(chats)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        assert "id" in column_names
        assert "title" in column_names
        assert "created_at" in column_names
        
        # Check messages table schema
        cursor.execute("PRAGMA table_info(messages)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        assert "id" in column_names
        assert "chat_id" in column_names
        assert "role" in column_names
        assert "content" in column_names
        assert "timestamp" in column_names
        
        conn.close()

    def test_create_new_chat(self, db):
        """Test creating a new chat."""
        chat_id = db.create_new_chat("Test Chat")
        
        # Check if chat was created
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM chats WHERE id = ?", (chat_id,))
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None, "Chat not created in database"
        assert result[0] == "Test Chat", "Chat title does not match"

    def test_get_all_chats(self, db):
        """Test getting all chats."""
        # Create some test chats
        chat_id1 = db.create_new_chat("Test Chat 1")
        chat_id2 = db.create_new_chat("Test Chat 2")
        
        # Get all chats
        chats = db.get_all_chats()
        
        # Should have at least 2 chats
        assert len(chats) >= 2
        
        # Find our test chats in the results
        chat1 = next((c for c in chats if c[0] == chat_id1), None)
        chat2 = next((c for c in chats if c[0] == chat_id2), None)
        
        assert chat1 is not None, "Chat 1 not found in get_all_chats result"
        assert chat2 is not None, "Chat 2 not found in get_all_chats result"
        assert chat1[1] == "Test Chat 1"
        assert chat2[1] == "Test Chat 2"

    def test_save_and_get_messages(self, db):
        """Test saving and retrieving messages."""
        # Create a chat
        chat_id = db.create_new_chat("Test Chat")
        
        # Save a user message
        db.save_message(chat_id, "user", "Hello, this is a test message")
        
        # Save an AI response
        db.save_message(chat_id, "assistant", "This is a test response")
        
        # Get messages
        messages = db.get_chat_messages(chat_id)
        
        assert len(messages) == 2, "Expected 2 messages"
        assert messages[0][0] == "user", "First message should be from user"
        assert messages[0][1] == "Hello, this is a test message", "User message content doesn't match"
        assert messages[1][0] == "assistant", "Second message should be from assistant"
        assert messages[1][1] == "This is a test response", "Assistant message content doesn't match"

    def test_delete_chat(self, db):
        """Test deleting a chat."""
        # Create a chat
        chat_id = db.create_new_chat("Test Chat to Delete")
        
        # Add some messages
        db.save_message(chat_id, "user", "Message to be deleted")
        db.save_message(chat_id, "assistant", "Response to be deleted")
        
        # Delete the chat
        db.delete_chat(chat_id)
        
        # Check if chat was deleted
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # Check chat
        cursor.execute("SELECT id FROM chats WHERE id = ?", (chat_id,))
        chat_result = cursor.fetchone()
        
        # Check messages
        cursor.execute("SELECT id FROM messages WHERE chat_id = ?", (chat_id,))
        message_result = cursor.fetchall()
        
        conn.close()
        
        assert chat_result is None, "Chat was not deleted"
        assert len(message_result) == 0, "Messages were not deleted"

    def test_chat_title_update(self, db):
        """Test that the chat title is updated based on the first message."""
        # Create a chat
        chat_id = db.create_new_chat("Initial Title")
        
        # Save a user message with enough words to update the title
        test_message = "First second third fourth fifth sixth"
        db.save_message(chat_id, "user", test_message)
        
        # Get chat info
        chat_info = db.get_chat_info(chat_id)
        title = chat_info[0]
        
        expected_title = "First second third fourth fifth..."
        assert title == expected_title, f"Title not updated correctly. Expected '{expected_title}', got '{title}'"
        
        # Save another user message, which should not update the title
        db.save_message(chat_id, "user", "This should not change the title")
        
        # Get chat info again
        chat_info = db.get_chat_info(chat_id)
        title_after_second_message = chat_info[0]
        
        assert title_after_second_message == expected_title, "Title should not have changed after the second message"

    def test_get_chat_info_nonexistent(self, db):
        """Test getting info for a non-existent chat."""
        # Try to get info for a chat with an ID that doesn't exist
        nonexistent_id = 9999
        chat_info = db.get_chat_info(nonexistent_id)
        
        assert chat_info is None, "Expected None for non-existent chat"

    def test_save_message_no_chat_id(self, db):
        """Test saving a message with no chat ID."""
        # Try to save a message with None as chat_id
        result = db.save_message(None, "user", "This message shouldn't be saved")
        
        assert result is False, "Expected False when saving message with no chat_id"
        
        # Check that no messages were saved
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        conn.close()
        
        assert count == 0, "Message was saved despite having no chat_id"
