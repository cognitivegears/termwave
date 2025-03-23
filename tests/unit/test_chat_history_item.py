import pytest
from textual.widgets import Button, Static

# Import the ChatHistoryItem class
from src.main import ChatHistoryItem


class TestChatHistoryItem:
    """Tests for the ChatHistoryItem class."""

    def test_chat_history_item_initialization(self):
        """Test that a ChatHistoryItem is correctly initialized."""
        # Create a ChatHistoryItem instance
        chat_id = 123
        title = "Test Chat"
        timestamp = "2023-01-01 12:00"
        item = ChatHistoryItem(chat_id, title, timestamp)
        
        # Check that the properties are correctly set
        assert item.chat_id == chat_id
        assert item.title == title
        assert item.timestamp == timestamp

    def test_chat_history_item_compose(self):
        """Test that a ChatHistoryItem correctly yields its child widgets."""
        # Create a ChatHistoryItem instance
        chat_id = 123
        title = "Test Chat"
        timestamp = "2023-01-01 12:00"
        item = ChatHistoryItem(chat_id, title, timestamp)
        
        # Get the composed widgets
        widgets = list(item.compose())
        
        # Check that there are two widgets: Static for the text and Button for deletion
        assert len(widgets) == 2
        
        # First widget should be a Static with the right ID and content
        assert isinstance(widgets[0], Static)
        assert widgets[0].id == f"title-{chat_id}"
        # The text should contain the timestamp in bold and the title
        assert f"[bold]{timestamp}[/bold]" in widgets[0].renderable
        assert title in widgets[0].renderable
        
        # Second widget should be a Button with the right ID and class
        assert isinstance(widgets[1], Button)
        assert widgets[1].id == f"delete-{chat_id}"
        assert "delete-btn" in widgets[1].classes