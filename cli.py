"""Command-line interface for SkillForge."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import create_skill, validate_skill


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skillforge",
        description="Create and validate portable SKILL.md packages for AI agents.",
    )
    parser.add_argument("--version", action="version", version=f"SkillForge {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a starter skill package")
    create.add_argument("name", help="Human-readable skill name")
    create.add_argument("--description", "-d", required=True, help="What the skill does and when to use it")
    create.add_argument("--output", "-o", default="skills", help="Output directory (default: ./skills)")
    create.add_argument("--source", help="Optional note identifying the source material")

    validate = sub.add_parser("validate", help="Validate a SKILL.md or skill directory")
    validate.add_argument("path", help="Path to SKILL.md or its containing directory")

    test = sub.add_parser("test", help="Run structural checks on a skill (MVP)")
    test.add_argument("path", help="Path to SKILL.md or its containing directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "create":
            file_path = create_skill(args.name, args.description, args.output, args.source)
            print(f"Created skill: {file_path}")
            print(f"Next: skillforge validate {file_path.parent}")
            return 0
        issues = validate_skill(Path(args.path))
        if issues:
            label = "Validation failed" if args.command == "validate" else "Skill tests failed"
            print(f"{label}:", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            return 1
        print(f"{args.command.title()} passed: {args.path}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"skillforge: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
