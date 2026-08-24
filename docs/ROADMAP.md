# Organic Discovery Roadmap

This roadmap separates **shipped capability** from **planned capability**. A phase is complete only when its commands, contracts, tests, examples, and documentation exist on the default branch and pass CI.

## Current state — v0.5.0

Organic Discovery currently ships:

- an installable Agent Skill;
- the deterministic v0.4 webpage auditor;
- the v0.5 Business Truth validator;
- exact-surface AI observation normalization and shelf mapping;
- hard-gated truthful wedge planning;
- versioned schemas;
- two reproducible offline examples;
- fourteen focused regression tests;
- Python 3.11 and 3.13 CI;
- evidence, platform, vertical, regional, source-earning, execution, and measurement references.

It does **not yet ship** a live prompt scheduler, Search Console or analytics connector, CMS connector, dashboard, database, hosted SaaS, or autonomous publisher.

## Build rule

Every phase leaves one runnable proof. README examples and release notes must never advertise planned software as implemented.

---

## v0.4 — Deterministic audit foundation

**Status: shipped**

### Interface

```bash
python scripts/od.py audit https://example.com --output output/
python scripts/od.py audit ./page.html --output output/
```

### Shipped proof

- bounded public-network-only fetching;
- crawler, index, canonical, initial-HTML, metadata, sitemap, JSON-LD, claim, accessibility, and hidden-instruction checks;
- `audit.json`, `work-orders.json`, and `report.md`;
- unknown downstream stages preserved as unknown;
- no opaque score;
- `examples/sample-site/` and six focused tests.

---

## v0.5 — Business Truth and AI Shelf Mapper

**Status: shipped**

### Goal

Turn business facts and exact-surface observations into deterministic publication gates, transparent shelf maps, and defensible wedge decisions.

### Interfaces

```bash
python scripts/od.py facts validate fact-registry.csv --output facts.json
python scripts/od.py shelf map observations.jsonl --facts fact-registry.csv --output output/
python scripts/od.py wedge plan shelf-map.json --facts fact-registry.csv --candidates candidates.json --output wedge-plan.json
```

### Business Truth

- canonical CSV input and normalized JSON output;
- stable claim and entity IDs;
- source URL and source ownership;
- verification date, evidence grade, owner, refresh trigger, limitations, market, language, prompt families, and expiry;
- product or service existence and availability;
- publication states: approved, approval required, research required, expired, and prohibited;
- hard failure for approved claims without provenance or maintenance controls;
- independent-evidence requirement for certification, safety, medical, and customer-result claims;
- seller-controlled evidence kept distinct from independent consensus.

### Exact-surface shelf mapping

Grouping preserves:

```text
platform, surface, mode, model, market, language, device,
account_state, session_state, prompt_family, target_entity_id, branded
```

Metrics preserve their numerators and denominators where applicable:

- recommendation coverage and target participation;
- first-mentioned share and recommendation order;
- incumbent concentration;
- set agreement and volatility;
- citation-domain overlap and source ownership;
- retrieval and citation when observable;
- fidelity, constraint satisfaction, and availability.

Shelf states:

```text
locked
contested
fragmented
open
unsafe
unknown
```

Branded validation is excluded from unbranded recommendation share. Null fields remain null and do not enter their metric denominator.

### Truthful wedge planning

Candidates are rejected when:

- required facts are missing, blocked, expired, prohibited, or unsupported;
- the offer does not exist or is unavailable;
- legitimate offer fit is false;
- observations are branded, insufficient, or not exact-surface;
- the shelf is locked, unsafe, or unknown.

Optional business factors produce a transparent planning index, not an engine score.

### Shipped proof

```text
examples/sample-shelf/
├── fact-registry.csv
├── observations.jsonl
├── candidates.json
├── expected/
└── README.md
```

The fixture contains open, locked, fragmented, unsafe, branded, unavailable-offer, prohibited-claim, accepted, and rejected cases. Eight focused v0.5 tests plus byte-for-byte CI prove the contracts.

### Explicitly out of scope

