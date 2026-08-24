# Output Contracts

Use this reference before emitting audits, fact validation, shelf maps, wedge plans, work orders, publication gates, experiments, acceptance reports, or learning records.

## Contract versions

```text
v0.4 audit artifact:          organic-discovery/audit/0.4
v0.5 normalized fact:         organic-discovery/facts/1.0
v0.5 normalized observation:  organic-discovery/observations/1.0
v0.5 shelf map:               organic-discovery/shelf-map/1.0
v0.5 wedge plan:              organic-discovery/wedge-plan/1.0
```

The project version and artifact schema version are separate. A project release may preserve an older artifact contract unchanged.

## General rules

- Preserve `unknown` and `null`; never coerce missing evidence to `false` or zero.
- Expose evidence and confidence.
- Expose numerator and denominator for every rate.
- Keep exact surface dimensions in every raw record and shelf group.
- Keep seller-controlled and independent evidence distinguishable.
- Keep planned, drafted, technically accepted, published, and outcome-validated states distinct.
- A technical pass does not establish ranking, citation, traffic, or conversion success.
- Every public material claim traces to the fact registry.
- Hard-gate failures remain visible and cannot be overridden by a high weighted score.

## 1. Discovery brief

```markdown
# Discovery Brief

- Controlled assets:
- Repository / CMS / listings:
- Entity / offer:
- Audience:
- Market / language:
- Page role:
- Primary user jobs and constraints:
- Conversion goal:
- Operator mode:
- Editing permissions:
- Approval policy:
- Analytics / Search Console / Bing / logs / CRM available:
- AI observation or tracker data available:
- Primary competitors:
- Regulated / YMYL / reputation constraints:
- Unknowns:
```

## 2. Fact-registry input

Canonical CSV header:

```csv
claim_id,entity_id,entity,claim_type,canonical_wording,value,unit,source_url,source_type,verified_at,evidence_grade,offer_exists,availability,publish_status,owner,refresh_trigger,limitations,prompt_families,market,language,expires_at
```

Example:

```csv
clm-001,example-crm,Example CRM,price,"Plans start at $29 per month",29,USD/month,https://example.com/pricing,first_party,2026-08-24,O,true,US,approved,finance,price_change,"Taxes may apply",small-agency-crm,US,en,2026-12-31
```

Allowed `source_type` values:

```text
first_party
seller_controlled
independent_editorial
independent_test
government
academic
customer_authorized
community
unknown
```

Allowed `publish_status` values:

```text
approved
approval_required
research_required
expired
prohibited
```

A missing source, invalid date, nonexistent offer, unavailable offer, expired fact, prohibited fact, or unsupported sensitive claim blocks publication-ready copy that depends on it.

## 3. Fact-validation output

```json
{
  "schema_version": "organic-discovery/facts/1.0",
  "tool": {"name": "Organic Discovery", "version": "0.5.0"},
  "source": "fact-registry.csv",
  "summary": {
    "record_count": 10,
    "publishable_count": 7,
    "blocked_count": 3,
    "error_count": 0
  },
  "records": [],
  "validation_errors": []
}
```

Each normalized record includes:

```json
{
  "claim_id": "clm-001",
  "entity_id": "example-crm",
  "entity": "Example CRM",
  "claim_type": "price",
  "canonical_wording": "Plans start at $29 per month",
  "value": "29",
  "unit": "USD/month",
  "source_url": "https://example.com/pricing",
  "source_type": "first_party",
  "source_ownership": "seller_controlled",
  "verified_at": "2026-08-24",
  "evidence_grade": "O",
  "offer_exists": true,
  "availability": ["US"],
  "publish_status": "approved",
  "owner": "finance",
  "refresh_trigger": "price_change",
  "limitations": ["Taxes may apply"],
  "prompt_families": ["small-agency-crm"],
  "market": "US",
  "language": "en",
  "expires_at": "2026-12-31",
  "publishable": true,
  "blocking_reasons": []
}
```

`publishable=true` means the deterministic record passed current gates. It does not replace legal, medical, safety, brand, or human review when required.

## 4. Eight-stage diagnosis

```markdown
| Stage | Status | Evidence | Confidence | Root issue / note |
|---|---|---|---|---|
| Activation | unknown | — | low | surface does not expose search invocation |
| Eligibility | blocked | [O] | high | crawler receives 403 |
| Retrieval | unknown | — | low | not observed |
| Context allocation | unknown | — | low | not exposed |
| Source selection | weak | [A] | medium | competitor cited in 7/10 comparable runs |
| Absorption | unknown | — | low | target not cited |
| Fidelity | healthy | [A] | medium | facts accurate |
| Behavior | weak | first-party | high | qualified sessions declining |
```

Statuses:

```text
blocked
weak
unknown
healthy
not_applicable
```

## 5. Prompt portfolio

