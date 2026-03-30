#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""VCS interface for workflow scripts (GitHub + Azure DevOps).

This module provides wrapper functions for interacting with GitHub (gh)
and Azure DevOps (az) CLIs.  The provider is auto-detected from the
git remote URL.

Usage:
    from vcs import get_username, get_contrib_branch, create_pr

    username = get_username()
    branch = get_contrib_branch()
    pr_url = create_pr(base="develop", head="contrib/user", title="...", body="...")
"""

from .operations import (
    GITHUB_GRAPHQL_TEMPLATE,
    check_auth,
    create_issue,
    create_pr,
    create_release,
    get_contrib_branch,
    get_username,
    query_pr_review_threads,
)
from .provider import VCSProvider, detect_provider

__all__ = [
    "VCSProvider",
    "check_auth",
    "create_issue",
    "create_pr",
    "create_release",
    "detect_provider",
    "get_contrib_branch",
    "get_username",
    "query_pr_review_threads",
    "GITHUB_GRAPHQL_TEMPLATE",
]
