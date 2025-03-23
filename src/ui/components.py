"""UI components for TermWave."""

from textual.widgets import ListItem, Static, Button


class ChatHistoryItem(ListItem):
    """A list item representing a chat history entry."""
    
    def __init__(self, chat_id, title, timestamp):
        """Initialize a chat history item.
        
        Args:
            chat_id: The ID of the chat in the database
            title: The title of the chat
            timestamp: The formatted timestamp of the chat
        """
        super().__init__()
        self.chat_id = chat_id
        self.title = title
        self.timestamp = timestamp
    
    def compose(self):
        """Compose the chat history item with title and delete button."""
        yield Static(f"[bold]{self.timestamp}[/bold]\n{self.title}", id=f"title-{self.chat_id}")
        yield Button("X", id=f"delete-{self.chat_id}", classes="delete-btn")