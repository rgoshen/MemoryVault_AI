# 🧠🔒 MemoryVault AI

**The AI Assistant That Never Forgets** - Your local, private AI with ChatGPT-like interface, persistent memory, document search, web capabilities, and VSCode integration.

---

## 🚧 Project Status: Foundation Complete ✅

**✅ What's Working:**

- Python 3.13+ virtual environment setup
- All dependencies installed and verified
- Project structure created
- Setup verification system
- Git repository with proper workflow

**🔄 Currently Building:**

- Core AI components with memory
- Web interface
- VSCode integration
- Master control panel

---

## 🚧 Project Status: Foundation Complete ✅

**✅ What's Working:**

- Python 3.13+ virtual environment setup
- All dependencies installed and verified
- Project structure created
- Setup verification system
- Git repository with proper workflow

**🔄 Currently Building:**

- Core AI components with memory
- Web interface
- VSCode integration
- Master control panel

---

## 🎯 Requirements

- **Python 3.13+** (enforced by `.python-version`)
- **Virtual Environment** (`.venv` - included in setup)
- **GPT4All** (for local LLM models - tested during setup)

---

## 🚀 Current Setup (Foundation)

### 1. Project Setup

```bash
# Navigate to your project location
mkdir MemoryVault_AI
cd MemoryVault_AI

# Initialize git
git init

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
# You should see (.venv) in your prompt
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 3. Verify Setup

```bash
# Run our verification script
python setup_verification.py
```

**Expected Results:**

✅ Python Version: 3.13+ detected
✅ Required Packages: All installed in virtual environment
✅ Project Folders: LocalDocs, memory, vectorstores, exports created
⚠️ Ollama Connection: May fail if GPT4All not running (normal for now)

Success Rate: 75% (100% when GPT4All is running)

---

## 📁 Current Project Structure

```bash
MemoryVault_AI/
├── .git/                    # Git repository
├── .gitignore              # Git exclusions (venv, data folders)
├── .python-version         # Python 3.13.5 requirement
├── .venv/                  # Virtual environment (excluded from git)
├── requirements.txt        # Dependencies (installed)
├── setup_verification.py   # ✅ System verification (working)
├── README.md              # 📖 This file
│
├── LocalDocs/             # 📚 Your documents (auto-created)
├── memory/                # 🧠 Conversation storage (auto-created)
├── vectorstores/          # 🗃️ Document database (auto-created)
└── exports/               # 📤 Export files (auto-created)

# 🔄 Next to Build

├── core_components.py     # 🧠 AI engine with memory
├── main_interface.py      # 🖥️ Web interface
├── vscode_extension/      # 🔧 VSCode integration
│   ├── package.json       #   Extension manifest
│   ├── extension.js       #   Extension code
│   └── server.py         #   API server
└── launcher.py           # 🎛️ Master control panel
```

---

## 🔧 Development Workflow

### Code Quality Standards

This project enforces professional code quality standards through automated tools:

**Pre-commit Hooks:**

- **Black** - Code formatting
- **Flake8** - Linting and style checking
- **MyPy** - Type checking
- **Standard hooks** - Trailing whitespace, file endings, YAML validation

**Install pre-commit locally:**

```bash
# Install pre-commit hooks (runs automatically on git commit)
pre-commit install

# Or run manually on all files
pre-commit run --all-files
```

### CI/CD Pipeline

**Automated Testing:**

- All Pull Requests trigger automated tests
- Memory Manager tests (100% coverage)
- Document Vault tests (100% coverage)
- Code quality checks must pass before merging

**Branch Protection:**

- ✅ No direct commits to main branch
- ✅ All changes must go through Pull Request workflow
- ✅ Status checks must pass before merging
- ✅ Code review recommended

### Contributing Workflow

1. Create feature branch: git checkout -b feature/your-feature-name
2. Make changes and ensure tests pass locally
3. Run pre-commit: pre-commit run --all-files
4. Commit and push: git push origin feature/your-feature-name
5. Create Pull Request on GitHub
6. Wait for CI checks to pass (automated)
7. Merge via GitHub after review

### Local Development

```bash
# Setup (one time)
source .venv/bin/activate
pip install -r requirements.txt
pre-commit install

# Daily workflow
git checkout -b feature/my-feature

# ... make changes ...

pre-commit run --all-files  # Check quality

# Run all tests (unified pytest approach)
python3 -m pytest# Clean output, all tests
python3 -m pytest -v# Verbose, show individual test names
python3 -m pytest -s -v# Detailed output for debugging# Run specific test modules (if needed)

# Run individual tests
python3 -m pytest tests/test_memory_manager.py
python3 -m pytest tests/test_document_vault.py

git add . && git commit -m "Description"
git push origin feature/my-feature

# Create PR on GitHub
```

### Verification

```bash
# Test system setup anytime
python setup_verification.py

# Expected output

# 🧠🔒 MEMORYVAULT AI SETUP VERIFICATION

# 🐍 Testing Python version... ✅ Python 3.13.5

# 📦 Testing required packages... ✅ All packages

# 🔧 Testing Ollama connection... ⚠️ (if GPT4All not running)

# 📁 Creating project folders... ✅ All folders
```

---

## 📊 Current Dependencies

**Successfully Installed:**

- langchain - Core AI framework
- streamlit - Web interface framework
- requests - HTTP requests
- chromadb - Vector database for documents
- pypdf - PDF processing
- bs4 (beautifulsoup4) - Web scraping
- fastapi - API server framework
- uvicorn - ASGI server

**All packages verified working in Python 3.13+ virtual environment.**

---

## 🎯 Planned Features

- 🧠 Persistent Memory - Never forgets conversations across sessions
- 📚 Enhanced LocalDocs - Chat with your private documents (better than GPT4All)
- 🌐 Web Search - Real-time internet information retrieval
- 🔧 VSCode Integration - AI coding assistant directly in your IDE
- 🖥️ ChatGPT-like Interface - Beautiful, responsive web UI
- 🎛️ Master Control Panel - Unified system management
- 🔒 100% Private - Everything runs locally, no cloud APIs

---

## 🐛 Troubleshooting

### Virtual Environment Issues

```bash
# If you don't see (.venv) in prompt:
source .venv/bin/activate

# If packages seem missing

pip install -r requirements.txt

# If Python version wrong

# Check: python --version (should be 3.13+)
```

### Verification Issues

- Python Version Fail: Ensure Python 3.13+ is installed and active
- Package Import Fail: Re-run pip install -r requirements.txt in activated venv
- Ollama Connection Fail: Start GPT4All application and load models
- Folder Creation Fail: Check write permissions in project directory

### Common Commands

```bash
# Check current Python version
python --version

# Check if in virtual environment

echo $VIRTUAL_ENV

# List installed packages

pip list

# Test imports manually

python -c "import langchain; print('LangChain works!')"
```

---

## 📈 Next Development Phase

Immediate Next Steps:

Core Components (core_components.py) - AI engine with memory management
Basic Testing - Verify core functionality
Web Interface (main_interface.py) - Streamlit-based UI
VSCode Extension - IDE integration
Master Launcher - Unified control system

Each step will be built incrementally and tested before proceeding.

---

## 🤝 Development Notes

Virtual Environment: Always activate before development
Git Commits: Each major milestone is committed
Verification: Run setup_verification.py after changes
Dependencies: Update requirements.txt when adding packages
Testing: Each component tested individually before integration

---

Foundation complete - Ready for core AI development! 🚀
