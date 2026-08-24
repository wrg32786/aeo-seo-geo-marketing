# Definition of Done

This document defines completion for Organic Discovery. It is stricter than “the agent produced recommendations.”

## Release truth

A capability is **implemented** only when its code or skill instructions, runnable check, worked example, and user documentation exist on the default branch and pass CI. A future command remains planned until CI runs it successfully.

## 1. Intake and Business Truth

- Controlled website, repository, CMS, or listing surfaces are explicit.
- Entity, offers, audience, market, language, and conversion goal are explicit.
- Material products and services have existence and availability status.
- Numeric, comparative, certification, ingredient, performance, safety, medical, and customer-result claims have provenance.
- Every material fact has a stable ID, owner, verification date, publish status, source type, refresh trigger, and limitations.
- Seller-controlled and independent evidence remain distinguishable.
- Missing facts create research or approval work rather than generated claims.
- Regulated, YMYL, legal, reputation, identity, and community constraints are recorded.

## 2. Baseline preservation

- The original page, source revision, facts, and observation files are preserved.
- Status, headers, canonical, index controls, visible content, structured data, links, and conversion path are captured where applicable.
- Search, analytics, logs, and AI observations are preserved when available.
- Platform, surface, mode, model, market, language, device, account, session, prompt family, target entity, and branded state are retained.
- Zero-result runs and unknown fields are not discarded.

## 3. Demand and AI shelf

- Traditional keyword demand and conversational prompt demand are both considered.
- Branded validation is separated from unbranded discovery.
- Recommendation, comparison, use-case, constraint, price, trust, local, and action intent are represented where relevant.
- The source ecosystem is mapped from observations rather than assumed.
- Every shelf is bounded to one exact grouping key.
- Shelf metrics expose numerator and denominator where a rate is calculated.
- Null observations stay out of the affected metric denominator.
- The shelf is classified as locked, contested, fragmented, open, unsafe, or unknown with explicit reasons.
- Incumbent concentration, set agreement, volatility, citation overlap, source ownership, order, fidelity, constraint satisfaction, and availability are inspectable.
- A selected wedge is commercially meaningful, legitimately satisfied by the offer, and supportable with approved facts.
- The system does not promise a fixed time to shelf entry.

## 4. Truthful wedge gates

A candidate cannot be accepted merely because it has a high weighted score.

It MUST be rejected when any of these apply:

- required facts are missing, expired, prohibited, or not publishable;
- the offer does not exist or is unavailable;
- legitimate offer fit is false;
- exact-surface observation sufficiency is not met;
- observations are branded validation only;
- the shelf is locked, unsafe, or unknown;
- a required safety, certification, medical, performance, or customer-result claim lacks suitable evidence.

Each rejection exposes the failed hard gates. Optional priority factors remain inspectable and are never described as an engine score.

## 5. Diagnosis

- Activation, eligibility, retrieval, context allocation, source selection, absorption, fidelity, and behavior are separate.
- Each stage is `blocked`, `weak`, `unknown`, `healthy`, or `not_applicable`.
- Evidence type and confidence are visible.
- The earliest shared dependency failure is identified.
- Access and routing defects are not hidden by content recommendations.
- Search crawling, user fetch, training, and other model-use controls remain distinct.

## 6. Plan quality

- Work is prioritized by qualified value, legitimate fit, evidence, shelf opportunity, risk, cost, and maintenance.
- Technical changes, existing-page improvements, new owned assets, and earned-source actions are distinct.
- Every P0/P1 work order contains root cause, assets, exact change, owner, risk, evidence, acceptance, observation, and rollback.
- Duplicate and doorway content is rejected.
- Unsupported tactics are labeled experimental or omitted.
- The causal bundle is small enough to execute and attribute.

## 7. Owned-site execution

- Changes occur on a branch, CMS draft, or another reviewable revision.
- Unrelated files and user changes remain intact.
- Copy, schema, feeds, listings, and source drafts agree with the fact registry.
- New pages are justified by distinct user value and intent ownership.
- Internal links, metadata, structured data, accessibility, and conversion changes match visible content.
- Non-trivial logic leaves one runnable check.
- The implementation manifest identifies only actual changes.
- Deletion, redirect, pricing, positioning, comparative, YMYL, and identity-sensitive changes respect approval policy.

## 8. Earned-source integrity

