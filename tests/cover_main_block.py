"""
Script to cover the `if __name__ == "__main__"` block in main.py.
This is a special case that's tricky to cover in regular pytest.
"""
import sys
import os
import runpy
from unittest.mock import patch

# Add the project root to path so we can import the module
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Patch the _run_if_main function to prevent app execution
with patch('src.main._run_if_main'):
    # Run the module as __main__
    runpy.run_module('src.main', run_name='__main__')

print("Successfully covered __name__ == '__main__' block in main.py")
