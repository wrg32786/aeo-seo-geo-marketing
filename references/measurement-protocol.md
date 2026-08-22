# Measurement Protocol

Use this reference whenever the task involves baselines, experiments, monitoring, or attribution. The goal is to measure the actual discovery pipeline without collapsing unlike signals into one score.

## 1. Measurement principles

1. Preserve raw observations before computing scores.
2. Separate eligibility, retrieval, citation, absorption, fidelity, referrals, and conversions.
3. Keep platform, product surface, model/mode, country, language, device, account state, and personalization explicit.
4. Never merge API and consumer-product results unless the platform documents them as equivalent.
5. Keep branded validation prompts separate from unbranded discovery prompts.
6. Preserve zero-result runs and denominators.
7. Treat referral attribution as a lower bound when referrers can be stripped.
8. Prefer first-party reports and logs for actual exposure; use synthetic probes diagnostically.
9. Do not claim causality from before/after movement without controlling obvious confounders.
10. Never hide variance behind a single composite score.

## 2. Baseline record

For each monitored asset or prompt family, capture:

```yaml
asset: https://example.com/page
captured_at: 2026-08-22T10:00:00-07:00
market: US
language: en
surface: chatgpt-search
query: best crm for small agencies
session_state: clean/new
account_state: logged_out_or_documented
personalization: none_known
result:
  search_triggered: true
  target_retrieved: true
  target_cited: false
  brand_mentioned: false
  recommendation_position: null
  source_urls:
    - https://competitor.example/guide
raw_artifact: ./runs/2026-08-22/chatgpt-search-001.json
```

If a field cannot be observed, use `unknown`, not `false`.

## 3. Prompt portfolio design

Build prompts from user jobs, not only keywords.

Recommended buckets:

- definition;
- how-to/problem solving;
- recommendation;
- comparison;
- alternatives;
- evaluation/trust;
- price/cost;
- use case/scenario;
- local/availability;
- brand verification;
- action/agent intent.

Tag each prompt with:

- intent;
- buying stage;
- business value;
- target market/language;
- expected source type;
- branded or unbranded;
- target engine/surface.

Do not let branded prompts inflate unbranded recommendation share.

## 4. Prompt variants and persona fan-out

Use variants to estimate robustness, not to manufacture a favorable answer.

Good variants change:

- persona: founder, buyer, practitioner, developer, local resident;
- constraints: price, location, team size, regulation, compatibility;
- phrasing: natural paraphrase;
- stage: learn, evaluate, buy;
- language/locale.

Preserve the parent prompt ID so variants can be grouped.

Do not average variants without retaining the distribution.

## 5. Core event record

Normalize each observed run into a stable schema:

```json
{
  "run_id": "2026-08-22-chatgpt-search-p014-v2",
  "timestamp": "2026-08-22T18:04:00Z",
  "platform": "openai",
  "surface": "chatgpt-search",
  "mode": "web-search",
  "country": "US",
  "language": "en",
  "device": "web-desktop",
  "account_state": "clean-session",
  "prompt_id": "p014",
  "variant_id": "v2",
  "prompt": "What is the best CRM for a three-person marketing agency?",
  "search_triggered": true,
  "search_queries": [],
  "answer": "...",
  "citations": [],
  "brand_mentions": [],
  "recommendations": [],
  "target_url_retrieved": false,
  "target_url_cited": false,
  "target_claims_used": [],
  "fidelity_issues": [],
  "evidence_grade": "A"
}
```

Keep raw platform payloads/screenshots separately when available.

## 6. Metrics by stage

### Activation

`search_activation_rate = search_triggered_runs / eligible_runs`

Use only where search invocation can actually be observed.

### Retrieval

`retrieval_rate = runs_where_target_entered_candidate_or_grounding_set / observable_retrieval_runs`

If a surface exposes citations but not candidate retrieval, do not infer retrieval failures from absent citations.

### Citation/source selection

`citation_rate = runs_with_target_cited / runs`

Also report:

- unique target URLs cited;
- citation position where observable;
- citation share among all cited domains;
- query coverage;
- per-surface distribution.

### Absorption/source use

Measure whether answer claims are actually supported by or derived from the target source.

Possible labels:

- `substantive` — answer clearly uses important facts/logic from the page;
- `partial` — one or more factual elements used;
- `decorative` — cited but little/no detectable support;
- `unknown` — cannot determine.

Do not equate citation with absorption.

### Fidelity

For each material brand/entity claim in an answer:

- correct;
- incomplete;
- outdated;
- unsupported;
- misattributed;
- fabricated.

Useful metric:

`material_fact_accuracy = correct_material_facts / evaluated_material_facts`

Keep severity notes; a wrong price can matter more than three correct trivial facts.

### Recommendation share

For unbranded commercial prompts:

`recommendation_share = prompts_where_brand_is_recommended / eligible_unbranded_recommendation_prompts`

Optionally distinguish:

- top recommendation;
- included recommendation;
- mentioned but not recommended.

Do not include branded validation prompts.

### Search outcomes

