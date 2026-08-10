# Build Provenance

Everything needed to verify or reproduce the artifacts in this package.

## Snapshot identity

| Field | Value |
|:---|:---|
| Snapshot taken | 2026-08-10 |
| Artifacts built | 2026-08-10 15:12 local (America/Indiana) |
| Repository | https://github.com/stharrold/yuimedi-paper-20250901 |
| Branch | `contrib/stharrold` |
| Base commit | `17d2de8f8e7d0f2e639e87d5d3d51293d879429e` |
| Working tree | **Dirty.** The copyedit changes were uncommitted when this snapshot was taken. |

Because the tree was dirty, the base commit alone does not reproduce these
artifacts. The uncommitted delta is captured verbatim in
`20260810_copyedit-source-changes.diff` and is the only difference between
`17d2de8` and the sources in this package. The modified source files
(`paper.md`, `metadata.yaml`, `references.bib`, `multimedia_appendix_1.md`,
`figures/architecture.mmd`, `figures/knowledge-cycle.mmd`, and both figure
caption files) are also included here in their post-edit state, so the diff is a
convenience record rather than the only route to the inputs. The regenerated
figure images are binary and therefore appear in `figures/`, not in the diff.

Verify the inputs match the diff:

```bash
git checkout 17d2de8
git apply ARCHIVED/20260810_IJMR-Copyediting/20260810_copyedit-source-changes.diff
diff paper.md ARCHIVED/20260810_IJMR-Copyediting/paper.md   # expect no output
```

## Toolchain used for these artifacts

| Tool | Version | Role |
|:---|:---|:---|
| pandoc | 3.8.2.1 | Markdown to DOCX, PDF, LaTeX, HTML |
| tectonic | 0.15.0 | LaTeX engine for PDF output |
| uv | 0.8.8 | Python environment and script runner |
| Python | 3.12.11 | Validation and audit scripts |
| Eisvogel | 3.3.0 | pandoc LaTeX template, vendored at `templates/eisvogel.latex` |

The pandoc version matters. CI pins pandoc to **3.8.2.1** in the `Containerfile`
precisely because Debian's apt pandoc (2.x) renders AMA references differently,
producing "Michal S. Gal" instead of the correct "Gal MS". Any rebuild that does
not use 3.8.2.1 should be checked against that failure mode before it is trusted.

`build_paper.sh` prefers `xelatex` and falls back to `tectonic` when xelatex is
not on the shell PATH. These artifacts were built through the **tectonic**
fallback, which is the normal path on this machine.

## External dependency, now vendored

`build_paper.sh` downloads the Eisvogel LaTeX template from GitHub into
`~/.local/share/pandoc/templates/` if it is not already present. That is a
network dependency on a third-party release, so the exact template used here is
vendored at `templates/eisvogel.latex` (v3.3.0, with its license and changelog).
If GitHub or that release ever becomes unavailable, copy the vendored file into
`~/.local/share/pandoc/templates/` before rebuilding.

## Reproducing the artifacts

### Host build (matches how these were produced)

```bash
git clone https://github.com/stharrold/yuimedi-paper-20250901
cd yuimedi-paper-20250901
git checkout 17d2de8
git apply <this-dir>/20260810_copyedit-source-changes.diff

mkdir -p ~/.local/share/pandoc/templates
cp <this-dir>/templates/eisvogel.latex ~/.local/share/pandoc/templates/

./scripts/build_paper.sh --format all
```

### Container build (hermetic, matches CI)

```bash
podman build -t yuimedi-paper -f Containerfile .
podman run --rm --security-opt label=disable \
  -v "$(pwd)":/app -v yuimedi_venv_cache:/app/.venv -w /app \
  yuimedi-paper ./scripts/build_paper.sh --format all
```

The named volume `yuimedi_venv_cache` avoids host and container binary conflicts.

### Regenerating figures

Figures are rendered from Mermaid sources with mermaid-cli 11.16.0 (node
v25.9.0). The repository's `figures/puppeteer-config.json` points at
`/usr/bin/chromium` and therefore only works inside the container. On this macOS
host, mermaid-cli failed with "Could not find Chrome (ver. 131.0.6778.204)"
because the puppeteer browser cache was empty. Rather than download a second
Chrome, the render was pointed at the installed one:

```bash
cat > /tmp/puppeteer-mac.json <<'JSON'
{
  "executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
}
JSON

npx --yes @mermaid-js/mermaid-cli@latest -p /tmp/puppeteer-mac.json \
  -i figures/architecture.mmd -o figures/architecture.mmd.svg
npx --yes @mermaid-js/mermaid-cli@latest -p /tmp/puppeteer-mac.json \
  -i figures/architecture.mmd -o figures/architecture.mmd.png

# journal upload copy: 1200px maximum dimension
cp figures/architecture.mmd.png figures/architecture.figure.png
sips --resampleHeight 1200 figures/architecture.figure.png
```

The re-render was checked for style drift against the previous PNG: dimensions
went from 1093x1247 to 1094x1247, and a visual comparison confirmed identical
layout, node positions, arrow routing, shading, and font. Only label text
differs.

## Verification performed on these artifacts

Checked after the final 2026-08-10 15:12 build:

- `paper.docx` body carries 25 instances of "health care" and preserves the HIMSS
  legal name in both places (body and abbreviations list).
- The reference list retains 24 instances of the original "Healthcare" spelling in
  published titles, journal names, and URLs, which is correct under AMA style.
  `healthcareitnews.com` and the IBM newsroom URL verified unbroken.
- `docProps/core.xml` title property updated to the new spelling. JMIR reads the
  title from there, not from the document body.
- AMA reference rendering regression check passes: references render as `Gal MS`.
- `paper.pdf` is 24 pages. Checked for the known LaTeX float hazard where reflowed
  text orphans a figure's introductory sentence onto a near-blank page: the only
  sparse pages are page 1 (title) and page 24 (end of references), both expected.
- No em-dashes introduced in any source file.
- `references.bib` corrected in five entries (see finding A and the no-DOI sweep
  in `20260810_copyedit-changes.md`). All five re-audited clean with
  `audit_references.py --only <key> --skip-landing --force`.
- Both figures regenerated and visually compared against their previous renders:
  layout, node positions, arrow routing, shading, and font unchanged.

## Word counts at this snapshot

Measured by `scripts/validate_jmir_compliance.py --article-type viewpoint`.

| Measure | Before this round | After |
|:---|---:|---:|
| Body only | 4,325 | 4,386 |
| JMIR method (authoritative) | 4,990 | 5,065 |
| Abstract | 270 | 272 |

The JMIR method count is the authoritative one: title, abstract, keywords, body
including tables and figure captions, end matter, and abbreviations, excluding
references. It now exceeds the 5,000 limit by 65 words. The copyeditor confirmed
that the length is acceptable, so this is an accepted deviation rather than a
defect. See `20260810_copyedit-changes.md` for the arithmetic.

Consequence for the repository: the `validate-jmir-compliance` pre-commit hook
fires on any change to `paper.md` or `metadata.yaml` and now exits 1. Commits
touching those files require:

```bash
SKIP=validate-jmir-compliance git commit -m "..."
```

The hook's 5,000-word limit was deliberately left in place, since it is a real
i-JMR rule that still applies to Papers 2 and 3.

## Integrity

`MANIFEST.sha256` lists the SHA-256 of every file in this package. Verify with:

```bash
cd <this-dir> && shasum -a 256 -c MANIFEST.sha256
```
