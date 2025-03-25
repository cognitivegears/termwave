"""Functional tests for the Eliza provider in the chat UI."""

import os
import tempfile
import pytest
from pathlib import Path

import pytest_asyncio

from src.app import AIChatApp
from src.providers.eliza import ElizaProvider


@pytest_asyncio.fixture
async def eliza_app():
    """Fixture that creates an instance of the AIChatApp using the Eliza provider."""
    # Create a temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_eliza_chat.db"
    
    # Create the app with the test database
    async with AIChatApp().run_test() as pilot:
        # Override the database path and initialize it
        pilot.app.db.db_path = db_path
        pilot.app.db.init_database()
        
        # Use the Eliza provider
        pilot.app.chat_provider = ElizaProvider()
        
        yield pilot
        
    # Clean up
    if db_path.exists():
        os.unlink(db_path)
    os.rmdir(temp_dir)


@pytest.mark.asyncio
async def test_eliza_initialization(eliza_app):
    """Test that the app initializes correctly with Eliza provider."""
    # Check that the app is using ElizaProvider
    assert isinstance(eliza_app.app.chat_provider, ElizaProvider)
    
    # Check that the app has the expected widgets
    assert eliza_app.app.query_one("#user-input") is not None
    assert eliza_app.app.query_one("#chat-container") is not None
    
    # Check that a new chat is created on startup
    assert eliza_app.app.current_chat_id is not None


@pytest.mark.asyncio
async def test_eliza_conversation(eliza_app):
    """Test having a conversation with Eliza."""
    # Send a message
    await eliza_app.press(*"I am feeling sad today")
    await eliza_app.press("enter")
    
    # Check that the user message appears in the chat container
    markdowns = eliza_app.app.query("#chat-container > Markdown")
    # Should be at least 3: welcome message, user message, and Eliza response
    assert len(markdowns) >= 3
    
    # Send another message
    await eliza_app.press(*"My mother doesn't understand me")
    await eliza_app.press("enter")
    
    # Check for more messages
    markdowns = eliza_app.app.query("#chat-container > Markdown")
    # Should be at least 5 now: welcome, user1, eliza1, user2, eliza2
    assert len(markdowns) >= 5


@pytest.mark.asyncio
async def test_eliza_provider_options(eliza_app):
    """Test setting Eliza provider options."""
    # Get the default response delay
    default_delay = eliza_app.app.chat_provider.options["response_delay"]
    
    # Change the response delay with the /provider command
    await eliza_app.press(*f"/provider response_delay={default_delay + 0.5}")
    await eliza_app.press("enter")
    
    # Verify the change took effect
    assert eliza_app.app.chat_provider.options["response_delay"] == default_delay + 0.5