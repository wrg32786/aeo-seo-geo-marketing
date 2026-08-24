# Organic Discovery AI Shelf Map

Exact surfaces are reported separately. Branded validation is excluded from unbranded recommendation-share denominators. No opaque GEO score or fixed time-to-shelf promise is produced.

## Surface groups

| Group | Prompt family | Surface | Market | Branded | Runs | State | Confidence |
|---|---|---|---|---:|---:|---|---|
| `surface-3a76d0bb878d` | sensitive-skin-magnesium | google / gemini-web / grounded | US / en | false | 4 | **locked** | low |
| `surface-6072eb9b66d5` | travel-deodorant | openai / chatgpt-search / web-search | US / en | false | 4 | **fragmented** | low |
| `surface-7d21bf96ab92` | eczema-safe-deodorant | openai / chatgpt-search / web-search | US / en | false | 4 | **unsafe** | low |
| `surface-d1effe1aa90f` | sensitive-skin-magnesium | openai / chatgpt-search / web-search | US / en | true | 2 | **unknown** | low |
| `surface-e697282df0c7` | best-natural-deodorant | openai / chatgpt-search / web-search | US / en | false | 4 | **locked** | low |
| `surface-f2900f34b318` | sensitive-skin-magnesium | openai / chatgpt-search / web-search | US / en | false | 4 | **open** | low |

## Classification rationale

### surface-3a76d0bb878d — locked
- top first-mentioned share=1.00
- top entity recommendation rate=1.00
- set agreement=1.00
- Recommendation coverage: 4/4 (1.0)
- Set agreement: 1.0
- Volatility: 0.0
- Fidelity: 4/4 (1.0)
- Constraint satisfaction: 4/4 (1.0)

### surface-6072eb9b66d5 — fragmented
- 4 distinct first-mentioned entities
- set agreement=0.22
- Recommendation coverage: 4/4 (1.0)
- Set agreement: 0.2222
- Volatility: 0.7778
- Fidelity: 4/4 (1.0)
- Constraint satisfaction: 4/4 (1.0)

### surface-7d21bf96ab92 — unsafe
- fidelity rate 0.25 is below 0.75
- constraint satisfaction 0.25 is below 0.75
- unavailable recommendation rate 0.50 exceeds 0.20
- Recommendation coverage: 4/4 (1.0)
- Set agreement: 1.0
- Volatility: 0.0
- Fidelity: 1/4 (0.25)
- Constraint satisfaction: 1/4 (0.25)
- Integrity issues:
  - constraint satisfaction 0.25 is below 0.75
  - fidelity rate 0.25 is below 0.75
  - no publishable fact establishes fit for this prompt family
  - one or more prompt-family facts are prohibited
  - unavailable recommendation rate 0.50 exceeds 0.20

### surface-d1effe1aa90f — unknown
- branded validation group; excluded from unbranded shelf classification
- Recommendation coverage: 2/2 (1.0)
- Set agreement: 1.0
- Volatility: 0.0
- Fidelity: 2/2 (1.0)
- Constraint satisfaction: 2/2 (1.0)

### surface-e697282df0c7 — locked
- top first-mentioned share=1.00
- top entity recommendation rate=1.00
- set agreement=1.00
- Recommendation coverage: 4/4 (1.0)
- Set agreement: 1.0
- Volatility: 0.0
- Fidelity: 4/4 (1.0)
- Constraint satisfaction: 4/4 (1.0)

### surface-f2900f34b318 — open
- recommendation coverage=0.75
- top first-mentioned share=0.25
- set agreement=0.17
- Recommendation coverage: 3/4 (0.75)
- Set agreement: 0.1667
- Volatility: 0.8333
- Fidelity: 4/4 (1.0)
- Constraint satisfaction: 4/4 (1.0)

## Boundary

- Technical or observational readiness is not a ranking, citation, traffic, or conversion guarantee.
- Seller-controlled evidence is counted separately from independent evidence.
- Unknown values are not converted to false or zero.
