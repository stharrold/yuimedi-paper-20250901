#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""VCS provider detection.

This module provides VCS provider enumeration and auto-detection from git remote URL.

Constants:
- _cached_provider: Module-level cache for detected provider
  Rationale: Avoid repeated subprocess calls within a single process
"""

import subprocess
from enum import Enum

# Module-level cache for detected provider
_cached_provider: "VCSProvider | None" = None


class VCSProvider(Enum):
    """Supported VCS providers."""

    GITHUB = "github"
    AZURE_DEVOPS = "azure_devops"


def detect_provider() -> VCSProvider:
    """Auto-detect VCS provider from git remote URL.

    Parses ``git config --get remote.origin.url`` and matches against known hosts.

    Returns:
        VCSProvider.GITHUB or VCSProvider.AZURE_DEVOPS

    Raises:
        RuntimeError: If remote URL cannot be determined or provider is unrecognised
    """
    global _cached_provider
    if _cached_provider is not None:
        return _cached_provider

    try:
        url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            text=True,
            stderr=subprocess.PIPE,
            timeout=10,
        ).strip()
    except FileNotFoundError:
        raise RuntimeError("'git' CLI not found")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to read git remote URL: {e.stderr.strip() if e.stderr else str(e)}"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Timeout while reading git remote URL")

    if "github.com" in url:
        _cached_provider = VCSProvider.GITHUB
    elif "dev.azure.com" in url or "visualstudio.com" in url:
        _cached_provider = VCSProvider.AZURE_DEVOPS
    else:
        raise RuntimeError(f"Unrecognised VCS provider in remote URL: {url}")

    return _cached_provider
