"""Tests for the Eliza provider."""

import pytest
from unittest.mock import patch, MagicMock

from src.providers.eliza import ElizaProvider


class TestElizaProvider:
    """Tests for the Eliza provider."""

    @pytest.fixture
    def provider(self):
        """Create an ElizaProvider instance for testing."""
        with patch('src.providers.eliza.Eliza') as mock_eliza_class:
            # Create a mock Eliza instance
            mock_eliza = MagicMock()
            mock_eliza.initial.return_value = "Hello, I'm Eliza. How can I help you?"
            mock_eliza.respond.return_value = "I understand your message."
            mock_eliza.final.return_value = "Goodbye!"
            
            # Make the class return our mock instance
            mock_eliza_class.return_value = mock_eliza
            
            # Create the provider
            provider = ElizaProvider()
            
            yield provider

    def test_initialization(self, provider):
        """Test provider initialization."""
        assert provider.name == "Eliza"
        assert "response_delay" in provider.options
        assert "model" in provider.options
        assert provider.options["model"] == "doctor"
    
    @pytest.mark.asyncio
    async def test_generate_response_initial(self, provider):
        """Test response generation with empty messages."""
        # Case 1: Empty messages list
        response = await provider.generate_response([])
        assert response == provider.eliza.initial.return_value
        provider.eliza.initial.assert_called_once()
        
        # Case 2: No user messages
        response = await provider.generate_response([{"role": "assistant", "content": "Hello"}])
        assert response == provider.eliza.initial.return_value

    @pytest.mark.asyncio
    async def test_generate_response_normal(self, provider):
        """Test normal response generation."""
        messages = [
            {"role": "user", "content": "Hello, I'm feeling sad."},
            {"role": "assistant", "content": "I'm sorry to hear that. Tell me more."},
            {"role": "user", "content": "I'm having a bad day."}
        ]
        
        response = await provider.generate_response(messages)
        
        assert response == "I understand your message."
        provider.eliza.respond.assert_called_once_with("I'm having a bad day.")

    @pytest.mark.asyncio
    async def test_generate_response_quit(self, provider):
        """Test response generation with quit message."""
        # Setup the respond method to return None for quit messages
        provider.eliza.respond.return_value = None
        
        messages = [
            {"role": "user", "content": "Goodbye"}
        ]
        
        response = await provider.generate_response(messages)
        
        assert response == "Goodbye!"
        provider.eliza.respond.assert_called_once_with("Goodbye")
        provider.eliza.final.assert_called_once()

    @pytest.mark.asyncio
    async def test_response_delay(self, provider):
        """Test response delay functionality."""
        # Set a small delay for testing
        provider.options["response_delay"] = 0.1
        
        # Patch asyncio.sleep to track calls
        with patch('asyncio.sleep') as mock_sleep:
            await provider.generate_response([{"role": "user", "content": "Hello"}])
            mock_sleep.assert_called_once_with(0.1)
            
        # Test with no delay
        provider.options["response_delay"] = 0
        with patch('asyncio.sleep') as mock_sleep:
            await provider.generate_response([{"role": "user", "content": "Hello"}])
            mock_sleep.assert_not_called()

    def test_get_provider_model_list(self, provider):
        """Test getting available models."""
        models = provider.get_provider_model_list()
        assert isinstance(models, list)
        assert "doctor" in models

    def test_get_provider_options(self, provider):
        """Test getting provider options."""
        options = provider.get_provider_options()
        assert "response_delay" in options
        assert "model" in options

    def test_set_provider_option(self, provider):
        """Test setting provider options."""
        # Valid option
        assert provider.set_provider_option("response_delay", 1.0) is True
        assert provider.options["response_delay"] == 1.0
        
        # Invalid option
        assert provider.set_provider_option("invalid_option", "value") is False