# TermWave

A TUI (Text User Interface) AI chat application built with Python and the Textual library.

## Features

- Multiple chat sessions
- Markdown rendering
- Chat history persistence
- Support for different AI providers (OpenAI, Anthropic, Mock)
- Command system

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/termwave.git
cd termwave

# Install dependencies
make install

# For development
make dev
```

## Usage

```bash
# Run directly (development)
PYTHONPATH=. python src/main.py

# Or install and run as a package
pip install -e .
termwave
```

## Commands

- `/help` - Show available commands
- `/new` - Start a new chat session
- `/provider` - Show or change the current provider
- `/provider openai` - Switch to OpenAI provider
- `/provider anthropic` - Switch to Anthropic provider
- `/provider mock` - Switch to Mock provider (for testing)
- `/provider model=gpt-4` - Change the model for the current provider
- `/quit` - Exit the application

## API Keys

For OpenAI or Anthropic providers, you need to set the appropriate API key:

```bash
# For OpenAI
export OPENAI_API_KEY="your-api-key"

# For Anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

## Development

```bash
# Run tests
make test

# Lint code
make lint

# Fix lint errors
make fix

# Build package
make build
```
