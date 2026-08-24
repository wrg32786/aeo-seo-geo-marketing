# AGENTS.md

## Purpose

This repository contains **Organic Discovery**, an evidence-grounded Agent Skill for SEO, AEO, GEO, AI search visibility, citation analysis, implementation, and measurement.

## Read order

1. Read `SKILL.md`.
2. Load only the reference files routed by the task.
3. Read `references/output-contracts.md` before changing output shapes.
4. Read `references/source-register.md` before changing platform doctrine or making a new effectiveness claim.
5. Read `docs/SELF-AUDIT.md` when changing the repository’s own positioning or discovery surface.

## Change rules

- Fix the earliest shared dependency failure rather than patching every symptom.
- Prefer current official platform documentation over repositories, vendor studies, or community claims.
- Never convert a correlation, benchmark, or field report into a guaranteed ranking or citation claim.
- Keep web, app, API, Search, assistant, model, locale, device, account, and session observations separate.
- Preserve unknown as unknown; do not silently convert missing data to `false` or zero.
- Do not require `llms.txt`, custom AI endpoints, fixed chunk sizes, fake freshness, or manufactured mentions.
- Any new public numeric, comparative, or platform-behavior claim must include provenance and an evidence boundary.
- Keep `SKILL.md` below 500 lines; move depth into `references/`.
- Update the changelog when doctrine, packaging, or output contracts materially change.
- Do not add a dependency for a check that the Python standard library can perform.

## Required check

Run before every commit or pull request:

```bash
python scripts/validate_skill.py
```

A change is incomplete if the validator fails, local links break, trigger evals drift, or versioned artifacts disagree.

## Pull-request summary

State:

- root cause;
- files changed;
- evidence class;
- deterministic validation performed;
- any delayed outcome still awaiting observation;
- any tactic deliberately not applied.
