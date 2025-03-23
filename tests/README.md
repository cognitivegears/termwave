# TermWave Tests

This directory contains tests for the TermWave application.

## Test Structure

- `unit/`: Unit tests for individual components and functions
- `functional/`: Functional tests for UI interaction using Textual's test capabilities

## Running Tests

To run all tests:

```bash
make test
```

To run a specific test file:

```bash
uv run pytest tests/path/to/test_file.py
```

To run a specific test function:

```bash
uv run pytest tests/path/to/test_file.py::test_function_name
```

To run with verbose output:

```bash
uv run pytest -v
```

To run with coverage:

```bash
make cov
```

## Writing Tests

### Unit Tests

Unit tests should focus on testing individual functions and components in isolation. Mock any dependencies as needed.

### Functional Tests

Functional tests should use Textual's `run_test()` method to test the UI interaction. Use the `pytest-asyncio` plugin for these tests.

Example:

```python
@pytest.mark.asyncio
async def test_feature(app):
    # Use app.press, app.click, etc. to interact with the UI
    await app.press(*"Hello")
    await app.press("enter")
    
    # Assert that the expected changes occurred
    assert app.app.query_one("#some-element").renderable == "Expected value"
```