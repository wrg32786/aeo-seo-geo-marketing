# Organic Discovery

A modular Agent Skill for conventional SEO plus evidence-grounded AEO/GEO: technical eligibility, retrieval, citation, actual source use, factual fidelity, recommendation, agent-readable interaction, and qualified business outcomes.

**Current release:** `0.3.0`  
**Research reconciled:** `2026-08-22`

## Why this exists

Most GEO checklists collapse a changing, stochastic pipeline into one score. They often confuse crawler access with indexing, citation with recommendation, API output with consumer-product behavior, and correlation with causation.

Organic Discovery instead:

- separates eight stages from search activation through business behavior;
- prioritizes repairs through access → routing → understanding → citability;
- builds a canonical fact registry before generating copy, schema, feeds, profiles, comparisons, or off-site assets;
- separates recommendation evidence from the provenance grade of each observation;
- keeps API, web, app, Search, assistant, country, language, account, personalization, and branded/unbranded samples distinct;
- reconciles first-party reports and verified logs with live samples and synthetic trackers;
- converts findings into owner-assigned work orders with baselines, acceptance checks, observation windows, and rollback.

The skill rejects ranking guarantees, opaque vendor scores as platform truth, prompt injection, hidden text, fake mentions, undisclosed community promotion, fixed universal word counts, and mandatory speculative AI files.

## Repository structure

```text
organic-discovery/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── references/
│   ├── evidence-and-tactics.md
│   ├── platform-adapters.md
│   ├── vertical-adapters.md
│   ├── source-earning.md
│   ├── measurement-protocol.md
│   ├── tracking-and-opportunity-recon.md
│   ├── execution-and-evidence.md
│   ├── regional-and-surface-adapters.md
│   ├── output-contracts.md
│   └── source-register.md
├── scripts/
│   └── validate_skill.py
└── evals/
    └── trigger-evals.json
```

`SKILL.md` is the compact runtime router. Reference files load only when their subject is relevant.

## Module map

| Module | Responsibility |
|---|---|
| [`references/evidence-and-tactics.md`](references/evidence-and-tactics.md) | Evidence boundaries for content, schema, freshness, links, `llms.txt`, and common GEO claims |
| [`references/platform-adapters.md`](references/platform-adapters.md) | Current crawler, indexing, preview, feed, product-control, and reporting distinctions |
| [`references/vertical-adapters.md`](references/vertical-adapters.md) | Local, commerce, SaaS, editorial, documentation, YMYL, travel, marketplace, and UGC adaptations |
| [`references/source-earning.md`](references/source-earning.md) | Ethical editorial, review, directory, GitHub, Reddit, forum, video, and partnership participation |
| [`references/measurement-protocol.md`](references/measurement-protocol.md) | Baselines, event records, metrics, experiments, first-party reconciliation, attribution limits, and stop rules |
| [`references/tracking-and-opportunity-recon.md`](references/tracking-and-opportunity-recon.md) | Prompt portfolios, persona fan-out, normalized raw runs, grounding-query capture, citation gaps, and drift |
| [`references/execution-and-evidence.md`](references/execution-and-evidence.md) | Facts, observation grades, deterministic observability, narrative states, no-site mode, work orders, acceptance, and rollback |
| [`references/regional-and-surface-adapters.md`](references/regional-and-surface-adapters.md) | Web/app/API separation, branded/unbranded portfolios, localization, regional source ecosystems, and no-owned-site surfaces |
| [`references/output-contracts.md`](references/output-contracts.md) | Deterministic audit, implementation, work-order, experiment, acceptance, and run-bundle templates |
| [`references/source-register.md`](references/source-register.md) | Official controls, research boundaries, repository recon, conflict resolution, and maintenance provenance |

## Typical operating sequence

1. Establish the controlled asset, entity, market, user job, permissions, and fact registry.
2. Preserve a before snapshot and verify current official platform controls.
3. Audit access, routing, understanding, and citability; diagnose the earliest failed stage.
4. Build branded and unbranded prompt portfolios with exact surface conditions.
5. Map recurring sources, competitors, factual narratives, and legitimate inclusion paths.
6. Convert only supported findings into risk-scoped work orders.
7. Apply the smallest patch that fixes the shared root cause.
8. Re-fetch and verify deterministic results immediately.
9. Measure retrieval, citation, absorption, fidelity, referral, and conversion on later observation windows.
10. Reconcile first-party actuals with live and synthetic probes without averaging disagreement.

## Validate

```bash
python scripts/validate_skill.py
```

The validator checks required files, frontmatter constraints, referenced local paths, trigger eval JSON, and common packaging mistakes.

## Research posture

This repo treats AEO/GEO as an evidence-management problem, not a bag of hacks. Current platform controls outrank third-party claims. Field studies inform hypotheses but are bounded to the engines, dates, markets, and interfaces actually tested. Community and vendor observations are useful discovery inputs, not ranking-factor declarations.

See [`references/source-register.md`](references/source-register.md) for the reconciled evidence base.

## License

MIT.
