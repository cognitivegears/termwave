"""Mock chat provider for testing and development."""

from .base import ChatProvider


class MockProvider(ChatProvider):
    """Mock chat provider that returns predefined responses."""

    @property
    def name(self):
        """Return the name of the provider."""
        return "Mock Provider"

    def __init__(self):
        """Initialize the mock provider with default options."""
        self.options = {
            "response_delay": 0.5,  # Seconds to delay before responding
            "response_type": "normal",  # Can be 'normal', 'code', 'error'
        }

    async def generate_response(self, messages):
        """Generate a mock response.

        Args:
            messages: List of message objects with 'role' and 'content'

        Returns:
            str: A mock response based on the last user message
        """
        import asyncio

        # Simulate a small delay to mimic network latency
        if self.options["response_delay"] > 0:
            await asyncio.sleep(self.options["response_delay"])

        if not messages:
            return "I don't have any messages to respond to."

        # Get the last user message
        last_user_messages = [m for m in messages if m['role'] == 'user']
        if not last_user_messages:
            return "I don't see any user messages to respond to."

        last_user_message = last_user_messages[-1]['content']

        # Generate response based on response_type
        if self.options["response_type"] == "code":
            return f"Here's some code that might help:\n```python\ndef process_text(text):\n    return text.upper()\n\n# Example usage\nresult = process_text('{last_user_message}')\nprint(result)\n```"
        elif self.options["response_type"] == "error":
            return "I'm sorry, but I encountered an error processing your request. Please try again."
        else:
            return f"You said: {last_user_message}\n\nThis is a mock response from the testing provider. In a real application, this would be a response from an AI service."

    def get_provider_model_list(self):
        """Get a list of available models for the provider.

        Returns:
            list: A list of available model names
        """
        return ["code", "error", "normal"]

    def get_provider_options(self):
        """Get provider-specific options.

        Returns:
            dict: A dictionary of available options and their current values
        """
        return self.options

    def set_provider_option(self, option_name, option_value):
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
