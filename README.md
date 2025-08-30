# CLIck - Command-Line Task Manager

[![CI/CD Pipeline](https://github.com/arsovskidev/CLIck/actions/workflows/ci.yml/badge.svg)](https://github.com/arsovskidev/CLIck/actions/workflows/ci.yml)

A beautiful and intuitive command-line task manager built with Python.

## Features

- ✅ Add, edit, and delete tasks
- 🎯 Set priorities (low, medium, high)
- 📅 Set due dates with flexible date parsing
- 🏷️ Organize tasks with tags
- 🔍 Search and filter tasks
- 💾 Persistent SQLite storage
- 🌈 Beautiful terminal output with Rich
- 📊 Task status tracking

## Installation & Building

### Prerequisites
- Python 3.8+
- pip package manager

### Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd CLIck
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running in Development Mode

Run CLIck directly with Python:
```bash
# Show help
python3 -m src.cli --help

# Add tasks
python3 -m src.cli add "Buy groceries" --priority high --due tomorrow

# List tasks
python3 -m src.cli list

# Complete tasks
python3 -m src.cli complete 1
```

### Building Standalone Executable

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --name click main.py --clean
```

3. The executable will be created in `dist/click`:
```bash
# Run the standalone executable
./dist/click --help
./dist/click add "Test task" --priority medium
```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run with coverage (requires pytest-cov)
pip install pytest-cov
python3 -m pytest tests/ --cov=src --cov-report=html
```

## Releases

### Automated Releases

The project uses automated releases triggered by commits to the master branch:

- **Patch release** (v1.0.1): Bug fixes and small improvements
- **Minor release** (v1.1.0): New features (use `feat:` in commit message)
- **Major release** (v2.0.0): Breaking changes (use `feat!:` or `BREAKING CHANGE` in commit message)

### Manual Release

Use the release script for controlled releases:

```bash
# Create a patch release (default)
./scripts/release.sh

# Create a minor release
./scripts/release.sh minor

# Create a major release
./scripts/release.sh major
```

### Release Process

1. Tests and quality checks run automatically
2. Version is bumped based on commit messages
3. Changelog is generated from commit history
4. GitHub release is created with executable artifact
5. Binary is available for download at: https://github.com/arsovskidev/CLIck/releases

## Usage

### Adding Tasks

```bash
# Basic task
click add "Buy groceries"

# Task with due date and priority
click add "Complete project" --due tomorrow --priority high

# Task with tags
click add "Call dentist" --tags health,appointments --priority medium
```

### Listing Tasks

```bash
# List all tasks
click list

# Filter by priority
click list --priority high

# Filter by due date
click list --due today

# Show completed tasks
click list --completed
```

### Managing Tasks

```bash
# Mark task as complete
click complete 1

# Delete a task
click delete 1
```

### Date Formats

CLIck supports flexible date parsing:
- `today`, `tomorrow`, `yesterday`
- `in 3 days`
- `2024-01-15` (ISO format)
- `01/15/2024` (US format)
- `15-01-2024` (European format)

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
```

### Type Checking

```bash
mypy src/
```

### Building Executable

```bash
pip install pyinstaller
pyinstaller --onefile --name click src/cli.py
```

## Requirements

- Python 3.8+
- click >= 8.0.0
- rich >= 13.0.0