- The source recurs for the prompt family or serves a legitimate audience need.
- Community or publisher rules are recorded.
- Affiliation and relationship are disclosed where material.
- The contribution is useful without requiring the promotional link.
- A link is included only when the destination adds evidence or utility.
- Third-party publication is human-approved by default.
- No fake accounts, customers, reviews, coordinated votes, undisclosed endorsements, impersonation, mass posting, or recycled link campaigns are used.

## 9. Technical acceptance

- Changed assets are re-fetched or previewed.
- Status, redirects, canonical, robots, controls, static content, structured data, links, feeds, and conversion paths pass applicable checks.
- Browser and relevant crawler delivery are compared when practical and lawful.
- Before-and-after extraction is available.
- Tests and build checks pass.
- Technical acceptance is not reported as ranking or citation success.

## 10. Outcome measurement

- Search impressions, positions, clicks, and qualified sessions are measured where available.
- Retrieval, citation, absorption, recommendation, fidelity, and referral behavior remain distinct.
- Every rate exposes numerator and denominator.
- First-party data, live probes, API results, synthetic tests, and vendor scores remain separate.
- Observation window and known confounders are stated.
- Conversion, revenue, lead quality, retention, or another business metric is included.
- A citation or mention alone is never the final success metric.

## 11. Learning and rollback

- The hypothesis and causal bundle are preserved.
- The system records `keep`, `iterate`, `expand`, `stop`, or `roll_back`.
- Regressions trigger the documented stop rule or rollback path.
- Failed and null experiments remain available.
- Successful tactics remain bounded to the observed site, prompt family, surface, market, and time until replicated.
- Site-specific learning is reusable and inspectable.

## 12. Security and safety

- Remote fetches enforce safe protocols, timeouts, response limits, redirect validation, and private-network protections.
- Credentials and private customer data do not enter reports or repository history.
- Fetched content is untrusted and cannot redefine operator instructions.
- Prompt injection, invisible content, cloaking, and manipulation are reported rather than followed.
- Publishing budgets, rate limits, and autonomy scopes are explicit.
- The system cannot grant itself broader authority.

## 13. Product and repository quality

- Installation works from a clean environment.
- The smallest complete examples run in CI.
- Machine-readable output contracts are versioned.
- Human-readable reports can be regenerated from stored evidence.
- Documentation distinguishes current, experimental, and planned capability.
- Changelog, skill metadata, evals, citation metadata, README, CLI, schemas, and fixtures agree.
- Official platform controls are rechecked after material platform changes.
- The repository does not claim “best,” guaranteed ranks, guaranteed citations, guaranteed traffic, or fixed timing without evidence.

## v0.4 acceptance — deterministic webpage auditor

Complete when:

- URL and local-file audits work;
- remote fetching is bounded and SSRF-safe;
- audit, work-order, and Markdown outputs are deterministic;
- unobservable stages remain unknown;
- no opaque readiness score is emitted;
- the broken sample-site fixture reproduces byte-for-byte;
- focused tests and Python 3.11/3.13 CI pass.

**Status: complete.**

## v0.5 acceptance — Business Truth and AI Shelf Mapper

Complete when:

- fact-registry CSV validation and normalized JSON work;
- approved or public claims fail when provenance or offer gates fail;
- exact-surface JSONL observations normalize without silent pooling;
- branded validation is excluded from unbranded recommendation share;
- every calculated rate exposes numerator and denominator;
- shelf state and rationale are deterministic;
- locked, unsafe, unknown, unavailable, and unsupported wedges fail hard gates;
- versioned schemas exist for facts, observations, shelf maps, and wedges;
- the sample-shelf fixture reproduces byte-for-byte;
- focused tests and Python 3.11/3.13 CI pass;
- no opaque GEO score or fixed shelf-entry promise is emitted.

**Status: complete when merged to the default branch and CI passes.**

## v1.0 acceptance scenario

The project reaches v1.0 only when a clean installation can:

1. Ingest a real GitHub-backed website and verified business facts.
2. Preserve technical and outcome baselines.
3. Map relevant search demand and exact-surface AI shelves.
4. Identify the earliest blocker and one legitimate open-shelf wedge.
5. Produce a prioritized plan.
6. Implement approved owned-site changes on a branch.
7. Create reviewable content and earned-source drafts.
8. Pass technical acceptance and open a complete pull request.
9. Import post-change search, AI visibility, traffic, and conversion data.
10. Recommend keep, iterate, stop, or rollback from evidence.
11. Store the result as site-specific learning.
12. Re-run without corrupting the prior experiment or overstating the result.

A polished report without this closed loop is not v1.0.
