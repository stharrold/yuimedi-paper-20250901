#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["keyring>=24.0.0"]
# ///
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Injects secrets from OS keyring into environment, then runs a command.

This is the ONE way to run commands that need secrets (e.g., gh CLI).
Do NOT set GH_TOKEN or GITHUB_TOKEN in shell profiles. Use this script.

Precedence:
    1. Environment variable already set -> use it (allows CI/container injection)
    2. CI detected (GITHUB_ACTIONS, etc.) -> require env vars, skip keyring
    3. Container detected (Docker/Podman) -> require env vars, skip keyring
    4. Local development -> fetch from OS keyring

Usage:
    uv run scripts/secrets_run.py <command> [args...]
    uv run scripts/secrets_run.py --root PATH <command> [args...]

Common patterns:
    # GitHub issue operations
    uv run scripts/secrets_run.py gh issue list --label "P0"
    uv run scripts/secrets_run.py gh issue create --title "..." --label "paper-1" --body "..."
    uv run scripts/secrets_run.py gh issue edit 123 --add-label "paper-1"

    # GitHub PR operations
    uv run scripts/secrets_run.py gh pr create --base develop --head contrib/stharrold --fill
    uv run scripts/secrets_run.py gh pr list

    # GitHub API (REST)
    uv run scripts/secrets_run.py gh api repos/stharrold/yuimedi-paper-20250901/issues/505

    # Run tests with secrets available
    uv run scripts/secrets_run.py uv run pytest

Setup:
    uv run scripts/secrets_setup.py          # First-time interactive setup
    uv run scripts/secrets_setup.py --check  # Verify keyring has required secrets
