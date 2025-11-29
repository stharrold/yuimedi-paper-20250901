"""Safe cross-platform output utilities with ASCII-only symbols.

Uses ASCII-only characters for maximum compatibility with:
- Legacy systems without Unicode support
- Windows terminals with encoding issues (cp1252)
- CI/CD environments with limited character sets
- SSH sessions with misconfigured locales

Issue: #102
"""

from typing import Any

# ASCII-only symbols for maximum compatibility
# Rationale: Simplicity over configurability - guaranteed compatibility
SYMBOLS = {
    "checkmark": "[OK]",
    "cross": "[FAIL]",
    "arrow": "->",
    "bullet": "*",
    "warning": "[WARN]",
    "info": "[INFO]",
}


def safe_print(*args: Any, **kwargs: Any) -> None:
    """Print function wrapper for consistency.

    Note: With ASCII-only symbols, no special handling is needed.
    This function is kept for API compatibility.
    """
    print(*args, **kwargs)


def format_check(message: str) -> str:
    """Format a success message with checkmark."""
    return f"{SYMBOLS['checkmark']} {message}"


def format_cross(message: str) -> str:
    """Format an error message with cross."""
    return f"{SYMBOLS['cross']} {message}"


def format_arrow(left: str, right: str) -> str:
    """Format an arrow between two items."""
    return f"{left} {SYMBOLS['arrow']} {right}"


def format_warning(message: str) -> str:
    """Format a warning message."""
    return f"{SYMBOLS['warning']} {message}"


def format_info(message: str) -> str:
    """Format an info message."""
    return f"{SYMBOLS['info']} {message}"


# Convenience functions
def print_success(message: str) -> None:
    """Print a success message."""
    safe_print(format_check(message))


def print_error(message: str) -> None:
    """Print an error message."""
    safe_print(format_cross(message))


def print_warning(message: str) -> None:
    """Print a warning message."""
    safe_print(format_warning(message))


def print_info(message: str) -> None:
    """Print an info message."""
    safe_print(format_info(message))
