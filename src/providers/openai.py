"""OpenAI chat provider implementation."""

import os
from typing import List, Dict, Any

from openai import AsyncOpenAI

from .base import ChatProvider


class OpenAIProvider(ChatProvider):
    """Chat provider using OpenAI's API."""
    
    @property
    def name(self):
        """Return the name of the provider."""
        return "OpenAI"
    
    def __init__(self, api_key=None):
        """Initialize the OpenAI provider.
        
        Args:
            api_key: API key for OpenAI. If None, will try to use environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.options = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
        }
    
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response using OpenAI's API.
        
        Args:
            messages: List of message objects with 'role' and 'content'
            
        Returns:
            str: The assistant's response
        """
        if not self.api_key:
            return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        
        try:
            # Convert messages to format expected by OpenAI API
            api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.options["model"],
                messages=api_messages,
                temperature=self.options["temperature"],
                max_tokens=self.options["max_tokens"],
            )
            
            # Extract response text
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response from OpenAI: {str(e)}"
    
    def get_provider_options(self) -> Dict[str, Any]:
        """Get provider-specific options.
        
        Returns:
            dict: A dictionary of available options and their current values
        """
        return self.options
    
    def set_provider_option(self, option_name: str, option_value: Any) -> bool:
        """Set a provider-specific option.
        
        Args:
            option_name: The name of the option to set
            option_value: The value to set for the option
            
        Returns:
            bool: True if the option was set successfully
        """
        if option_name in self.options:
            self.options[option_name] = option_value
            return True
        return False