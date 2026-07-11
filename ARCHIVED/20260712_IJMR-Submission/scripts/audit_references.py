#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Collect per-citation audit evidence for references.bib (issue #553).

For every entry in references.bib, writes bibliography-audit/<bibkey>/:
  0-bibentry.bib              verbatim entry from references.bib
  1-citing-sentences.txt      sentences/table rows in paper.md citing [@key], with line numbers
  2-doi.txt                   extracted DOI, normalization notes, syntax verdict
  3-resolution.json           doi.org handle-API result (registered? target URL)
  4-crossref.json             Crossref metadata for the DOI, or a title search for no-DOI entries
  5-landing-page.html         best-effort landing page fetch (browser User-Agent)
  5-landing-page.FAILED.txt   fetch failure details (page needs manual fetch)

Also writes:
  bibliography-audit/summary.json         machine-readable per-entry status
  bibliography-audit/manual-fetch-list.txt  bibkey, URL, destination for manual fetches

Idempotent: existing evidence files are skipped unless --force is given, so
manually fetched landing pages dropped into a citation directory survive re-runs.

Usage:
  uv run python scripts/audit_references.py                 # full collection
  uv run python scripts/audit_references.py --only wu2024   # single entry
  uv run python scripts/audit_references.py --skip-landing  # metadata only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_PATH = REPO_ROOT / "references.bib"
PAPER_PATH = REPO_ROOT / "paper.md"
OUT_DIR = REPO_ROOT / "bibliography-audit"

UA_SCRIPT = "yuimedi-paper-reference-audit/1.0 (https://github.com/stharrold/yuimedi-paper-20250901; mailto:samuel.harrold@gmail.com)"
UA_BROWSER = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

DOI_SYNTAX = re.compile(r"^10\.\d{4,9}/\S+$")
DOI_URL_PREFIX = re.compile(r"^https?://(dx\.)?doi\.org/", re.IGNORECASE)
BLOCK_MARKERS = (
    "just a moment",
    "access denied",
    "captcha",
    "enable javascript and cookies",
    "are you a robot",
)
FETCH_TIMEOUT = 20
MAX_BODY_BYTES = 3_000_000


