# AGENTS.md

## Purpose

This repository contains **Organic Discovery**, an evidence-grounded Agent Skill and deterministic audit foundation for SEO, AEO, GEO, AI search visibility, owned-site implementation, legitimate source earning, and outcome measurement.

## Read order

1. Read `SKILL.md`.
2. Run `python scripts/od.py audit <target> --output <dir>` when a URL or HTML target exists.
3. Load only the reference files routed by the task.
4. Read `references/output-contracts.md` before changing output shapes.
5. Read `references/source-register.md` before changing platform doctrine or making a new effectiveness claim.
6. Read `docs/PRODUCT-VISION.md`, `docs/ROADMAP.md`, and `docs/DEFINITION-OF-DONE.md` before changing product scope or release claims.
7. Read `docs/SELF-AUDIT.md` when changing this repository’s own discovery surface.

## Change rules

- Fix the earliest shared dependency failure rather than patching symptoms.
- Prefer current official platform documentation over repositories, vendor studies, or community claims.
- Never convert a correlation, benchmark, or field report into a guaranteed ranking or citation claim.
- Keep web, app, API, Search, assistant, model, locale, device, account, and session observations separate.
- Preserve unknown as unknown; do not convert missing data to `false` or zero.
- Do not require `llms.txt`, custom AI endpoints, fixed chunk sizes, fake freshness, or manufactured mentions.
- Public third-party posting is human-approved by default.
- Any public numeric, comparative, or platform-behavior claim needs provenance and an evidence boundary.
- Keep `SKILL.md` below 500 lines; move depth into `references/` or `docs/`.
- Update changelog and every versioned artifact together.
- Never advertise planned capability as shipped capability.
- Do not add a dependency for a check the Python standard library can correctly perform.
- Remote fetch changes must preserve protocol, credential, private-network, redirect, timeout, and response-size protections.
- The auditor may report technical eligibility; it must not infer indexing, retrieval, citation, recommendation, traffic, or conversion.
- Every work order keeps acceptance and rollback.
- Do not edit committed expected outputs by hand; regenerate them with the auditor.

## Required checks

Run before every commit or pull request:

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/od.py audit examples/sample-site/site/index.html --output /tmp/od-example
```

A change is incomplete if validation fails, local links break, expected output drifts unintentionally, trigger evals disagree, or versioned artifacts diverge.

## Pull-request summary

State:

- root cause;
- files changed;
- evidence class;
- deterministic validation performed;
- security implications for remote fetching or untrusted content;
- delayed outcomes still awaiting observation;
- planned capability deliberately excluded;
- tactics deliberately not applied.
