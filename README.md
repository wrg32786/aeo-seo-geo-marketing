# Organic Discovery - LLM-Operated SEO, AEO & GEO Growth Engine

[![Validate skill](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml/badge.svg)](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-open%20standard-111827)](https://agentskills.io/)
[![Version](https://img.shields.io/badge/version-0.5.0-2563eb)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

> Give an LLM a website, verified business facts, exact-surface observations, controlled editing access, and outcome data. Organic Discovery turns them into auditable SEO/AEO/GEO work instead of an opaque score.

**Organic Discovery** is an open-source Agent Skill and dependency-free Python toolchain for conventional search engine optimization (**SEO**), answer engine optimization (**AEO**), generative engine optimization (**GEO**), AI recommendation analysis, factual fidelity, and qualified organic growth.

It follows the complete chain:

```text
business truth → access → understanding → retrieval → citation
→ source use → factual fidelity → recommendation → traffic → conversion
```

[Quick start](#quick-start) · [Deterministic auditor](#deterministic-webpage-auditor) · [Business Truth](#business-truth-validator) · [AI Shelf Mapper](#ai-shelf-mapper) · [Wedge planner](#truthful-wedge-planner) · [Install the skill](#install-the-agent-skill) · [Roadmap](docs/ROADMAP.md) · [Evidence](references/source-register.md)

## Current state

Version `0.5.0` ships four executable surfaces:

1. **Webpage audit** — bounded technical and content inspection for a URL or local HTML file.
2. **Business Truth validation** — deterministic claim, provenance, existence, availability, and publication gates.
3. **AI Shelf mapping** — exact-surface observation normalization, metrics, and transparent shelf classification.
4. **Wedge planning** — hard rejection of locked, unsafe, unsupported, unavailable, or fabricated opportunities.

It also ships:

- stable JSON Schemas for normalized facts, observations, shelf maps, and wedge plans;
- two offline fixtures with committed expected outputs;
- fourteen focused regression tests;
- Python 3.11 and 3.13 CI;
- the installable Organic Discovery Agent Skill and its evidence, platform, source-earning, measurement, and execution references.

The repository does **not yet ship** a live multi-model scheduler, Search Console or analytics connector, CMS publisher, dashboard, database, hosted SaaS, or automatic Reddit/community poster. Those remain explicit later phases in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Quick start

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
cd aeo-seo-geo-marketing
python scripts/validate_skill.py
```

Audit a page:

```bash
python scripts/od.py audit https://example.com --output output/audit
```

Validate a fact registry:

```bash
python scripts/od.py facts validate examples/sample-shelf/fact-registry.csv \
  --output output/facts.json
```

Map exact AI shelves:

```bash
python scripts/od.py shelf map examples/sample-shelf/observations.jsonl \
  --facts examples/sample-shelf/fact-registry.csv \
  --output output/shelf
```

Plan defensible wedges:

```bash
python scripts/od.py wedge plan output/shelf/shelf-map.json \
  --facts examples/sample-shelf/fact-registry.csv \
  --candidates examples/sample-shelf/candidates.json \
  --output output/wedge-plan.json
```

## Deterministic webpage auditor

```bash
python scripts/od.py audit https://example.com --output output/audit
python scripts/od.py audit ./page.html --output output/audit
```

The auditor writes:

```text
output/audit/
├── audit.json
├── work-orders.json
└── report.md
```

It checks bounded HTTP behavior, crawler controls, index directives, canonicalization, initial HTML, metadata, headings, links, images, sitemaps, JSON-LD, visible/schema agreement, claim provenance, and hidden prompt-like instructions. Public URL fetching rejects private-network destinations, revalidates redirects, pins the validated public IP, and enforces timeout, byte, and redirect limits.

It does not treat technical eligibility as indexing, retrieval, citation, traffic, or conversion success. Unobservable stages remain `unknown`; `opaque_score` remains `null`.

See [`examples/sample-site/`](examples/sample-site/).

## Business Truth validator

A fact registry is the publication boundary between an LLM and public claims.

```bash
python scripts/od.py facts validate fact-registry.csv --output facts.json
```

The canonical CSV contract records:

```text
claim_id, entity_id, entity, claim_type, canonical_wording, value, unit,
source_url, source_type, verified_at, evidence_grade, offer_exists,
availability, publish_status, owner, refresh_trigger, limitations,
prompt_families, market, language, expires_at
```

The validator:

- requires stable IDs and valid dates;
- distinguishes seller-controlled, independent, community, and unknown evidence;
- blocks approved claims without provenance, verification, ownership, or refresh rules;
- blocks offer-dependent claims when existence or availability is not confirmed;
- requires independent evidence for certification, safety, medical, and customer-result claims;
- keeps `approval_required`, `research_required`, `expired`, and `prohibited` facts out of publication-ready copy;
- preserves seller-controlled facts while preventing them from being represented as independent consensus.

The normalized record contract is [`schemas/fact-record.schema.json`](schemas/fact-record.schema.json).

## AI Shelf Mapper

An AI shelf is the small recommendation set produced for one prompt family on one exact product surface. Organic Discovery never silently pools:

```text
platform + surface + mode + model + market + language + device
+ account state + session state + prompt family + target entity + branded state
```

```bash
python scripts/od.py shelf map observations.jsonl \
  --facts fact-registry.csv \
  --output output/shelf
```

The command writes:

```text
output/shelf/
├── normalized-observations.jsonl
├── shelf-map.json
└── shelf-report.md
```

For every exact-surface group it reports:

- recommendation coverage and target participation;
- first-mentioned share and recommendation order;
- incumbent concentration;
- recommendation-set agreement and volatility;
- citation-domain overlap;
- seller-controlled and independent source share;
- retrieval and citation rates when observable;
- fidelity, constraint satisfaction, and recommendation availability;
- the numerator and denominator behind every rate.

Shelf states are transparent operational classifications:

- **locked** — one entity dominates repeatedly;
- **contested** — a recurring set competes without one locked leader;
- **fragmented** — recommendations rotate with low agreement;
- **open** — recommendations are absent or unstable enough to warrant a narrow test;
- **unsafe** — fidelity, constraint satisfaction, or availability falls below the declared guardrail;
- **unknown** — evidence is insufficient or the group is branded validation.

Branded validation is grouped separately and excluded from unbranded recommendation-share denominators. Missing fields stay `null` and stay out of their metric denominator.

The contracts are [`schemas/observation.schema.json`](schemas/observation.schema.json) and [`schemas/shelf-map.schema.json`](schemas/shelf-map.schema.json).

## Truthful wedge planner

```bash
python scripts/od.py wedge plan shelf-map.json \
  --facts fact-registry.csv \
  --candidates candidates.json \
  --output wedge-plan.json
```

A wedge must pass hard gates before prioritization:

- the offer exists and is currently available;
- required facts are publishable;
- the prompt family has legitimate offer fit;
- the observations are unbranded and exact-surface;
- the shelf is not `locked`, `unsafe`, or `unknown`;
- no required fact is prohibited or unsupported.

Unsafe and unsupported opportunities are rejected, not merely scored lower. Optional business factors produce a transparent planning index; it is not an engine score and it carries no fixed time-to-shelf promise.

The contract is [`schemas/wedge-plan.schema.json`](schemas/wedge-plan.schema.json).

## Offline AI-shelf proof

[`examples/sample-shelf/`](examples/sample-shelf/) contains 22 synthetic observations across six exact-surface groups. The fixture proves:

- one narrow prompt family is open in the ChatGPT fixture but locked in the Gemini fixture;
- branded runs are excluded;
- a broad category shelf is locked;
- a travel shelf is fragmented;
- a health-related shelf is unsafe;
- a nonexistent product and a prohibited claim are rejected;
- two legitimate wedges pass the hard gates.

Every generated artifact is compared byte-for-byte in CI.

## Why it is different

| Common SEO/GEO tooling | Organic Discovery |
|---|---|
| One proprietary readiness score | Observable stages, exact metrics, facts, gates, and `null` for unknowns |
| Seller copy treated as neutral evidence | Seller-controlled and independent evidence remain distinct |
| Branded prompts inflate visibility | Branded validation is excluded from unbranded share |
| API and consumer surfaces pooled | Every material surface condition is part of the grouping key |
| Broad “best X” queries first | Narrow, legitimate wedges are tested before locked category shelves |
| Unsafe opportunities ranked lower | Unsupported, unavailable, unsafe, and prohibited opportunities are rejected |
| Advice without execution contracts | Deterministic files, schemas, examples, acceptance checks, and rollback |
| Visibility as the final KPI | Retrieval, citation, fidelity, qualified traffic, conversion, and revenue stay separate |

## Install the Agent Skill

The repository root is the skill directory.

### ChatGPT and Codex

Ask `$skill-installer` to install:

```text
https://github.com/wrg32786/aeo-seo-geo-marketing
```

Manual install:

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
cd aeo-seo-geo-marketing
python scripts/validate_skill.py
mkdir -p ~/.agents/skills
ln -s "$PWD" ~/.agents/skills/organic-discovery
```

### Claude Code

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
cd aeo-seo-geo-marketing
python scripts/validate_skill.py
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/organic-discovery
```

Repository-local installs may place the folder at `.agents/skills/organic-discovery/` or `.claude/skills/organic-discovery/`.

## Use it with an LLM

```text
Use Organic Discovery on this business and website.

Run the deterministic audit. Build and validate Business Truth. Preserve exact
AI observations, map each shelf separately, reject unsafe or unsupported wedges,
and choose the highest-value legitimate opening. Implement approved owned-site
changes on a branch, prepare reviewable earned-source drafts, validate the revision,
and define measurement, stop rules, and rollback.
```

Public third-party posting remains human-approved by default. The skill never authorizes fake identities, fake reviews, coordinated votes, undisclosed promotion, or mass link posting.

## Repository structure

```text
.
├── SKILL.md
├── README.md
├── schemas/
│   ├── fact-record.schema.json
│   ├── observation.schema.json
│   ├── shelf-map.schema.json
│   └── wedge-plan.schema.json
├── examples/
│   ├── sample-site/
│   └── sample-shelf/
├── scripts/
│   ├── od.py
│   ├── od_audit.py
│   ├── od_fetch.py
│   ├── od_truth.py
│   ├── od_shelf.py
│   └── validate_skill.py
├── tests/
│   ├── test_od.py
│   └── test_shelf.py
├── docs/
├── references/
├── agents/
└── evals/
```

## Roadmap

```text
v0.4 deterministic auditor — shipped
v0.5 Business Truth + AI Shelf Mapper — shipped
→ v0.6 GitHub-backed implementation operator
→ v0.7 content + earned-source queue
→ v0.8 measurement adapters
→ v0.9 CMS + bounded autonomy
→ v1.0 continuous loop
```

## Validate

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
```

The CI workflow additionally regenerates both offline examples and compares every expected artifact on Python 3.11 and 3.13.

## Evidence posture

- Current official platform controls outrank vendor claims and community advice.
- Benchmarks and field reports justify bounded experiments, not ranking guarantees.
- Correlations do not justify manufactured mentions, reviews, links, or dates.
- A result remains bounded to its exact surface, market, prompt family, and observation window until replicated.
- A recommendation-share increase with worse fidelity or constraint satisfaction is a regression.
- No output promises a fixed time to rank, citation, recommendation, traffic, or revenue.

## Project documents

- Product vision: [`docs/PRODUCT-VISION.md`](docs/PRODUCT-VISION.md)
- Roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)
- Definition of done: [`docs/DEFINITION-OF-DONE.md`](docs/DEFINITION-OF-DONE.md)
- Output contracts: [`references/output-contracts.md`](references/output-contracts.md)
- Evidence register: [`references/source-register.md`](references/source-register.md)
- Self-audit: [`docs/SELF-AUDIT.md`](docs/SELF-AUDIT.md)
- Contributing: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security: [`SECURITY.md`](SECURITY.md)
- Citation: [`CITATION.cff`](CITATION.cff)
- License: [`LICENSE`](LICENSE)
