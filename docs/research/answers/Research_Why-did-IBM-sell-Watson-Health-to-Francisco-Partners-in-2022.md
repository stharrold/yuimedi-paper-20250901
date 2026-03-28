# Why did IBM sell Watson Health to Francisco Partners in 2022?

**Status:** Answered
**Scope:** Paper1
**Search Date:** 2026-01-01
**Search Method:** Google Scholar Labs

## Summary

IBM sold Watson Health to Francisco Partners in January 2022 after years of underperformance. Academic literature identifies multiple contributing factors: a fundamental mismatch between AI capabilities and clinical reality, overpromising and underdelivering on AI healthcare applications, lack of domain expertise in healthcare, restrictive top-down commercialization strategy, suboptimal business performance (only breaking even), and the highly-regulated nature of the healthcare industry creating barriers to AI deployment.

## Key Findings

### Primary Causes of Divestiture

1. **Overpromising and Underdelivering:** IBM generated significant hubris and skepticism by boasting about Watson's capabilities before the technology could deliver. The company was criticized for being first to trumpet AI's potential in healthcare while failing to meet expectations [@strickland2019].

2. **Fundamental AI-Healthcare Mismatch:** There was a core mismatch between how machines learn (requiring structured data) and how doctors work (with messy, unstructured clinical reality). Watson's powerful technology was no match for the contemporary healthcare system's complexity [@strickland2019].

3. **Suboptimal Business Performance:** Watson Health's business performance was suboptimal, only managing to break even. IBM failed to generate significant profits from Watson due to General Purpose Technology limitations [@yang2020].

4. **Restrictive Commercialization Strategy:** IBM's top-down approach to pursuing use cases for Watson restricted innovation and commercialization opportunities. The decision to sell Watson Health primarily to hospitals limited market reach [@yang2020].

5. **Lack of Domain Expertise:** AI projects like Watson for Oncology suffered from lack of expert understanding regarding necessary healthcare domain knowledge. AI tools lacked the ability to diagnose patients like a physician [@dutta2023].

6. **Regulatory Complexity:** The highly-regulated nature of the healthcare industry created significant challenges for AI deployment and commercialization [@yang2020].

7. **Accuracy and Ethical Issues:** Watson Health encountered challenges with accuracy and ethical issues in AI healthcare applications. Analysis suggested returns were unlikely to materialize [@shekhar2025].

### Broader Context

The Watson Health divestiture represents a cautionary tale about AI hype cycles in healthcare. Despite IBM's significant investment and marketing, the gap between AI promise and clinical utility proved insurmountable within IBM's business model. The sale to Francisco Partners allowed IBM to exit while the private equity firm could potentially restructure the business with different expectations.

## Sources

### Primary Sources

1. **Strickland E** (2019). IBM Watson, heal thyself: How IBM overpromised and underdelivered on AI health care. IEEE Spectrum.
   - URL: https://ieeexplore.ieee.org/abstract/document/8678513/
   - PDF: http://www.mit.bme.hu/system/files/oktatas/targyak/9890/How_IBM_Watson_Overpromised_and_Underdelivered_on_AI_Health_Care_-_IEEE_Spectrum.pdf
   - Key finding: Fundamental mismatch between machine learning and clinical practice; hubris and hype
   - **Cited by: 516**

2. **Yang J, Chesbrough H, Hurmelinna-Laukkanen P** (2020). The rise, fall, and resurrection of IBM Watson Health. University of Oulu.
   - URL: https://oulurepo.oulu.fi/bitstream/handle/10024/27921/nbnfi-fe2020050424858.pdf
   - Key finding: Suboptimal business performance; restrictive top-down strategy; GPT limitations
   - Cited by: 7

3. **Dutta S, Faheem H** (2023). Artificial intelligence failure at IBM 'Watson for Oncology'. IUP Journal of Knowledge Management.
   - URL: https://search.proquest.com/openview/5d55d56634fb060f97ae707091489ec9/1
   - Key finding: Lack of domain expertise; AI tools couldn't diagnose like physicians
   - Cited by: 24

4. **Shekhar A, Gupta R, Sharma SK** (2025). IBM Watson health growth strategy: Is artificial intelligence (AI) the answer. Communications of the Association for Information Systems.
   - URL: https://aisel.aisnet.org/cais/vol57/iss1/63/
   - Key finding: Accuracy challenges, ethical issues, poor financial returns
   - Cited by: 1

## Relevance to Paper 1

This research directly supports Section 4.3 (Failed Standardization Approaches) of the three-pillar framework:

1. **Technical barriers (Pillar 3):** Watson's failure illustrates the gap between AI capabilities and healthcare's complexity, including unstructured data, clinical workflow variability, and regulatory requirements.

2. **Analytics maturity (Pillar 1):** Healthcare organizations lacked the data infrastructure and governance needed for AI-driven analytics, contributing to Watson's deployment challenges.

3. **Institutional knowledge (Pillar 2):** The lack of domain expertise at IBM and the mismatch between AI engineers and clinical practitioners demonstrates the importance of preserving and leveraging healthcare-specific knowledge.

The IBM Watson Health case, alongside Haven, provides evidence that even well-resourced technology initiatives face structural barriers when attempting to standardize healthcare analytics.

## Potential Citations for paper.md

```bibtex
@article{strickland2019,
  author = {Strickland, E.},
  title = {{IBM Watson, heal thyself: How IBM overpromised and underdelivered on AI health care}},
  journal = {IEEE Spectrum},
  year = {2019},
  volume = {56},
  number = {4},
  pages = {24--31},
  doi = {10.1109/MSPEC.2019.8678513},
  url = {https://ieeexplore.ieee.org/abstract/document/8678513/},
  note = {Watson Health failure analysis; cited by 516},
}

@techreport{yang2020,
  author = {Yang, J. and Chesbrough, H. and Hurmelinna-Laukkanen, P.},
  title = {{The rise, fall, and resurrection of IBM Watson Health}},
  year = {2020},
  institution = {University of Oulu},
  url = {https://oulurepo.oulu.fi/bitstream/handle/10024/27921/nbnfi-fe2020050424858.pdf},
  note = {Watson Health business performance and strategy analysis},
}
```
