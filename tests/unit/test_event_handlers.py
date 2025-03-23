"""Tests for various event handlers."""

import pytest
from unittest.mock import Mock, MagicMock

from src.app import AIChatApp
from src.ui.components import ChatHistoryItem


class TestEventHandlers:
    """Tests for various event handlers."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock app for testing event handlers."""
        app = AIChatApp()
        # Mock database and config-related methods
        app.db = Mock()
        app.config = Mock()
        app.command_handler = Mock()
        app.chat_provider = Mock()
        
        # Mock methods that would be called by event handlers
        app.load_chat = Mock()
        app.delete_chat = Mock()
        app.add_message_to_chat = Mock()
        app.save_and_respond_to_message = Mock()
        app.load_chat_history = Mock()
        
        # Mock UI elements
        def mock_query_one(selector):
            mock_widget = Mock()
            if selector == "#user-input":
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
        
    @pytest.mark.asyncio
    async def test_on_input_submitted_command(self, mock_app):
        """Test handling of input submission with a command."""
        # Create a mock event
        event = MagicMock()
        event.value = "/help"
        
        # Call the event handler
        await mock_app.on_input_submitted(event)
        
        # Check that handle_command was called
        mock_app.command_handler.handle_command.assert_called_once_with("/help")
        
        # Check that save_and_respond_to_message was not called
        mock_app.save_and_respond_to_message.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_on_input_submitted_message(self, mock_app):
        """Test handling of input submission with a regular message."""
        # Set up mock async response
        async def mock_save_and_respond():
            return "Test response"
        mock_app.save_and_respond_to_message = Mock(return_value=mock_save_and_respond())
        
        # Create a mock event
        event = MagicMock()
        event.value = "Test message"
        
        # Call the event handler
        await mock_app.on_input_submitted(event)
        
        # Check that save_and_respond_to_message was called
        mock_app.save_and_respond_to_message.assert_called_once_with("Test message")
        
        # Check that add_message_to_chat was called for both user and assistant messages
        assert mock_app.add_message_to_chat.call_count == 2
        mock_app.add_message_to_chat.assert_any_call("Test message", role="user")
        mock_app.add_message_to_chat.assert_any_call("Test response", role="assistant")
