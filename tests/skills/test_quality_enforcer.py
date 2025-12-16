# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for quality-enforcer skill."""

from pathlib import Path


def test_quality_enforcer_skill_exists(skills_dir: Path) -> None:
    """Verify quality-enforcer skill directory exists."""
    skill_path = skills_dir / "quality-enforcer"
    assert skill_path.exists(), f"quality-enforcer skill not found at {skill_path}"


def test_quality_enforcer_has_required_files(skills_dir: Path) -> None:
    """Verify quality-enforcer has required files."""
    skill_path = skills_dir / "quality-enforcer"

    required_files = ["SKILL.md", "CLAUDE.md"]
    for filename in required_files:
        file_path = skill_path / filename
        assert file_path.exists(), f"Required file {filename} not found in quality-enforcer"


def test_quality_enforcer_scripts_exist(skills_dir: Path) -> None:
    """Verify quality-enforcer has scripts directory with required scripts."""
    scripts_path = skills_dir / "quality-enforcer" / "scripts"
    assert scripts_path.exists(), "quality-enforcer/scripts not found"

    required_scripts = ["run_quality_gates.py"]
    for script in required_scripts:
        script_path = scripts_path / script
        assert script_path.exists(), f"Required script {script} not found"


def test_run_quality_gates_is_importable(skills_dir: Path) -> None:
    """Verify run_quality_gates.py has valid Python syntax."""
    script_path = skills_dir / "quality-enforcer" / "scripts" / "run_quality_gates.py"
    content = script_path.read_text()
    # Check it compiles (valid syntax)
    compile(content, str(script_path), "exec")
