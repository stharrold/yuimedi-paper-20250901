# Academic Literature Review Tool - Container Usage

Complete guide for running the Academic Literature Review Tool in containers using Docker or Podman.

## Quick Start

### Pull and Run

```bash
# Pull the latest image
docker pull ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest

# Run with help
docker run --rm ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest --help

# Initialize a review with volume
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  init "My Review" --question "What is the impact?"
```

### Using Podman

Podman is a drop-in replacement for Docker:

```bash
# Pull image
podman pull ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest

# Run (identical syntax)
podman run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  --help
```

## Container Features

### Multi-Stage Build

The container uses a multi-stage build for optimization:

1. **Builder stage**: Installs uv and dependencies
2. **Runtime stage**: Minimal image with only runtime requirements

**Benefits**:
- Small image size (~200MB vs ~1GB)
- Fast startup (<2s)
- Security hardening (non-root user)

### Security

- Runs as non-root user `reviewer` (UID 1000)
- No unnecessary packages installed
- Minimal attack surface
- Regular security updates

### Health Check

Built-in health check ensures container is functioning:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' container_name

# Health check command (runs every 30s)
python -c "import lit_review; print('OK')"
```

## Volume Management

### Data Persistence

Mount a volume to persist review data:

```bash
# Create data directory
mkdir -p review_data

# Run with volume
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  -e LIT_REVIEW_DATA_DIR=/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  init "My Review" -q "Question"
```

### Volume Location

Inside container: `/home/reviewer/data`

Mount from:
- **Linux/macOS**: `$(pwd)/review_data`
- **Windows (PowerShell)**: `${PWD}/review_data`
- **Windows (CMD)**: `%cd%/review_data`

### Permissions

The container runs as UID 1000. Ensure your host directory has appropriate permissions:

```bash
# Linux/macOS
chmod -R 755 review_data/
chown -R $(id -u):$(id -g) review_data/

# Or run container with your UID
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  --user $(id -u):$(id -g) \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  --help
```

## Environment Variables

### Required

None - the tool works without any environment variables.

### Optional

```bash
# Data directory location
-e LIT_REVIEW_DATA_DIR=/home/reviewer/data

# API keys
-e ANTHROPIC_API_KEY=sk-ant-...
-e PUBMED_EMAIL=your.email@example.com

# Logging
-e LOG_LEVEL=INFO
```

### Using .env File

Create `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-...
PUBMED_EMAIL=your.email@example.com
LIT_REVIEW_DATA_DIR=/home/reviewer/data
```

Run with env file:

```bash
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  --env-file .env \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  init "Review" -q "Question"
```

## Complete Workflow Example

```bash
# 1. Create data directory
mkdir -p review_data

# 2. Initialize review
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  init "ML Healthcare" \
  --question "What is the impact of ML in healthcare?" \
  --include "Peer-reviewed" \
  --include "English language"

# 3. Check status
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  status "ML Healthcare"

# 4. Advance to search stage
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  advance "ML Healthcare"

# 5. Search databases
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  search "ML Healthcare" \
  --database crossref \
  --keywords "machine learning healthcare"

# 6. Export results
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  export "ML Healthcare" \
  --format bibtex \
  --output /home/reviewer/data/refs.bib
```

## Docker Compose

### Basic Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  lit-review:
    image: ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest
    volumes:
      - ./review_data:/home/reviewer/data
    environment:
      - LIT_REVIEW_DATA_DIR=/home/reviewer/data
    command: ["--help"]
```

Usage:

```bash
# Show help
docker-compose run --rm lit-review --help

# Initialize
docker-compose run --rm lit-review init "Review" -q "Question"

# Status
docker-compose run --rm lit-review status "Review"
```

### With Environment Variables

```yaml
version: '3.8'

services:
  lit-review:
    image: ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest
    volumes:
      - ./review_data:/home/reviewer/data
    env_file:
      - .env
    command: ["--help"]
```

Create `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...
PUBMED_EMAIL=your.email@example.com
LIT_REVIEW_DATA_DIR=/home/reviewer/data
```

### Long-Running Service

For interactive development:

```yaml
version: '3.8'

services:
  lit-review:
    image: ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest
    volumes:
      - ./review_data:/home/reviewer/data
    environment:
      - LIT_REVIEW_DATA_DIR=/home/reviewer/data
    command: ["--version"]
    restart: "no"
```

