"""
This file is used to get coverage of the `if __name__ == "__main__"` block.
It's not a traditional test but a utility to ensure full coverage.
"""
import os
import sys
import importlib
from unittest.mock import patch

# Set testing flag to prevent actual execution of the app
os.environ['TERMWAVE_TESTING'] = 'true'

# Import the module
import src.main

# Save current value
original_name = src.main.__name__

try:
    # Set to __main__ to trigger the block
    src.main.__name__ = "__main__"
    
    # Reload to execute the __main__ block
    importlib.reload(src.main)
    
    print("Successfully tested __main__ block")
finally:
    # Restore original name
    src.main.__name__ = original_name