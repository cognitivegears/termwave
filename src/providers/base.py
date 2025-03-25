"""Base class for chat providers."""

from abc import ABC, abstractmethod


class ChatProvider(ABC):
    """Base class that all chat providers must implement."""

    @property
    @abstractmethod
    def name(self):
        """Return the name of the provider."""
        pass

    @abstractmethod
    async def generate_response(self, messages):
        """Generate a response based on the conversation history.

        Args:
            messages: List of message objects with 'role' and 'content'

        Returns:
            str: The assistant's response
        """
        pass

    @abstractmethod
    def get_provider_model_list(self):
        """Get a list of available models for the provider.

        Returns:
            list: A list of available model names
        """
        pass

    @abstractmethod
    def get_provider_options(self):
        """Get provider-specific options.

        Returns:
            dict: A dictionary of available options and their current values
        """
        pass

    @abstractmethod
    def set_provider_option(self, option_name, option_value):
        """Set a provider-specific option.

        Args:
            option_name: The name of the option to set
            option_value: The value to set for the option

        Returns:
            bool: True if the option was set successfully
        """
        pass
