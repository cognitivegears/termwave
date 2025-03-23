"""Main application for TermWave."""

import datetime
from textual.app import App
from textual.widgets import Header, Footer, Input, Markdown, Button, ListView
from textual.containers import Container
from textual.reactive import reactive

from src.ui.components import ChatHistoryItem
from src.ui.styles import APP_CSS
from src.db.database import ChatDatabase
from src.commands import CommandHandler
from src.config import Config
from src.providers.mock import MockProvider
from src.providers.openai import OpenAIProvider
from src.providers.anthropic import AnthropicProvider


class AIChatApp(App):
    """Main Textual application for the chat interface."""

    CSS = APP_CSS
    current_chat_id = reactive(None)

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.config = Config()
        self.db = ChatDatabase()
        self.command_handler = CommandHandler(self)

        # Set up the chat provider based on config
        provider_name = self.config.get("default_provider", "mock")
        self.setup_provider(provider_name)

    def setup_provider(self, provider_name):
        """Set up the chat provider.

        Args:
            provider_name: The name of the provider to use
        """
        if provider_name == "openai":
            api_key = self.config.get("providers.openai.api_key")
            self.chat_provider = OpenAIProvider(api_key=api_key)
        elif provider_name == "anthropic":
            api_key = self.config.get("providers.anthropic.api_key")
            self.chat_provider = AnthropicProvider(api_key=api_key)
        else:
            # Default to mock provider
            self.chat_provider = MockProvider()

        # Load provider-specific options from config
        provider_config = self.config.get(f"providers.{provider_name}", {})
        for option, value in provider_config.items():
            self.chat_provider.set_provider_option(option, value)

    def compose(self):
        """Compose the application UI."""
        yield Header()

        with Container(id="app-grid"):
            # Left sidebar for chat history
            with Container(id="sidebar"):
                yield ListView(id="history-list")

            # Main area (chat + input)
            with Container(id="main-area"):
                # Chat display area
                with Container(id="chat-container"):
                    yield Markdown("# New Chat\n\nStart typing below...")

                # Input area at bottom
                with Container(id="input-container"):
                    yield Input(placeholder="Type your message here...", id="user-input")

        yield Footer()

    def on_mount(self):
        """Initialize the app when it's mounted."""
        # Set focus to the input box
        self.query_one("#user-input").focus()

        # Create a new chat or load the most recent one
        self.load_chat_history()
        if not self.current_chat_id:
            self.create_new_chat()

    def create_new_chat(self, initial_title="New Chat"):
        """Create a new chat session.

        Args:
            initial_title: The initial title for the chat

        Returns:
            int: The ID of the newly created chat
        """
        chat_id = self.db.create_new_chat(initial_title)
        self.current_chat_id = chat_id
        self.load_chat_history()

        # Clear the chat container
        chat_container = self.query_one("#chat-container")
        chat_container.remove_children()
        chat_container.mount(Markdown("# New Chat\n\nStart typing below..."))

        return chat_id

    def load_chat_history(self):
        """Load the chat history list from the database."""
        chats = self.db.get_all_chats()

        # Update the history list
        history_list = self.query_one("#history-list")
        history_list.clear()

        for chat_id, title, timestamp in chats:
            # Format the timestamp
            dt = datetime.datetime.fromisoformat(timestamp)
            formatted_time = dt.strftime("%Y-%m-%d %H:%M")

            # Truncate title if needed
            display_title = title[:30] + "..." if len(title) > 30 else title

            # Add to the list
            history_list.append(ChatHistoryItem(chat_id, display_title, formatted_time))

    def load_chat(self, chat_id):
        """Load a specific chat into the main window.

        Args:
            chat_id: The ID of the chat to load
        """
        # Get chat info
        chat_info = self.db.get_chat_info(chat_id)

        if not chat_info:
            return

        chat_title = chat_info[0]

        # Get all messages for this chat
        messages = self.db.get_chat_messages(chat_id)

        # Update current chat ID
        self.current_chat_id = chat_id

        # Clear and rebuild the chat container
        chat_container = self.query_one("#chat-container")
        chat_container.remove_children()

        # Add chat title
        chat_container.mount(Markdown(f"# {chat_title}"))

        # Add all messages
        for role, content in messages:
            if role == "user":
                chat_container.mount(Markdown(f"**You:** {content}"))
            else:
                chat_container.mount(Markdown(f"**AI:** {content}"))

        # Scroll to bottom
        chat_container.scroll_end(animate=False)

    def add_message_to_chat(self, message, role=None):
        """Add a message to the current chat display.

        Args:
            message: The message content to add
            role: Optional role for the message (user/assistant)
        """
        chat_container = self.query_one("#chat-container")

        if role == "user":
            chat_container.mount(Markdown(f"**You:** {message}"))
        elif role == "assistant":
            chat_container.mount(Markdown(f"**AI:** {message}"))
        else:
            # No role, just add as system message
            chat_container.mount(Markdown(message))

        # Scroll to bottom
        chat_container.scroll_end(animate=False)

    async def save_and_respond_to_message(self, user_message):
        """Save a user message and generate a response.

        Args:
            user_message: The message from the user

        Returns:
            str: The assistant's response
        """
        # Save user message
        self.db.save_message(self.current_chat_id, "user", user_message)

        # Get all messages for context
        messages = self.db.get_chat_messages(self.current_chat_id)
        messages_for_provider = [{"role": role, "content": content} for role, content in messages]

        # Get response from provider
        response = await self.chat_provider.generate_response(messages_for_provider)

        # Save assistant response
        self.db.save_message(self.current_chat_id, "assistant", response)

        return response

    def delete_chat(self, chat_id):
        """Delete a chat and all its messages.

        Args:
            chat_id: The ID of the chat to delete
        """
        self.db.delete_chat(chat_id)

        # If we deleted the current chat, create a new one
        if self.current_chat_id == chat_id:
            self.create_new_chat()
        else:
            self.load_chat_history()

    def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses.

        Args:
            event: The button press event
        """
        button_id = event.button.id

        if button_id and button_id.startswith("delete-"):
            chat_id = int(button_id.split("-")[1])
            self.delete_chat(chat_id)
            # Stop event propagation to prevent the list item selection
            event.prevent_default()
            event.stop()

    def on_list_item_selected(self, event):
        """Handle selection of a chat history item.

        Args:
            event: The selection event
        """
        if hasattr(event, 'item') and isinstance(event.item, ChatHistoryItem):
            self.load_chat(event.item.chat_id)

    def on_list_view_selected(self, event):
        """Alternative handler for chat history selection.

        Args:
            event: The selection event
        """
        if hasattr(event, 'item') and isinstance(event.item, ChatHistoryItem):
            self.load_chat(event.item.chat_id)

    async def on_input_submitted(self, event: Input.Submitted):
        """Handle user input submission.

        Args:
            event: The input submission event
        """
        user_message = event.value
        self.query_one("#user-input").value = ""

        # Check for commands
        if user_message.startswith("/"):
            self.command_handler.handle_command(user_message)
            return

        # Add user message to chat
        self.add_message_to_chat(user_message, role="user")

        # Get AI response
        response = await self.save_and_respond_to_message(user_message)

        # Add AI response to chat
        self.add_message_to_chat(response, role="assistant")

        # Return focus to input after processing
        self.query_one("#user-input").focus()
