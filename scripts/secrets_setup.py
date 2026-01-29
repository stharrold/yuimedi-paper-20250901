#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["keyring>=24.0.0", "tomlkit"]
# ///
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Interactive keyring setup for secrets management.

Stores secret values in the OS keyring for local development.
Reads secret names from secrets.toml (which is committed to git; no values).

Usage:
    uv run scripts/secrets_setup.py                     # Interactive setup (all secrets)
    uv run scripts/secrets_setup.py --check             # Verify secrets exist in keyring
    uv run scripts/secrets_setup.py --set GH_TOKEN      # Set/update one secret (prompts)
    uv run scripts/secrets_setup.py --root PATH         # Use a different project root

First-time setup:
    1. Create a GitHub fine-grained PAT at https://github.com/settings/tokens?type=beta
       Required permissions: Issues (R/W), Pull requests (R/W), Contents (R/W)
    2. Run: uv run scripts/secrets_setup.py
    3. Paste the token when prompted for GH_TOKEN
    4. Verify: uv run scripts/secrets_setup.py --check

After regenerating a PAT:
    uv run scripts/secrets_setup.py --set GH_TOKEN

Cross-platform keyring backends:
    macOS: Keychain Access (service = "yuimedi-paper-20250901")
    Windows: Credential Manager (Windows Credential Locker)
    Linux: GNOME Keyring / KWallet (SecretService API)
"""

from __future__ import annotations

import getpass
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import keyring
import tomlkit


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
        root_path: The project root directory.

    Returns:
        Dictionary with 'required', 'optional', and 'service' keys.
    """
    config_path = root_path / "secrets.toml"
    if not config_path.exists():
        print(f"[FAIL] secrets.toml not found at: {config_path}")
        print()
        print("This file is required to configure which secrets should be stored in the keyring.")
        print("Create a secrets.toml file at the path above with content similar to:")
        print()
        print("[secrets]")
        print('required = ["EXAMPLE_REQUIRED_SECRET"]')
        print('optional = ["EXAMPLE_OPTIONAL_SECRET"]')
        print()
        print("[keyring]")
        print('service = "your-service-name"')
        print()
        print("Update the example names to match the secrets your project needs.")
        sys.exit(1)

    # Use Python 3.11+ stdlib tomllib for robust TOML parsing
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    return {
        "required": data.get("secrets", {}).get("required", []),
        "optional": data.get("secrets", {}).get("optional", []),
        "service": data.get("keyring", {}).get("service", "default"),
    }


def add_secret_to_config(root_path: Path, name: str, is_required: bool) -> bool:
    """Add a secret to secrets.toml using tomlkit to preserve formatting.

    Args:
        root_path: The project root directory.
        name: Secret name.
        is_required: If True, add to 'required' list, else 'optional'.

    Returns:
        True if successful, False otherwise.
    """
    config_path = root_path / "secrets.toml"
    if not config_path.exists():
        print(f"[FAIL] secrets.toml not found at: {config_path}")
        return False

    try:
        with open(config_path, encoding="utf-8") as f:
            doc = tomlkit.parse(f.read())

        # Ensure [secrets] table exists
        secrets_section = doc.get("secrets")
        if secrets_section is None:
            doc["secrets"] = tomlkit.table()
            secrets_section = doc["secrets"]

        key = "required" if is_required else "optional"

        # Ensure list exists
        current_list = secrets_section.get(key)
        if current_list is None:
            secrets_section[key] = []
            current_list = secrets_section[key]

        # Add if not present
        if name not in current_list:
            current_list.append(name)

            with open(config_path, "w", encoding="utf-8") as f:
                f.write(doc.as_string())
            print(f"[INFO] Added '{name}' to '{key}' secrets in secrets.toml")
            return True
        else:
            print(f"[INFO] '{name}' already exists in '{key}' secrets")
            return True

    except Exception as e:
        print(f"[FAIL] Failed to update secrets.toml: {e}")
        return False


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


def get_secret(service: str, name: str) -> str | None:
    """Get a secret from keyring.

    Args:
        service: Keyring service name.
        name: Secret name.

    Returns:
        Secret value or None if not found.
    """
    try:
        return keyring.get_password(service, name)
    except Exception as e:
        # Re-raise system exceptions that shouldn't be caught
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        print(f"[WARN] Keyring error for {name}: {e}")
        return None


def set_secret(service: str, name: str, value: str) -> bool:
    """Set a secret in keyring.

    Args:
        service: Keyring service name.
        name: Secret name.
        value: Secret value.

    Returns:
        True if successful, False otherwise.
    """
    try:
        keyring.set_password(service, name, value)
        return True
    except Exception as e:
        print(f"[FAIL] Error setting {name}: {e}")
        return False


def check_secrets(config: dict) -> int:
    """Check if all secrets exist in keyring.

    Args:
        config: Secrets configuration.

    Returns:
        Exit code (0 if all present, 1 if any missing).
    """
    service = config["service"]
    all_secrets = config["required"] + config["optional"]
    missing: list[str] = []

    print(f"[INFO] Checking secrets for service: {service}")
    print()

    for name in all_secrets:
        value = get_secret(service, name)
        if value:
            print(f"[OK] {name}: configured")
        else:
            print(f"[FAIL] {name}: not found")
            missing.append(name)

    print()
    if missing:
        print(f"[FAIL] Missing {len(missing)} secret(s)")
        print("Run 'uv run scripts/secrets_setup.py' to configure.")
        return 1
    else:
        print("[OK] All secrets configured")
        return 0


