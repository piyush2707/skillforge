# Contributing to SkillForge

Thanks for considering a contribution. The project is young, and thoughtful bug reports, tests, docs, and small improvements are all welcome.

## Set up locally

```bash
git clone https://github.com/piyush2707/skillforge.git
cd skillforge
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
```

## Before opening a pull request

```bash
pytest
ruff check src tests
```

Keep changes focused, add tests for behavior changes, and update docs when a command or user-facing behavior changes. Please do not include API keys, credentials, or private source documents in issues or pull requests.

## Proposing a feature

Open an issue describing the problem, the intended workflow, and any trade-offs before investing in a large change. For security-sensitive reports, avoid publishing exploit details in a public issue until a maintainer can coordinate a fix.
