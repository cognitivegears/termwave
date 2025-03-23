import os
import sqlite3
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock

# Import the main application to access its methods
from src.main import AIChatApp


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
    def mock_app(self, monkeypatch, temp_db_path):
        """Create a mock app with a test database."""
        # Create an app instance
        app = AIChatApp()
        
        # Override the database path
        monkeypatch.setattr(app, "db_path", temp_db_path)
        
        # Initialize the database
        app.init_database()
        
        # Mock the query_one method to avoid UI interactions
        def mock_query_one(selector):
            mock_widget = Mock()
            if selector == "#history-list":
                mock_widget.clear = Mock()
                mock_widget.append = Mock()
            elif selector == "#chat-container":
                mock_widget.remove_children = Mock()
                mock_widget.mount = Mock()
                mock_widget.scroll_end = Mock()
            elif selector == "#user-input":
                mock_widget.focus = Mock()
                mock_widget.value = ""
            return mock_widget
            
        monkeypatch.setattr(app, "query_one", mock_query_one)
        
        return app

    def test_init_database(self, mock_app, temp_db_path):
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

    def test_create_new_chat(self, mock_app):
        """Test creating a new chat."""
        chat_id = mock_app.create_new_chat("Test Chat")
        
        # Check if chat was created
        conn = sqlite3.connect(mock_app.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM chats WHERE id = ?", (chat_id,))
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None, "Chat not created in database"
        assert result[0] == "Test Chat", "Chat title does not match"
        assert mock_app.current_chat_id == chat_id, "Current chat ID not updated"

    def test_save_and_load_messages(self, mock_app):
        """Test saving and loading messages."""
        # Create a chat
        chat_id = mock_app.create_new_chat("Test Chat")
        
        # Save a user message
        mock_app.save_message("user", "Hello, this is a test message")
        
        # Save an AI response
        mock_app.save_message("assistant", "This is a test response")
        
        # Connect to the database and check messages
        conn = sqlite3.connect(mock_app.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM messages WHERE chat_id = ?", (chat_id,))
        messages = cursor.fetchall()
        conn.close()
        
        assert len(messages) == 2, "Expected 2 messages"
        assert messages[0][0] == "user", "First message should be from user"
        assert messages[0][1] == "Hello, this is a test message", "User message content doesn't match"
        assert messages[1][0] == "assistant", "Second message should be from assistant"
        assert messages[1][1] == "This is a test response", "Assistant message content doesn't match"

    def test_delete_chat(self, mock_app):
        """Test deleting a chat."""
        # Instead of testing the full flow with a live database which is causing issues with mocking,
        # let's create a direct connection to test just the delete_chat functionality
        
        # Get path to the test database
        db_path = mock_app.db_path
        
        # Create a connection and manually create test data
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert a test chat
        cursor.execute("INSERT INTO chats (id, title) VALUES (999, 'Test Chat to Delete')")
        chat_id = 999
        
        # Insert test messages
        cursor.execute("INSERT INTO messages (chat_id, role, content) VALUES (?, 'user', 'Message to be deleted')", (chat_id,))
        cursor.execute("INSERT INTO messages (chat_id, role, content) VALUES (?, 'assistant', 'Response to be deleted')", (chat_id,))
        conn.commit()
        
        # Close and reopen connection to ensure data is written
        conn.close()
        
        # Set the current chat ID in the app
        mock_app.current_chat_id = chat_id + 1  # Different from the one we'll delete
        
        # Now delete the chat
        mock_app.delete_chat(chat_id)
        
        # Check if chat was deleted
        conn = sqlite3.connect(db_path)
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

    def test_chat_title_update(self, mock_app):
        """Test that the chat title is updated based on the first message."""
        # Create a chat
        chat_id = mock_app.create_new_chat("Initial Title")
        
        # Save a user message with enough words to update the title
        test_message = "First second third fourth fifth sixth"
        mock_app.save_message("user", test_message)
        
        # Connect to the database and check the title
        conn = sqlite3.connect(mock_app.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM chats WHERE id = ?", (chat_id,))
        title = cursor.fetchone()[0]
        conn.close()
        
        expected_title = "First second third fourth fifth..."
        assert title == expected_title, f"Title not updated correctly. Expected '{expected_title}', got '{title}'"
        
        # Save another user message, which should not update the title
        mock_app.save_message("user", "This should not change the title")
        
        # Connect again and check the title hasn't changed
        conn = sqlite3.connect(mock_app.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM chats WHERE id = ?", (chat_id,))
        title_after_second_message = cursor.fetchone()[0]
        conn.close()
        
        assert title_after_second_message == expected_title, "Title should not have changed after the second message"

    def test_load_chat_nonexistent(self, mock_app):
        """Test loading a non-existent chat."""
        # Try to load a chat with an ID that doesn't exist
        nonexistent_id = 9999
        mock_app.load_chat(nonexistent_id)
        
        # Since the chat doesn't exist, load_chat should return early
        # We can't directly test the return value, but we can check that current_chat_id didn't change
        assert mock_app.current_chat_id != nonexistent_id
    
    def test_save_message_no_current_chat(self, mock_app):
        """Test saving a message when no chat is selected."""
        # Set current_chat_id to None
        mock_app.current_chat_id = None
        
        # Try to save a message
        mock_app.save_message("user", "This message shouldn't be saved")
        
        # Connect to the database and check no messages were saved
        conn = sqlite3.connect(mock_app.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        conn.close()
        
        assert count == 0, "Message was saved despite having no current chat"
    
    def test_delete_current_chat(self, mock_app):
        """Test deleting the current chat."""
        # Our current mocking approach won't accurately test this behavior
        # without more complex setup. Let's directly test the relevant code path:
        
        # Set a specific chat ID
        original_chat_id = 1234
        mock_app.current_chat_id = original_chat_id
        
        # Mock create_new_chat to return a different ID
        original_create_new_chat = mock_app.create_new_chat
        mock_app.create_new_chat = Mock(return_value=original_chat_id + 1)
        
        # Call delete_chat
        mock_app.delete_chat(original_chat_id)
        
        # Verify create_new_chat was called
        mock_app.create_new_chat.assert_called_once()
        
        # Restore original method
        mock_app.create_new_chat = original_create_new_chat