def setup_secret(service: str, name: str, is_optional: bool = False) -> bool:
    """Interactively set up a single secret.

    Args:
        service: Keyring service name.
        name: Secret name.
        is_optional: Whether the secret is optional.

    Returns:
        True if secret is now configured, False otherwise.
    """
    existing = get_secret(service, name)
    optional_tag = " (optional)" if is_optional else ""

    if existing:
        print(f"{name}{optional_tag}: [exists]", end=" ", flush=True)
        response = input("Keep existing value? [Y/n]: ").strip().lower()
        if response in ("", "y", "yes"):
            print("  -> Kept existing value")
            return True

    if is_optional:
        # Use getpass for consistency and security (hides input)
        response = getpass.getpass(f"{name}{optional_tag} - Enter value (or press Enter to skip): ")
        if not response:
            print("  -> Skipped")
            return True  # Optional secrets can be skipped
    else:
        response = getpass.getpass(f"{name}{optional_tag} - Enter value: ")
        if not response:
            print("  -> [FAIL] Required secret cannot be empty")
            return False

    if set_secret(service, name, response):
        print("  -> [OK] Saved to keyring")
        return True
    return False


def interactive_setup(config: dict) -> int:
    """Run interactive setup for all secrets.

    Args:
        config: Secrets configuration.

    Returns:
        Exit code (0 if successful, 1 if any required secrets failed).
    """
    service = config["service"]
    print(f"[INFO] Setting up secrets for service: {service}")
    print()

    failed_required: list[str] = []

    # Setup required secrets
    if config["required"]:
        print("Setting up required secrets:")
        for name in config["required"]:
            if not setup_secret(service, name, is_optional=False):
                failed_required.append(name)
        print()

    # Setup optional secrets
    if config["optional"]:
        print("Setting up optional secrets:")
        for name in config["optional"]:
            setup_secret(service, name, is_optional=True)
        print()

    # Verify configuration
    print("-" * 40)
    if failed_required:
        print(f"[FAIL] Failed to configure {len(failed_required)} required secret(s):")
        for name in failed_required:
            print(f"  - {name}")
        return 1
    else:
        print("[OK] All secrets configured successfully")
        print()
        print("You can now run commands with secrets:")
        print("  uv run scripts/secrets_run.py <command>")
        return 0


def set_single_secret_cmd(
    root_path: Path, config: dict, name: str, value: str | None = None
) -> int:
    """Set a single secret, optionally prompting for value.

    Args:
        root_path: The project root directory.
        config: Secrets configuration.
        name: Secret name.
        value: Secret value (optional).

    Returns:
        Exit code.
    """
    service = config["service"]

    # Check if secret is defined in config
    all_secrets = config["required"] + config["optional"]
    if name not in all_secrets:
        print(f"[WARN] '{name}' is not defined in secrets.toml")
        should_add = input(f"Add '{name}' to secrets.toml? [Y/n]: ").strip().lower()
        if should_add in ("", "y", "yes"):
            is_req_input = (
                input("Add to 'required' list? (default: optional) [y/N]: ").strip().lower()
            )
            is_required = is_req_input in ("y", "yes")
            if add_secret_to_config(root_path, name, is_required):
                # We assume success means it's now in the file.
                pass

    if value is None:
        print(f"Setting secret: {name}")
        # Use getpass to hide input
        value = getpass.getpass("Enter value: ")
        if not value:
            print("[FAIL] Secret value cannot be empty")
            return 1

    if set_secret(service, name, value):
        print(f"[OK] Secret '{name}' saved to keyring service '{service}'")
        return 0
    return 1


def print_usage() -> None:
    """Print usage information."""
    print("Usage: uv run scripts/secrets_setup.py [options]")
    print()
    print("Options:")
    print("  --check              Verify secrets exist without modifying")
    print("  --set <name>         Set a specific secret (always prompts securely)")
    print("  --root <path>        Specify the project root (defaults to CWD)")
    print("  --help               Show this help message")
    print()
    print("Examples:")
    print("  uv run scripts/secrets_setup.py                       # Interactive setup (all)")
    print("  uv run scripts/secrets_setup.py --check               # Verify secrets")
    print("  uv run scripts/secrets_setup.py --set API_KEY         # Set one secret (prompt)")
    print("  uv run scripts/secrets_setup.py --root ../my-project  # Set secrets for other repo")


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    # Check for CI/container environment
    if is_ci():
        print("[WARN] Running in CI environment.")
        print("Keyring setup is not applicable in CI.")
        print("Configure secrets as environment variables in your CI workflow.")
        return 1

    if is_container():
        print("[WARN] Running in container environment.")
        print("Keyring setup is not applicable in containers.")
        print("Inject secrets via -e flags or --secret mounts.")
        return 1

    # Parse arguments
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_usage()
        return 0

    target_root = None
    if "--root" in args:
        idx = args.index("--root")
        if len(args) > idx + 1:
            target_root = Path(args[idx + 1])
            # Clean up args so other parsers don't get confused
            del args[idx : idx + 2]
        else:
            print("[FAIL] Usage: --root <path>")
            return 1

    # Determine project root and load config
    root_path = get_repo_root(target_root)
    config = load_secrets_config(root_path)

    if "--check" in args:
        return check_secrets(config)

    if "--set" in args:
        try:
            idx = args.index("--set")
            if len(args) <= idx + 1:
                print("[FAIL] Usage: --set <name>")
                return 1

            name = args[idx + 1]

            # Do not accept secret values as CLI arguments to avoid leaks
            # via shell history and process listings. Always prompt securely.
            if len(args) > idx + 2:
                print("[FAIL] Usage: --set <name>")
                print(
                    "Do not pass secret values on the command line; you will be prompted securely."
                )
                return 1

            return set_single_secret_cmd(root_path, config, name, None)
        except IndexError:
            print("[FAIL] Usage: --set <name>")
            return 1

    return interactive_setup(config)


if __name__ == "__main__":
    sys.exit(main())
