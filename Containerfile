# Containerfile for yuimedi-paper-20250901
# Python 3.11 + uv environment for development and CI/CD
#
# Build:  podman build -t yuimedi-paper .
# Run:    podman run --rm -v .:/app yuimedi-paper <command>
# Shell:  podman run --rm -it -v .:/app yuimedi-paper bash

FROM python:3.12-slim

LABEL maintainer="stharrold"
LABEL description="YuiQuery research development environment with uv + Python 3.12"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install PDF generation dependencies (pandoc + texlive)
# Note: This adds ~450MB to the image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    lmodern \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Install Eisvogel template for academic PDF formatting
RUN mkdir -p /root/.local/share/pandoc/templates && \
    curl -sL https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz | \
    tar xz -C /root/.local/share/pandoc/templates --strip-components=1

# Install uv
ENV UV_VERSION=0.5.5
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files first (for layer caching)
# LICENSE and README.md required by hatchling build backend
COPY pyproject.toml uv.lock* LICENSE README.md ./

# Install dependencies (including dev and workflow extras for full functionality)
RUN uv sync --frozen --all-extras 2>/dev/null || uv sync --all-extras

# Copy project files
COPY . .

# Set default command
CMD ["bash"]
