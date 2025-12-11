#!/usr/bin/env bash
#
# build_paper.sh - Generate PDF, HTML, or DOCX from paper.md
#
# Usage:
#   ./scripts/build_paper.sh [--format FORMAT] [--help]
#
# Options:
#   --format FORMAT  Output format: pdf (default), html, docx, all
#   --help           Show this help message
#
# Examples:
#   ./scripts/build_paper.sh                  # Generate PDF
#   ./scripts/build_paper.sh --format html    # Generate HTML
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

# Eisvogel template location
EISVOGEL_URL="https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz"
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

# Install Eisvogel template if not present
install_eisvogel() {
    local template_file="${TEMPLATE_DIR}/eisvogel.latex"

    if [[ -f "$template_file" ]]; then
        info "Eisvogel template found at $template_file"
        return 0
    fi

    info "Installing Eisvogel template..."
    mkdir -p "$TEMPLATE_DIR"

    if command -v curl &> /dev/null; then
        curl -sL "$EISVOGEL_URL" | tar xz -C "$TEMPLATE_DIR" --strip-components=1
    elif command -v wget &> /dev/null; then
        wget -qO- "$EISVOGEL_URL" | tar xz -C "$TEMPLATE_DIR" --strip-components=1
    else
        error "Neither curl nor wget found. Cannot download Eisvogel template."
        echo "  Manual installation: https://github.com/Wandmalfarbe/pandoc-latex-template"
        exit 1
    fi

    if [[ -f "$template_file" ]]; then
        info "Eisvogel template installed successfully"
    else
        error "Failed to install Eisvogel template"
        exit 1
    fi
}

# Generate PDF
generate_pdf() {
    local output="${OUTPUT_DIR}/paper.pdf"
    info "Generating PDF: $output"

    local metadata_arg=""
    if [[ -f "$METADATA_FILE" ]]; then
        metadata_arg="--metadata-file=$METADATA_FILE"
    fi

    pandoc "$INPUT_FILE" \
        --from=markdown+smart \
        --to=pdf \
        --pdf-engine=xelatex \
        --template=eisvogel \
        --listings \
        --number-sections \
        --toc \
        --toc-depth=3 \
        $metadata_arg \
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

    local metadata_arg=""
    if [[ -f "$METADATA_FILE" ]]; then
        metadata_arg="--metadata-file=$METADATA_FILE"
    fi

    pandoc "$INPUT_FILE" \
        --from=markdown+smart \
        --to=html5 \
        --standalone \
        --toc \
        --toc-depth=3 \
        --number-sections \
        $metadata_arg \
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

    local metadata_arg=""
    if [[ -f "$METADATA_FILE" ]]; then
        metadata_arg="--metadata-file=$METADATA_FILE"
    fi

    pandoc "$INPUT_FILE" \
        --from=markdown+smart \
        --to=docx \
        --toc \
        --toc-depth=3 \
        --number-sections \
        $metadata_arg \
        --output="$output"

    if [[ -f "$output" && -s "$output" ]]; then
        info "DOCX generated successfully: $output ($(du -h "$output" | cut -f1))"
    else
        error "DOCX generation failed"
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
        pdf|html|docx|all)
            ;;
        *)
            error "Invalid format: $FORMAT. Must be one of: pdf, html, docx, all"
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

    # Install Eisvogel for PDF generation
    if [[ "$FORMAT" == "pdf" || "$FORMAT" == "all" ]]; then
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
        all)
            generate_pdf
            generate_html
            generate_docx
            ;;
    esac

    info "Build complete!"
}

main "$@"
