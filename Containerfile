# Containerfile for stharrold-templates
# Python 3.11 + uv environment for development and CI/CD
#
# Build:  podman build -t stharrold-templates .
# Run:    podman run --rm -v .:/app stharrold-templates <command>
# Shell:  podman run --rm -it -v .:/app stharrold-templates bash
#
# Secrets Management:
#   Secrets are detected via environment variables at runtime.
#   The container auto-detects it's running in a container environment.
#
#   Podman (recommended - uses secrets store):
#     podman run --secret db_pass,type=env,target=DB_PASSWORD \
#                --secret api_key,type=env,target=API_KEY \
#                -v .:/app stharrold-templates uv run scripts/run.py pytest
#
#   Docker/Podman (direct env vars):
#     docker run -e DB_PASSWORD="$DB_PASSWORD" -e API_KEY="$API_KEY" \
#                -v .:/app stharrold-templates uv run scripts/run.py pytest
#
#   See secrets.toml for required/optional secret definitions.

FROM python:3.11-slim

LABEL maintainer="stharrold"
LABEL description="MCP templates development environment with uv + Python 3.11"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ENV UV_VERSION=0.5.5
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen 2>/dev/null || uv sync

# Copy project files
COPY . .

# Set default command
CMD ["bash"]
