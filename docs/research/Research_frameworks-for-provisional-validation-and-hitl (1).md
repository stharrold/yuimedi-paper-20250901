# Research: Frameworks for Provisional Validation and HITL

**Question:** What frameworks exist for 'provisional validation' or 'human-in-the-loop' systems where domain knowledge is captured incrementally through iterative feedback cycles?

**Scope:** Paper1 (Analytical Framework)

**Source:** Google Scholar Labs

---

## Key Findings

Research identifies three specific frameworks that formalize "provisional validation" and incremental knowledge capture, validating the shift from "Eternal Truth" to iterative refinement.

1.  **Interactive Machine Learning (IML):** Mosqueira-Rey et al. (2023, 1039 citations) define IML as a sub-field of HITL where users supply feedback in a "focused, frequent, and incremental way." This contrasts with traditional batch learning and directly supports the concept of capturing domain knowledge through iterative cycles.
2.  **Machine Teaching (MT):** Distinct from active learning (where the AI asks questions), Machine Teaching puts the *human expert* in control of the learning process. This framework is specifically designed to allow experts to transfer their domain knowledge to the model efficiently, acting as a "teacher" rather than just an annotator.
3.  **Human-on-the-Loop (HotL):** Bravo Rocca (2023) introduces the "Human-on-the-Loop" paradigm for continual learning. This approach uses human specialists not just to label data, but to guide autonomous processes for model adaptation, identifying when adaptation is necessary without requiring explicit task boundaries.
4.  **Incremental Refinement:** Kumar et al. (2024) detail that effective HITL frameworks involve data pre-processing, modeling, and modification phases where "unbiased human feedback" is used to refine the model iteratively, rather than validating a final output once.

## Sources

| Study | Key Finding | Citation | URL / PDF |
|-------|-------------|----------|-----------|
| Mosqueira-Rey et al. (2023) | IML and Machine Teaching frameworks enable focused, frequent, and incremental knowledge transfer from experts. | Mosqueira-Rey, E., et al. (2023). Human-in-the-loop machine learning: a state of the art. *Artificial Intelligence Review*. | [PDF](https://link.springer.com/content/pdf/10.1007/s10462-022-10246-w.pdf) |
| Bravo Rocca (2023) | "Human-on-the-Loop" paradigm uses experts to guide continual learning and model adaptation. | Bravo Rocca, G. J. (2023). Human-on-the-loop continual learning. *Universitat Politècnica de Catalunya*. | [PDF](https://www.tdx.cat/bitstream/handle/10803/695722/TGJBR1de1.pdf?sequence=1) |
| Kumar et al. (2024) | Iterative HITL frameworks integrate human expertise to refine prediction models continuously. | Kumar, S., et al. (2024). Applications, challenges, and future directions of human-in-the-loop learning. *IEEE*. | [PDF](https://ieeexplore.ieee.org/iel7/6287639/6514899/10530996.pdf) |
