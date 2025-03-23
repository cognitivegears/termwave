# termwave - CLUI AI Chat application

## Overview

termwave (termwave.chat) is an AI chat application using the textual library to generate a CLI user interface and sqlite3 to store the chat history.

## Features

- [x] Create a new chat
- [x] Delete a chat
- [x] View an existing chat
- [ ] Multi-line input
- [x] Markdown and rich text rendering
- [x] Choose a model
- [x] Implement OpenAI API for chat
- [ ] Plugin setup to add additional API's for chat
- [ ] Implement MCP support
- [ ] Implement a command line interface
- [ ] Set model options such as temperature, max tokens, etc.
- [ ] Ability to set (and save) user context
- [ ] Ability to set (and save) assistant persona
- [ ] Ability to upload files to the assistant
- [ ] Copy from sections of the assistant's response
- [ ] termwave should be available as a Docker image
- [ ] Compiled binary version for Linux, MacOS, and Windows

## General Notes

* All code should be in the `src` directory
* All tests should be in the `tests` directory
* All documentation should be in the `docs` directory
* All code should be covered by unit tests
* Unit tests should cover the functionality of the code
* Unit tests should be runnable with `pytest`
* All new features should have corresponding unit tests
* All new features should be documented
* All code is linted with `ruff`
* A Makefile is provided to build, test, and clean the project
* All code should be linted prior to committing


## Structure

* `src/main.py` - The main entry point for the application
* `tests/` - The directory for the unit tests
* `docs/` - The directory for the documentation
* `Makefile` - The Makefile for the project
* `pyproject.toml` - The pyproject.toml for the project
* `README.md` - The README for the project
* `LICENSE` - The LICENSE for the project
* `CHANGELOG.md` - The CHANGELOG for the project

## Tools

* [textual](https://textual.textualize.io/) - The library used to create the CLI
* [pytest](https://docs.pytest.org/) - The testing framework used
* [ruff](https://beta.ruff.rs/) - The linter used
* [sqlite3](https://www.sqlite.org/index.html) - The database used
* [OpenAI](https://openai.com/) - The API used to interact with the OpenAI API
* [Anthropic](https://www.anthropic.com/) - The API used to interact with the Anthropic API
* [MCP](https://mcp.readthedocs.io/) - The MCP used to interact with the MCP API
* [uv](https://docs.astral.sh/uv/index.html) - The package manager used

## External commands

Using `make`:

```
Usage:
  make <target>
  help             Display this help
  uv               Install uv if it's not present.
  dev              Install dev dependencies
  install          Install dependencies
  test             Run tests
  lint             Run linters
  fix              Fix lint errors
  cov              Run tests with coverage
  doc              Build documentation
  build            Build package
```

## Functional Testing

* Features should be tested using functional tests
* Functional tests should be in the `tests/functional` directory
* Functional tests should be named like `test_<feature>.py`
* Functional tests should use the `pytest-asyncio` plugin
* It should use Textual's test functionality (`run_test` etc)
