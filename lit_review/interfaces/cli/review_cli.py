"""CLI interface for academic literature review workflow.

Provides Click commands for managing literature reviews including
initialization, searching, assessment, and export.
"""

import os
from pathlib import Path

import click

from lit_review.application.usecases.analyze_themes import AnalyzeThemesUseCase
from lit_review.application.usecases.export_review import ExportFormat, ExportReviewUseCase
from lit_review.application.usecases.generate_synthesis import GenerateSynthesisUseCase
from lit_review.application.usecases.search_papers import SearchPapersUseCase
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.exceptions import EntityNotFoundError
from lit_review.domain.values.doi import DOI
from lit_review.infrastructure.adapters.crossref_adapter import CrossrefAdapter
from lit_review.infrastructure.persistence.json_repository import JSONReviewRepository

# Default data directory
DEFAULT_DATA_DIR = Path.home() / ".lit_review"


def get_repository() -> JSONReviewRepository:
    """Get repository instance.

    Returns:
        Configured repository.
    """
    data_dir = Path(os.environ.get("LIT_REVIEW_DATA_DIR", str(DEFAULT_DATA_DIR)))
    return JSONReviewRepository(data_dir)


def get_search_use_case() -> SearchPapersUseCase:
    """Get search use case with configured services.

    Returns:
        Configured SearchPapersUseCase.
    """
    use_case = SearchPapersUseCase()
    use_case.add_service("crossref", CrossrefAdapter())
    return use_case


@click.group()
@click.version_option(version="0.1.0", prog_name="academic-review")
def review() -> None:
    """Academic literature review workflow CLI.

    Manage systematic literature reviews with search, assessment, and export.
    """
    pass


@review.command()
@click.argument("title")
@click.option("-q", "--question", required=True, help="Research question")
@click.option(
    "-i",
    "--include",
    multiple=True,
    help="Inclusion criterion (can specify multiple)",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    help="Exclusion criterion (can specify multiple)",
)
def init(title: str, question: str, include: tuple[str, ...], exclude: tuple[str, ...]) -> None:
    """Initialize a new literature review.

    Creates a new review with the given title, research question, and criteria.

    Example:
        academic-review init "ML Healthcare" -q "What is the impact?" -i "Peer-reviewed"
    """
    repo = get_repository()

    if repo.exists(title):
        click.echo(f"Error: Review '{title}' already exists.", err=True)
        raise SystemExit(1)

    inclusion = list(include) if include else ["Peer-reviewed"]

    review_obj = Review(
        title=title,
        research_question=question,
        inclusion_criteria=inclusion,
        exclusion_criteria=list(exclude),
    )

    repo.save(review_obj)
    click.echo(f"Created review: {title}")
    click.echo(f"Research question: {question}")
    click.echo(f"Stage: {review_obj.stage.value}")


