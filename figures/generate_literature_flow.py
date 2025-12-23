#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Generate PRISMA 2020 Literature Selection Flow diagram as SVG using Graphviz."""

from graphviz import Digraph


def create_literature_flow() -> Digraph:
    """Create the PRISMA 2020 literature flow diagram."""
    dot = Digraph(
        name="literature_flow",
        comment="PRISMA 2020 Literature Selection Flow",
        format="svg",
        graph_attr={
            "label": "PRISMA 2020 Literature Selection Flow",
            "labelloc": "t",
            "fontsize": "18",
            "fontname": "Helvetica-Bold",
            "fontcolor": "#1E3A5F",
            "rankdir": "TB",
            "splines": "spline",
            "nodesep": "0.25",
            "ranksep": "0.4",
            "margin": "0.2",
            "compound": "true",
        },
        node_attr={
            "fontname": "Helvetica",
            "fontsize": "9",
            "margin": "0.1,0.05",
        },
        edge_attr={
            "fontname": "Helvetica",
            "fontsize": "8",
            "color": "#1E3A5F",
        },
    )

    # IDENTIFICATION subgraph
    with dot.subgraph(name="cluster_ID") as c:
        c.attr(
            label="IDENTIFICATION",
            style="rounded",
            color="#1E3A5F",
            bgcolor="#f5f5f5",
            fontsize="10",
            margin="8",
        )

        # Database sources (cylinder shape)
        c.node(
            "A1",
            "Crossref\n(n=285)",
            shape="cylinder",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
            width="0.8",
            height="0.5",
        )
        c.node(
            "A2",
            "PubMed\n(n=142)",
            shape="cylinder",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
            width="0.8",
            height="0.5",
        )
        c.node(
            "A3",
            "ArXiv\n(n=71)",
            shape="cylinder",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
            width="0.8",
            height="0.5",
        )
        c.node(
            "A4",
            "Semantic Scholar\n(n=72)",
            shape="cylinder",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
            width="0.8",
            height="0.5",
        )

        # Articles identified (rectangle)
        c.node(
            "A",
            "Articles identified\nafter deduplication\n(n=570)",
            shape="box",
            style="filled,rounded",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
        )

    # SCREENING subgraph
    with dot.subgraph(name="cluster_SC") as c:
        c.attr(
            label="SCREENING",
            style="rounded",
            color="#1E3A5F",
            bgcolor="#f5f5f5",
            fontsize="10",
            margin="8",
        )

        # Title/abstract screening (diamond)
        c.node(
            "D",
            "Title/abstract\nscreening\n(n=570)",
            shape="diamond",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
        )

        # Articles excluded (rectangle)
        c.node(
            "E",
            "Articles excluded (n=480)\n• Not relevant to framework\n• Outside scope\n• Non-English",
            shape="box",
            style="filled,rounded",
            fillcolor="#f5f5f5",
            color="#999999",
        )

        # Full-text eligibility screening (diamond)
        c.node(
            "H",
            "Full-text eligibility\nscreening (n=90)",
            shape="diamond",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
        )

        # Articles excluded (rectangle)
        c.node(
            "I",
            "Articles excluded (n=46)\n• No verifiable DOI/URL (n=18)\n• Vendor marketing only (n=15)\n• Methodological concerns (n=13)",
            shape="box",
            style="filled,rounded",
            fillcolor="#f5f5f5",
            color="#999999",
        )

    # QUALITY ASSESSMENT subgraph
    with dot.subgraph(name="cluster_QA") as c:
        c.attr(
            label="QUALITY ASSESSMENT",
            style="rounded",
            color="#1E3A5F",
            bgcolor="#f5f5f5",
            fontsize="10",
            margin="8",
        )

        # Source classification (diamond)
        c.node(
            "J",
            "Source\nclassification\n(n=44)",
            shape="diamond",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
        )

        # AACODS checklist (diamond)
        c.node(
            "L",
            "AACODS\nchecklist\n(n=14)",
            shape="diamond",
            style="filled",
            fillcolor="#f5f5f5",
            color="#1E3A5F",
        )

        # Articles excluded (rectangle)
        c.node(
            "N",
            "Articles excluded (n=3)\n• Low objectivity\n• Insufficient detail",
            shape="box",
            style="filled,rounded",
            fillcolor="#f5f5f5",
            color="#999999",
        )

    # INCLUDED subgraph
    with dot.subgraph(name="cluster_IN") as c:
        c.attr(
            label="INCLUDED",
            style="rounded",
            color="#1E3A5F",
            bgcolor="#e8e8e8",
            fontsize="10",
            margin="8",
        )

        # Final corpus (rectangle)
        c.node(
            "O",
            "Final corpus (n=41)\nAcademic: 30\nIndustry: 11",
            shape="box",
            style="filled,rounded",
            fillcolor="#e8e8e8",
            color="#1E3A5F",
        )

    # Edges - IDENTIFICATION
    dot.edge("A1", "A")
    dot.edge("A2", "A")
    dot.edge("A3", "A")
    dot.edge("A4", "A")

    # Edges - SCREENING
    dot.edge("A", "D")
    dot.edge("D", "E", xlabel="Excluded")
    dot.edge("D", "H", xlabel="Passed")
    dot.edge("H", "I", xlabel="Excluded")

    # Edges - QUALITY ASSESSMENT
    dot.edge("H", "J", xlabel="Passed")
    dot.edge("J", "L", xlabel="Grey literature")
    dot.edge("L", "N", xlabel="Excluded")

    # Edges - INCLUDED
    dot.edge("J", "O", xlabel="Academic")
    dot.edge("L", "O", xlabel="Passed")

    return dot


def main() -> None:
    """Generate and save the literature flow diagram."""
    import pathlib

    output_dir = pathlib.Path(__file__).parent
    dot = create_literature_flow()

    # Render to SVG (graphviz adds .svg extension automatically)
    output_path = output_dir / "literature-flow"
    dot.render(output_path, cleanup=True)
    print(f"Generated: {output_path}.svg")


if __name__ == "__main__":
    main()
