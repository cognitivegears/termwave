"""Configuration management for TermWave."""

import json
import os
from pathlib import Path


class Config:
    """Manages application configuration."""
    
    def __init__(self, config_path=None):
        """Initialize the configuration.
        
        Args:
            config_path: Optional path to the config file. If None, uses default path.
        """
        if config_path is None:
            self.config_path = Path.home() / ".aichat" / "config.json"
            self.config_dir = self.config_path.parent
            self.config_dir.mkdir(exist_ok=True)
        else:
            self.config_path = Path(config_path)
            self.config_dir = self.config_path.parent
        
        self.defaults = {
            "default_provider": "mock",
            "providers": {
                "openai": {
                    "api_key": os.environ.get("OPENAI_API_KEY", ""),
                    "default_model": "gpt-3.5-turbo",
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                "anthropic": {
                    "api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
                    "default_model": "claude-2",
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                "eliza": {
                    "response_delay": 0.5,
                    "model": "doctor"
                },
                "mock": {
                    "response_delay": 0.5,
                    "response_type": "normal"
                }
            },
            "ui": {
                "theme": "dark"
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default.
        
        Returns:
            dict: The loaded configuration
        """
        if not self.config_path.exists():
            # Create default config
            self.save_config(self.defaults)
            return self.defaults
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
            # Ensure all defaults exist in the loaded config
            merged_config = self.defaults.copy()
            self._deep_update(merged_config, config)
            return merged_config
        except Exception:
            # If there's any error loading, return defaults
            return self.defaults
    
    def save_config(self, config=None):
        """Save configuration to file.
        
        Args:
            config: The configuration to save. If None, saves the current config.
            
        Returns:
            bool: True if the save was successful
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception:
            return False
    
    def get(self, key, default=None):
        """Get a configuration value.
        
        Args:
            key: The key to get, can use dot notation for nested keys (e.g., 'providers.openai.api_key')
            default: Default value to return if key is not found
            
        Returns:
            The configuration value, or default if not found
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """Set a configuration value.
        
        Args:
            key: The key to set, can use dot notation for nested keys
            value: The value to set
            
        Returns:
            bool: True if the set was successful and the config was saved
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the innermost dict
        for i, k in enumerate(keys[:-1]):
            if k not in config:
                config[k] = {}
            elif not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated config
        return self.save_config()
    
    def _deep_update(self, target, source):
        """Recursively update a dict.
        
        Args:
            target: The target dictionary to update
            source: The source dictionary with updates
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value