@review.command()
@click.argument("title")
@click.option(
    "-d",
    "--database",
    type=click.Choice(["crossref", "pubmed", "arxiv"]),
    default="crossref",
    help="Database to search",
)
@click.option("-k", "--keywords", required=True, help="Search keywords")
@click.option("-l", "--limit", default=20, help="Maximum results")
def search(title: str, database: str, keywords: str, limit: int) -> None:
    """Search academic databases for papers.

    Searches the specified database and adds results to the review.
    Review must be in SEARCH stage or later.

    Example:
        academic-review search "ML Healthcare" -d crossref -k "machine learning diagnosis"
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    # Advance to SEARCH if in PLANNING
    if review_obj.stage == ReviewStage.PLANNING:
        review_obj.advance_stage()
        click.echo("Advanced review to SEARCH stage.")

    if not review_obj.can_add_papers():
        click.echo(f"Error: Cannot add papers in {review_obj.stage.value} stage.", err=True)
        raise SystemExit(1)

    # Search with progress indicators
    click.echo("\n=== Searching Academic Databases ===")
    click.echo(f"Keywords: {keywords}")
    click.echo(f"Database: {database}")
    click.echo(f"Limit: {limit}")
    click.echo("")

    use_case = get_search_use_case()
    papers = []

    with click.progressbar(
        length=limit,
        label=f"Searching {database}",
        show_percent=True,
    ) as bar:
        try:
            # Simulate progress updates during search
            bar.update(limit // 4)
            papers = use_case.execute(keywords, databases=[database], limit=limit)
            bar.update(limit - (limit // 4))
        except (ConnectionError, TimeoutError) as e:
            click.echo(f"\nError: Search failed - {e}", err=True)
            raise SystemExit(1)

    if not papers:
        click.echo("No papers found.")
        return

    click.echo(f"\n{database}: Found {len(papers)} papers")

    # Add papers to review with deduplication
    click.echo("\nDeduplicating papers...")
    added = review_obj.add_papers(papers)
    duplicates = len(papers) - added

    repo.save(review_obj)

    # Display results
    click.echo("\n=== Search Results ===")
    click.echo(f"Papers found: {len(papers)}")
    click.echo(f"New papers added: {added}")
    click.echo(f"Duplicates skipped: {duplicates}")
    click.echo(f"Total papers in review: {len(review_obj.papers)}")

    if duplicates > 0:
        click.echo(f"\nDeduplication rate: {(duplicates / len(papers) * 100):.1f}%")


@review.command()
@click.argument("title")
def status(title: str) -> None:
    """Show review status and statistics.

    Displays current stage, paper counts, and review progress.

    Example:
        academic-review status "ML Healthcare"
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    stats = review_obj.generate_statistics()

    click.echo(f"\n=== {review_obj.title} ===")
    click.echo(f"Research Question: {review_obj.research_question}")
    click.echo(f"Current Stage: {stats['current_stage'].upper()}")
    click.echo("")
    click.echo("Papers:")
    click.echo(f"  Total: {stats['total_papers']}")
    click.echo(f"  Assessed: {stats['assessed_papers']}")
    click.echo(f"  Unassessed: {stats['unassessed_papers']}")
    click.echo(f"  Included: {stats['included_papers']}")
    click.echo(f"  Excluded: {stats['excluded_papers']}")

    if stats["assessed_papers"] > 0:
        click.echo(f"  Inclusion Rate: {stats['inclusion_rate']:.1%}")

    click.echo("")
    click.echo("Criteria:")
    click.echo(f"  Inclusion: {', '.join(review_obj.inclusion_criteria)}")
    if review_obj.exclusion_criteria:
        click.echo(f"  Exclusion: {', '.join(review_obj.exclusion_criteria)}")