"""

from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from pathlib import Path

# Lazy import keyring only when needed (CI/containers don't need it)
keyring = None


def load_keyring() -> None:
    """Lazily import keyring module."""
    global keyring
    if keyring is None:
        import keyring as kr

        keyring = kr


def get_repo_root(target_path: Path | None = None) -> Path:
    """Get the repository root directory as an absolute path.

    Args:
        target_path: Optional manual override for the root path.
    """
    if target_path:
        return target_path.resolve()

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip()).resolve()
    except subprocess.CalledProcessError:
        # Fallback to script parent if not in git repo
        return Path(__file__).parent.parent.resolve()


def load_secrets_config(root_path: Path) -> dict:
    """Load secrets configuration from secrets.toml.

    Args:
        root_path: Project root directory.

    Returns:
        Dictionary with 'required', 'optional', and 'service' keys.
    """
    config_path = root_path / "secrets.toml"
    if not config_path.exists():
        print(f"[FAIL] secrets.toml not found at: {config_path}")
        print()
        print("Create a secrets.toml file at this location with a structure like:")
        print()
        print("[secrets]")
        print('required = ["DB_PASSWORD", "API_KEY"]')
        print('optional = ["ANALYTICS_TOKEN"]')
        print()
        print("[keyring]")
        print('service = "your-service-name"')
        sys.exit(1)

    # Use Python 3.11+ stdlib tomllib for robust TOML parsing
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    return {
        "required": data.get("secrets", {}).get("required", []),
        "optional": data.get("secrets", {}).get("optional", []),
        "service": data.get("keyring", {}).get("service", "default"),
    }


def is_ci() -> bool:
    """Detect if running in a CI environment.

    Checks for common CI environment variables.
    """
    ci_vars = [
        "CI",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "TF_BUILD",  # Azure DevOps
        "JENKINS_URL",
        "CIRCLECI",
        "TRAVIS",
        "BUILDKITE",
        "DRONE",
        "CODEBUILD_BUILD_ID",  # AWS CodeBuild
    ]
    return any(os.environ.get(var) for var in ci_vars)


def is_container() -> bool:
    """Detect if running inside a container.

    Checks for Docker, Podman, and Kubernetes indicators.
    """
    # Docker
    if Path("/.dockerenv").exists():
        return True

    # Podman
    if Path("/run/.containerenv").exists():
        return True

    # Check cgroup for container indicators
    cgroup_path = Path("/proc/1/cgroup")
    if cgroup_path.exists():
        try:
            content = cgroup_path.read_text()
            if "docker" in content or "kubepods" in content or "containerd" in content:
                return True
        except (OSError, PermissionError):
            # Cannot read cgroup info (e.g., due to permissions), assume not in container
            pass

    return False


def get_secret_from_keyring(service: str, name: str) -> str | None:
    """Fetch a secret from the OS keyring.

    Args:
        service: Keyring service/namespace.
        name: Secret name (used as username in keyring).

    Returns:
        Secret value or None if not found.
    """
    load_keyring()
    try:
        return keyring.get_password(service, name)
    except Exception as e:
        # Re-raise system exceptions that shouldn't be caught
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        print(f"[WARN] Keyring error for {name}: {e}")
        return None


def resolve_secret(
    name: str, service: str, in_ci: bool, in_container: bool
) -> tuple[str | None, str]:
    """Resolve a secret from available sources.

    Args:
        name: Secret name.
        service: Keyring service name.
        in_ci: Whether running in CI.
        in_container: Whether running in container.

    Returns:
        Tuple of (value, source) where source describes where the value came from.
    """
    # Check environment first (highest precedence)
    if name in os.environ:
        return os.environ[name], "environment"

    # In CI/container, keyring is not available
    if in_ci or in_container:
        return None, "not set (CI/container mode)"

    # Try keyring for local development
    value = get_secret_from_keyring(service, name)
    if value:
        return value, "keyring"

    return None, "not found"


def inject_secrets(config: dict) -> tuple[list[str], list[str]]:
    """Inject secrets into the environment.

    Args:
        config: Secrets configuration dictionary.

    Returns:
        Tuple of (missing_required, missing_optional) secret names.
    """
    in_ci = is_ci()
    in_container = is_container()
    service = config["service"]

    env_type = "CI" if in_ci else ("container" if in_container else "local")
    print(f"[INFO] Environment: {env_type}")

    missing_required: list[str] = []
    missing_optional: list[str] = []

    # Process required secrets
    for name in config["required"]:
        value, source = resolve_secret(name, service, in_ci, in_container)
        if value:
            os.environ[name] = value
            print(f"[OK] {name}: loaded from {source}")
        else:
            missing_required.append(name)
            print(f"[FAIL] {name}: {source} (service: {service})")

    # Process optional secrets
    for name in config["optional"]:
        value, source = resolve_secret(name, service, in_ci, in_container)
        if value:
            os.environ[name] = value
            print(f"[OK] {name}: loaded from {source}")
        else:
            missing_optional.append(name)
            print(f"[WARN] {name}: {source} (optional)")

    return missing_required, missing_optional


def print_usage() -> None:
    """Print usage information."""
    print("Usage: uv run scripts/secrets_run.py [options] <command> [args...]")
    print()
    print("Injects secrets from keyring/environment, then runs the command.")
    print()
    print("Options:")
    print("  --root PATH    Specify project root containing secrets.toml")
    print()
    print("Examples:")
    print("  uv run scripts/secrets_run.py uv run pytest")
    print("  uv run scripts/secrets_run.py --root ../my-project python main.py")
    print()
    print("Setup (local development):")
    print("  uv run scripts/secrets_setup.py")


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    args = sys.argv[1:]
    target_root = None

    # Parse --root flag manually before handing over to command
    # We only look at the start of args to avoid stealing flags from the wrapped command
    if len(args) > 0 and args[0] == "--root":
        if len(args) > 1:
            target_root = Path(args[1])
            del args[0:2]  # Remove --root and value
        else:
            print("[FAIL] Usage: --root <path>")
            return 1

    if len(args) < 1:
        print_usage()
        return 1

    # Load configuration
    root_path = get_repo_root(target_root)
    config = load_secrets_config(root_path)

    # Inject secrets
    missing_required, _ = inject_secrets(config)

    # Fail if required secrets are missing
    if missing_required:
        print()
        print("[FAIL] Missing required secrets:")
        for name in missing_required:
            print(f"  - {name}")
        print()
        if is_ci():
            print("In CI: Set these as repository secrets and map to env vars in workflow.")
        elif is_container():
            print("In container: Inject via -e flags or --secret mounts.")
        else:
            print("Local: Run 'uv run scripts/secrets_setup.py' to configure keyring.")
        return 1

    # Execute the command
    print()
    cmd = args
    print(f"[INFO] Running: {' '.join(cmd)}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        # Re-raise system exceptions
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        # Do not print cmd or environment variables to avoid leaking secrets
        print(f"[FAIL] Command execution failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