def parse_bib_entries(text: str) -> list[dict[str, Any]]:
    """Parse BibTeX entries with balanced-brace field values (handles {{double braces}})."""
    entries: list[dict[str, Any]] = []
    for match in re.finditer(r"@([A-Za-z]+)\s*\{", text):
        start = match.start()
        brace_open = match.end() - 1
        depth = 0
        end = -1
        for i in range(brace_open, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            raise ValueError(f"Unbalanced braces in entry starting at offset {start}")
        body = text[brace_open + 1 : end]
        key, _, fields_src = body.partition(",")
        entries.append(
            {
                "key": key.strip(),
                "type": match.group(1).lower(),
                "raw": text[start : end + 1],
                "fields": parse_fields(fields_src),
            }
        )
    return entries


def parse_fields(src: str) -> dict[str, str]:
    """Parse 'name = {value}' pairs, tolerating nested braces and quoted values."""
    fields: dict[str, str] = {}
    pos = 0
    name_re = re.compile(r"\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*")
    while pos < len(src):
        m = name_re.match(src, pos)
        if not m:
            break
        name = m.group(1).lower()
        pos = m.end()
        if pos < len(src) and src[pos] == "{":
            depth = 0
            start = pos + 1
            while pos < len(src):
                if src[pos] == "{":
                    depth += 1
                elif src[pos] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                pos += 1
            fields[name] = src[start:pos].strip()
            pos += 1
        elif pos < len(src) and src[pos] == '"':
            end = src.find('"', pos + 1)
            fields[name] = src[pos + 1 : end].strip()
            pos = end + 1
        else:
            end = src.find(",", pos)
            end = end if end >= 0 else len(src)
            fields[name] = src[pos:end].strip()
            pos = end
        comma = src.find(",", pos)
        pos = comma + 1 if comma >= 0 else len(src)
    return fields


def citing_sentences(paper_lines: list[str], key: str) -> list[str]:
    """Return 'L<num>: <sentence>' for every paper.md sentence or table row citing @key."""
    pattern = re.compile(r"@" + re.escape(key) + r"\b")
    results: list[str] = []
    for lineno, line in enumerate(paper_lines, start=1):
        if not pattern.search(line):
            continue
        if line.lstrip().startswith("|"):
            results.append(f"L{lineno} (table row): {line.strip()}")
            continue
        sentences = re.split(r"(?<=[.!?])\s+", line.strip())
        hits = [s for s in sentences if pattern.search(s)] or [line.strip()]
        results.extend(f"L{lineno}: {s}" for s in hits)
    return results


def normalize_doi(raw: str) -> tuple[str, list[str]]:
    """Strip common transcription artifacts; report every issue found."""
    issues: list[str] = []
    doi = raw.strip()
    if doi != raw:
        issues.append("surrounding-whitespace")
    if DOI_URL_PREFIX.match(doi):
        issues.append("url-prefix-in-doi-field")
        doi = DOI_URL_PREFIX.sub("", doi)
    if doi.lower().startswith("doi:"):
        issues.append("doi:-prefix")
        doi = doi[4:].strip()
    if doi and doi[-1] in ".,;":
        issues.append("trailing-punctuation")
        doi = doi.rstrip(".,;")
    if doi and not DOI_SYNTAX.match(doi):
        issues.append("bad-syntax")
    return doi, issues


def http_get(url: str, user_agent: str, accept: str = "*/*") -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": accept})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        return resp.status, resp.read(MAX_BODY_BYTES)


def get_json(url: str) -> dict[str, Any]:
    try:
        status, body = http_get(url, UA_SCRIPT, accept="application/json")
        return {"http_status": status, "body": json.loads(body)}
    except urllib.error.HTTPError as e:
        return {"http_status": e.code, "error": str(e)}
    except Exception as e:  # noqa: BLE001 - audit evidence must record any failure mode
        return {"http_status": None, "error": f"{type(e).__name__}: {e}"}


def resolve_doi(doi: str) -> dict[str, Any]:
    """Query the doi.org handle API: registration status and target URL, no publisher contact."""
    result = get_json(f"https://doi.org/api/handles/{urllib.parse.quote(doi, safe='')}")
    body = result.get("body") or {}
    values = body.get("values", []) if isinstance(body, dict) else []
    target = next((v.get("data", {}).get("value") for v in values if v.get("type") == "URL"), None)
    return {
        "doi": doi,
        "http_status": result.get("http_status"),
        "handle_response_code": body.get("responseCode") if isinstance(body, dict) else None,
        "registered": isinstance(body, dict) and body.get("responseCode") == 1,
        "target_url": target,
        "error": result.get("error"),
    }


def trim_crossref_message(message: dict[str, Any]) -> dict[str, Any]:
    """Drop the bulky reference list; keep everything the judge pass needs."""
    return {k: v for k, v in message.items() if k != "reference"}


def crossref_by_doi(doi: str) -> dict[str, Any]:
    result = get_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}")
    body = result.get("body")
    if isinstance(body, dict) and "message" in body:
        return {
            "mode": "doi-lookup",
            "http_status": result["http_status"],
            "message": trim_crossref_message(body["message"]),
        }
    return {
        "mode": "doi-lookup",
        "http_status": result.get("http_status"),
        "error": result.get("error", "no message in response"),
    }


def crossref_by_title(title: str, author: str, year: str) -> dict[str, Any]:
    """Title search for no-DOI entries: surfaces DOIs that should be added."""
    query = urllib.parse.urlencode(
        {"query.bibliographic": f"{title} {author} {year}".strip(), "rows": "5"}
    )
    result = get_json(f"https://api.crossref.org/works?{query}")
    body = result.get("body")
    if not (isinstance(body, dict) and "message" in body):
        return {
            "mode": "title-search",
            "http_status": result.get("http_status"),
            "error": result.get("error", "no message in response"),
        }
    candidates = [
        {
            "doi": item.get("DOI"),
            "title": (item.get("title") or [None])[0],
            "container": (item.get("container-title") or [None])[0],
            "year": (item.get("issued", {}).get("date-parts") or [[None]])[0][0],
            "score": item.get("score"),
        }
        for item in body["message"].get("items", [])
    ]
    return {"mode": "title-search", "http_status": result["http_status"], "candidates": candidates}


