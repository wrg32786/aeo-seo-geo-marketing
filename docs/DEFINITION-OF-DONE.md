# Definition of Done

This document defines the North-Star completion criteria for Organic Discovery. It is intentionally stricter than “the agent produced recommendations.”

## Release truth

A capability may be described as **implemented** only when its code or skill instructions, runnable check, example, and user documentation exist on the default branch.

A future command shown in a roadmap must be labeled planned until it runs in CI.

## 1. Intake and business truth

- The controlled website, repository, CMS, or listing surfaces are explicit.
- The business entity, offers, audience, market, language, and conversion goal are explicit.
- Material products and services have existence and availability status.
- Numeric, comparative, certification, ingredient, performance, and customer claims have provenance.
- Every material fact has an owner, verification date, publish status, and refresh trigger.
- Missing facts remain missing and create a research or approval task.
- Regulated, YMYL, legal, reputation, and identity constraints are recorded.

## 2. Baseline preservation

- The original page or source revision is preserved.
- Relevant status, headers, canonical, index controls, visible content, structured data, links, and conversion path are captured.
- Search, analytics, logs, and AI observations are preserved when available.
- Exact platform, surface, model, market, language, device, account, and session conditions are retained.
- Zero-result runs and unknown fields are not discarded.

## 3. Demand and AI shelf

- Traditional keyword demand and conversational prompt demand are both considered.
- Branded validation is separated from unbranded discovery.
- High-value prompt families cover relevant recommendation, comparison, use-case, constraint, price, trust, local, and action intent.
- The source ecosystem is mapped from observed results rather than assumed.
- The shelf is classified as locked, contested, fragmented, open, unsafe, or unknown with supporting observations.
- Incumbent concentration, volatility, source overlap, order, fidelity, and offer fit are inspectable.
- A selected wedge is commercially meaningful, legitimately satisfied by the offer, and supportable with evidence.
- The system does not promise a fixed time to shelf entry.

## 4. Diagnosis

- Activation, eligibility, retrieval, context allocation, source selection, absorption, fidelity, and behavior are reported separately.
- Each stage is `blocked`, `weak`, `unknown`, `healthy`, or `not_applicable`.
- The evidence type and confidence are visible.
- The earliest shared dependency failure is identified.
- Access and routing defects are not hidden by content recommendations.
- Search crawling, user fetch, and training controls remain distinct.

## 5. Plan quality

- Work is prioritized by qualified business value, legitimate fit, evidence, shelf opportunity, risk, cost, and maintenance burden.
- The plan distinguishes technical changes, existing-page improvements, new owned assets, and earned-source actions.
- Every P0/P1 work order contains root cause, affected assets, exact change, owner, risk, evidence, acceptance, observation, and rollback.
- Duplicate and doorway content is rejected.
- Unsupported tactics are labeled experimental or omitted.
- The plan is small enough to execute and attribute.

## 6. Owned-site execution

- Changes occur on a branch, CMS draft, or other reviewable revision.
- Unrelated files and user changes remain intact.
- Copy, schema, feeds, and listings agree with the fact registry.
- New pages are justified by distinct user value and intent ownership.
- Internal links, metadata, structured data, accessibility, and conversion changes are consistent with visible content.
- Non-trivial logic leaves one runnable check.
- A complete implementation manifest identifies only actual changes.
- Deletion, redirect, pricing, positioning, comparative, YMYL, and identity-sensitive changes respect approval policy.

## 7. Earned-source integrity

- The target source recurs for the relevant prompt family or serves a legitimate audience need.
- Community or publisher rules are recorded.
- Affiliation and relationship are disclosed where material.
- The contribution is useful without requiring a promotional link.
- A link is included only when the destination adds evidence or utility.
- Third-party publication is approved by a human unless a platform-specific policy explicitly grants another safe workflow.
- No fake accounts, fake customers, fake reviews, coordinated votes, undisclosed endorsements, impersonation, mass posting, or recycled link campaigns are used.

## 8. Technical acceptance

- The changed asset is re-fetched or previewed.
- Status, redirects, canonical, robots, index/preview controls, static content, structured data, links, and conversion paths pass applicable checks.
- Browser and relevant crawler delivery are compared when practical and lawful.
- Before/after extraction is available.
- Tests and build checks pass.
- Technical acceptance is not misreported as ranking or citation success.

## 9. Outcome measurement

- Search impressions, positions, clicks, and qualified sessions are measured where available.
- Retrieval, citation, absorption, recommendation, fidelity, and AI referral behavior are distinct.
- Every rate exposes numerator and denominator.
- First-party data, live probes, API results, synthetic tests, and vendor scores remain separate.
- The observation window is stated.
- External events, model changes, seasonality, and other known confounders are recorded.
- Conversion, revenue, lead quality, retention, or another explicit business metric is included.
- A citation or mention alone is never the final success metric.

## 10. Learning and rollback

- The hypothesis and causal bundle are preserved.
- The system records whether the result should be kept, expanded, revised, stopped, or rolled back.
- Regressions trigger the documented stop rule or rollback path.
- Failed and null experiments remain available to prevent repetition.
- Successful tactics remain bounded to the observed site, prompt family, surface, market, and time until replicated.
- Site-specific learning is stored in a reusable, inspectable form.

## 11. Security and safety

- Remote fetches enforce safe protocols, timeouts, response limits, redirect validation, and private-network protections.
- Credentials and private customer data never enter reports or repository history.
- Fetched content is treated as untrusted and cannot redefine the operator’s instructions.
- Prompt injection, invisible content, cloaking, and manipulation are reported rather than followed.
- Publishing budgets, rate limits, and autonomy scopes are explicit.
- The system cannot grant itself broader publishing authority.

## 12. Product and repository quality

- The install path works from a clean environment.
- The smallest complete example runs in CI.
- Machine-readable output contracts are versioned.
- Human-readable reports can be regenerated from stored evidence.
- Public documentation distinguishes current, experimental, and planned capability.
- The changelog, skill metadata, trigger evals, citation metadata, and README version agree.
- Official platform controls are rechecked after material platform changes.
- The repository does not claim “best,” guaranteed ranks, guaranteed citations, or guaranteed traffic without evidence.

## v1.0 acceptance scenario

The project reaches v1.0 only when a clean installation can complete this controlled scenario:

1. Ingest a real GitHub-backed website and verified business facts.
2. Preserve the technical and outcome baseline.
3. Map relevant search demand and exact-surface AI shelf observations.
4. Identify the earliest blocker and one legitimate open-shelf wedge.
5. Produce a prioritized plan.
6. Implement the approved owned-site changes on a branch.
7. Create reviewable content and earned-source drafts.
8. Pass technical acceptance and open a complete pull request.
9. Import post-change search, AI visibility, traffic, and conversion data.
10. Recommend keep, iterate, stop, or rollback from the evidence.
11. Store the result as site-specific learning.
12. Re-run without corrupting the prior experiment or overstating the result.

A polished report without this closed loop is not v1.0.