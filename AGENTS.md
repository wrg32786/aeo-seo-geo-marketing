# AGENTS.md

## Purpose

This repository contains **Organic Discovery**, an evidence-grounded Agent Skill and product blueprint for an LLM-operated SEO, AEO, GEO, source-earning, implementation, measurement, and learning system.

The current release is a skill and operating specification. Do not imply that planned crawler, CLI, connector, dashboard, scheduler, CMS, or publishing capabilities exist until their files, tests, examples, and release gates are on the default branch.

## Read order

1. Read `SKILL.md`.
2. Read `docs/PRODUCT-VISION.md` for the North Star.
3. Read `docs/ROADMAP.md` before implementing a planned capability.
4. Read `docs/DEFINITION-OF-DONE.md` for release gates.
5. Load only the reference files routed by the task.
6. Read `references/ai-shelf-and-growth-loop.md` for recommendation shelves, wedges, and continuous operation.
7. Read `references/output-contracts.md` before changing artifact shapes.
8. Read `references/source-register.md` before changing platform doctrine or making a new effectiveness claim.
9. Read `docs/SELF-AUDIT.md` when changing the repository’s own positioning or discovery surface.

## Change rules

- Fix the earliest shared dependency failure rather than patching every symptom.
- Prefer current official platform documentation over repositories, vendor studies, or community claims.
- Never convert a correlation, benchmark, field report, or one-model observation into a guaranteed ranking, citation, recommendation, traffic, or timing claim.
- Keep web, app, API, Search, assistant, model, locale, device, account, and session observations separate.
- Preserve unknown as unknown; do not silently convert missing data to `false` or zero.
- Build and enforce the fact registry before generating material public claims.
- Verify that the product or service exists and is available before optimizing it into recommendations.
- Treat seller-controlled and independent evidence as different source types.
- Do not require `llms.txt`, custom AI endpoints, fixed chunk sizes, fake freshness, or manufactured mentions.
- Do not create doorway pages for prompt paraphrases.
- Any new public numeric, comparative, product-behavior, or platform-behavior claim must include provenance and an evidence boundary.
- Keep `SKILL.md` below 500 lines; move depth into `references/` or `docs/`.
- Update the changelog when doctrine, packaging, outputs, or release status materially change.
- Do not add a dependency for a check the Python standard library can correctly perform.
- Prefer one runnable proof over broad scaffolding.

## Owned-site execution

When repository or CMS access exists:

- preserve the baseline and current user work;
- use a branch or draft;
- implement the smallest coherent patch;
- validate the exact changed surface;
- include acceptance, observation, and rollback;
- state which outcomes remain pending;
- do not merge, deploy, delete, redirect, or materially reposition without the controlling approval policy.

Low-risk autonomous owned-site changes require an explicit approved class, deterministic checks, rate limits, and rollback.

## Third-party and community policy

The agent may research sources, inspect community rules, identify legitimate questions, and draft useful contributions.

Public third-party posting is human-approved by default. Never implement:

- fake accounts or personas;
- fake customers, testimonials, or reviews;
- coordinated votes or engagement;
- undisclosed endorsements;
- mass posting or repeated link drops;
- identity impersonation;
- moderation or platform-control evasion.

A community contribution must remain useful without the promotional link. Include a link only when it adds necessary evidence or utility, and disclose material affiliation.

## Current-versus-planned truth gate

Before documenting a command or feature as current:

1. confirm the file or interface exists;
2. confirm its smallest example runs;
3. confirm CI validates it;
4. confirm the README does not place it under a planned heading;
5. update versioned metadata and the changelog.

If any item fails, describe the capability as planned.

## Required checks

Run before every commit or pull request:

```bash
python scripts/validate_skill.py
```

When executable modules exist, also run the smallest applicable unit or example check declared in the roadmap and CI.

A change is incomplete if:

- package validation fails;
- local links break;
- trigger evals drift;
- versioned artifacts disagree;
- current and planned capability are conflated;
- a public claim lacks provenance;
- a non-trivial change has no runnable check.

## Pull-request summary

State:

- root cause;
- files changed;
- current capability added or doctrine changed;
- evidence class;
- deterministic validation performed;
- approval and publishing state;
- delayed outcomes still awaiting observation;
- rollback path;
- tactics deliberately not applied.