Use first-party or trustworthy ranking/search data:

- impressions;
- clicks;
- CTR;
- average position or rank distribution;
- indexed pages;
- rich-result appearance;
- AI-feature impressions/citations where a first-party report exposes them.

Do not assume an AI-feature impression means a click.

### Referral traffic

Track AI/search referrers separately from crawler activity.

Common fields:

- source/referrer;
- landing page;
- session count;
- engaged session rate;
- conversion rate;
- revenue/lead quality;
- first-touch and last-touch source snapshots when possible.

Because apps and privacy layers can remove referrers, report attributable AI referral sessions as a measured lower bound.

### Business outcomes

Tie to the actual goal:

- signups;
- purchases;
- qualified leads;
- appointments;
- downloads;
- repository clones/stars only if those are meaningful;
- assisted conversions;
- revenue;
- retention.

Visibility without business value is not the final KPI.

## 7. Competitor and source-gap analysis

For each prompt/surface:

1. list cited/recommended competitors;
2. list cited URLs/domains;
3. classify source type;
4. record whether the source is independent, competitor-owned, community, documentation, marketplace, publisher, government, etc.;
5. identify legitimate ways the target could become relevant to that source ecosystem.

Useful opportunity records:

```yaml
prompt_id: p014
surface: perplexity
competitor: RivalCRM
source: https://review.example/crm-comparison
source_type: independent-review
our_brand_present: false
competitor_present: true
natural_inclusion_path: submit verified product listing and provide current pricing/docs
risk: low
```

Never turn a competitor citation gap directly into spam outreach.

## 8. First-party reconciliation

When platforms expose first-party data, compare it to synthetic/live probes.

Examples:

- Google Search Console Search performance;
- generative-search reports if available to the property;
- Bing Webmaster Tools;
- Merchant Center/Product feeds;
- Business Profile insights;
- server access logs;
- analytics referral/channel data.

Reconciliation questions:

- Are probes over- or under-sampling real demand?
- Are synthetic tests seeing citations that generate no real impressions?
- Are first-party impressions high on topics missing from the prompt portfolio?
- Is crawler activity rising before citation behavior changes?
- Are traffic changes explained by classic search rather than AI surfaces?

Do not blend actual and synthetic counts into one denominator.

## 9. Experiment design

### Hypothesis

Write one specific causal hypothesis:

> Replacing three vague feature paragraphs with a sourced comparison table and updated canonical pricing will increase citation/absorption for the comparison prompt family without reducing organic impressions.

### Treatment

Document exact changes and URLs.

### Controls

Use whichever are feasible:

- unchanged sibling pages;
- untouched prompt clusters;
- competitor control;
- geographic control;
- phased rollout;
- twin pages only when duplicate/canonical risk is controlled.

### Windows

Separate:

- pre-change baseline;
- technical acceptance window;
- crawl/index observation window;
- retrieval/citation window;
- business outcome window.

Do not pick the endpoint after seeing the result.

### Confounders

Record:

- model/platform updates;
- algorithm updates;
- major competitor launches;
- PR/news events;
- seasonality;
- site migration/release;
- paid campaigns;
- outages;
- source-page changes outside your control.

## 10. Statistical caution

Most site-level GEO programs have small samples and unstable engines. Prefer transparent descriptive statistics over fake precision.

Report:

- numerator and denominator;
- confidence interval when sample size supports it;
- distribution across runs;
- variance by platform and prompt family;
- number of zero-result runs;
- exact dates.

Do not claim “+37% GEO visibility” from one prompt moving from one citation to two.

## 11. Drift monitoring

Track changes over time at several layers:

### Technical drift

- robots/header changes;
- WAF/CDN behavior;
- canonical/indexability;
- schema/feed/profile consistency;
- content rendering.

### Content/fact drift

- prices;
- versions;
- availability;
- leadership;
- locations;
- legal/regulatory claims;
- benchmark data;
- source URLs.

### AI narrative drift

- description accuracy;
- recommendation position;
- competitors associated;
- stale facts;
- negative/misleading framing.

### Source-chain drift

- new recurring cited domains;
- disappearing communities/publishers;
- changes in platform-specific source ecosystems;
- competitor source gains.

Flag drift; do not auto-rewrite everything.

## 12. Monitoring cadence

Choose cadence by volatility and value.

- **Daily/weekly**: breaking news, availability, price-sensitive commerce, active reputation incidents.
- **Weekly/biweekly**: high-value active GEO experiments.
- **Monthly**: stable B2B/product visibility.
- **Quarterly**: broad source ecosystem and entity consistency review.

Avoid excessive probing that adds cost without decision value.

## 13. Stop rules

Stop or revert a tactic when:

- deterministic quality worsens;
- organic search declines materially with no compensating outcome;
- factual fidelity degrades;
- community/source rules prohibit the tactic;
- maintenance burden exceeds measured benefit;
- repeated controlled observations show no movement at the intended stage;
- the platform officially deprecates/rejects the mechanism.

Document the result so the same failed experiment is not endlessly repeated.
