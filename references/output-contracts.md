# Output Contracts

Use this reference before emitting audits, shelf maps, implementation plans, work orders, publication gates, experiment records, acceptance reports, or learning records. The purpose is deterministic handoff: another operator should be able to execute or verify the work without reconstructing intent.

## General rules

- Preserve `unknown`/`null`; do not coerce missing observations to `false` or zero.
- Expose evidence class and confidence.
- Expose numerators and denominators for every rate.
- Keep exact platform/surface conditions in raw records.
- Keep planned, drafted, technically accepted, published, and outcome-validated states distinct.
- A technical acceptance pass does not establish ranking, citation, traffic, or conversion success.
- Every public material claim must trace to the fact registry.

## 1. Discovery brief

```markdown
# Discovery Brief

- Controlled asset(s):
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

## 2. Canonical fact registry

Recommended CSV:

```csv
claim_id,entity,claim_type,canonical_wording,value,unit,source_url,source_type,verified_at,evidence_grade,offer_exists,availability,publish_status,owner,refresh_trigger,limitations
clm-001,Example,price,"Plans start at $29 per month",29,USD/month,https://example.com/pricing,first_party,2026-08-24,O,true,US,approved,finance,price_change,"Taxes may apply"
```

Allowed `publish_status` values:

```text
approved
approval_required
research_required
expired
prohibited
```

A missing source, expired fact, unavailable offer, or prohibited status MUST block publication-ready copy that depends on it.

## 3. Eight-stage diagnosis

```markdown
## Stage Diagnosis

