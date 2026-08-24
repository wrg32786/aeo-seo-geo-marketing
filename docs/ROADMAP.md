# Organic Discovery Roadmap

This roadmap separates **shipped capability** from **planned capability**. A phase is complete only when its runnable artifacts, tests, examples, and documentation exist in the repository.

## Current state — v0.3.1

Organic Discovery currently ships as:

- an installable Agent Skill;
- an evidence model and eight-stage discovery framework;
- platform, vertical, regional, source-earning, measurement, and execution references;
- fact/claim governance and work-order contracts;
- an AI-shelf and wedge operating method;
- a public repository self-audit;
- trigger evals and package validation.

It does **not yet ship** a bundled site crawler, `od.py` audit CLI, search-console connector, AI-answer scheduler, CMS connector, dashboard, or autonomous publisher.

## Build rule

Each phase must leave one runnable proof behind. Documentation may describe the North Star, but README examples and release notes must not advertise a planned command as implemented.

---

## v0.4 — Deterministic audit foundation

### Goal

Turn the methodology into one dependency-light, repeatable webpage audit.

### Required interface

```bash
python scripts/od.py audit https://example.com --output output/
python scripts/od.py audit ./page.html --output output/
```

### Required checks

- HTTP status, safe redirects, timeouts, and response limits;
- `robots.txt` evaluation by crawler purpose;
- meta and header indexing/preview controls;
- canonical URL and routing conflicts;
- initial HTML availability and JavaScript-only risk;
- title, description, H1, headings, language, links, images, and accessibility basics;
- sitemap discovery;
- JSON-LD extraction and parse errors;
- visible-content and structured-data disagreement;
- entity, offer, author, date, and claim gaps;
- hidden instructions, invisible text, and prompt-injection patterns;
- known versus inferred versus unknown stage status.

### Required outputs

```text
output/
├── audit.json
├── work-orders.json
└── report.md
```

### Required proof

```text
examples/sample-site/
├── site/
├── expected/audit.json
├── expected/work-orders.json
├── expected/report.md
└── README.md
```

The sample must contain intentional canonical, crawler, schema, sourcing, rendering, and hidden-instruction failures.

### Release gates

- Standard library first; no dependency for a check the standard library can correctly perform.
- One small test module covering non-trivial logic.
- CI runs package validation, unit tests, and the offline example.
- Safe URL handling prevents private-network and redirect abuse.
- Unknown stages remain unknown.
- No opaque readiness score.
- Review-first install instructions exist.

### Explicitly out of scope

- dashboard;
- database;
- scheduled prompt tracking;
- autonomous publishing;
- social/community posting;
- full-site rendering browser;
- paid data-provider integrations.

---

## v0.5 — Business Truth and AI Shelf Mapper

### Goal

Let an LLM turn business facts plus exact-surface observations into a defensible demand and wedge plan.

### Deliverables

- canonical fact-registry schema and validator;
- product/service existence, availability, evidence, and publish-status gates;
- prompt-portfolio generator contract;
- raw observation importer;
- AI-shelf classifications: `locked`, `contested`, `fragmented`, `open`, `unsafe`;
- brand concentration, volatility, source-overlap, recommendation-order, and fidelity calculations;
- wedge opportunity records with legitimate-fit and risk gates;
- one worked shelf-mapping example with preserved raw observations;
- no hard-coded promise that a shelf moves in a fixed number of days.

### Interface target

```bash
python scripts/od.py facts validate fact-registry.csv
python scripts/od.py shelf map observations.jsonl --output output/
python scripts/od.py wedge plan shelf-map.json --facts fact-registry.csv
```

### Release gates

- Branded validation is excluded from unbranded recommendation share.
- Exact surfaces are never pooled silently.
- Missing data remains null/unknown.
- Seller-controlled and independent sources are distinguishable.
- Unsafe or unsupported opportunities are rejected, not merely scored lower.

---

## v0.6 — GitHub-backed owned-site operator

### Goal

Let the LLM implement approved technical and content work through auditable branches and pull requests.

### Initial supported environment

- GitHub-backed static sites;
- Next.js and similar repository-based web applications;
- generic HTML/Markdown content where the edit path is explicit.

### Deliverables

- repository intake and framework detection;
- baseline manifest;
- small, dependency-ordered work plan;
- branch creation and file edits;
- content updates and new owned assets when justified;
- internal-link, metadata, canonical, schema, and sitemap changes;
- fact-registry enforcement before publication-ready copy;
- deterministic acceptance checks;
- pull-request summary containing evidence, risk, observation, and rollback;
- before/after extraction and regression report.

