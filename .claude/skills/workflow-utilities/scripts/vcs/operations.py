#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""VCS wrapper functions for GitHub and Azure DevOps.

Each function auto-detects the provider from the git remote URL unless
an explicit ``provider`` argument is given.  Errors from the underlying
CLI are surfaced as ``RuntimeError`` with the stderr message so that
callers can inspect strings like "already exists".

Constants:
- GITHUB_CLI / AZURE_CLI: CLI command names
  Rationale: Centralise for easier testing/mocking
- GITHUB_GRAPHQL_TEMPLATE: GraphQL query for PR review threads
  Rationale: GitHub requires GraphQL for isResolved status (not in REST API)
"""

import json
import subprocess

from .provider import VCSProvider, detect_provider

# CLI command names
GITHUB_CLI = "gh"
AZURE_CLI = "az"

# GraphQL query for GitHub review threads (moved from generate_work_items_from_pr.py)
GITHUB_GRAPHQL_TEMPLATE = """
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      url
      title
      reviewDecision
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          isCollapsed
          comments(first: 100) {
            nodes {
              id
              author {
                login
              }
              body
              url
              createdAt
              path
              line
            }
          }
        }
      }
    }
  }
}
"""


def _run(cmd: list[str], *, timeout: int = 30) -> str:
    """Run a CLI command and return stripped stdout.

    Raises:
        RuntimeError: On FileNotFoundError, CalledProcessError, or TimeoutExpired
    """
    try:
        result = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE, timeout=timeout)
        return result.strip()
    except FileNotFoundError:
        raise RuntimeError(f"'{cmd[0]}' CLI not found")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(error_msg)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Timeout while running: {' '.join(cmd)}")


# ---------------------------------------------------------------------------
# 1. get_username
# ---------------------------------------------------------------------------


def get_username(*, fallback: str | None = "", provider: VCSProvider | None = None) -> str:
    """Get the authenticated VCS username.

    Args:
        fallback: Value to return when the CLI call fails.
            ``""`` (default) returns an empty string on failure.
            ``None`` causes the RuntimeError to propagate.
        provider: Explicit provider; auto-detected if None.

    Returns:
        Username string.

    Raises:
        RuntimeError: If fallback is None and the CLI call fails.
    """
    if provider is None:
        provider = detect_provider()

    try:
        if provider == VCSProvider.GITHUB:
            return _run([GITHUB_CLI, "api", "user", "--jq", ".login"], timeout=10)
        elif provider == VCSProvider.AZURE_DEVOPS:
            return _run(
                [AZURE_CLI, "devops", "user", "show", "--query", "user.uniqueName", "-o", "tsv"],
                timeout=10,
            )
    except RuntimeError:
        if fallback is None:
            raise
        return fallback

    raise RuntimeError(f"Unsupported VCS provider: {provider}")


# ---------------------------------------------------------------------------
# 2. get_contrib_branch
# ---------------------------------------------------------------------------


def get_contrib_branch(
    *, fallback: str | None = "stharrold", provider: VCSProvider | None = None
) -> str:
    """Build ``contrib/<username>`` branch name.

    Consolidates three duplicate implementations across workflow scripts.

    Args:
        fallback: Username fallback when CLI call fails.
            ``"stharrold"`` (default) matches previous behaviour in
            backmerge_workflow.py / pr_workflow.py.
            ``None`` causes the RuntimeError to propagate (matches
            release_workflow.py behaviour).
        provider: Explicit provider; auto-detected if None.

    Returns:
        Branch name like ``contrib/stharrold``.

    Raises:
        RuntimeError: If fallback is None and username cannot be obtained.
    """
    username = get_username(fallback=fallback, provider=provider)
    if not username:
        if fallback is None:
            raise RuntimeError(
                "Failed to get VCS username. Ensure you are authenticated:\n"
                "  GitHub: gh auth login\n"
                "  Azure DevOps: az login\n\n"
                "Or specify the contrib branch explicitly."
            )
        username = fallback or "unknown"
    return f"contrib/{username}"


# ---------------------------------------------------------------------------
# 3. create_pr
# ---------------------------------------------------------------------------


def create_pr(
    *,
    base: str,
    head: str,
    title: str,
    body: str,
    fill: bool = False,
    provider: VCSProvider | None = None,
) -> str:
    """Create a pull request.

    Args:
        base: Target branch.
        head: Source branch.
        title: PR title.
        body: PR description.
        fill: If True, add ``--fill`` (GitHub only; ignored for Azure DevOps) to auto-fill title/body from commits.
        provider: Explicit provider; auto-detected if None.

    Returns:
        PR URL (GitHub) or PR ID string (Azure DevOps).

    Raises:
        RuntimeError: If PR creation fails (message contains stderr for
            callers to inspect e.g. "already exists").
    """
    if provider is None:
        provider = detect_provider()

    if provider == VCSProvider.GITHUB:
        cmd = [GITHUB_CLI, "pr", "create", "--base", base, "--head", head]
        if fill:
            cmd.append("--fill")
        if title:
            cmd.extend(["--title", title])
        if body:
            cmd.extend(["--body", body])
        return _run(cmd, timeout=30)

    elif provider == VCSProvider.AZURE_DEVOPS:
        cmd = [
            AZURE_CLI,
            "repos",
            "pr",
            "create",
            "--target-branch",
            base,
            "--source-branch",
            head,
            "--title",
            title,
            "--description",
            body,
        ]
        return _run(cmd, timeout=30)

    raise RuntimeError(f"Unsupported provider: {provider}")


# ---------------------------------------------------------------------------
# 4. create_release
# ---------------------------------------------------------------------------


def create_release(version: str, *, provider: VCSProvider | None = None) -> str | None:
    """Create a VCS release (e.g. GitHub Release).

    Args:
        version: Semantic version tag (e.g. ``v1.6.0``).
        provider: Explicit provider; auto-detected if None.

    Returns:
        Release URL on success, ``None`` if not applicable (Azure DevOps).

    Raises:
        RuntimeError: If release creation fails on GitHub.
    """
    if provider is None:
        provider = detect_provider()

    if provider == VCSProvider.GITHUB:
        return _run([GITHUB_CLI, "release", "create", version, "--generate-notes"], timeout=30)

    elif provider == VCSProvider.AZURE_DEVOPS:
        # Azure DevOps has no direct CLI equivalent for releases
        return None

    raise RuntimeError(f"Unsupported provider: {provider}")


# ---------------------------------------------------------------------------
# 5. create_issue
# ---------------------------------------------------------------------------


def create_issue(
    *,
    title: str,
    body: str,
    labels: list[str] | None = None,
    assignee_self: bool = False,
    provider: VCSProvider | None = None,
) -> str:
    """Create an issue / work-item.

    Args:
        title: Issue title.
        body: Issue description.
        labels: Labels to apply (GitHub only).
        assignee_self: Assign to current user (GitHub ``@me``).
        provider: Explicit provider; auto-detected if None.

    Returns:
        Issue URL (GitHub) or work-item ID (Azure DevOps).

    Raises:
        RuntimeError: If creation fails.
    """
    if provider is None:
        provider = detect_provider()

    if provider == VCSProvider.GITHUB:
        cmd = [GITHUB_CLI, "issue", "create", "--title", title, "--body", body]
        for label in labels or []:
            cmd.extend(["--label", label])
        if assignee_self:
            cmd.extend(["--assignee", "@me"])
        return _run(cmd, timeout=30)

    elif provider == VCSProvider.AZURE_DEVOPS:
        cmd = [
            AZURE_CLI,
            "boards",
            "work-item",
            "create",
            "--type",
            "Task",
            "--title",
            title,
            "--description",
            body,
        ]
        return _run(cmd, timeout=30)

    raise RuntimeError(f"Unsupported provider: {provider}")


# ---------------------------------------------------------------------------
# 6. query_pr_review_threads
# ---------------------------------------------------------------------------


def query_pr_review_threads(pr_number: int, *, provider: VCSProvider | None = None) -> list[dict]:
    """Fetch unresolved PR review threads.

    Args:
        pr_number: Pull request number.
        provider: Explicit provider; auto-detected if None.

    Returns:
        List of conversation dicts with keys: id, url, file, line,
        author, body, created_at.

    Raises:
        RuntimeError: If the query fails.
    """
    if provider is None:
        provider = detect_provider()

    if provider == VCSProvider.GITHUB:
        return _query_github_review_threads(pr_number)
    elif provider == VCSProvider.AZURE_DEVOPS:
        return _query_azure_review_threads(pr_number)

    raise RuntimeError(f"Unsupported provider: {provider}")


def _parse_github_remote() -> tuple[str, str]:
    """Parse owner/repo from git remote URL.

    Returns:
        (owner, repo) tuple.

    Raises:
        RuntimeError: If parsing fails.
    """
    try:
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            text=True,
            stderr=subprocess.PIPE,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(f"Failed to read git remote URL: {e}")

    if remote_url.startswith("https://"):
        parts = remote_url.replace("https://github.com/", "").replace(".git", "").split("/")
    elif remote_url.startswith("git@"):
        parts = remote_url.replace("git@github.com:", "").replace(".git", "").split("/")
    else:
        raise RuntimeError(f"Unsupported remote URL format: {remote_url}")

    try:
        return parts[0], parts[1]
    except IndexError:
        raise RuntimeError(f"Failed to parse owner/repo from: {remote_url}")


def _query_github_review_threads(pr_number: int) -> list[dict]:
    """Fetch unresolved GitHub PR review threads via GraphQL."""
    owner, repo = _parse_github_remote()

    raw = _run(
        [
            GITHUB_CLI,
            "api",
            "graphql",
            "-f",
            f"query={GITHUB_GRAPHQL_TEMPLATE}",
            "-f",
            f"owner={owner}",
            "-f",
            f"repo={repo}",
            "-F",
            f"pr={pr_number}",
        ],
        timeout=30,
    )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse GitHub GraphQL response: {e}")

    try:
        pr_data = data["data"]["repository"]["pullRequest"]
        review_threads = pr_data["reviewThreads"]["nodes"]
    except (KeyError, TypeError) as e:
        raise RuntimeError(f"Failed to parse GitHub review threads: {e}")

    conversations: list[dict] = []
    for thread in review_threads:
        if thread["isResolved"]:
            continue
        if not thread["comments"]["nodes"]:
            continue

        first_comment = thread["comments"]["nodes"][0]
        conversations.append(
            {
                "id": thread["id"],
                "url": first_comment.get("url", f"{pr_data['url']}#discussion_{thread['id']}"),
                "file": first_comment.get("path"),
                "line": first_comment.get("line"),
                "author": first_comment["author"]["login"]
                if first_comment.get("author")
                else "Unknown",
                "body": first_comment["body"],
                "created_at": first_comment["createdAt"],
            }
        )

    return conversations


def _query_azure_review_threads(pr_number: int) -> list[dict]:
    """Fetch Azure DevOps PR threads via REST API."""
    raw = _run(
        [
            AZURE_CLI,
            "devops",
            "invoke",
            "--area",
            "git",
            "--resource",
            "pullRequestThreads",
            "--route-parameters",
            f"pullRequestId={pr_number}",
            "--api-version",
            "7.0",
            "--query",
            "[?status=='active'].{id:id, comments:comments}",
            "-o",
            "json",
        ],
        timeout=30,
    )

    try:
        threads = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse Azure DevOps threads: {e}")

    conversations: list[dict] = []
    for thread in threads or []:
        comments = thread.get("comments", [])
        if not comments:
            continue
        first = comments[0]
        conversations.append(
            {
                "id": str(thread.get("id", "")),
                "url": "",
                "file": first.get("_links", {}).get("self", {}).get("href", ""),
                "line": None,
                "author": first.get("author", {}).get("uniqueName", "Unknown"),
                "body": first.get("content", ""),
                "created_at": first.get("publishedDate", ""),
            }
        )

    return conversations


# ---------------------------------------------------------------------------
# 7. check_auth
# ---------------------------------------------------------------------------


def check_auth(*, provider: VCSProvider | None = None) -> bool:
    """Check if the user is authenticated with the VCS provider.

    Args:
        provider: Explicit provider; auto-detected if None.

    Returns:
        True if authenticated, False otherwise.
    """
    if provider is None:
        provider = detect_provider()

    try:
        if provider == VCSProvider.GITHUB:
            _run([GITHUB_CLI, "auth", "status"], timeout=10)
        elif provider == VCSProvider.AZURE_DEVOPS:
            _run([AZURE_CLI, "account", "show"], timeout=10)
        else:
            return False
    except RuntimeError:
        return False

    return True
