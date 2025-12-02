"""CLI interface for academic literature review workflow.

Provides Click commands for managing literature reviews including
initialization, searching, assessment, and export.
"""

import os
from pathlib import Path

import click

from lit_review.application.usecases.export_review import ExportFormat, ExportReviewUseCase
from lit_review.application.usecases.search_papers import SearchPapersUseCase
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.exceptions import EntityNotFoundError
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

    # Search
    click.echo(f"Searching {database} for: {keywords}")
    use_case = get_search_use_case()

    try:
        papers = use_case.execute(keywords, databases=[database], limit=limit)
    except (ConnectionError, TimeoutError) as e:
        click.echo(f"Error: Search failed - {e}", err=True)
        raise SystemExit(1)

    if not papers:
        click.echo("No papers found.")
        return

    # Add papers to review
    added = review_obj.add_papers(papers)
    repo.save(review_obj)

    click.echo(f"Found {len(papers)} papers, added {added} new papers.")
    click.echo(f"Total papers in review: {len(review_obj.papers)}")


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
    "fmt",
    type=click.Choice(["bibtex", "json"]),
    default="bibtex",
    help="Export format",
)
@click.option("-o", "--output", required=True, help="Output file path")
@click.option("--all", "export_all", is_flag=True, help="Export all papers, not just included")
def export_cmd(title: str, fmt: str, output: str, export_all: bool) -> None:
    """Export review to file.

    Exports papers from the review in the specified format.
    By default, only exports papers marked as included.

    Example:
        academic-review export "ML Healthcare" -f bibtex -o refs.bib
    """
    repo = get_repository()

    try:
        review_obj = repo.load(title)
    except EntityNotFoundError:
        click.echo(f"Error: Review '{title}' not found.", err=True)
        raise SystemExit(1)

    export_format = ExportFormat.BIBTEX if fmt == "bibtex" else ExportFormat.JSON
    output_path = Path(output)

    use_case = ExportReviewUseCase()

    try:
        count = use_case.execute(
            review_obj,
            export_format,
            output_path,
            included_only=not export_all,
        )
    except OSError as e:
        click.echo(f"Error: Failed to write file - {e}", err=True)
        raise SystemExit(1)

    click.echo(f"Exported {count} papers to {output}")


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


if __name__ == "__main__":
    review()