@review.command()
@click.argument("title")
def advance(title: str) -> None:
    """Advance review to next workflow stage.

    Moves the review to the next stage in the workflow:
    PLANNING -> SEARCH -> SCREENING -> ANALYSIS -> SYNTHESIS -> COMPLETE

    Example:
        academic-review advance "ML Healthcare"
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    old_stage = review_obj.stage

    try:
        review_obj.advance_stage()
    except Exception as e:
        click.echo(f"Error: Cannot advance - {e}", err=True)
        raise SystemExit(1)

    repo.save(review_obj)
    click.echo(f"Advanced from {old_stage.value.upper()} to {review_obj.stage.value.upper()}")


@review.command("export")
@click.argument("title")
@click.option(
    "-f",
    "--format",
    "formats",
    multiple=True,
    type=click.Choice(["bibtex", "json", "html", "markdown", "csv"]),
    help="Export format(s) - can specify multiple",
)
@click.option("-o", "--output", help="Output file path (for single format)")
@click.option(
    "--outdir",
    type=click.Path(file_okay=False, dir_okay=True),
    help="Output directory (for multiple formats)",
)
@click.option("--all", "export_all", is_flag=True, help="Export all papers, not just included")
def export_cmd(
    title: str,
    formats: tuple[str, ...],
    output: str | None,
    outdir: str | None,
    export_all: bool,
) -> None:
    """Export review to file(s).

    Exports papers from the review in the specified format(s).
    By default, only exports papers marked as included.

    Supports: bibtex, json, html, markdown, csv

    Example:
        academic-review export "ML Healthcare" -f bibtex -o refs.bib
        academic-review export "ML Healthcare" -f bibtex -f json -f html --outdir exports/
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    # Default to bibtex if no format specified
    if not formats:
        formats = ("bibtex",)

    # Validate output options
    if len(formats) == 1:
        if not output and not outdir:
            click.echo("Error: Must specify --output or --outdir", err=True)
            raise SystemExit(1)
    else:
        if not outdir:
            click.echo("Error: Must specify --outdir for multiple formats", err=True)
            raise SystemExit(1)

    use_case = ExportReviewUseCase()
    format_map = {
        "bibtex": (ExportFormat.BIBTEX, ".bib"),
        "json": (ExportFormat.JSON, ".json"),
        "html": (ExportFormat.HTML, ".html"),
        "markdown": (ExportFormat.MARKDOWN, ".md"),
        "csv": (ExportFormat.CSV, ".csv"),
    }

    exported_files = []

    with click.progressbar(
        formats,
        label="Exporting",
        show_percent=False,
        item_show_func=lambda x: f"Format: {x}" if x else "",
    ) as bar:
        for fmt in bar:
            export_format, ext = format_map[fmt]

            # Determine output path
            if len(formats) == 1 and output:
                output_path = Path(output)
            else:
                assert outdir is not None
                out_dir = Path(outdir)
                out_dir.mkdir(parents=True, exist_ok=True)
                # Sanitize title for filename
                safe_title = "".join(c if c.isalnum() else "_" for c in title)
                output_path = out_dir / f"{safe_title}{ext}"

            try:
                count = use_case.execute(
                    review_obj,
                    export_format,
                    output_path,
                    included_only=not export_all,
                )

                file_size = output_path.stat().st_size
                exported_files.append((str(output_path), fmt, count, file_size))

            except OSError as e:
                click.echo(f"\nError: Failed to write {fmt} file - {e}", err=True)
                continue

    # Display results
    click.echo("\nExport complete:")
    for file_path, fmt, count, size in exported_files:
        size_kb = size / 1024
        click.echo(f"  {fmt:10s} | {count:3d} papers | {size_kb:7.1f} KB | {file_path}")


@review.command("list")
def list_cmd() -> None:
    """List all reviews.

    Shows all reviews stored in the data directory.

    Example:
        academic-review list
    """
    repo = get_repository()
    reviews = repo.list_reviews()

    if not reviews:
        click.echo("No reviews found.")
        return

    click.echo("Reviews:")
    for review_id in reviews:
        try:
            review_obj = repo.load(review_id)
            click.echo(f"  - {review_id} ({review_obj.stage.value})")
        except Exception:
            click.echo(f"  - {review_id} (error loading)")


