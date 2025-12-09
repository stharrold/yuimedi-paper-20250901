"""Analyze themes use case using TF-IDF and hierarchical clustering.

This use case extracts themes from a collection of papers using:
1. TF-IDF for keyword extraction
2. Co-occurrence matrix for keyword relationships
3. Hierarchical clustering (Ward linkage) for theme grouping
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore[import-untyped]
from scipy.spatial.distance import pdist  # type: ignore[import-untyped]
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore[import-untyped]

from lit_review.application.ports.ai_analyzer import ThemeHierarchy
from lit_review.domain.entities.paper import Paper


@dataclass
class AnalyzeThemesUseCase:
    """Use case for extracting themes from papers using TF-IDF and clustering.

    This implementation uses keyword-based analysis without requiring AI APIs.
    Performance optimized for <30s processing of 500 papers.

    Attributes:
        max_features: Maximum number of keywords to extract per theme.
        min_df: Minimum document frequency for keywords (filters rare terms).
        max_df: Maximum document frequency for keywords (filters common terms).
    """

    max_features: int = 100
    min_df: int = 2
    max_df: float = 0.8

    def execute(
        self,
        papers: list[Paper],
        max_themes: int = 10,
    ) -> ThemeHierarchy:
        """Extract hierarchical themes from papers.

        Args:
            papers: List of papers to analyze (must have abstracts).
            max_themes: Maximum number of themes to extract.

        Returns:
            ThemeHierarchy with themes, relationships, and summary.

        Raises:
            ValueError: If papers list is empty, no abstracts available,
                       or max_themes is invalid.
        """
        if not papers:
            raise ValueError("Cannot analyze themes from empty paper list")

        if max_themes < 1:
            raise ValueError("max_themes must be at least 1")

        # Filter papers with abstracts
        papers_with_abstracts = [p for p in papers if p.abstract]
        if not papers_with_abstracts:
            raise ValueError("No papers with abstracts available for analysis")

        # Extract keywords using TF-IDF
        keywords, tfidf_matrix = self._extract_keywords(papers_with_abstracts)

        # Build co-occurrence matrix
        cooccurrence = self._build_cooccurrence_matrix(tfidf_matrix)

        # Cluster keywords into themes
        theme_clusters = self._cluster_keywords(cooccurrence, keywords, max_themes)

        # Calculate theme relationships
        relationships = self._calculate_theme_relationships(theme_clusters, cooccurrence)

        # Generate summary
        summary = self._generate_summary(theme_clusters, len(papers_with_abstracts))

        return ThemeHierarchy(
            themes=theme_clusters,
            relationships=relationships,
            summary=summary,
        )

    def _extract_keywords(self, papers: list[Paper]) -> tuple[list[str], np.ndarray[Any, Any]]:
        """Extract keywords from papers using TF-IDF.

        Args:
            papers: Papers with abstracts.

        Returns:
            Tuple of (keyword list, TF-IDF matrix).
        """
        # Combine title, abstract, and keywords for better feature extraction
        documents = []
        for paper in papers:
            text_parts = [paper.title]
            if paper.abstract:
                text_parts.append(paper.abstract)
            if paper.keywords:
                text_parts.extend(paper.keywords)
            documents.append(" ".join(text_parts))

        # Adjust parameters for small datasets
        num_docs = len(documents)
        min_df = min(self.min_df, max(1, num_docs // 10))  # At least 1, max 10% of docs

        # For small or very similar documents, use more permissive max_df
        if num_docs <= 10:
            max_df = 1.0  # Allow all terms for small datasets
        else:
            max_df = self.max_df

        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            min_df=min_df,
            max_df=max_df,
            stop_words="english",
            ngram_range=(1, 2),  # Unigrams and bigrams
        )

        tfidf_matrix = vectorizer.fit_transform(documents)
        keywords = vectorizer.get_feature_names_out().tolist()

        return keywords, tfidf_matrix.toarray()

    def _build_cooccurrence_matrix(
        self, tfidf_matrix: np.ndarray[Any, Any]
    ) -> np.ndarray[Any, Any]:
        """Build co-occurrence matrix from TF-IDF matrix.

        Args:
            tfidf_matrix: TF-IDF matrix (documents x keywords).

        Returns:
            Co-occurrence matrix (keywords x keywords).
        """
        # Convert to binary presence matrix
        binary_matrix = (tfidf_matrix > 0).astype(float)

        # Co-occurrence = keyword matrix @ keyword matrix^T
        cooccurrence = binary_matrix.T @ binary_matrix

        # Normalize by document frequency
        doc_freq = np.sum(binary_matrix, axis=0)
        doc_freq_matrix = np.outer(doc_freq, doc_freq)

        # Avoid division by zero
        with np.errstate(divide="ignore", invalid="ignore"):
            normalized = cooccurrence / np.sqrt(doc_freq_matrix)
            normalized = np.nan_to_num(normalized, 0.0)  # type: ignore[call-overload]

        return normalized  # type: ignore[no-any-return]

    def _cluster_keywords(
        self,
        cooccurrence: np.ndarray[Any, Any],
        keywords: list[str],
        max_themes: int,
    ) -> dict[str, list[str]]:
        """Cluster keywords into themes using hierarchical clustering.

        Args:
            cooccurrence: Co-occurrence matrix.
            keywords: List of keyword strings.
            max_themes: Maximum number of themes.

        Returns:
            Dictionary mapping theme names to keyword lists.
        """
        if len(keywords) < max_themes:
            # Not enough keywords for requested themes
            max_themes = max(1, len(keywords) // 2)

        # Convert similarity to distance
        distance_matrix = 1.0 - cooccurrence

        # Handle edge case of single keyword
        if len(keywords) == 1:
            return {"Theme 1": keywords}

        # Hierarchical clustering with Ward linkage
        condensed_dist = pdist(distance_matrix, metric="euclidean")
        linkage_matrix = linkage(condensed_dist, method="ward")

        # Cut tree to get clusters
        cluster_labels = fcluster(linkage_matrix, max_themes, criterion="maxclust")

        # Group keywords by cluster
        theme_clusters: dict[str, list[str]] = {}
        for keyword, label in zip(keywords, cluster_labels):
            theme_name = f"Theme {label}"
            if theme_name not in theme_clusters:
                theme_clusters[theme_name] = []
            theme_clusters[theme_name].append(keyword)

        # Sort keywords within each theme by co-occurrence strength
        for theme_name, theme_keywords in theme_clusters.items():
            keyword_indices = [keywords.index(kw) for kw in theme_keywords]
            keyword_scores = [np.sum(cooccurrence[idx, keyword_indices]) for idx in keyword_indices]
            sorted_keywords = [
                kw for _, kw in sorted(zip(keyword_scores, theme_keywords), reverse=True)
            ]
            theme_clusters[theme_name] = sorted_keywords[:10]  # Top 10 per theme

        return theme_clusters

    def _calculate_theme_relationships(
        self,
        theme_clusters: dict[str, list[str]],
        cooccurrence: np.ndarray[Any, Any],
    ) -> dict[str, dict[str, float]]:
        """Calculate relationships between themes.

        Args:
            theme_clusters: Dictionary mapping theme names to keywords.
            cooccurrence: Co-occurrence matrix.

        Returns:
            Dictionary mapping theme names to related themes with similarity scores.
        """
        theme_names = list(theme_clusters.keys())
        relationships: dict[str, dict[str, float]] = {}

        # Calculate cross-theme similarity
        for i, theme1 in enumerate(theme_names):
            relationships[theme1] = {}
            for j, theme2 in enumerate(theme_names):
                if i != j:
                    # Calculate average co-occurrence between theme keywords
                    keywords1 = theme_clusters[theme1]
                    keywords2 = theme_clusters[theme2]

                    # Get all keywords for indexing
                    all_keywords = []
                    for keywords in theme_clusters.values():
                        all_keywords.extend(keywords)
                    all_keywords = list(set(all_keywords))

                    try:
                        indices1 = [all_keywords.index(kw) for kw in keywords1]
                        indices2 = [all_keywords.index(kw) for kw in keywords2]

                        # Average co-occurrence
                        similarities = [
                            cooccurrence[idx1, idx2]
                            for idx1 in indices1
                            for idx2 in indices2
                            if idx1 < cooccurrence.shape[0] and idx2 < cooccurrence.shape[1]
                        ]
                        avg_similarity = float(np.mean(similarities)) if similarities else 0.0

                        if avg_similarity > 0.1:  # Only include significant relationships
                            relationships[theme1][theme2] = avg_similarity
                    except (ValueError, IndexError):
                        # Keywords not found in co-occurrence matrix
                        continue

        return relationships

    def _generate_summary(self, theme_clusters: dict[str, list[str]], num_papers: int) -> str:
        """Generate textual summary of themes.

        Args:
            theme_clusters: Dictionary mapping theme names to keywords.
            num_papers: Number of papers analyzed.

        Returns:
            Summary string.
        """
        num_themes = len(theme_clusters)
        theme_summaries = []

        for theme_name, keywords in theme_clusters.items():
            top_keywords = ", ".join(keywords[:5])
            theme_summaries.append(f"- **{theme_name}**: {top_keywords}")

        summary = f"""Analyzed {num_papers} papers and identified {num_themes} major themes:

{chr(10).join(theme_summaries)}

These themes were extracted using TF-IDF keyword analysis and hierarchical clustering \
to identify groups of related concepts."""

        return summary
