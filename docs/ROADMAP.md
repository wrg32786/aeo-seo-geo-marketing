# Organic Discovery Roadmap

This roadmap separates **shipped capability** from **planned capability**. A phase is complete only when its runnable artifacts, tests, examples, and documentation exist on the default branch.

## Current state — v0.4.0

Organic Discovery currently ships:

- an installable Agent Skill;
- an evidence model and eight-stage discovery framework;
- platform, vertical, regional, source-earning, measurement, and execution references;
- Business Truth and work-order contracts;
- an AI-shelf and wedge operating method;
- `scripts/od.py`, a standard-library-first deterministic auditor for one URL or local HTML file;
- private-network-safe bounded HTTP fetching;
- deterministic `audit.json`, `work-orders.json`, and `report.md` outputs;
- an offline failure fixture, expected artifacts, tests, and Python 3.11/3.13 CI.

It does **not yet ship** search-console or analytics connectors, scheduled AI-answer tracking, CMS execution, a dashboard, a database, autonomous publishing, or community-post automation.

## Build rule

Every phase leaves one runnable proof. README commands and release notes must never advertise planned software as implemented.

---

## v0.4 — Deterministic audit foundation

**Status: shipped**

### Goal

Turn the methodology into one dependency-free, repeatable webpage audit.

### Interface

```bash
python scripts/od.py audit https://example.com --output output/
python scripts/od.py audit ./page.html --output output/
```

### Shipped checks

- HTTP status, safe redirects, timeout, response-size, and content-type bounds;
- DNS resolution and pinned public-IP connections that reject private, loopback, link-local, reserved, and non-global targets;
- redirect revalidation;
- `robots.txt` evaluation by conventional search, AI search, training, and other model-use purpose;
- meta and HTTP indexing/preview directives;
- canonical presence, conflicts, and mismatch;
- initial HTML and JavaScript-only risk;
- title, description, H1, heading hierarchy, language, viewport, links, images, and accessibility basics;
- sitemap discovery and XML parsing;
- JSON-LD extraction, `@graph` traversal, and parse errors;
- visible-content and structured-data disagreement;
- offer, author, date, and material-claim provenance gaps;
- hidden instructions, invisible content, comments, and prompt-injection patterns;
- separate eight-stage statuses with unobservable stages preserved as `unknown`.

### Outputs

```text
output/
├── audit.json
├── work-orders.json
└── report.md
```

### Proof

```text
examples/sample-site/
├── site/
├── expected/audit.json
├── expected/work-orders.json
├── expected/report.md
└── README.md
```

The sample contains intentional canonical, crawler, schema, sourcing, rendering, sitemap, accessibility, and hidden-instruction failures. `tests/test_od.py` compares generated output byte-for-byte with the committed expected artifacts.

### Release gates passed

- Standard library only for the auditor.
- URL and local-file targets.
- No opaque GEO score.
- Unknown downstream stages remain unknown.
- Remote fetches are bounded and reject private-network destinations before every hop.
- One focused unit-test module covers non-trivial parsing, output, work-order, and URL-safety logic.
- CI runs package validation, tests, and the offline example on Python 3.11 and 3.13.
- README commands are promoted only with the executable interface and CI contract present.
- Skill, README, changelog, citation metadata, evals, auditor, and expected output versions agree.

### Explicitly out of scope

- dashboard or database;
- scheduled prompt tracking;
- analytics or search-console connectors;
- CMS or repository publishing;
- social/community posting;
- browser rendering farm;
- paid data providers;
- hosted SaaS.

---

## v0.5 — Business Truth and AI Shelf Mapper

### Goal

Turn verified business facts and exact-surface observations into a defensible demand and wedge plan.

### Deliverables

- fact-registry schema and validator;
- product/service existence, availability, evidence, limitation, and publish-status gates;
- prompt-portfolio contract;
- raw observation importer;
- shelf classifications: `locked`, `contested`, `fragmented`, `open`, `unsafe`, `unknown`;
- concentration, volatility, source-overlap, order, absorption, and fidelity calculations;
- wedge records with legitimate-fit and risk rejection gates;
- one worked shelf example with raw observations;
- no fixed promise that a shelf moves within a certain number of days.

### Interface target

```bash
python scripts/od.py facts validate fact-registry.csv
python scripts/od.py shelf map observations.jsonl --output output/
python scripts/od.py wedge plan shelf-map.json --facts fact-registry.csv
```

### Release gates

- Branded validation excluded from unbranded recommendation share.
- Exact surfaces never pooled silently.
- Missing data stays null/unknown.
- Seller-controlled and independent evidence remain distinguishable.
- Unsupported or unsafe opportunities are rejected rather than merely scored lower.

---

