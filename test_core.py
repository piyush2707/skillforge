from pathlib import Path

import pytest

from skillforge.core import create_skill, slugify, validate_skill


def test_slugify():
    assert slugify("React Component Library") == "react-component-library"
    assert slugify("  Hello, World!  ") == "hello-world"
    assert slugify("C++ / Python") == "c-python"


def test_create_and_validate_skill(tmp_path: Path):
    skill_file = create_skill(
        "FastAPI Backend",
        "Help build and review reliable FastAPI services.",
        tmp_path,
        source="example docs",
    )
    assert skill_file.name == "SKILL.md"
    assert (skill_file.parent / "README.md").exists()
    assert (skill_file.parent / "SOURCE.txt").read_text() == "example docs\n"
    assert validate_skill(skill_file) == []


def test_reject_empty_description(tmp_path: Path):
    with pytest.raises(ValueError, match="Description cannot be empty"):
        create_skill("Test Skill", "  ", tmp_path)


def test_reject_description_over_limit(tmp_path: Path):
    with pytest.raises(ValueError, match="1024 characters or fewer"):
        create_skill("Test Skill", "x" * 1025, tmp_path)


def test_reject_existing_directory(tmp_path: Path):
    create_skill("Example", "A useful example skill.", tmp_path)
    with pytest.raises(FileExistsError):
        create_skill("Example", "Another description.", tmp_path)


def test_validate_missing_file(tmp_path: Path):
    issues = validate_skill(tmp_path / "missing")
    assert len(issues) == 1
    assert "not found" in issues[0]


def test_validate_invalid_frontmatter(tmp_path: Path):
    target = tmp_path / "SKILL.md"
    target.write_text("# no frontmatter\n", encoding="utf-8")
    assert "Missing YAML frontmatter at the start of the file." in validate_skill(target)


def test_validate_requires_name_description_and_body(tmp_path: Path):
    target = tmp_path / "SKILL.md"
    target.write_text("---\nunknown: value\n---\nShort\n", encoding="utf-8")
    issues = validate_skill(target)
    assert any("missing 'name'" in issue for issue in issues)
    assert any("missing 'description'" in issue for issue in issues)
    assert any("too short" in issue for issue in issues)


def test_validate_rejects_invalid_name(tmp_path: Path):
    target = tmp_path / "SKILL.md"
    target.write_text(
        '---\nname: Invalid_Name\ndescription: "A valid description."\n---\n'
        "These instructions contain enough words to be considered a useful body.\n",
        encoding="utf-8",
    )
    assert any("'name' must be lowercase" in issue for issue in validate_skill(target))