```csv
prompt_id,prompt,family,intent,buying_stage,constraint,market,language,branded,parent_prompt_id,priority,notes
p001,"what is example crm",definition,learn,learn,,US,en,false,,medium,
p002,"best crm for a three person agency",small-agency-crm,recommendation,buy,"three person agency",US,en,false,,high,
p003,"is Example CRM good for agencies",small-agency-crm,evaluation,evaluate,"agency",US,en,true,,medium,
```

Prompts are measurement units. They do not automatically justify separate pages.

## 6. Raw observation input

Required exact-surface dimensions:

```text
run_id
timestamp
platform
surface
mode
model
market
language
device
account_state
session_state
prompt_id
prompt_family
prompt
branded
target_entity
```

Recommended JSONL record:

```json
{
  "run_id": "2026-08-24-chatgpt-search-p002-01",
  "timestamp": "2026-08-24T18:04:00Z",
  "platform": "openai",
  "surface": "chatgpt-search",
  "mode": "web-search",
  "model": "gpt-example",
  "market": "US",
  "language": "en",
  "device": "web-desktop",
  "account_state": "logged-out",
  "session_state": "clean",
  "prompt_id": "p002",
  "prompt_family": "small-agency-crm",
  "prompt": "best crm for a three person agency",
  "branded": false,
  "target_entity": "Example CRM",
  "search_triggered": true,
  "search_queries": [],
  "answer": "...",
  "citations": [
    {
      "url": "https://source.example/review",
      "domain": "source.example",
      "source_type": "independent_editorial",
      "position": 1
    }
  ],
  "recommendations": [
    {
      "entity": "Example CRM",
      "position": 2,
      "constraint_satisfied": true,
      "available": true
    }
  ],
  "target_url_retrieved": null,
  "target_url_cited": false,
  "target_claims_used": [],
  "fidelity_issues": [],
  "evidence_grade": "A"
}
```

Do not infer retrieval from citation absence when retrieval is not exposed.

## 7. Normalized observation

The normalized observation retains the complete grouping key and normalized recommendation/citation arrays. Invalid required dimensions are validation errors. Optional missing metrics remain `null`.

Machine contract: [`../schemas/observation.schema.json`](../schemas/observation.schema.json).

## 8. AI shelf map

```json
{
  "schema_version": "organic-discovery/shelf-map/1.0",
  "tool": {"name": "Organic Discovery", "version": "0.5.0"},
  "grouping_dimensions": [
    "platform",
    "surface",
    "mode",
    "model",
    "market",
    "language",
    "device",
    "account_state",
    "session_state",
    "prompt_family",
    "target_entity",
    "branded"
  ],
  "groups": [
    {
      "group_id": "...",
      "dimensions": {},
      "run_count": 4,
      "eligible_unbranded_runs": 4,
      "shelf_state": "fragmented",
      "classification": {
        "reason": "Recommendation sets rotate and agreement is low.",
        "thresholds": {}
      },
      "metrics": {
        "recommendation_coverage": {"numerator": 4, "denominator": 4, "rate": 1.0},
        "target_recommendation_share": {"numerator": 1, "denominator": 4, "rate": 0.25},
        "target_first_mentioned_share": {"numerator": 0, "denominator": 4, "rate": 0.0},
        "leading_entity_share": {"entity": "Rival A", "numerator": 2, "denominator": 4, "rate": 0.5},
        "set_agreement": {"numerator": 1, "denominator": 6, "rate": 0.1667},
        "set_volatility": {"numerator": 5, "denominator": 6, "rate": 0.8333},
        "citation_domain_overlap": {"numerator": 1, "denominator": 6, "rate": 0.1667},
        "constraint_satisfaction": {"numerator": 3, "denominator": 4, "rate": 0.75},
        "fidelity": {"numerator": 4, "denominator": 4, "rate": 1.0}
      },
      "entities": [],
      "source_mix": {},
      "integrity_issues": [],
      "unknowns": []
    }
  ]
}
```

Shelf states:

```text
locked
contested
fragmented
open
unsafe
unknown
```

The classification rationale and thresholds MUST be emitted. A branded group is `unknown` for unbranded opportunity planning.

Machine contract: [`../schemas/shelf-map.schema.json`](../schemas/shelf-map.schema.json).

## 9. Wedge candidate input

```json
{
  "wedge_id": "wedge-small-agency-no-admin",
  "prompt_family": "small-agency-crm",
  "target_entity": "Example CRM",
  "required_claim_ids": ["clm-001", "clm-002"],
  "legitimate_offer_fit": true,
  "user_constraint": "minimal administration",
  "controlled_asset": "https://example.com/crm-for-small-agencies",
  "priority_factors": {
    "qualified_demand": 4,
    "legitimate_fit": 5,
    "evidence_strength": 4,
    "shelf_openness": 4,
    "execution_probability": 5,
    "cost": 2,
    "risk": 2,
    "maintenance": 2
  }
}
```

## 10. Wedge-plan output

