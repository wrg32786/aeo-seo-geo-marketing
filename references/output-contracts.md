# Output Contracts

Use this reference before emitting audits, implementation plans, work orders, experiment records, or acceptance reports. The purpose is deterministic handoff: another operator should be able to execute or verify the work without reconstructing intent.

## 1. Discovery brief

```markdown
# Discovery Brief

- Controlled asset(s):
- Entity / offer:
- Audience:
- Market / language:
- Page role:
- Primary user jobs:
- Conversion goal:
- Editing permissions:
- Analytics / Search Console / logs available:
- Primary competitors:
- Regulated / YMYL / reputation constraints:
- Unknowns:
```

## 2. Eight-stage diagnosis

```markdown
## Stage Diagnosis

| Stage | Status | Evidence | Confidence | Root issue / note |
|---|---|---|---|---|
| Activation | unknown | — | low | surface does not expose search invocation |
| Eligibility | blocked | [O] | high | WAF challenge to citation crawler |
| Retrieval | unknown | — | low | cannot evaluate until access fixed |
| Context allocation | unknown | — | low | not observable |
| Source selection | weak | [A] | medium | competitor cited in 7/10 clean runs |
| Absorption | unknown | — | low | target not cited |
| Fidelity | healthy | [A] | medium | branded validation facts accurate |
| Behavior | weak | first-party | high | AI-attributable referrals below 1% |
```

Statuses: `blocked`, `weak`, `unknown`, `healthy`, `not_applicable`.

## 3. Claim/fact ledger

```markdown
## Fact Registry

| Entity | Claim | Canonical value | Source | Verified | Grade | Publish status | Refresh trigger |
|---|---|---|---|---|---|---|---|
```

Never leave a material numeric or comparative claim without a source/status.

## 4. Prompt portfolio

Recommended machine-readable shape:

```csv
prompt_id,prompt,intent,buying_stage,market,language,branded,parent_prompt_id,priority,notes
p001,what is example crm,definition,learn,US,en,false,,medium,
p002,best crm for a three person agency,recommendation,buy,US,en,false,,high,
p003,is example crm good for agencies,evaluation,evaluate,US,en,true,,medium,
```

Branded validation rows MUST be excluded from unbranded recommendation-share denominators.

## 5. Raw observation record

```json
{
  "run_id": "2026-08-22-chatgpt-search-p002-01",
  "timestamp": "2026-08-22T18:04:00Z",
  "platform": "openai",
  "surface": "chatgpt-search",
  "mode": "web-search",
  "market": "US",
  "language": "en",
  "device": "web-desktop",
  "session_state": "clean",
  "prompt_id": "p002",
  "prompt": "best crm for a three person agency",
  "search_triggered": true,
  "search_queries": [],
  "answer": "...",
  "citations": [],
  "recommendations": [],
  "target_url_retrieved": null,
  "target_url_cited": false,
  "target_claims_used": [],
  "fidelity_issues": [],
  "evidence_grade": "A"
}
```

Use `null`/`unknown` rather than false when a platform does not expose a field.

## 6. Technical blocker table

```markdown
## Technical Blockers

| Priority | Layer | Asset | Finding | Evidence | Exact fix | Acceptance |
|---|---|---|---|---|---|---|
| P0 | Access | /pricing | crawler receives 403 | [O] + fetch | adjust WAF verified-bot rule | 200 + matching extraction |
```

Order by dependency, not by visual importance.

## 7. Source-chain map

```markdown
## Source Chain

| Prompt family | Surface | Recurring source | Type | Competitor present | Target present | Legitimate inclusion path | Confidence |
|---|---|---|---|---|---|---|---|
```

Do not add an inclusion path when the only route would be spam, deception, undisclosed promotion, or policy circumvention.

## 8. Work order

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
  - add current pricing table from canonical pricing sources
  - add verification date
  - disclose methodology and relationship
acceptance:
  - every price matches source of truth
  - comparison dimensions are symmetric
  - visible page and schema agree
  - page build/test passes
observation:
  prompt_family: comparison
  metric: citation_rate_and_absorption
  window: 28d
rollback:
  - revert comparison section if facts cannot be maintained
status: planned
```

## 9. Implementation manifest

After direct edits:

```markdown
## Implementation Manifest

| File / URL | Change | Why | Validation |
|---|---|---|---|
| `app/pricing/page.tsx` | rendered canonical price facts server-side | initial HTML was empty | curl extraction contains pricing |
| `public/robots.txt` | removed accidental wildcard block | citation crawler denied | parser + live request allow target path |
```

Include only files actually changed.

## 10. Acceptance report

```markdown
## Acceptance

| Work order | Technical acceptance | Evidence | Delayed outcome | Next check |
|---|---|---|---|---|
| OD-001 | PASS | fetched page + tests | pending_observation | 2026-09-19 |
```

A work order can pass technical acceptance while retrieval/citation outcome remains pending.

## 11. Experiment record

```yaml
experiment_id: EXP-004
hypothesis: sourced symmetric comparison data improves citation/absorption for comparison prompts without harming search impressions
baseline_window: 2026-07-20/2026-08-19
treatment_started: 2026-08-22
treatment_assets:
  - https://example.com/compare/rival
control:
  - unchanged comparison prompt family for rival-2
primary_metric: citation_rate
secondary_metrics:
  - absorption_rate
  - organic_impressions
  - referral_sessions
stop_rules:
  - factual maintenance failure
  - >15% sustained decline in organic impressions unexplained by broader site trend
confounders:
  - none_known
result: pending
```

## 12. Measurement report

```markdown
## Measurement

| Metric | Numerator | Denominator | Rate | Surface / source | Window | Notes |
|---|---:|---:|---:|---|---|---|
| Citation | 8 | 40 | 20.0% | ChatGPT Search | 28d | 10 prompts × 4 runs |
| Absorption | 5 | 8 cited | 62.5% | ChatGPT Search | 28d | substantive + partial |
| Recommendation share | 6 | 20 | 30.0% | unbranded buy prompts | 28d | branded prompts excluded |
| Attributable AI sessions | 23 | — | — | analytics + logs | 28d | lower bound |
```

Always expose denominators.

## 13. Final audit/report contract

Unless user requests another format:

```markdown
# Organic Discovery Audit — [entity / URL]

## Executive diagnosis
[3–6 sentences: earliest blocker, biggest opportunity, confidence, business consequence.]

## Discovery brief
[inputs and unknowns]

## Stage diagnosis
[eight-stage table]

## P0/P1 blockers
[dependency-ordered]

## Prompt and source map
[high-value demand + recurring sources]

## Claim / entity gaps
[unsupported, inconsistent, stale, missing]

## Work orders
[exact changes]

## Measurement plan
[raw events, denominators, cadence]

## Deliberately not done
[unsupported/experimental tactics avoided]
```

## 14. Do not emit fake certainty

Avoid:

- “GEO score 87 means this page will be cited.”
- “Adding schema will raise citations by X%.”
- “Reddit links make ChatGPT rank the page.”
- “This page is optimized for every AI engine.”
- “Crawler allowed = indexed/cited.”
- “Our API test proves the consumer app result.”

Prefer:

- “The page is technically eligible; citation outcome is pending observation.”
- “This tactic is [C] evidence from a fixed-context experiment, so we are treating it as a bounded test.”
- “Reddit recurs in this exact source chain, so authentic participation is an earned tactic for this prompt family.”
