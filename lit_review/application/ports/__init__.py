"""Application ports - abstract interfaces for external dependencies."""

from lit_review.application.ports.paper_repository import PaperRepository
from lit_review.application.ports.search_service import SearchService

__all__ = ["SearchService", "PaperRepository"]
