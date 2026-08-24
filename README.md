# Organic Discovery - LLM-Operated SEO, AEO & GEO Growth Engine

[![Validate skill](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml/badge.svg)](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-open%20standard-111827)](https://agentskills.io/)
[![Version](https://img.shields.io/badge/version-0.4.0-2563eb)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

> Give an LLM a website, verified business facts, controlled editing access, and outcome data. Organic Discovery helps it find under-defended demand, improve owned assets, prepare legitimate supporting content, measure the result, and learn what works.

**Organic Discovery** is an open-source Agent Skill plus a dependency-free deterministic auditor for conventional search engine optimization (**SEO**), answer engine optimization (**AEO**), generative engine optimization (**GEO**), AI search visibility, factual fidelity, and qualified organic growth.

It follows the full chain from **business truth → crawler access → retrieval → citation → actual source use → factual fidelity → recommendation → qualified traffic and conversion** across Google Search, Google AI Overviews and AI Mode, ChatGPT Search, Claude, Perplexity, Bing/Copilot, and other retrieval-driven systems.

[Audit a page](#deterministic-auditor) · [Install the skill](#install-the-agent-skill) · [Use it with an LLM](#use-it-with-an-llm) · [Product vision](docs/PRODUCT-VISION.md) · [Roadmap](docs/ROADMAP.md) · [Definition of done](docs/DEFINITION-OF-DONE.md) · [Evidence](references/source-register.md) · [Self-audit](docs/SELF-AUDIT.md)

## Current state

Version `0.4.0` ships:

- the installable Organic Discovery Agent Skill;
- `scripts/od.py`, a standard-library-first auditor for one remote URL or local HTML file;
- bounded HTTP fetching with private-network rejection, pinned public IP connections, timeout, response-size, and redirect limits;
- deterministic analysis of crawler controls, index directives, canonicalization, initial HTML, metadata, headings, links, images, sitemaps, JSON-LD, visible/schema agreement, claim provenance, and hidden prompt-like instructions;
- eight-stage output that preserves unobservable downstream stages as `unknown`;
- exact work orders with owner, change, acceptance, observation, and rollback;
- an intentionally broken offline fixture with committed expected outputs;
- one focused unit-test module and Python 3.11/3.13 CI;
- Business Truth, AI-shelf, source-earning, measurement, publication-gate, and learning doctrine for LLM-led operation.

The repository does **not yet ship** an analytics connector, AI-answer scheduler, CMS connector, dashboard, database, autonomous publisher, or automatic Reddit/community poster. Those remain staged release milestones in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Deterministic auditor

Audit a public page:

```bash
python scripts/od.py audit https://example.com --output output/
```

Audit a local HTML file and its sibling `robots.txt` and `sitemap.xml`:

```bash
python scripts/od.py audit ./page.html --output output/
```

Optionally preserve the target questions that motivated the audit:

```bash
python scripts/od.py audit https://example.com/product \
  --query "best product for a narrow use case" \
  --query "product without ingredient x" \
  --output output/
```

The command writes:

```text
output/
├── audit.json
├── work-orders.json
└── report.md
```

### What it checks

- HTTP status, content type, bounded redirects, timeouts, and response limits;
- public-IP-only remote fetching with every redirect revalidated;
- `robots.txt` by crawler purpose: conventional search, AI search, training, and other model use;
- meta and HTTP index/preview controls;
- canonical presence, conflicts, and target mismatch;
- initial HTML and likely client-side-only core content;
- title, description, language, viewport, H1s, heading hierarchy, links, images, and accessibility basics;
- sibling or standard-location sitemap discovery and XML parsing;
- JSON-LD parsing, `@graph` traversal, and important visible/schema disagreement;
- material claim provenance gaps;
- offer and editorial provenance gaps;
- hidden text, comments, and inline prompt-injection patterns;
- activation, eligibility, retrieval, context allocation, source selection, absorption, fidelity, and behavior without collapsing them into one score.

### What it does not claim

The auditor never treats technical eligibility as proof of indexing, retrieval, citation, recommendation, traffic, or conversion. It has no opaque GEO score. Retrieval, context allocation, source selection, absorption, and behavior remain `unknown` until exact-surface or first-party evidence exists.

### Offline proof

```bash
python scripts/od.py audit examples/sample-site/site/index.html \
  --output /tmp/organic-discovery-example
python -m unittest discover -s tests -v
python scripts/validate_skill.py
```

The sample intentionally contains canonical, crawler, rendering, schema, sourcing, sitemap, accessibility, and hidden-instruction failures. The generated artifacts are compared byte-for-byte with [`examples/sample-site/expected/`](examples/sample-site/expected/).

## North Star

Organic Discovery is becoming a closed-loop **Organic Growth Operator**:

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

AI answer systems compress categories into small recommendation sets. Organic Discovery maps those shelves as:

- **Locked** — one incumbent dominates consistently.
- **Contested** — a recurring small set rotates.
- **Fragmented** — engines and runs disagree.
- **Open** — no stable recommendation exists for the specific constraint.
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
| Starts by generating content | Builds Business Truth and fixes the earliest dependency first |
| Chases broad “best X” prompts first | Maps incumbent concentration and finds truthful open-shelf wedges |
| Produces generic recommendations | Produces exact work orders with acceptance, observation, and rollback |
| Pools APIs and consumer products | Isolates web, app, API, Search, assistant, model, locale, account, device, and session state |
| Automates public posting | Drafts third-party contributions for human approval by default |
| Measures mentions alone | Measures search, retrieval, citation, absorption, fidelity, qualified traffic, conversion, and revenue separately |
| Requires speculative AI files | Makes `llms.txt`, AI manifests, and fixed formatting conditional experiments |

## Install the Agent Skill

The repository root is the skill directory.

### ChatGPT and Codex

Ask the built-in `$skill-installer` to install:

```text
https://github.com/wrg32786/aeo-seo-geo-marketing
```

Review-first manual install:

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

Repository-local installations can place this folder at `.agents/skills/organic-discovery/` or `.claude/skills/organic-discovery/`.

## Use it with an LLM

### Closed-loop site operation

```text
Use Organic Discovery on this website.

Goal: increase qualified organic traffic and leads.

Run the deterministic auditor first. Build the verified fact registry. Research
conventional search demand, AI-answer demand, competitors, recurring sources, and
the AI shelf. Select the best legitimate wedge. Implement approved owned-site
changes on a branch, prepare reviewable supporting content and earned-source drafts,
validate the revision, and report baseline, evidence, risks, measurement, and rollback.
```

### AI-shelf mapping

```text
Map the recommendation shelf for our product category across ChatGPT Search,
Google AI Mode, Gemini, Claude web search, Perplexity, and Copilot. Keep every
surface separate, identify locked and open prompt families, reject any wedge we
cannot support truthfully, and create the owned-asset and corroboration plan.
```

### Ethical community support

```text
Find Reddit and industry forum discussions that genuinely match this guide. Check
the rules, draft complete helpful responses with affiliation disclosure, include a
link only when it adds necessary evidence, and leave every public post pending human
approval.
```

## What the skill produces

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
├── docs/
├── references/
├── agents/
├── evals/
├── examples/sample-site/
│   ├── site/
│   └── expected/
├── scripts/
│   ├── od.py
│   ├── od_audit.py
│   ├── od_fetch.py
│   └── validate_skill.py
└── tests/
    └── test_od.py
```

## Roadmap

```text
v0.4 deterministic auditor — shipped
→ v0.5 Business Truth + AI shelf mapper
→ v0.6 GitHub implementation operator
→ v0.7 content + earned-source queue
→ v0.8 measurement adapters
→ v0.9 CMS + bounded autonomy
→ v1.0 continuous loop
```

Organic Discovery integrates with trackers, analytics systems, and data providers rather than rebuilding every dashboard, scheduler, crawler farm, and keyword index.

## Validate

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/od.py audit examples/sample-site/site/index.html --output /tmp/od-example
```

The validation workflow runs all three checks on Python 3.11 and 3.13.

## Evidence posture

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
