"""Tests for the command handling functionality."""

import pytest
from unittest.mock import Mock

from src.commands import CommandHandler
from src.app import AIChatApp


class TestCommands:
    """Tests for the command handling functionality."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock app for testing."""
        app = Mock(spec=AIChatApp)
        app.exit = Mock()
        app.create_new_chat = Mock(return_value=1)
        app.add_message_to_chat = Mock()
        app.chat_provider = Mock()
        app.chat_provider.name = "Mock Provider"
        app.chat_provider.get_provider_options = Mock(return_value={"option1": "value1"})
        app.chat_provider.set_provider_option = Mock(return_value=True)

        return app

    @pytest.fixture
    def command_handler(self, mock_app):
        """Create a command handler with a mock app."""
        return CommandHandler(mock_app)

    def test_handle_quit_command(self, command_handler, mock_app):
        """Test handling the /quit command."""
        # Call the handle_command method with /quit
        command_handler.handle_command("/quit")

        # Check if exit was called
        mock_app.exit.assert_called_once()

    def test_handle_help_command(self, command_handler, mock_app):
        """Test handling the /help command."""
        # Call the handle_command method with /help
        command_handler.handle_command("/help")

        # Check that add_message_to_chat was called
        assert mock_app.add_message_to_chat.called
        # The first argument should contain the help text
        help_call_args = mock_app.add_message_to_chat.call_args[0][0]
        assert "Available Commands" in help_call_args
        for cmd in CommandHandler.COMMAND_LIST:
            assert cmd in help_call_args

    def test_handle_new_command(self, command_handler, mock_app):
        """Test handling the /new command."""
        # Call the handle_command method with /new
        command_handler.handle_command("/new")

        # Check if create_new_chat was called
        mock_app.create_new_chat.assert_called_once()

    def test_handle_provider_command_no_args(self, command_handler, mock_app):
        """Test handling the /provider command with no arguments."""
        # Call the handle_command method with /provider
        command_handler.handle_command("/provider")

        # Check that add_message_to_chat was called with provider info
        assert mock_app.add_message_to_chat.called
        message = mock_app.add_message_to_chat.call_args[0][0]
        assert "Mock Provider" in message
        assert "option1" in message
        assert "value1" in message

    def test_handle_provider_command_set_option(self, command_handler, mock_app):
        """Test handling the /provider command with option setting."""
        # Call the handle_command method with /provider option=value
        command_handler.handle_command("/provider option1=newvalue")

        # Check that set_provider_option was called
        mock_app.chat_provider.set_provider_option.assert_called_once_with("option1", "newvalue")

        # Check that success message was shown
        message = mock_app.add_message_to_chat.call_args[0][0]
        assert "option1" in message
        assert "newvalue" in message

    def test_handle_provider_command_set_option_numeric(self, command_handler, mock_app):
        """Test handling the /provider command with numeric option setting."""
        # Test with integer
        command_handler.handle_command("/provider option1=42")
        mock_app.chat_provider.set_provider_option.assert_called_with("option1", 42)

        # Test with float
        command_handler.handle_command("/provider option1=3.14")
        mock_app.chat_provider.set_provider_option.assert_called_with("option1", 3.14)

    def test_handle_unknown_command(self, command_handler, mock_app):
        """Test handling an unknown command."""
        # Call the handle_command method with an unknown command
        result = command_handler.handle_command("/unknown")

        # Check the result is False
        assert result is False

        # Check that error message was shown
        message = mock_app.add_message_to_chat.call_args[0][0]
        assert "Unknown command" in message
        assert "/help" in message
