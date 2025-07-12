# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MemoryVault AI is a local AI assistant with persistent memory, document search capabilities, and VSCode integration. The project emphasizes privacy (100% local) and provides ChatGPT-like functionality with enhanced memory persistence.

**Key Architecture Principles:**

- Domain-driven design with single responsibility components
- Local-first approach (no cloud APIs)
- Persistent conversation memory across sessions
- Vector-based document search and retrieval

## Core Components

### Memory Management (`memory_manager.py`)

- **Purpose**: Handles persistent conversation storage and retrieval
- **Key Features**: Session management, automatic session resumption, conversation search
- **Storage**: JSON-based persistence in `memory/conversation_memory.json`
- **Session Strategy**: Automatically resumes most recent session or creates new one

### Document Processing (`document_vault.py`)

- **Purpose**: Document indexing, processing, and AI-powered querying
- **Supported Formats**: PDF, TXT, DOCX, CSV, MD, code files (Python, JS, TS, etc.)
- **AI Backend**: Uses Ollama with `deepseek-r1-distill-8b` model (configurable)
- **Vector Storage**: ChromaDB with persistent storage in `vectorstores/documents/`
- **Graceful Degradation**: Works without AI model (scanning only) until model is available

## Development Commands

### Testing

```bash
# Run all tests with unified pytest framework
python3 -m pytest

# Verbose output with individual test names
python3 -m pytest -v

# Detailed output for debugging
python3 -m pytest -s -v

# Run specific test modules
python3 -m pytest tests/test_memory_manager.py
python3 -m pytest tests/test_document_vault.py
```

### Code Quality

```bash
# Install pre-commit hooks (one-time setup)
pre-commit install

# Run all quality checks manually
pre-commit run --all-files

# Individual tools (if needed)
black .                    # Code formatting
flake8 .                   # Linting
mypy .                     # Type checking
```

### Environment Setup

```bash
# Activate virtual environment (always required)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify system setup
python setup_verification.py
```

## Project Structure

```
MemoryVault_AI/
├── memory_manager.py      # Core memory persistence
├── document_vault.py      # Document processing & AI querying
├── memory_vault.py        # Main integration (currently empty)
├── memory/               # Conversation storage (JSON files)
├── LocalDocs/            # User documents for indexing
├── vectorstores/         # ChromaDB vector storage
├── tests/                # Comprehensive test suite
└── exports/              # Export functionality
```

## Key Implementation Details

### Memory Manager Architecture

- Session-based conversation storage with automatic session management
- Smart resumption: continues last session or creates new one
- Full conversation search and context retrieval
- Metadata tracking for session management

### Document Vault Architecture

- Multi-format document loader with comprehensive metadata
- Chunking strategy: 1000 chars with 200 char overlap
- AI connectivity testing before initialization
- Robust error handling with graceful degradation

### Testing Strategy

- Pytest configuration in `pytest.ini` with custom markers
- 100% test coverage for core components
- Markers: `@pytest.mark.memory`, `@pytest.mark.document`, `@pytest.mark.integration`
- CI/CD integration with automated quality gates

## Development Workflow

### Branch Management

- Main branch: `main`
- Feature branches: `feature/description`
- No direct commits to main (enforced by CI)
- All changes via Pull Request workflow

### Quality Standards

- Pre-commit hooks enforce Black formatting, Flake8 linting, MyPy type checking
- All tests must pass before merging
- Code coverage requirements maintained
- Professional code quality standards enforced

### AI Model Dependencies

- Default model: `deepseek-r1-distill-8b` via Ollama
- Document processing gracefully degrades without AI model
- Model connectivity tested during initialization
- Configurable model selection in DocumentVault constructor

## Important Notes

- **Python Version**: Requires Python 3.13+ (enforced by `.python-version`)
- **Virtual Environment**: Always activate `.venv` before development
- **Local First**: No external API dependencies for core functionality
- **Memory Persistence**: Conversations automatically saved and resumed
- **Document Size Limits**: Files over 10MB automatically skipped during indexing
- **Vector Database**: ChromaDB persistence ensures indexed documents survive restarts
