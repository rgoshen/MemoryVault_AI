# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MemoryVault AI is a **full-featured local AI assistant** with persistent memory, being built through a **4-phase learning methodology** to avoid tutorial hell and ensure deep understanding. The project provides a **ChatGPT-like experience** that runs 100% locally with memory that persists across sessions.

**Target Capabilities:**

- General-purpose AI conversation and assistance
- Coding mentor and pair programming partner
- Document processing and intelligent search
- Web research and information retrieval
- Academic assistance (study help, note-taking, etc.)
- VSCode integration for development workflow

**Current Status: Phase 1 - "Memory That Actually Works"**

## Learning Methodology

### Anti-Tutorial Hell Approach

- **Problem-First**: Each phase solves a real frustration
- **Immediate Usage**: Build tools actually used for real work
- **Understanding Checkpoints**: Student explains WHY before advancing
- **Your Code**: Student writes code with guidance, no copy-paste
- **Progressive Complexity**: Start simple, add complexity when pain emerges

### 4-Phase Development Plan

#### **Phase 1: "Memory That Actually Works" (CURRENT)**

**Problem**: AI conversations disappear every restart, losing valuable context

- Build terminal chat using existing `memory_manager.py`
- **Value**: AI assistant that remembers across sessions
- **Learning**: Context management, data persistence fundamentals

#### **Phase 2: "Documents That Answer Questions" (NEXT)**

**Problem**: Information scattered across files, can't query effectively

- Add document processing to existing structure
- **Value**: AI that knows your documents and can answer questions about them
- **Learning**: Knowledge representation, retrieval systems, document processing

#### **Phase 3: "Specialized Assistant" (FUTURE)**

**Problem**: Generic responses don't leverage your specific context/workflow

- Build domain-specific behavior and response patterns
- **Value**: AI that adapts to your work style and preferences
- **Learning**: System design, specialization, user modeling

#### **Phase 4: "Production AI Assistant" (FINAL)**

**Problem**: Need competitive alternative to ChatGPT with better memory

- Integrate real LLM into proven architecture
- **Value**: Full-featured AI assistant with web UI and VSCode integration
- **Learning**: Modern AI architecture, RAG systems, production deployment

## Architecture Patterns & Design Principles

### Clean Architecture Requirements

- **Core Logic Independence**: Business logic must not depend on UI, frameworks, or external systems
- **Dependency Inversion**: High-level modules should not depend on low-level modules. Both should depend on abstractions
- **Interface Segregation**: No component should depend on interfaces it doesn't use
- **Single Responsibility**: Each class/module has one reason to change

### Layer Separation Rules

```
📱 Presentation Layer     (Terminal, Web UI, VSCode Extension)
    ↓ (depends on)
🧠 Application Layer      (Chat orchestration, conversation flow)
    ↓ (depends on)
💼 Domain Layer          (Core AI logic, memory management, document processing)
    ↓ (depends on)
🔧 Infrastructure Layer   (File I/O, LLM APIs, vector databases)
```

### Key Patterns to Follow

#### **Repository Pattern**

- Memory persistence should be abstracted behind interfaces
- Core logic shouldn't know if memory is JSON, database, or cloud storage

#### **Strategy Pattern**

- AI response generation should be pluggable
- Core logic shouldn't care if responses come from local LLM, API, or mock responses

#### **Command Pattern**

- User actions should be encapsulated as commands
- Makes undo/redo, logging, and multiple UIs easier

#### **Observer Pattern**

- UI should observe core state changes
- Enables real-time updates across multiple interface types

### Implementation Guidelines

1. **Core classes never import UI libraries** - No Streamlit, tkinter, etc. in business logic
2. **Interfaces define contracts** - Use Python protocols/ABC for clean boundaries
3. **Dependency injection** - Core logic receives its dependencies, doesn't create them
4. **Pure functions where possible** - Easier to test and reason about

### Test-Driven Development (TDD) Requirements

#### TDD Cycle (Red-Green-Refactor)

1. **Red**: Write a failing test that describes desired behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests green

#### TDD Benefits for Learning

- **Forces clear requirements** - Can't write test without understanding what you're building
- **Prevents over-engineering** - Only build what the test requires
- **Validates understanding** - Test describes your mental model
- **Enables confident refactoring** - Architecture changes don't break functionality

#### Testing Strategy by Layer

```
🧪 Unit Tests        → Domain layer (ChatEngine, MemoryManager)
🔄 Integration Tests → Application layer (components working together)
🖥️ E2E Tests         → Presentation layer (full user workflows)
```

#### Phase 1 TDD Focus

- **Test first, code second** - Write test describing chat behavior before implementing
- **Start with simplest test** - "ChatEngine can accept a message"
- **One test at a time** - Don't write multiple tests until current one passes
- **Test the interface, not implementation** - Test what ChatEngine does, not how

