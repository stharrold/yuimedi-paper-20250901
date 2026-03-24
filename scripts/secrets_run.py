#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["keyring>=24.0.0"]
# ///
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Universal secrets injector for cross-platform secret management.

This script injects secrets into the environment before running a command.
It supports multiple secret sources with the following precedence:

1. Environment variable already set -> use it (allows external injection)
2. CI detected -> require env vars, skip keyring
3. Container detected -> require env vars, skip keyring
4. Local development -> fetch from OS keyring

Usage:
    uv run scripts/secrets_run.py [options] <command> [args...]
    uv run scripts/secrets_run.py [options] --get-to-stdout SECRET_NAME

Options:
    --root PATH                Specify project root containing secrets.toml
    --get-to-stdout SECRET_NAME  Print a single secret value to stdout (pipe-friendly)

Example:
    uv run scripts/secrets_run.py uv run pytest
    uv run scripts/secrets_run.py --root ../project python main.py
    uv run scripts/secrets_run.py --get-to-stdout API_KEY | pbcopy
    export TOKEN=$(uv run scripts/secrets_run.py --get-to-stdout API_TOKEN)
"""

from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from pathlib import Path

from scripts.environment_utils import is_ci, is_container

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
        print(f"[FAIL] secrets.toml not found at: {config_path}", file=sys.stderr)
        print(file=sys.stderr)
        print("Create a secrets.toml file at this location with a structure like:", file=sys.stderr)
        print(file=sys.stderr)
        print("[secrets]", file=sys.stderr)
        print('required = ["DB_PASSWORD", "API_KEY"]', file=sys.stderr)
        print('optional = ["ANALYTICS_TOKEN"]', file=sys.stderr)
        print(file=sys.stderr)
        print("[keyring]", file=sys.stderr)
        print('service = "your-service-name"', file=sys.stderr)
        sys.exit(1)

    # Use Python 3.11+ stdlib tomllib for robust TOML parsing
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    return {
        "required": data.get("secrets", {}).get("required", []),
        "optional": data.get("secrets", {}).get("optional", []),
        "service": data.get("keyring", {}).get("service", "default"),
    }


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


def get_secret_to_stdout(secret_name: str, root_path: Path) -> int:
    """Print a single secret value to stdout.

    All diagnostics go to stderr. Stdout contains only the raw secret value.

    Args:
        secret_name: Name of the secret to retrieve.
        root_path: Project root directory containing secrets.toml.

    Returns:
        0 on success, 1 on failure.
    """
    config = load_secrets_config(root_path)

    all_secrets = list(config["required"]) + list(config["optional"])
    if secret_name not in all_secrets:
        print(f"[FAIL] Secret '{secret_name}' is not defined in secrets.toml", file=sys.stderr)
        return 1

    in_ci = is_ci()
    in_container = is_container()
    service = config["service"]

    env_type = "CI" if in_ci else ("container" if in_container else "local")
    print(f"[INFO] Environment: {env_type}", file=sys.stderr)

    value, source = resolve_secret(secret_name, service, in_ci, in_container)
    if value is None:
        print(f"[FAIL] {secret_name}: {source} (service: {service})", file=sys.stderr)
        return 1

    print(f"[OK] {secret_name}: loaded from {source}", file=sys.stderr)
    sys.stdout.write(value)
    return 0


def print_usage() -> None:
    """Print usage information."""
    print("Usage: uv run scripts/secrets_run.py [options] <command> [args...]")
    print("       uv run scripts/secrets_run.py [options] --get-to-stdout SECRET_NAME")
    print()
    print("Injects secrets from keyring/environment, then runs the command.")
    print()
    print("Options:")
    print("  --root PATH                  Specify project root containing secrets.toml")
    print("  --get-to-stdout SECRET_NAME  Print a single secret to stdout (pipe-friendly)")
    print()
    print("Examples:")
    print("  uv run scripts/secrets_run.py uv run pytest")
    print("  uv run scripts/secrets_run.py --root ../my-project python main.py")
    print("  uv run scripts/secrets_run.py --get-to-stdout API_KEY | pbcopy")
    print("  export TOKEN=$(uv run scripts/secrets_run.py --get-to-stdout API_TOKEN)")
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
        try:
            if len(args) > 1:
                target_root = Path(args[1])
                del args[0:2]  # Remove --root and value
            else:
                print("[FAIL] Usage: --root <path>")
                return 1
        except IndexError:
            pass

    # Check for --get-to-stdout mode
    if len(args) > 0 and args[0] == "--get-to-stdout":
        if len(args) < 2:
            print("[FAIL] Usage: --get-to-stdout SECRET_NAME", file=sys.stderr)
            return 1
        secret_name = args[1]
        remaining = args[2:]
        if remaining:
            print("[FAIL] --get-to-stdout is mutually exclusive with command mode", file=sys.stderr)
            return 1
        return get_secret_to_stdout(secret_name, get_repo_root(target_root))

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