def fetch_landing(url: str, dest_html: Path, dest_failed: Path) -> str:
    """Best-effort landing page fetch. Returns status: ok | suspect | failed."""
    try:
        status, body = http_get(url, UA_BROWSER, accept="text/html,application/xhtml+xml,*/*;q=0.8")
    except Exception as e:  # noqa: BLE001 - failure details go into the manual-fetch list
        dest_failed.write_text(f"url: {url}\nerror: {type(e).__name__}: {e}\n")
        return "failed"
    if status >= 400:
        dest_failed.write_text(f"url: {url}\nhttp_status: {status}\n")
        return "failed"
    dest_html.write_bytes(body)
    text_head = body[:20_000].decode("utf-8", errors="replace").lower()
    if len(body) < 1000 or any(marker in text_head for marker in BLOCK_MARKERS):
        dest_failed.write_text(
            f"url: {url}\nhttp_status: {status}\nsuspect: bot wall or empty page ({len(body)} bytes); verify or fetch manually\n"
        )
        return "suspect"
    return "ok"


def landing_url_for(
    entry_fields: dict[str, str], resolution: dict[str, Any], crossref: dict[str, Any]
) -> str | None:
    if entry_fields.get("url"):
        return entry_fields["url"]
    message = crossref.get("message") or {}
    resource_url = message.get("resource", {}).get("primary", {}).get("URL")
    return resource_url or resolution.get("target_url")


