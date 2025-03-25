"""
Eliza is a program that simulates conversation with a human.
It uses pattern matching and substitution methodology to provide responses.
The Eliza class is a chat provider that implements the ChatProvider interface.

This uses the library https://github.com/wadetb/eliza, which is a Python implementation of the classic Eliza program.
"""

import sys
import os
import asyncio
from pathlib import Path

from .base import ChatProvider

# Import the Eliza class from the eliza module we copied locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from eliza import Eliza


class ElizaProvider(ChatProvider):
    """Eliza chat provider that uses pattern matching for responses."""

    @property
    def name(self):
        """Return the name of the provider."""
        return "Eliza"

    def __init__(self):
        """Initialize the Eliza provider with default options."""
        self.options = {
            "response_delay": 0.5,  # Seconds to delay before responding
            "model": "doctor",  # Can be 'doctor' only for now
        }
        
        # Initialize the Eliza instance
        self.eliza = Eliza()
        
        # Get the path to the doctor.txt file
        root_dir = Path(__file__).parent.parent.parent.parent
        doctor_file = root_dir / "doctor.txt"
        
        # Check if the file exists, if not, use default responses
        if doctor_file.exists():
            self.eliza.load(str(doctor_file))
        else:
            # Configure with default responses for testing
            self.eliza.initials = ["How do you do. Please tell me your problem."]
            self.eliza.finals = ["Goodbye. Thank you for talking to me."]
            self.eliza.quits = ["bye", "goodbye", "quit"]
            
            # Set up some basic patterns
            from eliza import Key, Decomp
            
            # Create a default key for unknown input
            default_key = Key("xnone", 1, [])
            default_decomp = Decomp(["*"], False, [
                ["I'm not sure I understand you fully."],
                ["Please go on."],
                ["What does that suggest to you?"],
                ["Do you feel strongly about discussing such things?"]
            ])
            default_key.decomps.append(default_decomp)
            
            # Add to the keys dictionary
            self.eliza.keys["xnone"] = default_key

    async def generate_response(self, messages):
        """Generate a response using Eliza's pattern matching.

        Args:
            messages: List of message objects with 'role' and 'content'

        Returns:
            str: The assistant's response
        """
        # Simulate a small delay to mimic network latency
        if self.options["response_delay"] > 0:
            await asyncio.sleep(self.options["response_delay"])

        if not messages:
            return self.eliza.initial()

        # Get the last user message
        last_user_messages = [m for m in messages if m['role'] == 'user']
        if not last_user_messages:
            return self.eliza.initial()

        last_user_message = last_user_messages[-1]['content']
        
        # Generate response using Eliza's pattern matching
        response = self.eliza.respond(last_user_message)
        
        # If we got None as a response (user sent a quit message), return a goodbye
        if response is None:
            return self.eliza.final()
            
        return response

    def get_provider_model_list(self):
        """Get a list of available models for the provider.

        Returns:
            list: A list of available model names
        """
        # Eliza only has one personality for now
        return ["doctor"]

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