- live model execution or scraping;
- prompt scheduling;
- proprietary demand-volume estimates;
- Search Console, Bing, analytics, or CRM connectors;
- dashboard or database;
- CMS publication;
- autonomous community posting.

---

## v0.6 — GitHub-backed owned-site operator

### Goal

Let the LLM implement approved technical and content work through auditable branches and pull requests.

### Initial supported environment

- GitHub-backed static sites;
- Next.js and similar repository web applications;
- HTML and Markdown where the edit path is explicit.

### Deliverables

- repository intake and framework detection;
- baseline manifest;
- fact-registry enforcement before public copy;
- a small dependency-ordered work plan;
- branch creation and file edits;
- internal-link, metadata, canonical, schema, sitemap, content, and asset changes;
- deterministic acceptance checks;
- pull-request summary with evidence, risk, delayed observation, and rollback;
- before-and-after extraction and regression report.

### Default mode

`supervised execute`: create a branch and pull request; do not merge or deploy without the controlling repository’s policy.

### Release gates

- unrelated work is preserved;
- material claims have provenance;
- valuable URLs are not deleted or redirected without approval;
- every non-trivial change has one runnable check;
- delayed outcomes remain pending observation;
- one real GitHub-backed example completes the loop from audit and facts to pull request.

---

## v0.7 — Content portfolio and earned-source queue

### Goal

Create the strongest truthful owned answer and prepare legitimate corroboration where the source map proves it belongs.

### Deliverables

- intent-cluster and cannibalization planner;
- refresh, consolidation, and new-page decision rules;
- briefs for comparisons, case studies, research, tools, guides, documentation, local, and commerce assets;
- source-chain opportunity mapper;
- Reddit, forum, and community rule and relevance records;
- editorial, partner, directory, review, GitHub, video, and community draft contracts;
- affiliation and disclosure fields;
- human approval queue;
- post-publication URL and result ledger.

### Hard boundary

No fake accounts, mass posting, vote coordination, fake reviews, undisclosed endorsements, impersonation, or recycled link-drop campaigns.

---

## v0.8 — Measurement adapters and experiment ledger

### Goal

Connect implementation to actual outcomes without rebuilding every upstream data platform.

### Initial adapters

- Google Search Console exports;
- Bing Webmaster and AI Performance exports;
- GA4 or generic analytics exports;
- server-log referrals and crawler events;
- Elmo-compatible data;
- GeoLook-compatible observations;
- `geo-aeo-tracker`-style observations;
- generic JSONL raw-answer records.

### Deliverables

- import validation;
- exact-surface normalization;
- baseline and treatment comparison;
- search, retrieval, citation, absorption, fidelity, referral, conversion, and revenue reports;
- experiment ledger with confounders and stop rules;
- keep, iterate, expand, stop, or rollback recommendation;
- site-specific learning record.

---

## v0.9 — CMS adapters and bounded autonomy

### Goal

Extend controlled execution beyond GitHub while retaining drafts, approvals, tests, and rollback.

### Adapter order

1. WordPress
2. Shopify
3. Webflow or another structured CMS
4. generic CMS or API adapter

### Deliverables

- CMS drafts;
- content and metadata patch manifests;
- preview validation;
- approval state and publisher identity;
- rollback and revision support;
- allowlisted low-risk automation;
- explicit budgets and rate limits.

---

## v1.0 — Continuous Organic Growth Operator

### Goal

Complete the governed loop:

```text
truth → observe → map → diagnose → plan → execute → approve
→ publish → measure → learn → expand or roll back
```

### Required proof

A real site must demonstrate:

- verified Business Truth;
- deterministic audit;
- exact-surface shelf map;
- an accepted truthful wedge;
- GitHub or CMS implementation;
- reviewable earned-source drafts;
- technical acceptance;
- imported post-change search, AI, traffic, and conversion evidence;
- evidence-based keep, iterate, stop, or rollback decision;
- inspectable site-specific memory;
- a second run that does not corrupt the first experiment or overstate causation.

A polished report without the closed loop is not v1.0.
