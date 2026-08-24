# AGENTS.md

## Purpose

This repository contains **Organic Discovery**, an evidence-grounded Agent Skill and deterministic Python toolchain for SEO, AEO, GEO, webpage auditing, Business Truth validation, exact-surface AI shelf mapping, truthful wedge planning, implementation, and measurement.

## Read order

1. Read `SKILL.md`.
2. Load only the references routed by the task.
3. Read `references/output-contracts.md` before changing machine-readable outputs.
4. Read `references/source-register.md` before changing platform doctrine or effectiveness claims.
5. Read `docs/ROADMAP.md` and `docs/DEFINITION-OF-DONE.md` before calling a planned capability shipped.
6. Read the relevant offline example before changing deterministic behavior.

## Current executable boundary

Version `0.5.0` ships:

- `python scripts/od.py audit`;
- `python scripts/od.py facts validate`;
- `python scripts/od.py shelf map`;
- `python scripts/od.py wedge plan`;
- versioned schemas and two deterministic examples.

A live prompt scheduler, analytics connector, CMS publisher, dashboard, database, hosted service, and autonomous public posting remain planned capability.

## Change rules

- Fix the earliest shared dependency failure rather than patching every symptom.
- Prefer current official platform documentation over repositories, vendor studies, or community claims.
- Never convert a correlation, benchmark, or field report into a guaranteed ranking or citation claim.
- Keep platform, surface, mode, model, market, language, device, account, session, prompt family, target entity, and branded state separate unless the output explicitly preserves every component.
- Preserve unknown as unknown; do not convert missing data to `false` or zero.
- Branded validation must not inflate unbranded recommendation share.
- Seller-controlled evidence must not be relabeled as independent consensus.
- Unsafe, unavailable, prohibited, expired, unsupported, locked, or insufficient opportunities must fail their hard gate rather than disappear inside a weighted score.
- Do not require `llms.txt`, custom AI endpoints, fixed chunk sizes, fake freshness, or manufactured mentions.
- Any public numeric, comparative, or platform-behavior claim must include provenance and an evidence boundary.
- Keep `SKILL.md` below 500 lines; move depth into `references/`.
- Update the changelog and versioned artifacts together for material releases.
- Do not add a dependency for a check the Python standard library can perform correctly.
- Public third-party posting is human-approved by default.

## Required checks

Run before every pull request:

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
```

The validator also regenerates the offline audit, Business Truth, shelf, and wedge outputs and compares them with committed expected artifacts.

## Fixture discipline

When deterministic output changes intentionally:

1. explain the root-cause behavior change;
2. update the smallest relevant code path;
3. run the command against the fixture;
4. inspect the diff rather than copying blindly;
5. update the expected artifact;
6. keep one focused regression assertion;
7. confirm Python 3.11 and 3.13 CI.

## Pull-request summary

State:

- root cause;
- files changed;
- schema or contract changes;
- evidence class;
- deterministic validation performed;
- hard-gate behavior affected;
- any delayed outcome still awaiting observation;
- any tactic deliberately not applied;
- rollback path.
