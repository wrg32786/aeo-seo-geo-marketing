# Definition of Done

This document defines completion for Organic Discovery. It is stricter than “the agent produced recommendations.”

## Release truth

A capability is **implemented** only when its code or skill instructions, runnable check, worked example, and user documentation exist on the default branch. A future command remains planned until CI runs it successfully.

## v0.4 acceptance

The deterministic auditor release is complete only when all of these are true:

- `python scripts/od.py audit https://example.com --output output/` is a real interface.
- `python scripts/od.py audit ./page.html --output output/` is a real interface.
- Each run writes valid `audit.json`, `work-orders.json`, and `report.md`.
- Remote fetches allow only HTTP(S), reject credentials and non-public destinations, pin a validated public address, revalidate redirects, and enforce timeout, redirect, and response-size limits.
- The auditor covers crawler purpose, index controls, canonicalization, initial HTML, metadata, headings, links, images, sitemaps, JSON-LD, visible/schema agreement, provenance gaps, and hidden prompt-like instructions.
- No opaque readiness score is emitted.
- Activation, retrieval, context allocation, source selection, absorption, and behavior remain `unknown` unless later evidence exists.
- Every work order has root cause, owner, risk, change, acceptance, observation, and rollback.
- One intentionally broken offline fixture produces committed deterministic expected artifacts.
- One focused test module covers non-trivial logic.
- CI runs package validation, tests, and the offline example on Python 3.11 and 3.13.
- Versioned skill, README, changelog, citation, eval, auditor, and expected-output metadata agree.
- Dashboard, scheduler, CMS publishing, analytics integration, and public community posting are not claimed as shipped.

## 1. Intake and business truth

- Controlled website, repository, CMS, or listing surfaces are explicit.
- Entity, offers, audience, market, language, and conversion goal are explicit.
- Material products and services have existence and availability status.
- Numeric, comparative, certification, ingredient, performance, and customer claims have provenance.
- Every material fact has an owner, verification date, publish status, and refresh trigger.
- Missing facts create a research or approval task.
- Regulated, YMYL, legal, reputation, and identity constraints are recorded.

## 2. Baseline preservation

- The original page or source revision is preserved.
- Status, headers, canonical, index controls, visible content, structured data, links, and conversion path are captured.
- Search, analytics, logs, and AI observations are preserved when available.
- Platform, surface, model, market, language, device, account, and session conditions are retained.
- Zero-result runs and unknown fields are not discarded.

## 3. Demand and AI shelf

- Traditional keyword demand and conversational prompt demand are both considered.
- Branded validation is separated from unbranded discovery.
- Relevant recommendation, comparison, use-case, constraint, price, trust, local, and action intents are covered.
- The source ecosystem is mapped from observations rather than assumed.
- The shelf is classified as locked, contested, fragmented, open, unsafe, or unknown with evidence.
- Concentration, volatility, source overlap, order, fidelity, and offer fit are inspectable.
- A selected wedge is commercially meaningful, legitimately satisfied, and supportable with evidence.
- No fixed shelf-entry timeline is promised.

## 4. Diagnosis

- Activation, eligibility, retrieval, context allocation, source selection, absorption, fidelity, and behavior are separate.
- Each stage is `blocked`, `weak`, `unknown`, `healthy`, or `not_applicable`.
- Evidence type and confidence are visible.
- The earliest shared dependency failure is identified.
- Access and routing defects are not hidden by content recommendations.
- Search crawling, user fetch, training, and other model-use controls remain distinct.

## 5. Plan quality

- Work is prioritized by qualified business value, legitimate fit, evidence, shelf opportunity, risk, cost, and maintenance.
- Technical changes, existing-page improvements, new owned assets, and earned-source actions are distinct.
- Every P0/P1 order contains root cause, asset, exact change, owner, risk, evidence, acceptance, observation, and rollback.
- Duplicate and doorway content is rejected.
- Unsupported tactics are labeled experimental or omitted.
- The causal bundle is small enough to execute and attribute.

