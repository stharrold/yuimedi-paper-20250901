"""Shared pytest fixtures for lit_review tests."""

import json
from pathlib import Path

import pytest

from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


@pytest.fixture
def sample_doi() -> DOI:
    """Return a valid sample DOI."""
    return DOI("10.1234/sample-article-2024")


@pytest.fixture
def sample_author() -> Author:
    """Return a sample author."""
    return Author(
        last_name="Smith",
        first_name="John",
        initials="J.",
        orcid="0000-0001-2345-6789",
    )


@pytest.fixture
def sample_authors() -> list[Author]:
    """Return a list of sample authors."""
    return [
        Author(last_name="Smith", first_name="John", initials="J."),
        Author(last_name="Jones", first_name="Jane", initials="J."),
        Author(last_name="Wilson", first_name="Bob", initials="B."),
    ]


@pytest.fixture
def sample_paper(sample_doi: DOI, sample_authors: list[Author]) -> Paper:
    """Return a sample paper entity."""
    return Paper(
        doi=sample_doi,
        title="A Sample Research Paper",
        authors=sample_authors,
        publication_year=2024,
        journal="Journal of Testing",
        abstract="This is a sample abstract for testing purposes.",
        keywords=["testing", "sample", "research"],
    )


@pytest.fixture
def sample_review() -> Review:
    """Return a sample review entity."""
    return Review(
        title="Sample Literature Review",
        research_question="What is the impact of testing on software quality?",
        inclusion_criteria=["Peer-reviewed", "English language", "Published after 2020"],
        exclusion_criteria=["Conference abstracts", "Non-empirical studies"],
    )


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_papers_json(fixtures_dir: Path) -> list[dict]:
    """Load sample papers from JSON fixture."""
    json_path = fixtures_dir / "sample_papers.json"
    if json_path.exists():
        data = json.loads(json_path.read_text())
        return data.get("papers", [])
    return []


@pytest.fixture
def mock_crossref_response(fixtures_dir: Path) -> dict:
    """Load mock Crossref response from JSON fixture."""
    json_path = fixtures_dir / "mock_crossref_response.json"
    if json_path.exists():
        return json.loads(json_path.read_text())
    return {}


@pytest.fixture
def sample_review_with_papers(sample_review: Review) -> Review:
    """Return a sample review with papers in SEARCH stage."""
    sample_review.advance_stage()  # Move to SEARCH

    papers = [
        Paper(
            doi=DOI("10.1038/nature12373"),
            title="Machine learning for healthcare",
            authors=[Author("Chen", "Tianqi", "T.")],
            publication_year=2023,
            journal="Nature Medicine",
        ),
        Paper(
            doi=DOI("10.1016/j.jbi.2023.104567"),
            title="NLP in clinical text mining",
            authors=[Author("Wang", "Yanshan", "Y.")],
            publication_year=2023,
            journal="Journal of Biomedical Informatics",
        ),
    ]

    for paper in papers:
        sample_review.add_paper(paper)

    return sample_review
