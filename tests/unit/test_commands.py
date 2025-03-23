import pytest
from unittest.mock import Mock, patch

# Import the main application to access its methods
from src.main import AIChatApp


class TestCommands:
    """Tests for the command handling functionality."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock app with mocked database functionality."""
        app = AIChatApp()
        # Mock the database connection and initialization
        app.init_database = Mock()
        app.load_chat_history = Mock()
        app.create_new_chat = Mock(return_value=1)
        app.current_chat_id = 1
        
        # Create mock UI elements with proper mocking for Markdown objects
        chat_container_mock = Mock()
        chat_container_mock.mount = Mock()
        chat_container_mock.scroll_end = Mock()
        
        user_input_mock = Mock()
        user_input_mock.focus = Mock()
        
        def mock_query_one(selector):
            if selector == "#chat-container":
                return chat_container_mock
            elif selector == "#user-input":
                return user_input_mock
            return Mock()
            
        app.query_one = mock_query_one
        
        return app

    def test_handle_quit_command(self, mock_app):
        """Test handling the /quit command."""
        # Mock the exit method
        mock_app.exit = Mock()
        
        # Call the handle_command method with /quit
        mock_app.handle_command("/quit")
        
        # Check if exit was called
        mock_app.exit.assert_called_once()

    def test_handle_help_command(self, mock_app):
        """Test handling the /help command."""
        # Call the handle_command method with /help
        mock_app.handle_command("/help")
        
        # Get the chat container through our mocked query_one
        chat_container = mock_app.query_one("#chat-container")
        
        # Check that mount was called
        assert chat_container.mount.called

    def test_handle_new_command(self, mock_app):
        """Test handling the /new command."""
        # Call the handle_command method with /new
        mock_app.handle_command("/new")
        
        # Check if create_new_chat was called
        mock_app.create_new_chat.assert_called_once()

    def test_handle_unknown_command(self, mock_app):
        """Test handling an unknown command."""
        # Call the handle_command method with an unknown command
        mock_app.handle_command("/unknown")
        
        # Get the chat container through our mocked query_one
        chat_container = mock_app.query_one("#chat-container")
        
        # Check that mount was called
        assert chat_container.mount.called