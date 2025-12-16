# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Application ports - abstract interfaces for external dependencies."""

from lit_review.application.ports.ai_analyzer import AIAnalyzer, ThemeHierarchy
from lit_review.application.ports.paper_repository import PaperRepository
from lit_review.application.ports.search_service import SearchService

__all__ = ["SearchService", "PaperRepository", "AIAnalyzer", "ThemeHierarchy"]