```json
{
  "schema_version": "organic-discovery/wedge-plan/1.0",
  "tool": {"name": "Organic Discovery", "version": "0.5.0"},
  "summary": {"candidate_count": 5, "accepted_count": 2, "rejected_count": 3},
  "accepted": [
    {
      "wedge_id": "wedge-small-agency-no-admin",
      "status": "accepted_for_planning",
      "hard_gates": [],
      "planning_index": 3.0,
      "planning_index_boundary": "Transparent planning aid; not an engine score or timing promise."
    }
  ],
  "rejected": [
    {
      "wedge_id": "wedge-broad-category",
      "status": "rejected",
      "hard_gates": [
        {"code": "shelf.locked", "detail": "The exact shelf is locked."}
      ]
    }
  ]
}
```

Hard gates include, as applicable:

```text
facts.missing
facts.not_publishable
offer.nonexistent
offer.unavailable
fit.false
shelf.not_found
shelf.branded_only
shelf.insufficient_observations
shelf.locked
shelf.unsafe
shelf.unknown
```

Rejected candidates cannot be restored by the planning index.

Machine contract: [`../schemas/wedge-plan.schema.json`](../schemas/wedge-plan.schema.json).

## 11. Technical blocker table

```markdown
| Priority | Layer | Asset | Finding | Evidence | Exact fix | Acceptance |
|---|---|---|---|---|---|---|
| P0 | Access | `/pricing` | crawler receives 403 | [O] + fetch | adjust verified-bot WAF rule | 200 + matching extraction |
```

Order by:

```text
access → routing → understanding → citability → corroboration → behavior
```

## 12. Truth and publication gate

```yaml
gate_id: publish-wedge-small-agency
asset: https://example.com/crm-for-small-agencies
offer_exists: pass
availability: pass
price_current: pass
specifications_current: pass
performance_claims_supported: pass
seller_vs_independent_evidence_distinguished: pass
limitations_visible: pass
copy_schema_feed_agreement: pass
named_attribution_authorized: not_applicable
regulated_review: not_applicable
human_approval: pending
blocking_claims: []
decision: blocked_pending_approval
```

Allowed decisions:

```text
pass
blocked_missing_fact
blocked_expired_fact
blocked_unavailable_offer
blocked_policy
blocked_pending_approval
rejected
```

## 13. Work order

```yaml
id: OD-001
priority: P1
stage: source_selection
root_cause: competitor comparison pages provide current sourced pricing while ours does not
recommendation_evidence: B
observation_grade: A
risk: low
assets:
  - https://example.com/compare/rival
owner: content
change:
  - add current pricing from approved facts
  - add verification date
  - disclose methodology and relationship
acceptance:
  - every price matches the fact registry
  - comparison dimensions are symmetric
  - visible page and schema agree
  - build and extraction checks pass
observation:
  prompt_family: comparison
  metrics:
    - organic_clicks
    - citation_rate
    - absorption_rate
    - qualified_conversion_rate
  window: 28d
rollback:
  - revert if facts cannot be maintained
status: planned
```

## 14. Implementation manifest

```markdown
| File / URL | Change | Why | Validation |
|---|---|---|---|
| `app/pricing/page.tsx` | render approved price facts server-side | initial HTML was empty | extraction contains pricing |
```

Include only assets actually changed.

## 15. Experiment record

```yaml
experiment_id: EXP-004
hypothesis: sourced comparison data improves retrieval and qualified discovery without harming fidelity
baseline_window: 2026-07-20/2026-08-19
treatment_started: 2026-08-24
treatment_assets:
  - https://example.com/compare/rival
primary_metric: qualified_organic_sessions
secondary_metrics:
  - citation_rate
  - absorption_rate
  - fidelity_rate
  - conversion_rate
stop_rules:
  - factual maintenance failure
  - material fidelity regression
  - sustained unexplained organic decline
result: pending
```

## 16. Final report

```markdown
# Organic Discovery Report — [entity]

## Executive diagnosis
## Business Truth
## Stage diagnosis
## Exact shelf map
## Accepted and rejected wedges
## P0/P1 blockers
## Owned-asset plan
## Earned-source queue
## Measurement and stop rules
## Unknowns and delayed outcomes
## Deliberately not done
```

## 17. Do not emit fake certainty

Avoid:

- “GEO score 87 means this page will be cited.”
- “This shelf will move in 21 days.”
- “Branded mentions prove unbranded discovery.”
- “Adding schema will raise citations by X%.”
- “Reddit links make ChatGPT rank the page.”
- “API tests prove consumer-product results.”
- “A high weighted score overrides an unavailable offer.”

Prefer:

- “The fact passes deterministic publication gates; regulated or brand approval may still be required.”
- “This is one exact-surface shelf observed under the recorded conditions.”
- “The wedge passed hard gates and is accepted for planning; no ranking or timing outcome is promised.”
- “The page is technically eligible; retrieval and citation remain pending observation.”
