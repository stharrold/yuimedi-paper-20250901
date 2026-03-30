# Research: Frameworks for Provisional Validation and Human-in-the-Loop Systems

**Issue:** [Paper 1 Research]
**Scope:** Paper 1 (Three-Pillar Framework)
**Status:** Answered

## Executive Summary
Frameworks for **provisional validation** and **human-in-the-loop (HITL)** oversight in healthcare AI focus on mitigating the risks of "fatal" errors through stringent accuracy assessments and iterative feedback cycles. Key frameworks like **CRAFT-MD** and **MedAgentBench** provide structured environments for evaluating clinical LLMs, emphasizing human review as an essential safeguard for safe implementation.

---

## Human-in-the-Loop (HITL) Frameworks

### 1. MedAgentBench (2025)
Jiang et al. (2025) proposed MedAgentBench, a virtual EHR environment specifically designed to benchmark medical LLM agents:
- **Rule-Based Validity Checks:** The framework uses manually written rule-based checks to verify the correctness of actions (e.g., payload of POST requests).
- **Single-Attempt Constraint:** assesses models using **pass@1**, reflecting the clinical requirement for high accuracy where even a single incorrect action can have significant consequences.
- **Human Oversight:** Involving human staff is considered "essential to ensure safe and effective implementation" of AI/ML tools (AHIMA, 2023).

### 2. CRAFT-MD (2024)
Johri et al. (2024) introduced CRAFT-MD, a conversational evaluation framework for comprehensive assessment of clinical LLMs:
- **Conversational Interaction:** assessed model performance through multi-turn tool-agent-user interactions, mirroring real-world clinical data retrieval.
- **Iterative Feedback:** emphasizes capturing domain knowledge incrementally through continuous interaction and feedback from medical professionals.

---

## Provisional Validation and Incremental Capture

### 1. Active Knowledge Capture
Ideally, knowledge capture systems should consume minimal time and create immediate value (Ju, 2024). In the context of healthcare analytics:
- **Active Validation:** Validation happens at the point of use (Active Validation), where the query itself serves as the documentation (Moore, 2018).
- **Incremental Growth:** Rather than requiring full upfront documentation, systems accumulate knowledge incrementally through confirmed query-SQL pairs.

### 2. Safeguarding against "Fatal" Mistakes
Lee (2023) highlights that healthcare QA systems must avoid fatal mistakes—incorrectly executing unanswerable questions. Provisional validation by human experts serves as the primary mechanism to filter these errors before they reach clinical decision-makers.

---

## References
- AHIMA-NORC. (2023). *Health Information Workforce Survey: Workforce Challenges and Emerging Technologies*.
- Jiang, Y., et al. (2025). MedAgentBench: A virtual EHR environment to benchmark medical LLM agents. *NEJM AI*.
- Johri, S., et al. (2024). CRAFT-MD: a conversational evaluation framework for comprehensive assessment of clinical LLMs. *AAAI Spring Symposium*.
- Ju, W., et al. (2024). ActiveNavigator: Toward Real-Time Knowledge Capture and Feedback in Design Workspaces. *IJEE*.
- Lee, J., et al. (2023). EHRSQL: A New Text-to-SQL Benchmark for Electronic Health Records. *arXiv preprint*.
- Moore, D., et al. (2018). ActiveNavigator: Toward real-time knowledge capture and feedback in active learning spaces. *IJEE*.
