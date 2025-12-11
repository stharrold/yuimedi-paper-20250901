#!/usr/bin/env bash
#
# build_paper.sh - Generate PDF, HTML, DOCX, or LaTeX from paper.md
#
# Usage:
#   ./scripts/build_paper.sh [--format FORMAT] [--help]
#
# Options:
#   --format FORMAT  Output format: pdf (default), html, docx, latex, all
#   --help           Show this help message
#
# Examples:
#   ./scripts/build_paper.sh                  # Generate PDF
#   ./scripts/build_paper.sh --format html    # Generate HTML
#   ./scripts/build_paper.sh --format latex   # Generate LaTeX source
#   ./scripts/build_paper.sh --format all     # Generate all formats
#
# Exit codes:
#   0 - Success
#   1 - Missing dependency (pandoc, xelatex)
#   2 - Conversion failed

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
INPUT_FILE="${PROJECT_ROOT}/paper.md"
METADATA_FILE="${PROJECT_ROOT}/metadata.yaml"
OUTPUT_DIR="${PROJECT_ROOT}"

# Eisvogel template configuration
# Pin to specific version for reproducibility and supply chain security
EISVOGEL_VERSION="3.3.0"
EISVOGEL_URL="https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v${EISVOGEL_VERSION}/Eisvogel-${EISVOGEL_VERSION}.tar.gz"
EISVOGEL_SHA256="0eb287d299e73aa884d0b35fa27a28ae326afa04f51959e54f01cbbe76601489"
TEMPLATE_DIR="${HOME}/.local/share/pandoc/templates"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored message
info() { echo -e "${GREEN}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Show help
show_help() {
    sed -n '3,16p' "$0" | sed 's/^# //' | sed 's/^#//'
    exit 0
}

# Check if command exists
check_command() {
    local cmd="$1"
    local install_hint="$2"
    if ! command -v "$cmd" &> /dev/null; then
        error "$cmd not found."
        echo "  Install via: $install_hint"
        return 1
    fi
    return 0
}

# Check dependencies
check_dependencies() {
    local missing=0

    if ! check_command "pandoc" "brew install pandoc (macOS) or apt install pandoc (Ubuntu)"; then
        missing=1
    fi

    # Only check xelatex for PDF generation
    if [[ "$FORMAT" == "pdf" || "$FORMAT" == "all" ]]; then
        if ! check_command "xelatex" "brew install --cask mactex-no-gui (macOS) or apt install texlive-xetex (Ubuntu)"; then
            missing=1
        fi
    fi

    if [[ $missing -eq 1 ]]; then
        exit 1
    fi
}

# Verify SHA256 checksum
verify_checksum() {
    local file="$1"
    local expected="$2"
    local actual

    if command -v sha256sum &> /dev/null; then
        actual=$(sha256sum "$file" | cut -d' ' -f1)
    elif command -v shasum &> /dev/null; then
        actual=$(shasum -a 256 "$file" | cut -d' ' -f1)
    else
        warn "No checksum tool found, skipping verification"
        return 0
    fi

    if [[ "$actual" != "$expected" ]]; then
        error "Checksum verification failed!"
        echo "  Expected: $expected"
        echo "  Got:      $actual"
        return 1
    fi
    return 0
}

# Install Eisvogel template if not present
install_eisvogel() {
    local template_file="${TEMPLATE_DIR}/eisvogel.latex"

    if [[ -f "$template_file" ]]; then
        info "Eisvogel template found at $template_file"
        return 0
    fi

    info "Installing Eisvogel template v${EISVOGEL_VERSION}..."
    mkdir -p "$TEMPLATE_DIR"

    local temp_file
    temp_file=$(mktemp)
    trap "rm -f '$temp_file'" EXIT

    # Download template
    if command -v curl &> /dev/null; then
        curl -sL "$EISVOGEL_URL" -o "$temp_file"
    elif command -v wget &> /dev/null; then
        wget -qO "$temp_file" "$EISVOGEL_URL"
    else
        error "Neither curl nor wget found. Cannot download Eisvogel template."
        echo "  Manual installation: https://github.com/Wandmalfarbe/pandoc-latex-template"
        exit 1
    fi

    # Verify checksum for supply chain security
    if ! verify_checksum "$temp_file" "$EISVOGEL_SHA256"; then
        error "Eisvogel template download failed checksum verification"
        exit 1
    fi
    info "Checksum verified"

    # Extract template
    tar xzf "$temp_file" -C "$TEMPLATE_DIR" --strip-components=1

    if [[ -f "$template_file" ]]; then
        info "Eisvogel template v${EISVOGEL_VERSION} installed successfully"
    else
        error "Failed to install Eisvogel template"
        exit 1
    fi
}

# Build pandoc arguments array (avoids unquoted variable expansion)
build_pandoc_args() {
    local -n args_ref=$1
    args_ref=(
        "$INPUT_FILE"
        "--from=markdown+smart"
    )
    if [[ -f "$METADATA_FILE" ]]; then
        args_ref+=("--metadata-file=$METADATA_FILE")
    fi
}

# Generate PDF
generate_pdf() {
    local output="${OUTPUT_DIR}/paper.pdf"
    info "Generating PDF: $output"

    local -a pandoc_args
    build_pandoc_args pandoc_args

    pandoc "${pandoc_args[@]}" \
        --to=pdf \
        --pdf-engine=xelatex \
        --template=eisvogel \
        --listings \
        --number-sections \
        --toc \
        --toc-depth=3 \
        --output="$output"

    if [[ -f "$output" && -s "$output" ]]; then
        info "PDF generated successfully: $output ($(du -h "$output" | cut -f1))"
    else
        error "PDF generation failed"
        exit 2
    fi
}

# Generate HTML
generate_html() {
    local output="${OUTPUT_DIR}/paper.html"
    info "Generating HTML: $output"

    local -a pandoc_args
    build_pandoc_args pandoc_args

    pandoc "${pandoc_args[@]}" \
        --to=html5 \
        --standalone \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --output="$output"

    if [[ -f "$output" && -s "$output" ]]; then
        info "HTML generated successfully: $output ($(du -h "$output" | cut -f1))"
    else
        error "HTML generation failed"
        exit 2
    fi
}

# Generate DOCX
generate_docx() {
    local output="${OUTPUT_DIR}/paper.docx"
    info "Generating DOCX: $output"

    local -a pandoc_args
    build_pandoc_args pandoc_args

    pandoc "${pandoc_args[@]}" \
        --to=docx \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --output="$output"

    if [[ -f "$output" && -s "$output" ]]; then
        info "DOCX generated successfully: $output ($(du -h "$output" | cut -f1))"
    else
        error "DOCX generation failed"
        exit 2
    fi
}

# Generate LaTeX (intermediate format)
generate_latex() {
    local output="${OUTPUT_DIR}/paper.tex"
    info "Generating LaTeX: $output"

    local -a pandoc_args
    build_pandoc_args pandoc_args

    pandoc "${pandoc_args[@]}" \
        --to=latex \
        --template=eisvogel \
        --listings \
        --number-sections \
        --toc \
        --toc-depth=3 \
        --output="$output"

    if [[ -f "$output" && -s "$output" ]]; then
        info "LaTeX generated successfully: $output ($(du -h "$output" | cut -f1))"
    else
        error "LaTeX generation failed"
        exit 2
    fi
}

# Main
main() {
    # Default format
    FORMAT="pdf"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --format)
                FORMAT="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                ;;
            *)
                error "Unknown option: $1"
                show_help
                ;;
        esac
    done

    # Validate format
    case $FORMAT in
        pdf|html|docx|latex|all)
            ;;
        *)
            error "Invalid format: $FORMAT. Must be one of: pdf, html, docx, latex, all"
            exit 1
            ;;
    esac

    # Change to project root
    cd "$PROJECT_ROOT"

    # Check input file
    if [[ ! -f "$INPUT_FILE" ]]; then
        error "Input file not found: $INPUT_FILE"
        exit 1
    fi

    # Check dependencies
    check_dependencies

    # Install Eisvogel for PDF/LaTeX generation
    if [[ "$FORMAT" == "pdf" || "$FORMAT" == "latex" || "$FORMAT" == "all" ]]; then
        install_eisvogel
    fi

    # Generate output
    case $FORMAT in
        pdf)
            generate_pdf
            ;;
        html)
            generate_html
            ;;
        docx)
            generate_docx
            ;;
        latex)
            generate_latex
            ;;
        all)
            generate_pdf
            generate_html
            generate_docx
            generate_latex
            ;;
    esac

    info "Build complete!"
}

main "$@"