#### Testing Tools & Standards

```bash
# Run tests (always before committing)
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Test specific module
python -m pytest tests/test_chat_engine.py
```

### Phase 1 Architecture Focus

- Build **ChatEngine** as pure business logic (no UI dependencies)
- **MemoryManager** already follows this pattern ✅
- **Terminal interface** should be thin adapter that calls ChatEngine
- All user input/output handled by presentation layer only

## Current Components (Phase 1)

### Memory Management (`memory_manager.py`) ✅ WORKING

- **Purpose**: Handles persistent conversation storage and retrieval
- **Features**: Session management, message storage, conversation search
- **Storage**: JSON-based persistence in `memory/conversation_memory.json`
- **Status**: Tested and functional

### Terminal Chat Interface (IN PROGRESS)

- **Purpose**: Full-featured chat interface with AI assistant capabilities
- **Goal**: Prove memory persistence works for real AI conversations
- **Usage**: General AI assistance, coding help, document queries, etc.

### Future Components (Later Phases)

- Document processing and search (Phase 2)
- Web interface with ChatGPT-like UI (Phase 3-4)
- VSCode integration for coding assistance (Phase 4)
- LLM integration with local models (Phase 4)

## Development Commands (Phase 1)

### Current Testing

```bash
# Test memory manager (working)
python3 tests/test_memory_manager.py

# Test basic functionality
python3 -c "from memory_manager import MemoryManager; m = MemoryManager(); print('Memory works!')"
```

### Environment Setup

```bash
# Always activate virtual environment first
source .venv/bin/activate

# Verify setup
python setup_verification.py

# Current dependencies (Phase 1 only)
pip install -r requirements.txt
```

## Current Project Structure

```
MemoryVault_AI/
├── memory_manager.py      # ✅ Core memory (working)
├── tests/                 # ✅ Memory tests (working)
│   └── test_memory_manager.py
├── memory/               # ✅ Storage (auto-created)
├── .venv/                # ✅ Virtual environment
├── requirements.txt      # ✅ Dependencies
└── setup_verification.py # ✅ System check

# Phase 1 Target Structure
├── terminal_chat.py      # 🔄 Building now
└── README_PHASE1.md      # 📝 Phase 1 documentation
```

## Phase 1 Development Focus

### What We're Building Now

- **Full-featured terminal chat interface** for AI assistance
- Integration with existing memory_manager.py for conversation persistence
- Proof that memory persistence enables continuous AI relationships
- Foundation for coding assistance, document queries, and general AI help

### What We're NOT Building Yet

- Web interfaces (Phase 3-4)
- Document processing (Phase 2)
- LLM integration (Phase 4)
- Complex testing frameworks (Phase 4)

### Success Criteria for Phase 1

1. **Functional terminal chat** that saves/loads conversations across sessions
2. **Daily usage** for coding questions, problem-solving, general assistance
3. **Understanding checkpoint** - student explains WHY persistent memory transforms AI interaction
4. **Pain identification** - what limitations drive the need for document processing (Phase 2)

## Development Workflow (Simplified for Learning)

### Git Workflow

```bash
# Current branch (Phase 1)
git checkout phase-1-memory-chat

# Simple commit process
git add filename.py
git commit -m "Phase 1: Add terminal chat interface"
```

### Quality Standards (Learning-Appropriate)

- **Test-driven development** - Write tests first to clarify requirements
- Code that works and solves the real problem
- Basic error handling for user experience
- Clear, readable code that student understands
- **Clean architecture** - UI-agnostic core logic with proper separation
- Functional testing through actual daily usage

## Important Notes for Claude Code

- **Stay in Phase 1** - Don't suggest advanced features until this phase is complete
- **Full AI assistant scope** - This isn't just note-taking, it's a complete AI assistant
- **Architecture-first thinking** - Always guide toward clean separation of concerns
- **UI-agnostic core logic** - Business logic should never depend on presentation layer
- **TDD methodology** - Guide student to write tests first, then implement
- **Test-driven learning** - Use tests to validate understanding before building
- **Problem-first guidance** - Always explain WHY before HOW architecturally
- **Student codes** - Provide guidance and architectural thinking, not complete solutions
- **Check understanding** - Ask student to explain architectural decisions before advancing
- **Design patterns** - Guide toward proper use of Repository, Strategy, Command patterns
- **Real usage focus** - Build for actual AI assistant workflows (coding help, problem-solving, etc.)

## Learning Checkpoints

Before advancing to Phase 2, student must:

1. ✅ Demonstrate terminal chat being used for real AI assistance tasks
2. ✅ Explain WHY persistent memory changes the AI assistant experience
3. ✅ Identify pain points that document processing would solve
4. ✅ Walk through memory_manager.py code and architecture decisions

---

**Current Priority**: Build terminal chat interface for full AI assistant functionality with persistent memory.
