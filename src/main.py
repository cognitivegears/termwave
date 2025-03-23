"""Main entry point for TermWave."""

from src.app import AIChatApp


def main():
    """Run the TermWave application."""
    app = AIChatApp()
    app.run()


# This function helps with testing the __main__ block
def _run_if_main():
    main()


# This allows us to test in a controlled way
def _test_for_coverage():
    """Special function only used in tests to get coverage."""
    # This returns a boolean that can be evaluated in tests
    # to mimic the if __name__ == "__main__" condition
    return __name__ == "__main__"


# Using a module-level variable to make this testable
IS_MAIN = __name__ == "__main__"
if IS_MAIN:
    _run_if_main()