## 6. Owned-site execution

- Changes occur on a branch, CMS draft, or reviewable revision.
- Unrelated work remains intact.
- Copy, schema, feeds, and listings agree with Business Truth.
- New pages have distinct user value and intent ownership.
- Internal links, metadata, structured data, accessibility, and conversion changes match visible content.
- Non-trivial logic leaves one runnable check.
- The implementation manifest lists only actual changes.
- Deletion, redirect, pricing, positioning, comparative, YMYL, and identity-sensitive work respects approval policy.

## 7. Earned-source integrity

- The source recurs for the relevant prompt family or serves a real audience need.
- Community or publisher rules are recorded.
- Affiliation is disclosed where material.
- The contribution is useful without a promotional link.
- A link is included only when it adds evidence or utility.
- Third-party publication has human approval by default.
- No fake accounts, fake customers, fake reviews, coordinated votes, undisclosed endorsements, impersonation, mass posting, or recycled link campaigns are used.

## 8. Technical acceptance

- The changed asset is re-fetched or previewed.
- Applicable status, redirects, canonical, robots, index controls, static content, structured data, links, and conversion paths pass.
- Browser and crawler delivery are compared when practical and lawful.
- Before/after extraction is available.
- Tests and build checks pass.
- Technical acceptance is not reported as ranking or citation success.

## 9. Outcome measurement

- Search impressions, positions, clicks, and qualified sessions are measured where available.
- Retrieval, citation, absorption, recommendation, fidelity, and referral behavior remain distinct.
- Every rate exposes numerator and denominator.
- First-party data, live probes, API results, synthetic tests, and vendor scores remain separate.
- The observation window and known confounders are stated.
- Conversion, revenue, lead quality, retention, or another business metric is included.
- A citation or mention is never the final success metric.

## 10. Learning and rollback

- The hypothesis and causal bundle are preserved.
- The system records keep, expand, revise, stop, rollback, or inconclusive.
- Regressions trigger the documented stop rule or rollback path.
- Failed and null experiments remain available.
- Successful tactics remain bounded to observed site, prompt family, surface, market, and time until replicated.
- Site-specific learning is reusable and inspectable.

## 11. Security and safety

- Remote fetches enforce safe protocols, timeout, response limits, redirect validation, and private-network protection.
- Credentials and private data do not enter reports or history.
- Fetched content is untrusted and cannot redefine operator instructions.
- Prompt injection, invisible content, cloaking, and manipulation are reported rather than followed.
- Publishing budgets, rate limits, and autonomy scopes are explicit.
- The system cannot grant itself broader authority.

## 12. Product and repository quality

- Installation works from a clean environment.
- The smallest complete example runs in CI.
- Machine-readable output contracts are versioned.
- Human-readable reports can be regenerated from stored evidence.
- Documentation distinguishes current, experimental, and planned capability.
- Changelog, skill metadata, evals, citation metadata, auditor version, and README agree.
- Official platform controls are rechecked after material changes.
- The repository does not claim “best,” guaranteed ranks, guaranteed citations, or guaranteed traffic without evidence.

## v1.0 acceptance scenario

The project reaches v1.0 only when a clean installation can:

1. Ingest a real GitHub-backed website and verified business facts.
2. Preserve technical and outcome baselines.
3. Map search demand and exact-surface AI shelf observations.
4. Identify the earliest blocker and one legitimate open-shelf wedge.
5. Produce a prioritized plan.
6. Implement approved owned-site changes on a branch.
7. Create reviewable content and earned-source drafts.
8. Pass technical acceptance and open a complete pull request.
9. Import post-change search, AI visibility, traffic, and conversion data.
10. Recommend keep, iterate, stop, or rollback from evidence.
11. Store site-specific learning.
12. Re-run without corrupting the prior experiment or overstating the result.

A polished report without this closed loop is not v1.0.