def audit_entry(
    entry: dict[str, Any], paper_lines: list[str], skip_landing: bool, force: bool
) -> dict[str, Any]:
    key = entry["key"]
    fields = entry["fields"]
    cite_dir = OUT_DIR / key
    cite_dir.mkdir(parents=True, exist_ok=True)

    def fresh(path: Path) -> bool:
        return force or not path.exists()

    if fresh(cite_dir / "0-bibentry.bib"):
        (cite_dir / "0-bibentry.bib").write_text(entry["raw"] + "\n")

    sentences = citing_sentences(paper_lines, key)
    if fresh(cite_dir / "1-citing-sentences.txt"):
        content = (
            "\n".join(sentences)
            if sentences
            else "WARNING: no citation of this key found in paper.md (orphaned bibliography entry?)"
        )
        (cite_dir / "1-citing-sentences.txt").write_text(content + "\n")

    raw_doi = fields.get("doi", "")
    doi, doi_issues = normalize_doi(raw_doi) if raw_doi else ("", [])
    if fresh(cite_dir / "2-doi.txt"):
        lines = [
            f"raw: {raw_doi or '(no doi field)'}",
            f"normalized: {doi or '(none)'}",
            f"issues: {', '.join(doi_issues) if doi_issues else 'none'}",
        ]
        (cite_dir / "2-doi.txt").write_text("\n".join(lines) + "\n")

    resolution: dict[str, Any] = {"skipped": "no DOI"}
    if doi and "bad-syntax" not in doi_issues:
        if fresh(cite_dir / "3-resolution.json"):
            resolution = resolve_doi(doi)
            (cite_dir / "3-resolution.json").write_text(json.dumps(resolution, indent=2) + "\n")
        else:
            resolution = json.loads((cite_dir / "3-resolution.json").read_text())
    elif fresh(cite_dir / "3-resolution.json"):
        resolution = {"skipped": "no DOI" if not doi else "bad-syntax DOI, not resolvable as-is"}
        (cite_dir / "3-resolution.json").write_text(json.dumps(resolution, indent=2) + "\n")

    if fresh(cite_dir / "4-crossref.json"):
        if doi and "bad-syntax" not in doi_issues:
            crossref = crossref_by_doi(doi)
        else:
            crossref = crossref_by_title(
                fields.get("title", ""), fields.get("author", ""), fields.get("year", "")
            )
        (cite_dir / "4-crossref.json").write_text(json.dumps(crossref, indent=2) + "\n")
    else:
        crossref = json.loads((cite_dir / "4-crossref.json").read_text())

    landing_status = "skipped"
    landing_url = landing_url_for(fields, resolution, crossref)
    if not skip_landing and landing_url:
        html_path = cite_dir / "5-landing-page.html"
        failed_path = cite_dir / "5-landing-page.FAILED.txt"
        if html_path.exists() and not failed_path.exists() and not force:
            landing_status = "ok (existing)"
        else:
            if force:
                failed_path.unlink(missing_ok=True)
            landing_status = fetch_landing(landing_url, html_path, failed_path)
            if landing_status == "ok":
                failed_path.unlink(missing_ok=True)

    message = crossref.get("message") or {}
    return {
        "key": key,
        "has_doi": bool(raw_doi),
        "doi": doi or None,
        "doi_issues": doi_issues,
        "doi_registered": resolution.get("registered"),
        "crossref_title": (message.get("title") or [None])[0],
        "bib_title": fields.get("title", "").strip("{}"),
        "citing_sentence_count": len(sentences),
        "landing_url": landing_url,
        "landing_status": landing_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--only", help="comma-separated bib keys to audit (default: all)")
    parser.add_argument(
        "--skip-landing", action="store_true", help="skip landing-page fetches (metadata only)"
    )
    parser.add_argument(
        "--force", action="store_true", help="re-fetch evidence files that already exist"
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="concurrent entries (default 4; polite to Crossref)"
    )
    args = parser.parse_args()

    entries = parse_bib_entries(BIB_PATH.read_text())
    if args.only:
        wanted = {k.strip() for k in args.only.split(",")}
        entries = [e for e in entries if e["key"] in wanted]
        missing = wanted - {e["key"] for e in entries}
        if missing:
            print(
                f"ERROR: keys not found in references.bib: {', '.join(sorted(missing))}",
                file=sys.stderr,
            )
            return 1

    paper_lines = PAPER_PATH.read_text().splitlines()
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Auditing {len(entries)} entries -> {OUT_DIR}")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows = list(
            pool.map(lambda e: audit_entry(e, paper_lines, args.skip_landing, args.force), entries)
        )

    rows.sort(key=lambda r: str(r["key"]))
    (OUT_DIR / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")

    manual: list[str] = []
    for row in rows:
        if row["landing_status"] in ("failed", "suspect") and row["landing_url"]:
            manual.append(
                f"{row['key']}\t{row['landing_url']}\t{OUT_DIR / str(row['key']) / '5-landing-page.html'}"
            )
    (OUT_DIR / "manual-fetch-list.txt").write_text("\n".join(manual) + ("\n" if manual else ""))

    n_doi = sum(1 for r in rows if r["has_doi"])
    n_unregistered = [r["key"] for r in rows if r["has_doi"] and r["doi_registered"] is False]
    n_issues = [r["key"] for r in rows if r["doi_issues"]]
    n_orphan = [r["key"] for r in rows if r["citing_sentence_count"] == 0]
    print(f"\nEntries: {len(rows)}  with DOI: {n_doi}  without: {len(rows) - n_doi}")
    print(f"DOI transcription issues ({len(n_issues)}): {', '.join(n_issues) or 'none'}")
    print(
        f"DOIs NOT registered at doi.org ({len(n_unregistered)}): {', '.join(n_unregistered) or 'none'}"
    )
    print(
        f"Bibliography entries never cited in paper.md ({len(n_orphan)}): {', '.join(n_orphan) or 'none'}"
    )
    print(
        f"Landing pages needing manual fetch: {len(manual)} (see {OUT_DIR / 'manual-fetch-list.txt'})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