## v0.6 — GitHub-backed owned-site operator

### Goal

Implement approved technical and content work through auditable branches and pull requests.

### Initial environments

- GitHub-backed static sites;
- Next.js and similar repository applications;
- explicit HTML and Markdown edit paths.

### Deliverables

- repository intake and framework detection;
- baseline and patch manifests;
- dependency-ordered plan;
- branch creation and small file edits;
- source-backed content updates and new owned assets when justified;
- internal-link, metadata, canonical, schema, sitemap, and accessibility changes;
- fact-registry enforcement;
- deterministic acceptance checks;
- pull-request summary with evidence, risk, delayed observation, and rollback;
- before/after extraction and regression report.

### Default mode

`supervised execute`: create a branch and pull request; do not merge or deploy without the controlling repository’s policy.

### Release gates

- Preserve unrelated work.
- No material claim without provenance.
- No deletion or redirect of traffic-bearing pages without approval.
- Every non-trivial change leaves one runnable check.
- Every pull request identifies delayed outcomes.

---

## v0.7 — Content portfolio and earned-source queue

### Goal

Create the strongest truthful owned answer and prepare legitimate corroboration where the source map proves it belongs.

### Deliverables

- intent-cluster and cannibalization planner;
- refresh, consolidation, and new-page decision rules;
- briefs for comparisons, case studies, research, tools, guides, documentation, local pages, and commerce assets;
- source-chain opportunity mapper;
- Reddit/forum/community rule and relevance records;
- editorial, partner, directory, review, GitHub, video, and community draft contracts;
- affiliation and disclosure fields;
- human approval queue;
- post-publication URL and result ledger.

### Hard boundary

No fake accounts, mass posting, vote coordination, fake reviews, undisclosed endorsements, impersonation, or recycled link campaigns.

### Release gates

- Public third-party content remains draft-and-approve.
- The contribution answers the question without requiring a link.
- Links appear only when the destination adds material evidence or utility.
- Rules and affiliation are recorded.
- Removal, referral, citation, and conversion are measured separately.

---

## v0.8 — Measurement adapters and experiment ledger

### Goal

Connect implementation to actual outcomes without rebuilding every upstream platform.

### Initial adapters

- Google Search Console exports;
- Bing Webmaster and AI Performance exports;
- GA4 or generic analytics exports;
- server-log referrals and crawler events;
- Elmo-compatible data;
- GeoLook-compatible observations;
- `geo-aeo-tracker`-style observations;
- generic JSONL answer records.

### Deliverables

- import contracts and validation;
- exact-surface normalization without destructive pooling;
- baseline/treatment comparison;
- search, retrieval, citation, absorption, fidelity, referral, conversion, and revenue reports;
- experiment ledger with confounders and stop rules;
- keep, iterate, expand, stop, or rollback recommendation;
- site-specific learning record.

### Release gates

- Every rate exposes numerator and denominator.
- Referral traffic remains a lower bound.
- API observations are not presented as consumer-surface results.
- Vendor scores remain labeled vendor scores.
- No credit without a preserved baseline and observation window.

---

## v0.9 — CMS adapters and bounded autonomy

### Goal

Extend controlled execution beyond GitHub while retaining drafts, approvals, checks, and rollback.

### Adapter order

1. WordPress
2. Shopify
3. Webflow or another structured CMS
4. generic CMS/API adapter

### Deliverables

- CMS draft creation;
- content and metadata patch manifests;
- preview validation;
- approval state and publisher identity;
- rollback/revision support;
- allowlisted low-risk owned-site automation;
- rate limits, budgets, stop rules, and audit logs.

### Release gates

- Default remains draft or supervised execution.
- The adapter cannot grant itself broader permissions.
- Material claims and third-party actions remain approval-gated.
- Rollback is tested per adapter.

---

## v1.0 — Continuous Organic Growth Operator

### Goal

Complete the bounded closed loop:

```text
observe → diagnose → select → implement → validate → measure → learn → repeat
```

### Required proof

A real site must demonstrate:

- verified Business Truth;
- preserved technical and outcome baseline;
- traditional demand and exact-surface AI shelf mapping;
- one legitimate wedge;
- approved owned-site implementation;
- reviewable earned-source drafts;
- technical acceptance;
- post-change search, AI, traffic, and conversion data;
- keep/iterate/stop/rollback decision;
- reusable site memory;
- a second run that preserves the first experiment and does not overstate causation.

A polished report without that loop is not v1.0.

## Non-goals across every phase

- guaranteed rankings, citations, traffic, or timelines;
- proprietary ranking-oracle scores;
- fake consensus or authority laundering;
- automatic public community posting;
- one page per prompt variation;
- rebuilding every tracker, crawler farm, analytics warehouse, or CMS.
