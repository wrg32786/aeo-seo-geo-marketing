# Organic Discovery — SEO, AEO & GEO Agent Skill

[![Validate skill](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml/badge.svg)](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-open%20standard-111827)](https://agentskills.io/)
[![Version](https://img.shields.io/badge/version-0.3.0-2563eb)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

> Audit, improve, implement, and measure organic discovery across conventional search and AI-generated answers—without pretending a proprietary “GEO score” is platform truth.

**Organic Discovery** is an open-source Agent Skill for **search engine optimization (SEO)**, **answer engine optimization (AEO)**, **generative engine optimization (GEO)**, **AI search optimization**, and **LLM citation visibility**. It helps an AI agent diagnose and improve webpages for Google Search, Google AI Overviews and AI Mode, ChatGPT Search, Claude, Perplexity, Bing/Copilot, and other retrieval-driven systems.

It follows the full chain from **crawler access → indexing/retrieval → citation → actual source use → factual fidelity → qualified traffic and conversion**.

[Install](#install) · [Use it](#use-it) · [Outputs](#what-it-produces) · [Evidence](references/source-register.md) · [Self-audit](docs/SELF-AUDIT.md)

## About

Most SEO/AEO/GEO tools stop at a checklist or an opaque readiness score. Organic Discovery separates the problem into eight observable stages, keeps platform conditions isolated, labels the evidence behind each recommendation, and turns findings into implementation work orders with acceptance checks and rollback.

Use it when you need to:

- audit a webpage or site for classic search and AI-answer discovery;
- understand why competitors are cited or recommended instead;
- fix crawler, rendering, robots, WAF, canonical, schema, or entity problems;
- rewrite content so it is clearer, more factual, more useful, and easier to source accurately;
- map prompts, source ecosystems, comparisons, reviews, communities, and earned-authority opportunities;
- measure retrieval, citations, absorption, recommendation share, narrative accuracy, referrals, and conversions separately;
- optimize local, ecommerce, SaaS, editorial, documentation, marketplace, travel, or YMYL assets;
- decide whether experimental files such as `llms.txt` are justified for a named consumer.

## Why it is different

| Common GEO tooling | Organic Discovery |
|---|---|
| Collapses everything into one score | Diagnoses activation, eligibility, retrieval, context allocation, source selection, absorption, fidelity, and behavior separately |
| Treats crawler access as citation success | Distinguishes access, indexing, retrieval, citation, recommendation, referral, and conversion |
| Pools API and consumer-product outputs | Isolates web, app, API, Search, assistant, model, locale, account, device, and session state |
| Recommends generic “best practices” | Labels evidence as official, controlled, observational, correlational, field, or experimental |
| Produces advice only | Produces exact work orders with owner, acceptance, observation window, and rollback |
| Requires speculative AI files | Makes `llms.txt`, AI manifests, fixed chunk sizes, and similar tactics conditional experiments |
| Optimizes for visibility alone | Adds claim governance, factual fidelity, accessibility, security, and business outcomes |

## Install

The repository root is the skill directory: it contains `SKILL.md`, `references/`, `scripts/`, and host metadata.

### ChatGPT and Codex

Ask the built-in `$skill-installer` to install:

```text
https://github.com/wrg32786/aeo-seo-geo-marketing
```

For a manual personal install:

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
mkdir -p ~/.agents/skills
ln -s "$PWD/aeo-seo-geo-marketing" ~/.agents/skills/organic-discovery
```

For one repository only, place or symlink this folder at:

```text
<repo>/.agents/skills/organic-discovery/
```

### Claude Code

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
mkdir -p ~/.claude/skills
ln -s "$PWD/aeo-seo-geo-marketing" ~/.claude/skills/organic-discovery
```

For one repository only, place or symlink this folder at:

```text
<repo>/.claude/skills/organic-discovery/
```

Claude can invoke it automatically when the task matches the description, or explicitly as:

```text
/organic-discovery
```

## Use it

Start with the URL, asset, business goal, and market. The skill proceeds with partial context and marks unknowns rather than treating them as zero.

```text
Audit https://example.com/pricing for SEO, ChatGPT Search, Google AI Overviews,
Perplexity, and Copilot. Compare the sources cited for our five highest-value
buyer prompts, implement the smallest safe fixes, and give me the measurement plan.
```

```text
Why does Perplexity cite our competitor instead of our comparison page?
Trace the source chain, check factual gaps, and turn the findings into work orders.
```

```text
We have no website—only GitHub, App Store, and marketplace listings.
Build a verified fact registry and an organic discovery plan for the US and Germany.
```

```text
Should this documentation site publish llms.txt?
Identify a real consumer first; do not add it as a generic GEO checkbox.
```

## What it analyzes

1. **Activation** — whether the surface invoked retrieval.
2. **Eligibility** — crawl, rendering, indexing, and snippet eligibility.
3. **Retrieval** — whether the page entered the candidate set.
4. **Context allocation** — whether it survived reranking with useful context.
5. **Source selection** — citation, linking, attribution, and recommendation.
6. **Absorption** — whether the answer actually used the page’s claims or evidence.
7. **Fidelity** — accuracy, entity attribution, freshness, and framing.
8. **Behavior** — qualified visits, actions, leads, sales, and other outcomes.

Repairs are ordered by dependency:

```text
access → routing → understanding → citability
```

## What it produces

- Discovery brief and unknowns
- Eight-stage diagnosis with evidence and confidence
- Canonical fact/claim registry
- Dependency-ordered technical blockers
- Prompt portfolio and live source-chain map
- Competitor citation and narrative gaps
- Exact P0–P3 work orders
- Implementation manifest and deterministic acceptance checks
- Exact-surface observation records
- Retrieval, citation, absorption, fidelity, referral, and conversion measurement
- Explicit list of speculative tactics deliberately avoided

See [`references/output-contracts.md`](references/output-contracts.md) for the machine-readable and human-readable contracts.

## Knowledge modules

| Module | Responsibility |
|---|---|
| [`references/evidence-and-tactics.md`](references/evidence-and-tactics.md) | Evidence hierarchy, tactic boundaries, and rejected manipulation |
| [`references/platform-adapters.md`](references/platform-adapters.md) | Crawler roles, indexing, preview controls, feeds, profiles, and platform reporting |
| [`references/vertical-adapters.md`](references/vertical-adapters.md) | Local, ecommerce, SaaS, editorial, documentation, YMYL, travel, marketplace, and UGC adaptation |
| [`references/source-earning.md`](references/source-earning.md) | Ethical editorial, review, directory, GitHub, Reddit, forum, video, and partnership participation |
| [`references/measurement-protocol.md`](references/measurement-protocol.md) | Baselines, exact-surface observations, metrics, experiments, attribution limits, and stop rules |
| [`references/tracking-and-opportunity-recon.md`](references/tracking-and-opportunity-recon.md) | Prompt portfolios, fan-out, citations, grounding queries, competitors, and drift |
| [`references/execution-and-evidence.md`](references/execution-and-evidence.md) | Fact registries, observation grades, work orders, acceptance, and rollback |
| [`references/regional-and-surface-adapters.md`](references/regional-and-surface-adapters.md) | Web/app/API separation, localization, regional source ecosystems, and no-site mode |
| [`references/output-contracts.md`](references/output-contracts.md) | Deterministic audit, implementation, observation, experiment, and reporting formats |
| [`references/source-register.md`](references/source-register.md) | Official controls, research provenance, conflict resolution, and maintenance dates |

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
│   └── SELF-AUDIT.md
├── references/
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

`SKILL.md` is the compact runtime router. It loads only the references relevant to the task.

## Validate

No third-party Python dependencies are required:

```bash
python scripts/validate_skill.py
```

The validator checks the skill package, frontmatter, referenced paths, local links, trigger evals, host metadata, citation metadata, CI contract, and common packaging mistakes.

## Evidence posture

This project treats AEO/GEO as an evidence-management and implementation problem, not a bag of ranking hacks.

- Current official platform controls outrank vendor claims and community advice.
- Fixed-context GEO research can justify bounded content experiments, not organic-ranking guarantees.
- Correlations identify hypotheses; they do not justify manufactured links, mentions, reviews, or dates.
- A tactic observed on one engine, interface, locale, vertical, or date stays bounded to that setting until replicated.
- Uncertainty, null observations, denominators, and zero-result runs are preserved.

The reconciled evidence base and its limits are documented in [`references/source-register.md`](references/source-register.md).

## Self-audit

This repository applies its own workflow to its GitHub surface. The baseline, stage diagnosis, implemented changes, unresolved GitHub metadata controls, target queries, and measurement plan are public in [`docs/SELF-AUDIT.md`](docs/SELF-AUDIT.md).

## Contributing, security, and citation

- Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security reporting: [`SECURITY.md`](SECURITY.md)
- Citation metadata: [`CITATION.cff`](CITATION.cff)
- Release history: [`CHANGELOG.md`](CHANGELOG.md)
- License: [`LICENSE`](LICENSE)
