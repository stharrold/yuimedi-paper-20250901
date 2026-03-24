# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Shared environment detection utilities.

Provides functions for detecting CI and container environments,
used by both secrets_setup.py and run.py (secrets_run.py).
"""

from __future__ import annotations

import os
from pathlib import Path


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