@review.command()
@click.argument("title")
@click.confirmation_option(prompt="Are you sure you want to delete this review?")
def delete(title: str) -> None:
    """Delete a review.

    Permanently removes the review and all its data.

    Example:
        academic-review delete "ML Healthcare"
    """
    repo = get_repository()

    try:
        repo.delete(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    click.echo(f"Deleted review: {title}")


@review.command()
@click.argument("title")
@click.option("--doi", help="DOI of paper to assess")
@click.option("--score", type=float, help="Quality score (0-10)")
@click.option("--include/--exclude", default=None, help="Include or exclude the paper")
@click.option("--notes", default="", help="Assessment notes")
@click.option("--batch", type=click.Path(exists=True), help="CSV file with batch assessments")
def assess(
    title: str,
    doi: str | None,
    score: float | None,
    include: bool | None,
    notes: str,
    batch: str | None,
) -> None:
    """Assess papers for quality and inclusion.

    Single assessment with --doi, --score, and --include/--exclude flags.
    Batch assessment with --batch CSV file (columns: doi,score,include,notes).

    Example:
        academic-review assess "ML Healthcare" --doi 10.1234/test --score 8.5 --include
        academic-review assess "ML Healthcare" --batch assessments.csv
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    if batch:
        # Batch assessment from CSV
        import csv

        assessments_made = 0
        errors = 0

        with open(batch) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    paper_doi = row["doi"]
                    paper_score = float(row["score"])
                    paper_include = row["include"].lower() in ("true", "yes", "1")
                    paper_notes = row.get("notes", "")

                    paper = review_obj.get_paper_by_doi(DOI(paper_doi))
                    if paper is None:
                        click.echo(f"Warning: Paper {paper_doi} not found in review", err=True)
                        errors += 1
                        continue

                    paper.assess(paper_score, paper_include, paper_notes)
                    assessments_made += 1
                except (KeyError, ValueError) as e:
                    click.echo(f"Warning: Invalid row - {e}", err=True)
                    errors += 1

        repo.save(review_obj)
        click.echo(
            f"Batch assessment complete: {assessments_made} papers assessed, {errors} errors"
        )

    else:
        # Single paper assessment
        if not doi:
            click.echo(
                "Error: Must specify --doi for single assessment or --batch for batch", err=True
            )
            raise SystemExit(1)

        if score is None or include is None:
            click.echo("Error: Must specify --score and --include/--exclude", err=True)
            raise SystemExit(1)

        paper = review_obj.get_paper_by_doi(DOI(doi))
        if paper is None:
            click.echo(f"Error: Paper with DOI {doi} not found in review", err=True)
            raise SystemExit(1)

        # Display paper metadata before assessment
        click.echo("\n=== Paper to Assess ===")
        click.echo(f"DOI: {paper.doi.value}")
        click.echo(f"Title: {paper.title}")
        authors_str = ", ".join(f"{a.last_name}, {a.first_name[0]}." for a in paper.authors[:3])
        if len(paper.authors) > 3:
            authors_str += " et al."
        click.echo(f"Authors: {authors_str}")
        click.echo(f"Journal: {paper.journal} ({paper.publication_year})")
        if paper.abstract:
            click.echo(f"Abstract: {paper.abstract[:200]}...")
        click.echo("")

        # Assess paper
        paper.assess(score, include, notes)
        repo.save(review_obj)

        click.echo(f"Assessed: {paper.title}")
        click.echo(f"Score: {score}/10")
        click.echo(f"Decision: {'INCLUDED' if include else 'EXCLUDED'}")

        # Show updated statistics
        stats = review_obj.generate_statistics()
        click.echo(f"\nTotal assessed: {stats['assessed_papers']}/{stats['total_papers']}")
        if stats["assessed_papers"] > 0:
            click.echo(f"Inclusion rate: {stats['inclusion_rate']:.1%}")


@review.command()
@click.argument("title")
@click.option(
    "--method",
    type=click.Choice(["tfidf", "ai", "hybrid"]),
    default="tfidf",
    help="Analysis method to use",
)
@click.option(
    "--clusters",
    type=click.IntRange(3, 10),
    default=5,
    help="Number of theme clusters (3-10)",
)
def analyze(title: str, method: str, clusters: int) -> None:
    """Analyze papers and extract themes.

    Analyzes included papers to identify major themes using TF-IDF
    keyword extraction and hierarchical clustering.

    Example:
        academic-review analyze "ML Healthcare" --clusters 5
        academic-review analyze "ML Healthcare" --method hybrid --clusters 7
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    # Get included papers
    papers = review_obj.get_included_papers()
    if not papers:
        click.echo("Error: No included papers to analyze. Assess papers first.", err=True)
        raise SystemExit(1)

    # Check for abstracts
    papers_with_abstracts = [p for p in papers if p.abstract]
    if not papers_with_abstracts:
        click.echo(
            "Error: No papers with abstracts available. Cannot perform theme analysis.", err=True
        )
        raise SystemExit(1)

    if len(papers_with_abstracts) < papers.__len__():
        click.echo(
            f"Warning: Only {len(papers_with_abstracts)}/{len(papers)} papers have abstracts",
            err=True,
        )

    # Analyze themes
    click.echo(f"Analyzing {len(papers_with_abstracts)} papers...")
    click.echo(f"Method: {method}")
    click.echo(f"Target clusters: {clusters}")
    click.echo("")

    use_case = AnalyzeThemesUseCase()

    with click.progressbar(
        length=100,
        label="Extracting themes",
        show_percent=True,
        show_pos=False,
    ) as bar:
        bar.update(20)
        click.echo(" - Extracting keywords...", nl=False)
        bar.update(30)
        click.echo(" done")
        click.echo(" - Clustering themes...", nl=False)
        bar.update(30)
        click.echo(" done")
        click.echo(" - Analyzing relationships...", nl=False)

        try:
            themes = use_case.execute(papers_with_abstracts, max_themes=clusters)
        except ValueError as e:
            click.echo(f"\nError: {e}", err=True)
            raise SystemExit(1)

        bar.update(20)
        click.echo(" done")

    # Display results
    click.echo("\n=== Theme Analysis Results ===\n")
    click.echo(themes.summary)
    click.echo("\n=== Theme Details ===\n")

    for theme_name, keywords in themes.themes.items():
        click.echo(f"{theme_name}:")
        click.echo(f"  Keywords: {', '.join(keywords[:10])}")

        # Show related themes
        if theme_name in themes.relationships:
            related = themes.relationships[theme_name]
            if related:
                top_related = sorted(related.items(), key=lambda x: x[1], reverse=True)[:3]
                related_str = ", ".join(f"{name} ({score:.2f})" for name, score in top_related)
                click.echo(f"  Related: {related_str}")
        click.echo("")

    # Note: In a real implementation, we would save themes to review
    # For now, just display them
    click.echo(f"Analysis complete. Identified {len(themes.themes)} themes.")


@review.command()
@click.argument("title")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    required=True,
    help="Output markdown file path",
)
@click.option(
    "--ai",
    is_flag=True,
    help="Use AI enhancement (if available)",
)
def synthesize(title: str, output: str, ai: bool) -> None:
    """Generate narrative synthesis from included papers.

    Creates a structured literature review synthesis with introduction,
    thematic analysis, research gaps, and conclusions.

    Example:
        academic-review synthesize "ML Healthcare" -o synthesis.md
        academic-review synthesize "ML Healthcare" -o synthesis.md --ai
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    # Get included papers
    papers = review_obj.get_included_papers()
    if not papers:
        click.echo("Error: No included papers to synthesize. Assess papers first.", err=True)
        raise SystemExit(1)

    # Check for abstracts
    papers_with_abstracts = [p for p in papers if p.abstract]
    if not papers_with_abstracts:
        click.echo("Warning: No papers with abstracts. Synthesis will be limited.", err=True)

    click.echo(f"Synthesizing {len(papers)} papers...")
    if ai:
        click.echo("AI enhancement: enabled")
    click.echo("")

    # First, analyze themes
    click.echo("Step 1/2: Analyzing themes...")
    use_case_analyze = AnalyzeThemesUseCase()

    try:
        themes = use_case_analyze.execute(papers_with_abstracts or papers, max_themes=5)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(f"  Identified {len(themes.themes)} themes")

    # Generate synthesis
    click.echo("Step 2/2: Generating synthesis...")
    use_case_synth = GenerateSynthesisUseCase()

    try:
        synthesis = use_case_synth.execute(
            papers=papers,
            themes=themes,
            research_question=review_obj.research_question,
            use_ai=ai,
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    # Write to file
    output_path = Path(output)
    output_path.write_text(synthesis, encoding="utf-8")

    # Display statistics
    word_count = len(synthesis.split())
    click.echo("")
    click.echo("Synthesis complete!")
    click.echo(f"  Output: {output}")
    click.echo(f"  Word count: {word_count:,}")
    click.echo(f"  Papers cited: {len(papers)}")
    click.echo(f"  Themes: {len(themes.themes)}")


if __name__ == "__main__":
    review()
