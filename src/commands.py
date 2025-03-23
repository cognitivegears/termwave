"""Command handling for TermWave."""


class CommandHandler:
    """Handles command processing for the app."""
    
    # Dictionary of available commands and their descriptions
    COMMAND_LIST = {
        "/quit": "Exit the application",
        "/help": "Show available commands",
        "/new": "Start a new chat session",
        "/provider": "Switch or configure the chat provider"
    }
    
    def __init__(self, app):
        """Initialize the command handler.
        
        Args:
            app: The parent application instance
        """
        self.app = app
    
    def handle_command(self, command):
        """Handle a slash command.
        
        Args:
            command: The command string including the leading slash
            
        Returns:
            bool: True if the command was handled successfully
        """
        parts = command.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == "/quit":
            self.app.exit()
            return True
        
        elif cmd == "/help":
            self._show_help()
            return True
        
        elif cmd == "/new":
            self.app.create_new_chat()
            return True
        
        elif cmd == "/provider":
            self._handle_provider_command(args)
            return True
        
        else:
            self._show_unknown_command(command)
            return False
    
    def _show_help(self):
        """Display the help message in the chat."""
        help_text = "## Available Commands\n\n"
        for cmd, desc in self.COMMAND_LIST.items():
            help_text += f"- `{cmd}`: {desc}\n"
        
        self.app.add_message_to_chat(help_text)
    
    def _show_unknown_command(self, command):
        """Display an unknown command message."""
        self.app.add_message_to_chat(
            f"Unknown command: `{command}`\nType `/help` to see available commands."
        )
    
    def _handle_provider_command(self, args):
        """Handle provider-related commands."""
        if not args:
            # Show current provider and available options
            current_provider = self.app.chat_provider.name
            provider_options = self.app.chat_provider.get_provider_options()
            
            message = f"## Current Provider: {current_provider}\n\n"
            message += "### Provider Options:\n\n"
            
            for option, value in provider_options.items():
                message += f"- `{option}`: {value}\n"
            
            message += "\nUse `/provider [name]` to switch providers or `/provider option=value` to set options."
            self.app.add_message_to_chat(message)
            return
        
        # Check if it's a provider name or an option setting
        if "=" in args:
            # Setting an option
            option, value = args.split("=", 1)
            option = option.strip()
            value = value.strip()
            
            # Try to parse value as a number if it looks like one
            if value.replace(".", "", 1).isdigit():
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
            
            success = self.app.chat_provider.set_provider_option(option, value)
            if success:
                self.app.add_message_to_chat(f"Option `{option}` set to `{value}`.")
            else:
                self.app.add_message_to_chat(f"Unknown option: `{option}`.")
        else:
            # Switching provider
            provider_name = args.strip().lower()
            if provider_name in ["openai", "anthropic", "mock"]:
                try:
                    self.app.setup_provider(provider_name)
                    self.app.add_message_to_chat(f"Switched to the **{self.app.chat_provider.name}** provider.")
                except Exception as e:
                    self.app.add_message_to_chat(f"Error switching provider: {str(e)}")
            else:
                self.app.add_message_to_chat(
                    "Invalid provider name. Available providers: `openai`, `anthropic`, `mock`."
                )