### Default operating mode

`supervised execute`: create the branch and PR; do not merge or deploy without the controlling repository’s approval policy.

### Release gates

- Never overwrite unrelated work.
- Never publish a material claim without provenance.
- Never delete or redirect traffic-bearing pages without explicit approval.
- Every non-trivial change has a runnable check.
- Every PR identifies delayed outcomes still pending observation.

---

## v0.7 — Content portfolio and earned-source queue

### Goal

Create the strongest truthful owned answer and prepare legitimate corroboration where the source map proves it belongs.

### Deliverables

- intent-cluster and cannibalization planner;
- existing-page refresh, consolidation, and new-page decision rules;
- briefs for comparison pages, case studies, original research, tools, guides, documentation, local pages, and commerce assets;
- source-chain opportunity mapper;
- Reddit/forum/community rule and relevance record;
- editorial, partner, directory, review, GitHub, video, and community draft contracts;
- affiliation/disclosure field;
- human approval queue;
- post-publication URL and result ledger.

### Hard boundary

The repository will not ship fake accounts, automated mass posting, vote coordination, fake reviews, undisclosed endorsements, identity impersonation, or repeated link-drop automation.

### Release gates

- Public third-party content remains draft-and-approve.
- The contribution answers the community’s question without requiring the link.
- A link is included only when the destination adds material evidence or utility.
- Community rules and affiliation are recorded.
- Removal, referral, citation, and conversion outcomes are measured separately.

---

## v0.8 — Measurement adapters and experiment ledger

### Goal

Connect implementation to actual outcomes without rebuilding every upstream data platform.

### Initial adapters

- Google Search Console exports;
- Bing Webmaster and AI Performance exports;
- GA4 or generic analytics exports;
- server-log referrals and crawler events;
- Elmo-compatible exports/API data;
- GeoLook-compatible observations;
- `geo-aeo-tracker`-style observations;
- generic JSONL raw answer records.

### Deliverables

- import contracts and validation;
- exact-surface normalization without destructive pooling;
- baseline/treatment comparison;
- search, retrieval, citation, absorption, fidelity, referral, and conversion reports;
- experiment ledger with confounders and stop rules;
- keep, iterate, stop, or rollback recommendation;
- site-specific learning record.

### Release gates

- Every rate exposes numerator and denominator.
- Referral traffic is a lower bound, not complete attribution.
- API observations are not reported as consumer-surface observations.
- Vendor scores remain labeled vendor scores.
- Changes cannot be credited without a preserved baseline and observation window.

---

## v0.9 — CMS adapters and bounded autonomy

### Goal

Extend controlled execution beyond GitHub while retaining drafts, approvals, tests, and rollback.

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
- policy-defined low-risk autonomous classes;
- budget, rate, and change-volume limits.

### Release gates

- Draft is the default.
- Credentials never enter repository artifacts.
- Every adapter has a non-destructive dry run.
- Autonomy is granted per change class, not globally.
- Public third-party posting remains outside autonomous scope.

---

## v1.0 — Continuous Organic Growth Operator

### Goal

Run the complete loop safely and repeatedly for a real website.

### Definition

A v1.0 operator can:

1. ingest the business and controlled surfaces;
2. maintain the fact registry;
3. audit the live site and source ecosystem;
4. map traditional demand and the AI shelf;
5. identify a legitimate high-value wedge;
6. create a prioritized experiment plan;
7. implement approved owned-site changes;
8. prepare approved earned-source contributions;
9. validate and publish through policy gates;
10. ingest outcome data;
11. keep, iterate, or roll back;
12. retain site-specific learning for the next run.

The full gates are in [`DEFINITION-OF-DONE.md`](DEFINITION-OF-DONE.md).

---

## Workstreams that should remain integrations

Do not rebuild mature upstream infrastructure unless an integration proves impossible:

- full multi-engine scraping farms;
- long-term prompt scheduling dashboards;
- general-purpose analytics warehouses;
- backlink indexes;
- broad keyword databases;
- headless browser farms;
- account and billing systems.

Organic Discovery should be the **truth, diagnosis, planning, implementation, and learning layer** between those data sources and the website.

## Priority order

```text
v0.4 deterministic auditor
→ v0.5 truth + shelf mapper
→ v0.6 GitHub implementation
→ v0.7 content + earned-source queue
→ v0.8 measurement imports
→ v0.9 CMS + bounded autonomy
→ v1.0 continuous loop
```

Do not skip the runnable proof at the end of each phase.