## Building Custom Images

### Build from Source

```bash
# Clone repository
git clone https://github.com/stharrold/yuimedi-paper-20250901.git
cd yuimedi-paper-20250901

# Build image
docker build -f Containerfile.lit_review -t lit-review-tool:local .

# Test build
docker run --rm lit-review-tool:local --version
```

### Custom Containerfile

Modify `Containerfile.lit_review` for custom needs:

```dockerfile
# Add custom dependencies
RUN apt-get update && \
    apt-get install -y your-package && \
    apt-get clean

# Add custom Python packages
RUN uv pip install your-package
```

### Multi-Platform Builds

Build for multiple architectures:

```bash
# Enable buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f Containerfile.lit_review \
  -t lit-review-tool:multi \
  --push \
  .
```

## Performance Optimization

### Layer Caching

The Containerfile is optimized for layer caching:

1. Install uv (rarely changes)
2. Copy dependency files (changes with new deps)
3. Install dependencies (changes with new deps)
4. Copy application code (changes frequently)

### Image Size

Optimizations applied:

- Multi-stage build: ~80% size reduction
- Minimal base image: `python:3.11-slim-bookworm`
- No dev dependencies: ~50% size reduction
- Cleaned apt cache: ~30MB savings

### Startup Time

Optimizations:

- Pre-built virtual environment: ~5s savings
- No runtime compilation: immediate startup
- Health check: verifies quick startup

## Troubleshooting

### Permission Denied

```bash
# Check volume permissions
ls -la review_data/

# Fix permissions
chmod -R 755 review_data/
chown -R $(id -u):$(id -g) review_data/

# Or run as your user
docker run --rm \
  --user $(id -u):$(id -g) \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  --help
```

### Volume Not Mounting

```bash
# Verify volume path
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  bash -c "ls -la /home/reviewer/data"

# Use absolute path
docker run --rm \
  -v /absolute/path/to/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  --help
```

### Container Won't Start

```bash
# Check logs
docker logs container_name

# Check health
docker inspect --format='{{.State.Health.Status}}' container_name

# Run with debug
docker run --rm \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  python -c "import lit_review; print(lit_review.__version__)"
```

### Image Pull Fails

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull specific version
docker pull ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:v1.0.0

# Check available tags
curl https://ghcr.io/v2/stharrold/yuimedi-paper-20250901/lit-review-tool/tags/list
```

## Advanced Usage

### Interactive Shell

```bash
# Open shell in container
docker run --rm -it \
  -v $(pwd)/review_data:/home/reviewer/data \
  --entrypoint bash \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest

# Inside container
reviewer@container:~$ academic-review --help
reviewer@container:~$ python -c "import lit_review; print(lit_review.__version__)"
```

### Batch Processing

```bash
# Create script
cat > batch_review.sh <<'EOF'
#!/bin/bash
for review in "Review 1" "Review 2" "Review 3"; do
  docker run --rm \
    -v $(pwd)/review_data:/home/reviewer/data \
    ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
    status "$review"
done
EOF

chmod +x batch_review.sh
./batch_review.sh
```

### CI/CD Integration

GitHub Actions example:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest
    steps:
      - name: Run tests
        run: pytest tests/lit_review/ -v
```

## Security Best Practices

1. **Don't run as root**: Use `--user` flag
2. **Limit resources**: Use `--memory` and `--cpus` flags
3. **Read-only filesystem**: Use `--read-only` flag (with tmpfs for /tmp)
4. **Network isolation**: Use `--network none` if no API calls needed
5. **Secret management**: Use Docker secrets or vault, not environment variables

Example secure run:

```bash
docker run --rm \
  --user $(id -u):$(id -g) \
  --memory 512m \
  --cpus 1 \
  --read-only \
  --tmpfs /tmp \
  -v $(pwd)/review_data:/home/reviewer/data \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  status "Review"
```

## Support

- **Image Issues**: https://github.com/stharrold/yuimedi-paper-20250901/issues
- **Setup Guide**: [lit_review_setup.md](lit_review_setup.md)
- **Workflow Guide**: [lit_review_workflow.md](lit_review_workflow.md)
