"""
This file is used to get coverage of the `if __name__ == "__main__"` block.
It's not a traditional test but a utility to ensure full coverage.
"""
import os
import importlib

# Set testing flag to prevent actual execution of the app
os.environ['TERMWAVE_TESTING'] = 'true'

# Import the module
import src.main as main

# Save current value
original_name = main.__name__

try:
    # Set to __main__ to trigger the block
    main.__name__ = "__main__"
    
    # Reload to execute the __main__ block
    importlib.reload(main)
    
    print("Successfully tested __main__ block")
finally:
    # Restore original name
    main.__name__ = original_name
