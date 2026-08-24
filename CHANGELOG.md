# Changelog

All notable changes to Organic Discovery are documented here.

## 0.5.0 — 2026-08-24

- Added `od.py facts validate` with a canonical CSV contract, stable IDs, validation errors, publication gates, normalized output, existence and availability checks, source ownership, verification dates, evidence grades, owners, refresh triggers, limitations, markets, languages, prompt families, and expiry.
- Hard-blocked approved/public claims that lack provenance, refer to nonexistent or unavailable offers, omit maintenance ownership, are expired or prohibited, or make certification, safety, medical, or customer-result claims without independent evidence.
- Added `od.py shelf map` for exact-surface JSONL observations. Platform, surface, mode, model, market, language, device, account, session, prompt family, target entity, and branded state remain separate grouping dimensions.
- Added transparent shelf metrics for recommendation coverage, target participation, first-mentioned share, order, incumbent concentration, set agreement, volatility, source overlap, source ownership, retrieval, citation, fidelity, constraint satisfaction, and availability. Every rate includes its numerator and denominator.
- Added operational shelf states: `locked`, `contested`, `fragmented`, `open`, `unsafe`, and `unknown`, with machine-readable reasons and thresholds.
- Excluded branded validation runs from unbranded recommendation-share calculations.
- Added `od.py wedge plan` with hard gates for legitimate fit, publishable facts, offer existence and availability, observation sufficiency, unbranded exact-surface evidence, and safe/open shelf states.
- Unsafe, locked, unknown, unavailable, prohibited, and unsupported wedge candidates are rejected rather than merely receiving a lower score.
- Added versioned JSON Schemas for facts, observations, shelf maps, and wedge plans.
- Added the deterministic `examples/sample-shelf/` fixture with open, locked, fragmented, unsafe, branded, unavailable-offer, prohibited-claim, accepted, and rejected cases.
- Added eight v0.5-focused tests; the repository now runs fourteen regression tests plus byte-for-byte reproduction of both offline examples on Python 3.11 and 3.13.
- Updated the Agent Skill, README, output contracts, roadmap, release gates, metadata, CI, evals, and validator to the v0.5.0 capability boundary.
- Retained the no-opaque-score and no-fixed-time-to-shelf boundaries.

## 0.4.0 — 2026-08-24

- Added `scripts/od.py audit` for public HTTP(S) URLs and local HTML files.
- Added bounded standard-library remote fetching with public-IP validation, credential rejection, pinned connections, redirect revalidation, timeouts, response-size limits, and redirect limits.
- Added deterministic checks for HTTP behavior, crawler controls, index directives, canonicalization, initial HTML, JavaScript-only risk, metadata, headings, links, images, accessibility basics, sitemaps, JSON-LD, visible/schema agreement, entity and claim gaps, hidden content, and prompt-injection patterns.
- Added `audit.json`, `work-orders.json`, and `report.md` outputs with no opaque readiness score.
- Preserved unobservable activation, retrieval, context allocation, source selection, absorption, and behavior stages as `unknown`.
- Added exact work orders with owner, change, evidence, acceptance, delayed observation, and rollback.
- Added an intentionally broken offline sample site and committed expected artifacts.
- Added six focused regression tests and expanded CI to validate the package, tests, and fixture on Python 3.11 and 3.13.
- Updated README, Skill metadata, host metadata, output contracts, roadmap, definition of done, evals, contribution guidance, and citation metadata.

## 0.3.1 — 2026-08-24

- Reframed the North Star from a page auditor into an LLM-operated Organic Growth Operator.
- Added the complete closed loop: Business Truth, observation, demand and AI-shelf mapping, diagnosis, planning, owned-site execution, legitimate corroboration, validation, measurement, rollback, and learning.
- Added `docs/PRODUCT-VISION.md`, `docs/ROADMAP.md`, and `docs/DEFINITION-OF-DONE.md`.
- Added the `locked`, `contested`, `fragmented`, `open`, and `unsafe` AI-shelf model and a wedge-to-category expansion strategy.
- Added the Morrowen field observation as bounded evidence rather than a universal ranking tactic or timing promise.
- Added recommendation-integrity and authority-laundering checks.
- Added hard product/service existence, availability, evidence, and publication gates.
- Added operator modes from read-only audit through bounded continuous operation; supervised execution remains the default.
- Added explicit human approval for public third-party posting, identity-sensitive content, material claims, outreach, review requests, redirects, and other high-risk actions.
- Expanded output contracts for shelf maps, wedge records, publication gates, owned-asset briefs, source contributions, operator runs, and site-specific learning.
- Added an implementation roadmap beginning with a dependency-light deterministic auditor in v0.4, followed by truth/shelf mapping, GitHub execution, source earning, measurement adapters, CMS adapters, and bounded autonomy.
- Added validation rules that prevent planned commands and software from being presented as shipped capability.
- Updated README, Agent Skill metadata, host metadata, trigger evals, citation metadata, and agent instructions.

## 0.3.0 — 2026-08-22

- Added canonical fact registry and claim provenance gates.
- Added dependency-layer repair order: access → routing → understanding → citability.
- Added exact surface isolation across API, web, app, Search, assistant, country, locale, language, account, personalization, and branded/unbranded sampling.
- Added first-party versus synthetic reconciliation and narrative-drift tracking.
- Added deterministic crawler/WAF/rendering checks and prompt-injection diagnostics to the operating doctrine.
- Added market-specific source ecosystems and no-owned-site mode.
- Added work orders with risk, acceptance, observation windows, and rollback.
- Added traffic/conversion attribution as a measurable lower bound rather than visibility theater.
- Applied the Organic Discovery workflow to the repository’s own GitHub surface.
- Reworked the README around an answer-first SEO/AEO/GEO identity, installation, use cases, differentiation, outputs, and evidence.
- Added OpenAI host metadata, GitHub Actions validation, `AGENTS.md`, contribution guidance, security reporting, citation metadata, and a public self-audit.

## 0.2.0 — 2026-08-22

- Added prompt portfolio research, persona variants, multi-engine tracking, citation gaps, grounding-query capture, and recurring monitoring.
- Added source-earning workflow across editorial sources, communities, reviews, directories, GitHub, and other recurring citation ecosystems.
- Kept `llms.txt`, fixed GEO scores, and manufactured mentions explicitly non-mandatory.

## 0.1.0 — 2026-08-22

- Initial evidence-grounded SEO/AEO/GEO skill.
- Added eight-stage discovery model, platform adapters, vertical adapters, measurement protocol, source register, output contracts, validator, and trigger evaluations.
