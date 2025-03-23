import pytest
from unittest.mock import Mock, MagicMock

from src.main import AIChatApp, ChatHistoryItem, Button


class TestEventHandlers:
    """Tests for various event handlers."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock app with mocked database functionality."""
        app = AIChatApp()
        # Mock database-related methods
        app.init_database = Mock()
        app.load_chat_history = Mock()
        app.create_new_chat = Mock(return_value=1)
        app.load_chat = Mock()
        app.delete_chat = Mock()
        app.current_chat_id = 1
        
        # Mock UI elements
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
            
        app.query_one = mock_query_one
        
        return app

    def test_on_button_pressed_delete(self, mock_app):
        """Test handling of delete button press."""
        # Create a mock event
        event = MagicMock()
        event.button = MagicMock()
        event.button.id = "delete-123"
        event.prevent_default = Mock()
        event.stop = Mock()
        
        # Call the event handler
        mock_app.on_button_pressed(event)
        
        # Check that delete_chat was called with the correct ID
        mock_app.delete_chat.assert_called_once_with(123)
        
        # Check that event propagation was stopped
        event.prevent_default.assert_called_once()
        event.stop.assert_called_once()

    def test_on_button_pressed_other(self, mock_app):
        """Test handling of non-delete button press."""
        # Create a mock event
        event = MagicMock()
        event.button = MagicMock()
        event.button.id = "other-button"
        event.prevent_default = Mock()
        event.stop = Mock()
        
        # Call the event handler
        mock_app.on_button_pressed(event)
        
        # Check that delete_chat was not called
        mock_app.delete_chat.assert_not_called()
        
        # Check that event propagation was not stopped
        event.prevent_default.assert_not_called()
        event.stop.assert_not_called()

    def test_on_list_item_selected(self, mock_app):
        """Test handling of list item selection."""
        # Create a mock event with a ChatHistoryItem
        event = MagicMock()
        event.item = ChatHistoryItem(123, "Test Chat", "2023-01-01 12:00")
        
        # Call the event handler
        mock_app.on_list_item_selected(event)
        
        # Check that load_chat was called with the correct ID
        mock_app.load_chat.assert_called_once_with(123)

    def test_on_list_item_selected_not_chat_item(self, mock_app):
        """Test handling of list item selection with a non-ChatHistoryItem."""
        # Create a mock event with a non-ChatHistoryItem
        event = MagicMock()
        event.item = "Not a ChatHistoryItem"
        
        # Call the event handler
        mock_app.on_list_item_selected(event)
        
        # Check that load_chat was not called
        mock_app.load_chat.assert_not_called()

    def test_on_list_view_selected(self, mock_app):
        """Test handling of list view selection."""
        # Create a mock event with a ChatHistoryItem
        event = MagicMock()
        event.item = ChatHistoryItem(456, "Another Chat", "2023-01-02 12:00")
        
        # Call the event handler
        mock_app.on_list_view_selected(event)
        
        # Check that load_chat was called with the correct ID
        mock_app.load_chat.assert_called_once_with(456)

    def test_on_list_view_selected_not_chat_item(self, mock_app):
        """Test handling of list view selection with a non-ChatHistoryItem."""
        # Create a mock event with a non-ChatHistoryItem
        event = MagicMock()
        event.item = "Not a ChatHistoryItem"
        
        # Call the event handler
        mock_app.on_list_view_selected(event)
        
        # Check that load_chat was not called
        mock_app.load_chat.assert_not_called()