# Release checklist

Before publishing a release:

- [ ] Run `python -m pip install -e '.[dev]'` in a clean Python 3.10+ environment.
- [ ] Run `python -m pytest -q`.
- [ ] Run `ruff check src tests`.
- [ ] Verify the GitHub Actions matrix passes on Python 3.10, 3.11, 3.12, and 3.13.
- [ ] Review the README's commands against the current CLI.
- [ ] Confirm generated skill files contain no API keys or private source material.
- [ ] Check `git status` and confirm no virtual environments, caches, or local secrets are included.
- [ ] Add release notes and publish a version tag only after CI passes.

Do not describe the project as LLM-powered or as importing repositories/PDFs until those features are implemented and tested.
