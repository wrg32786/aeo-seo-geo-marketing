# Organic Discovery — LLM-Operated SEO, AEO & GEO Growth Engine

[![Validate skill](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml/badge.svg)](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-open%20standard-111827)](https://agentskills.io/)
[![Version](https://img.shields.io/badge/version-0.3.1-2563eb)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

> Give an LLM a website, verified business facts, controlled editing access, and outcome data. Organic Discovery helps it find under-defended demand, improve owned assets, prepare legitimate supporting content, measure the result, and learn what works.

**Organic Discovery** is an open-source Agent Skill and product blueprint for operating qualified organic growth across:

- conventional search engine optimization (**SEO**);
- answer engine optimization (**AEO**);
- generative engine optimization (**GEO**);
- Google Search, Google AI Overviews and AI Mode;
- ChatGPT Search, Claude, Perplexity, Bing/Copilot, and other retrieval-driven systems;
- local, product, marketplace, documentation, editorial, review, community, and other source ecosystems.

It follows the full chain from **business truth → crawler access → retrieval → citation → actual source use → factual fidelity → recommendation → qualified traffic and conversion**.

[Install](#install) · [Use it](#use-it) · [Product vision](docs/PRODUCT-VISION.md) · [Roadmap](docs/ROADMAP.md) · [Definition of done](docs/DEFINITION-OF-DONE.md) · [Evidence](references/source-register.md)

## Current state

Version `0.3.1` ships:

- an installable Agent Skill for LLM-led research, audits, planning, owned-site implementation, source-earning drafts, validation, and measurement;
- an eight-stage discovery model;
- fact and claim governance;
- exact-surface AI observation rules;
- an AI-shelf and long-tail wedge method;
- work-order, experiment, publication-gate, and learning contracts;
- platform, vertical, regional, source-earning, and measurement modules;
- trigger evals, package validation, and a public self-audit.

It does **not yet ship** a bundled site crawler, `scripts/od.py` audit CLI, analytics connector, AI-answer scheduler, CMS connector, dashboard, or autonomous publisher. Those are staged, testable milestones in the [roadmap](docs/ROADMAP.md), beginning with a deterministic auditor in `v0.4`.

This distinction is deliberate: planned software is never advertised as shipped software.

## North Star

Organic Discovery is becoming a **closed-loop Organic Growth Operator**:

```text
UNDERSTAND THE BUSINESS
        ↓
MAP SEARCH DEMAND + THE AI SHELF
        ↓
OBSERVE THE SITE, COMPETITORS, AND SOURCE ECOSYSTEM
        ↓
DIAGNOSE THE EARLIEST FAILING STAGE
        ↓
SELECT THE HIGHEST-VALUE DEFENSIBLE WEDGE
        ↓
EDIT OWNED ASSETS + PREPARE EARNED-SOURCE CONTRIBUTIONS
        ↓
VALIDATE, APPROVE, AND PUBLISH
        ↓
MEASURE SEARCH, AI VISIBILITY, TRAFFIC, AND CONVERSION
        ↓
KEEP, IMPROVE, EXPAND, OR ROLL BACK
        ↓
STORE SITE-SPECIFIC LEARNING
```

The detailed product contract is in [`docs/PRODUCT-VISION.md`](docs/PRODUCT-VISION.md).

## The AI shelf

AI answer systems compress a category into a small recommendation set. Incumbents can dominate that **AI shelf**, while new entrants struggle to appear for broad prompts.

Organic Discovery looks for a better entry point: a commercially useful, under-defended question where the business has a genuine fit and can publish the clearest, best-supported answer.

Shelf states:

- **Locked** — one incumbent dominates consistently.
- **Contested** — a recurring small set rotates.
- **Fragmented** — engines and runs disagree.
- **Open** — no stable answer exists for the specific constraint.
- **Unsafe** — recommendations repeatedly violate constraints or launder unsupported claims.

The operating strategy is:

```text
MAP THE SHELF
      ↓
FIND A LEGITIMATE OPEN WEDGE
      ↓
PUBLISH THE MOST DEFENSIBLE TRUE ANSWER
      ↓
EARN RELEVANT CORROBORATION
      ↓
MEASURE EACH SURFACE
      ↓
EXPAND INTO ADJACENT SHELF SPACE
```

The method and evidence boundaries—including the Morrowen field observation—are documented in [`references/ai-shelf-and-growth-loop.md`](references/ai-shelf-and-growth-loop.md).

## Why it is different

| Common SEO/GEO tooling | Organic Discovery |
|---|---|
| Collapses the problem into one score | Separates activation, eligibility, retrieval, context allocation, source selection, absorption, fidelity, and behavior |
| Treats crawler access as citation success | Distinguishes access, indexing, retrieval, citation, recommendation, referral, and conversion |
| Pools APIs and consumer products | Isolates web, app, API, Search, assistant, model, locale, account, device, and session state |
| Starts by generating content | Builds Business Truth and fixes the earliest dependency first |
| Produces generic recommendations | Produces exact work orders with owner, risk, acceptance, observation, and rollback |
| Chases broad “best X” prompts first | Maps incumbent concentration and finds truthful open-shelf wedges |
| Treats every authority site as link inventory | Pursues only sources that serve the exact audience and source chain |
| Automates public posting | Drafts third-party contributions for human approval by default |
| Measures mentions alone | Measures search, retrieval, citation, absorption, fidelity, qualified traffic, conversion, and revenue separately |
| Requires speculative AI files | Makes `llms.txt`, AI manifests, and fixed formatting conditional experiments |

## What the skill can do today

When the host LLM has the necessary tools and permissions, the skill can guide it to:

- understand the business, offer, audience, market, and conversion goal;
- create a canonical fact and claim registry;
- audit a live page, site, repository, or listing ecosystem;
- verify current crawler and platform controls;
- diagnose technical SEO, content, entity, evidence, and conversion problems;
- map traditional queries, conversational prompts, competitors, citations, and recurring sources;
- classify an AI shelf and select a defensible wedge;
- create or improve pages, code, internal links, metadata, schema, feeds, and supporting content;
- work on a GitHub branch or CMS draft when connected;
- prepare ethical Reddit, forum, directory, review, editorial, partner, GitHub, and video contributions;
- enforce publication and approval gates;
- validate owned-site changes;
- design and interpret exact-surface experiments;
- recommend keep, iterate, expand, stop, or rollback.

The repository itself currently supplies the operating intelligence and contracts. The deterministic tooling that makes more of this repeatable without relying on host behavior is the next build phase.

## Operator modes

| Mode | Behavior |
|---|---|
| Audit | Read-only research and diagnosis |
| Plan | Prioritized work orders and experiment design |
| Draft | Code, content, and community drafts without publication |
| Supervised execute | Owned-site branch/PR or CMS draft with approval |
| Approved owned-site autonomy | Only pre-approved low-risk change classes with checks and rollback |
| Continuous operator | Scheduled loops under explicit budgets, gates, and stop rules |

The default is **supervised execute**.

Public third-party posting is human-approved by default. The project will not create fake people, fake customers, fake reviews, coordinated votes, undisclosed endorsements, or mass link campaigns.

## Install

The repository root is the skill directory: it contains `SKILL.md`, `references/`, `docs/`, `scripts/`, and host metadata.

### ChatGPT and Codex

Ask the built-in `$skill-installer` to install:

```text
https://github.com/wrg32786/aeo-seo-geo-marketing
```

Manual personal install:

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
mkdir -p ~/.agents/skills
ln -s "$PWD/aeo-seo-geo-marketing" ~/.agents/skills/organic-discovery
```

Repository-local install:

```text
<repo>/.agents/skills/organic-discovery/
```

### Claude Code

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
mkdir -p ~/.claude/skills
ln -s "$PWD/aeo-seo-geo-marketing" ~/.claude/skills/organic-discovery
```

Repository-local install:

```text
<repo>/.claude/skills/organic-discovery/
```

Claude can invoke it automatically from the description or explicitly as:

```text
/organic-discovery
```

## Use it

### Closed-loop site operation

```text
Use Organic Discovery on this website.

Goal: increase qualified organic traffic and leads.

Understand the business and create the verified fact registry. Audit the codebase,
live site, conventional search demand, AI-answer demand, competitors, and recurring
sources. Map the AI shelf, identify the best legitimate wedge, and produce a small
P0/P1 plan. Implement approved owned-site changes on a branch, create reviewable
supporting content and earned-source drafts, run validation, and open a pull request
with baseline, evidence, risks, acceptance checks, measurement, and rollback.
```

### AI-shelf mapping

```text
Map the recommendation shelf for our product category across ChatGPT Search,
Google AI Mode, Gemini, Claude web search, Perplexity, and Copilot. Keep every
surface separate, identify locked and open prompt families, reject any wedge we
cannot support truthfully, and create the owned-asset and corroboration plan.
```

### Existing-page improvement

```text
Why does Perplexity cite our competitor instead of our comparison page? Trace the
source chain, verify our claims, fix the earliest blocker, implement the smallest
safe change, and define the 28-day experiment.
```

### Ethical community support

```text
Find Reddit and industry forum discussions that genuinely match this guide. Check
the rules, draft complete helpful responses with affiliation disclosure, include a
link only when it adds necessary evidence, and leave every public post pending human
approval.
```

## What it produces

- discovery brief and permission model;
- canonical fact/claim registry;
- eight-stage diagnosis with evidence and confidence;
- dependency-ordered technical blockers;
- keyword, prompt, competitor, and source map;
- AI-shelf classification and recommendation-integrity review;
- selected wedge and owned-asset brief;
- exact P0–P3 work orders;
- implementation manifest and deterministic acceptance checks;
- earned-source queue with rules, disclosure, and approval state;
- exact-surface observation records;
- experiment and measurement plan;
- learning record and keep/iterate/expand/stop/rollback decision;
- explicit list of speculative or deceptive tactics deliberately avoided.

See [`references/output-contracts.md`](references/output-contracts.md).

## Knowledge modules

| Module | Responsibility |
|---|---|
| [`references/evidence-and-tactics.md`](references/evidence-and-tactics.md) | Evidence hierarchy, tactic boundaries, and rejected manipulation |
| [`references/platform-adapters.md`](references/platform-adapters.md) | Crawler roles, indexing, preview controls, feeds, profiles, and platform reporting |
| [`references/vertical-adapters.md`](references/vertical-adapters.md) | Local, ecommerce, SaaS, editorial, documentation, YMYL, travel, marketplace, and UGC adaptation |
| [`references/ai-shelf-and-growth-loop.md`](references/ai-shelf-and-growth-loop.md) | Shelf mapping, wedge selection, recommendation integrity, corroboration, and expansion |
| [`references/source-earning.md`](references/source-earning.md) | Ethical editorial, review, directory, GitHub, Reddit, forum, video, and partnership participation |
| [`references/measurement-protocol.md`](references/measurement-protocol.md) | Baselines, exact-surface observations, experiments, attribution limits, and stop rules |
| [`references/tracking-and-opportunity-recon.md`](references/tracking-and-opportunity-recon.md) | Prompt portfolios, fan-out, citations, grounding queries, competitors, and drift |
| [`references/execution-and-evidence.md`](references/execution-and-evidence.md) | Fact registries, observation grades, work orders, acceptance, and rollback |
| [`references/regional-and-surface-adapters.md`](references/regional-and-surface-adapters.md) | Web/app/API separation, localization, regional source ecosystems, and no-site mode |
| [`references/output-contracts.md`](references/output-contracts.md) | Audit, shelf, wedge, publication, implementation, experiment, and learning formats |
| [`references/source-register.md`](references/source-register.md) | Official controls, research provenance, conflict resolution, and maintenance dates |

## Product documents

- North Star: [`docs/PRODUCT-VISION.md`](docs/PRODUCT-VISION.md)
- Phased implementation: [`docs/ROADMAP.md`](docs/ROADMAP.md)
- Full release gates: [`docs/DEFINITION-OF-DONE.md`](docs/DEFINITION-OF-DONE.md)
- Repository self-audit: [`docs/SELF-AUDIT.md`](docs/SELF-AUDIT.md)

## Repository structure

```text
.
├── SKILL.md
├── README.md
├── AGENTS.md
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── agents/
│   └── openai.yaml
├── docs/
│   ├── PRODUCT-VISION.md
│   ├── ROADMAP.md
│   ├── DEFINITION-OF-DONE.md
│   └── SELF-AUDIT.md
├── references/
│   ├── ai-shelf-and-growth-loop.md
│   ├── evidence-and-tactics.md
│   ├── execution-and-evidence.md
│   ├── measurement-protocol.md
│   ├── output-contracts.md
│   ├── platform-adapters.md
│   ├── regional-and-surface-adapters.md
│   ├── source-earning.md
│   ├── source-register.md
│   ├── tracking-and-opportunity-recon.md
│   └── vertical-adapters.md
├── evals/
│   └── trigger-evals.json
└── scripts/
    └── validate_skill.py
```

## Roadmap

The shortest path from intelligence to product is:

```text
v0.4 deterministic auditor
→ v0.5 Business Truth + AI shelf mapper
→ v0.6 GitHub implementation operator
→ v0.7 content + earned-source queue
→ v0.8 measurement adapters
→ v0.9 CMS + bounded autonomy
→ v1.0 continuous loop
```

The project intentionally integrates with trackers, analytics systems, and data providers rather than rebuilding every dashboard, scheduler, crawler farm, and keyword index.

## Validate

No third-party Python dependencies are required for the current package validator:

```bash
python scripts/validate_skill.py
```

The validator checks frontmatter, versions, required modules, current-versus-planned capability language, local links, trigger evals, host metadata, citation metadata, CI, and common packaging errors.

## Evidence posture

This project treats SEO/AEO/GEO as an evidence, execution, and learning problem—not a bag of ranking hacks.

- Current official platform controls outrank vendor claims and community advice.
- Fixed-context GEO research can justify bounded experiments, not organic-ranking guarantees.
- Correlations identify hypotheses; they do not justify manufactured links, mentions, reviews, or dates.
- A tactic observed on one engine, interface, locale, vertical, or date remains bounded until replicated.
- Uncertainty, denominators, null observations, and zero-result runs are preserved.
- A higher recommendation share with worse factual fidelity or constraint satisfaction is a regression.

## Contributing, security, and citation

- Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Agent rules: [`AGENTS.md`](AGENTS.md)
- Security reporting: [`SECURITY.md`](SECURITY.md)
- Citation metadata: [`CITATION.cff`](CITATION.cff)
- Release history: [`CHANGELOG.md`](CHANGELOG.md)
- License: [`LICENSE`](LICENSE)