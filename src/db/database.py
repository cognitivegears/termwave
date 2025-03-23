"""Database operations for storing chat history."""

import sqlite3
from pathlib import Path


class ChatDatabase:
    """Handles all database operations for chat storage."""
    
    def __init__(self, db_path=None):
        """Initialize the database.
        
        Args:
            db_path: Optional path to the database file. If None, uses default path.
        """
        if db_path is None:
            self.db_path = Path.home() / ".aichat" / "chat_history.db"
            self.db_path.parent.mkdir(exist_ok=True)
        else:
            self.db_path = db_path
            
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create chats table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_new_chat(self, title="New Chat"):
        """Create a new chat in the database.
        
        Args:
            title: The title for the new chat
            
        Returns:
            int: The ID of the newly created chat
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO chats (title) VALUES (?)",
            (title,)
        )
        chat_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return chat_id
    
    def get_all_chats(self):
        """Get all chats from the database.
        
        Returns:
            list: List of tuples containing (id, title, timestamp)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, title, created_at FROM chats ORDER BY created_at DESC"
        )
        chats = cursor.fetchall()
        conn.close()
        
        return chats
    
    def get_chat_info(self, chat_id):
        """Get information about a specific chat.
        
        Args:
            chat_id: The ID of the chat to retrieve
            
        Returns:
            tuple: (title,) or None if chat not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT title FROM chats WHERE id = ?", (chat_id,))
        chat_info = cursor.fetchone()
        conn.close()
        
        return chat_info
    
    def get_chat_messages(self, chat_id):
        """Get all messages for a specific chat.
        
        Args:
            chat_id: The ID of the chat to retrieve messages for
            
        Returns:
            list: List of tuples containing (role, content)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY timestamp",
            (chat_id,)
        )
        messages = cursor.fetchall()
        conn.close()
        
        return messages
    
    def save_message(self, chat_id, role, content):
        """Save a message to the specified chat.
        
        Args:
            chat_id: The ID of the chat to save the message to
            role: The role of the message sender ('user' or 'assistant')
            content: The content of the message
            
        Returns:
            bool: True if the message was saved successfully
        """
        if chat_id is None:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save the message
        cursor.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content)
        )
        
        # If this is the first user message, update the chat title
        if role == "user":
            cursor.execute(
                "SELECT COUNT(*) FROM messages WHERE chat_id = ?",
                (chat_id,)
            )
            count = cursor.fetchone()[0]
            
            if count <= 1:  # This is the first message (we just inserted it)
                # Use first few words as title
                title = content.split()[:5]
                title = " ".join(title) + ("..." if len(content.split()) > 5 else "")
                
                cursor.execute(
                    "UPDATE chats SET title = ? WHERE id = ?",
                    (title, chat_id)
                )
        
        conn.commit()
        conn.close()
        
        return True
    
    def delete_chat(self, chat_id):
        """Delete a chat and all its messages.
        
        Args:
            chat_id: The ID of the chat to delete
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete messages first (foreign key constraint)
        cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        
        # Delete the chat
        cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
        
        conn.commit()
        conn.close()