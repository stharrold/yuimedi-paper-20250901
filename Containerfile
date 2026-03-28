# Containerfile for yuimedi-paper-20250901
# Python 3.11 + uv + pandoc + texlive for development, CI/CD, and paper generation
#
# Build:  podman build -t yuimedi-paper .
# Run:    podman run --rm -v .:/app yuimedi-paper <command>
# Shell:  podman run --rm -it -v .:/app yuimedi-paper bash
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
LABEL description="YuiQuery research environment with uv + Python 3.11 + pandoc + texlive"

# Install system dependencies including pandoc and texlive for paper generation
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-latex-recommended \
    lmodern \
    librsvg2-bin \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ENV UV_VERSION=0.5.5
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files first (for layer caching)
# LICENSE and README.md are required because pyproject.toml references
# license = {file = "LICENSE"} and readme = "README.md", and hatchling
# validates these files exist during editable install
COPY pyproject.toml uv.lock* LICENSE README.md ./

# Install dependencies
RUN uv sync --frozen 2>/dev/null || uv sync

# Copy project files
COPY . .

# Set default command
CMD ["bash"]
