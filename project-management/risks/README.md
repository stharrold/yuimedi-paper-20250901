# Risk Management

This directory contains risk assessment and management documentation for the YuiQuery Healthcare Analytics research project.

## Contents

| File | Description |
|------|-------------|
| `risk-register.csv` | Initial risk register |
| `risk-register-v2.csv` | Updated risk register with mitigations |

## Risk Categories

### Critical Risks
- **Single Point of Failure**: Primary developer unavailability
- **Data Access**: Healthcare data access delays or restrictions

### High Risks
- **Budget Overrun**: Scope expansion or unforeseen costs
- **Timeline Delays**: Research or publication delays

### Medium Risks
- **Technical Complexity**: NL2SQL accuracy challenges
- **Regulatory Changes**: HIPAA/compliance requirement changes

## Risk Assessment Methodology

Risk scoring uses:
- **Probability**: 1-5 scale (Very Low to Very High)
- **Impact**: 1-5 scale (Negligible to Catastrophic)
- **Risk Score**: Probability x Impact (1-25)

See `../risk-assessment-methodology.md` for detailed methodology.

## Mitigation Strategies

Key mitigations implemented:
1. Backup developer assigned
2. Synthetic data backup (Synthea)
3. Phased budget approval
4. Quality gates at each milestone

## Related Documentation

- `../risk-assessment-methodology.md` - Methodology documentation
- `../probability-calculation.md` - Success probability calculations
- `../budget/` - Budget allocation for risk mitigation