| Stage | Status | Evidence | Confidence | Root issue / note |
|---|---|---|---|---|
| Activation | unknown | — | low | surface does not expose search invocation |
| Eligibility | blocked | [O] | high | WAF challenge to search crawler |
| Retrieval | unknown | — | low | cannot evaluate until access is fixed |
| Context allocation | unknown | — | low | not observable |
| Source selection | weak | [A] | medium | competitor cited in 7/10 comparable runs |
| Absorption | unknown | — | low | target not cited |
| Fidelity | healthy | [A] | medium | branded validation facts accurate |
| Behavior | weak | first-party | high | qualified organic sessions declining |
```

Statuses:

```text
blocked
weak
unknown
healthy
not_applicable
```

## 4. Prompt portfolio

```csv
prompt_id,prompt,family,intent,buying_stage,constraint,market,language,branded,parent_prompt_id,priority,notes
p001,"what is example crm",definition,learn,learn,,US,en,false,,medium,
p002,"best crm for a three person agency",small-agency-crm,recommendation,buy,"three person agency",US,en,false,,high,
p003,"is Example CRM good for agencies",small-agency-crm,evaluation,evaluate,"agency",US,en,true,,medium,
```

Branded validation rows MUST be excluded from unbranded recommendation-share denominators.

Prompts are measurement units. They do not automatically justify separate pages.

## 5. Raw observation record

```json
{
  "run_id": "2026-08-24-chatgpt-search-p002-01",
  "timestamp": "2026-08-24T18:04:00Z",
  "platform": "openai",
  "surface": "chatgpt-search",
  "mode": "web-search",
  "model": null,
  "market": "US",
  "language": "en",
  "device": "web-desktop",
  "account_state": "logged-out",
  "session_state": "clean",
  "prompt_id": "p002",
  "prompt": "best crm for a three person agency",
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
      "constraint_satisfied": true
    }
  ],
  "target_url_retrieved": null,
  "target_url_cited": false,
  "target_claims_used": [],
  "fidelity_issues": [],
  "evidence_grade": "A"
}
```

Do not infer retrieval from citation absence when the surface does not expose retrieval.

## 6. AI shelf map

```json
{
  "shelf_map_id": "shelf-small-agency-crm-us-en-2026-08-24",
  "prompt_family": "small-agency-crm",
  "market": "US",
  "language": "en",
  "surfaces": ["chatgpt-search", "perplexity-web", "google-ai-mode"],
  "eligible_runs": 60,
  "shelf_state": "fragmented",
  "confidence": "medium",
  "leading_entities": [
    {
      "entity": "Rival A",
      "mention_rate": 0.55,
      "first_mentioned_share": 0.32,
      "recommendation_share": 0.28
    }
  ],
  "incumbent_concentration": {
    "metric": "leading_entity_share",
    "value": 0.28
  },
  "volatility": {
    "metric": "set_change_rate",
    "value": 0.47
  },
  "cross_surface_agreement": 0.38,
  "constraint_satisfaction_rate": 0.72,
  "source_mix": {
    "seller_controlled": 19,
    "independent_editorial": 31,
    "community": 12,
    "other": 8
  },
  "integrity_issues": [],
  "unknowns": []
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

The classification rationale MUST be emitted alongside the class.

## 7. Wedge opportunity record

```yaml
wedge_id: wedge-small-agency-no-admin
prompt_family: small-agency-crm
user_constraint: minimal administration for a three-person agency
business_value: high
legitimate_offer_fit: strong
fact_support: approved
shelf_state: open
shelf_evidence: A
current_answer_gap: existing answers recommend enterprise tools without addressing setup burden
controlled_asset: https://example.com/crm-for-small-agencies
priority_factors:
  qualified_demand: 4
  legitimate_fit: 5
  evidence_strength: 4
  shelf_openness: 4
  execution_probability: 5
  cost: 2
  risk: 2
  maintenance: 2
priority_rationale: "High-fit constraint with weak current answers; all claims are supportable."
rejection_conditions:
  - offer availability changes
  - setup-time claim cannot be substantiated
status: approved_for_planning
```

The factors are inspectable planning inputs—not an engine score.

## 8. Technical blocker table

```markdown
## Technical Blockers

| Priority | Layer | Asset | Finding | Evidence | Exact fix | Acceptance |
|---|---|---|---|---|---|---|
| P0 | Access | `/pricing` | crawler receives 403 | [O] + fetch | adjust verified-bot WAF rule | 200 + matching extraction |
```

Order by dependency:

```text
access → routing → understanding → citability → corroboration → behavior
```

## 9. Source-chain map

```markdown
## Source Chain

| Prompt family | Surface | Recurring source | Source type | Competitor present | Target present | Legitimate inclusion path | Confidence |
|---|---|---|---|---|---|---|---|
```

Do not add an inclusion path when the only route would be spam, deception, undisclosed promotion, identity manipulation, or policy circumvention.

## 10. Truth and publication gate

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

## 11. Work order

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
  - add current pricing table from canonical sources
  - add verification date
  - disclose methodology and relationship
acceptance:
  - every price matches the fact registry
  - comparison dimensions are symmetric
  - visible page and schema agree
  - page build and extraction checks pass
observation:
  prompt_family: comparison
  metrics:
    - organic_clicks
    - citation_rate
    - absorption_rate
    - qualified_conversion_rate
  window: 28d
rollback:
  - revert the comparison section if facts cannot be maintained
status: planned
```

Required work-order states:

```text
planned
drafted
approval_required
approved
implemented
technical_acceptance_passed
published
observing
validated
failed
rolled_back
```

## 12. Owned-asset brief

```markdown
# Owned Asset Brief

- Wedge:
- User job:
- Material constraint:
- Search intent:
- AI shelf state:
- Why the offer legitimately fits:
- Claims allowed:
- Claims requiring approval:
- Required limitations:
- Independent evidence:
- Original evidence / demonstration:
- Existing asset to update or new asset justification:
- Canonical destination:
- Internal-link plan:
- Conversion path:
- Acceptance checks:
- Observation plan:
```

## 13. Implementation manifest

```markdown
## Implementation Manifest

| File / URL | Change | Why | Validation |
|---|---|---|---|
| `app/pricing/page.tsx` | render canonical price facts server-side | initial HTML was empty | extraction contains approved pricing |
| `public/robots.txt` | remove accidental wildcard block | search crawler denied | parser + live request allow path |
```

Include only assets actually changed. Preserve the source revision and rollback revision.

## 14. Earned-source contribution record

```yaml
contribution_id: src-reddit-example-001
source: reddit
community: r/example
thread_url: https://www.reddit.com/r/example/comments/...
prompt_family: small-agency-crm
observed_source_role: community_language_and_referral
rules_checked_at: 2026-08-24
audience_need: user asked for low-admin tools for a three-person agency
affiliation: employee of Example CRM
draft: |
  Full useful answer goes here.
link:
  included: true
  url: https://example.com/crm-for-small-agencies
  why_needed: contains the setup-time methodology and comparison table
approval: pending
published_url: null
outcomes:
  survived_moderation: null
  engagement: null
  referral_sessions: null
  later_citations: null
```

Public third-party publication remains approval-gated by default.

## 15. Acceptance report

```markdown
## Acceptance

| Work order | Technical acceptance | Evidence | Delayed outcome | Next check |
|---|---|---|---|---|
| OD-001 | PASS | fetched page + tests | pending_observation | 2026-09-21 |
```

A work order may pass technical acceptance while retrieval, citation, traffic, and conversion remain pending.

## 16. Experiment record

```yaml
experiment_id: EXP-004
hypothesis: sourced symmetric comparison data improves qualified discovery for comparison prompts without harming search traffic
baseline_window: 2026-07-20/2026-08-19
treatment_started: 2026-08-24
treatment_assets:
  - https://example.com/compare/rival
control:
  - unchanged comparison prompt family for rival-2
primary_metric: qualified_organic_sessions
secondary_metrics:
  - citation_rate
  - absorption_rate
  - fidelity_rate
  - organic_impressions
  - conversion_rate
stop_rules:
  - factual maintenance failure
  - material constraint-satisfaction regression
  - sustained organic decline unexplained by broader site trend
confounders:
  - none_known
result: pending
```

## 17. Measurement report

```markdown
## Measurement

| Metric | Numerator | Denominator | Rate | Surface / source | Window | Notes |
|---|---:|---:|---:|---|---|---|
| Citation | 8 | 40 | 20.0% | ChatGPT Search | 28d | 10 prompts × 4 runs |
| Absorption | 5 | 8 cited | 62.5% | ChatGPT Search | 28d | substantive + partial |
| Recommendation share | 6 | 20 | 30.0% | unbranded buy prompts | 28d | branded prompts excluded |
| Fidelity | 7 | 8 appearances | 87.5% | ChatGPT Search | 28d | one limitation omitted |
| Qualified organic sessions | 143 | — | — | analytics | 28d | target landing cluster |
| Attributable AI sessions | 23 | — | — | analytics + logs | 28d | lower bound |
| Conversions | 9 | 166 qualified sessions | 5.4% | analytics + CRM | 28d | deduplicated |
```

## 18. Learning record

```yaml
learning_id: learn-exp-004
experiment_id: EXP-004
site: example.com
prompt_family: comparison
surfaces:
  - chatgpt-search
  - google-ai-mode
market: US
result_summary: "Search clicks increased; citations improved only on ChatGPT Search; one answer omitted a limitation."
technical_acceptance: pass
business_outcome: positive
fidelity_outcome: mixed
decision: iterate
do_again:
  - sourced symmetric comparison table
avoid:
  - unsupported setup-time wording
next_action:
  - tighten limitation block before expanding to adjacent prompts
bounded_to:
  - this site
  - US English
  - comparison prompt family
  - observed window
```

Allowed decisions:

```text
keep
iterate
expand
stop
rollback
inconclusive
```

## 19. Operator run manifest

```yaml
run_id: od-run-2026-08-24-001
mode: supervised_execute
controlled_assets:
  - https://example.com
repository_revision_before: abc123
repository_revision_after: def456
facts_version: facts-2026-08-24
baseline_artifacts:
  - baseline/page.json
  - baseline/observations.jsonl
selected_wedge: wedge-small-agency-no-admin
work_orders:
  - OD-001
  - OD-002
publication_gates:
  - publish-wedge-small-agency
approvals:
  owned_site_merge: pending
  third_party_posts: pending
technical_acceptance: pass
outcome_status: pending_observation
rollback_revision: abc123
```

## 20. Final report contract

Unless the user requests another format:

```markdown
# Organic Discovery Operator Report — [entity / asset]

## Executive diagnosis
[earliest blocker, strongest wedge, confidence, business consequence]

## Discovery brief and permissions
[assets, mode, approvals, goals, unknowns]

## Business Truth
[fact gaps, stale or prohibited claims]

## Stage diagnosis
[eight-stage table]

## Demand and AI shelf
[prompt families, shelf state, concentration, sources, integrity]

## Selected wedge
[value, legitimate fit, evidence, rejection conditions]

## P0/P1 work orders
[dependency-ordered exact changes]

## Implementation and acceptance
[actual files/URLs changed, checks, approval state]

## Earned-source queue
[justified sources, drafts, disclosure, approval]

## Experiment and measurement
[baseline, denominators, cadence, stop rules, business outcomes]

## Learning decision
[keep, iterate, expand, stop, rollback, or inconclusive]

## Deliberately not done
[unsupported, deceptive, premature, or unnecessary tactics]
```

## 21. Do not emit fake certainty

Avoid:

- “GEO score 87 means this page will be cited.”
- “Adding schema will raise citations by X%.”
- “Reddit links make ChatGPT rank the page.”
- “This page is optimized for every AI engine.”
- “Crawler allowed means indexed or cited.”
- “Our API test proves the consumer app result.”
- “This open shelf will move in 21 days.”
- “The model’s recommendation independently validates the seller claim.”

Prefer:

- “The page is technically eligible; retrieval and citation remain pending observation.”
- “This tactic is [C] fixed-context evidence, so it is a bounded experiment.”
- “Reddit recurs in this source chain; an authentic, disclosed contribution is an earned tactic for this prompt family.”
- “The shelf appears fragmented across 60 comparable observations; confidence is medium.”
- “The recommendation share increased, but fidelity declined, so the result is a regression pending correction.”