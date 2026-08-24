# Organic Discovery: Product Vision

## Status

**Current product:** an installable, evidence-grounded Agent Skill and operating specification for SEO, AEO, GEO, source earning, implementation, and measurement.

**North Star:** an LLM-operated Organic Growth Operator that can understand a business, audit its owned and earned discovery surfaces, find under-defended demand, improve the website through controlled changes, prepare legitimate supporting content, measure outcomes, and learn what works.

The North Star is a build contract, not a claim that every capability already ships. See [`ROADMAP.md`](ROADMAP.md) for implemented and planned phases.

## The job to be done

Give an AI agent a website, its business facts, controlled publishing access, and outcome data. The agent should be able to increase qualified organic discovery across:

- conventional search results;
- local and commerce surfaces;
- AI-generated answers and citations;
- AI product and service recommendations;
- communities, reviews, directories, editorial sources, documentation, and other recurring source ecosystems;
- the downstream visits, leads, sales, and retained customers that make visibility valuable.

The operator must improve the whole system rather than optimize one synthetic score.

## The closed loop

```text
UNDERSTAND THE BUSINESS
        ↓
MAP SEARCH DEMAND + THE AI SHELF
        ↓
OBSERVE THE SITE, COMPETITORS, AND SOURCE ECOSYSTEM
        ↓
DIAGNOSE THE EARLIEST FAILING STAGE
        ↓
PRIORITIZE THE HIGHEST-VALUE DEFENSIBLE OPPORTUNITY
        ↓
EDIT OWNED ASSETS + PREPARE EARNED-SOURCE CONTRIBUTIONS
        ↓
VALIDATE, APPROVE, AND PUBLISH
        ↓
MEASURE SEARCH, AI VISIBILITY, TRAFFIC, AND CONVERSION
        ↓
KEEP, IMPROVE, OR ROLL BACK
        ↓
STORE THE RESULT AS SITE-SPECIFIC LEARNING
```

Every loop must preserve the baseline, evidence, exact changes, acceptance checks, observation window, result, and rollback path.

## The AI shelf

AI answer systems compress a category into a small set of repeatedly mentioned brands, products, pages, and sources. That recommendation set is the **AI shelf**.

Broad shelves often favor incumbents because repeated citations, mentions, consumer demand, and prior recommendations can reinforce one another. New entrants should not begin by trying to displace a dominant brand for the broadest query. The operator should locate **open shelf space**: commercially useful questions where no stable recommendation consensus has formed and the business has a legitimate, verifiable fit.

### Authority laundering

An AI answer may restate seller-controlled claims in a neutral, confident voice and place them beside independently tested options. That can make unverified claims appear vetted even when the model merely retrieved the seller’s page. Organic Discovery treats this **Authority laundering** failure mode as a product-integrity risk: seller and independent evidence stay distinct, material limitations remain visible, and a recommendation gain with worse fidelity is a regression.

### Shelf states

- **Locked** — one incumbent dominates consistently across runs and surfaces.
- **Contested** — several credible alternatives rotate within a relatively stable set.
- **Fragmented** — engines and runs disagree materially.
- **Open** — no stable recommendation exists for the user constraint.
- **Unsafe** — answers frequently violate user constraints, repeat unsupported claims, or blur seller claims with independent evidence.

### Wedge-to-category strategy

```text
one truthful under-defended constraint
        ↓
related constraints and failure modes
        ↓
comparison and alternatives cluster
        ↓
use-case category
        ↓
broader category shelf
```

A wedge is valid only when the product, service, or information genuinely satisfies the question and the supporting claims pass the publication gate.

## Core product modules

### 1. Business Truth

The operator first creates a canonical source of truth:

- legal and public entity identity;
- products, services, markets, and availability;
- prices, ingredients, specifications, features, and exclusions;
- credentials, certifications, methodologies, and evidence;
- customer problems, use cases, objections, and conversion goals;
- claims the system may publish, claims requiring approval, and prohibited claims;
- refresh conditions and accountable owners.

No generated page, schema object, comparison, review response, community answer, or outreach message may invent around missing facts.

### 2. Observe

The operator should ingest or inspect, when available:

- live pages, source code, CMS records, headers, robots controls, sitemaps, feeds, and structured data;
- Google Search Console and Bing Webmaster data;
- Bing AI Performance data;
- analytics, conversion systems, and server logs;
- exact-surface AI-answer observations;
- existing AI-visibility tracker exports;
- competitor pages, recurring citations, reviews, directories, communities, videos, documentation, research, and editorial sources;
- deployments, content history, and experiment history.

First-party actuals, live controlled probes, APIs, synthetic tests, and vendor scores remain separate evidence lanes.

### 3. Demand and shelf mapping

The operator maps both keywords and prompts across:

- definitions and explanations;
- how-to and problem-solving intent;
- recommendations and buying questions;
- comparisons and alternatives;
- evaluation, trust, and risk;
- price and availability;
- location and market;
- use cases, compatibility, ingredients, specifications, and constraints;
- objections, failure modes, and who should not use the offer;
- agentic purchase or action intent.

For each prompt family, it records exact platform, surface, search mode, model, market, language, device, account state, session state, citations, recommendation order, source mix, and answer fidelity.

### 4. Diagnose

The operator uses the eight-stage chain:

1. Activation
2. Eligibility
3. Retrieval
4. Context allocation
5. Source selection
6. Absorption
7. Fidelity
8. Behavior

It fixes the earliest shared dependency in this order:

```text
access → routing → understanding → citability → corroboration → behavior
```

### 5. Plan

Opportunities are prioritized by expected business value rather than content volume:

```text
expected qualified demand
× legitimate offer fit
× evidence confidence
× probability of execution
× shelf openness
÷ cost, risk, and maintenance burden
```

The output is a small queue of technical, existing-page, new-owned-content, and earned-source work orders. The system should prefer one strong causal bundle over dozens of speculative tasks.

### 6. Execute owned-site changes

With repository or CMS access, the operator may:

- create a branch or CMS draft;
- repair crawl, canonical, redirect, sitemap, feed, rendering, and structured-data defects;
- improve titles, headings, page structure, internal links, accessibility, and conversion paths;
- update or consolidate existing content;
- create a genuinely needed page, comparison, case study, guide, tool, research asset, or documentation page;
- add verified sources, limitations, authorship, methodology, and update dates;
- run tests and produce a reviewable implementation manifest;
- open a pull request with acceptance checks and rollback.

It must not publish unsupported claims or create doorway pages for every query variation.

### 7. Earn corroboration

The operator identifies external sources that already influence the target prompt family. It may research and draft:

- editorial pitches and expert contributions;
- accurate directory and association profiles;
- partner and customer references with permission;
- review-generation requests to real customers;
- GitHub, documentation, research, dataset, and tooling contributions;
- useful Reddit, forum, and community answers;
- video, podcast, and demonstration opportunities.

Public third-party participation is **draft-and-approve by default**. The operator must not create fake people, fake customers, fake reviews, coordinated votes, undisclosed endorsements, mass link posts, or recycled comment campaigns.

### 8. Measure and learn

The operator measures separately:

- search impressions, positions, clicks, and qualified landing sessions;
- retrieval activation;
- target-page retrieval;
- citation and cited URL;
- substantive claim absorption;
- recommendation share and order;
- factual accuracy and narrative drift;
- attributable AI referrals;
- conversions, revenue, lead quality, retention, or another stated business outcome.

Each completed experiment becomes site-specific memory: what changed, where it worked, where it failed, what confounded the result, and whether to repeat or retire the tactic.

## Truth and recommendation-integrity gate

The operator must verify before publishing any material product, service, comparison, or recommendation claim:

- the offer exists and is currently available;
- the business actually provides it;
- prices, ingredients, specifications, and compatibility are current;
- claimed evidence supports the exact statement;
- seller-controlled and independent evidence are distinguished;
- limitations, exclusions, contraindications, and uncertainty are visible when material;
- visible copy, structured data, feeds, listings, and canonical records agree;
- the named person or organization has authorized attribution.

A missing fact creates a research or approval task—not permission to infer a favorable claim.

## Operator modes

| Mode | Behavior |
|---|---|
| Audit | Read-only research and diagnosis |
| Plan | Produces prioritized work orders and experiments |
| Draft | Creates code/content/community drafts without publishing |
| Supervised execute | Opens owned-site PRs or CMS drafts and requests approval |
| Approved owned-site autonomy | Publishes only pre-approved, low-risk change classes with rollback |
| Continuous operator | Repeats the loop on a schedule under budgets, gates, and stop rules |

The default is **supervised execute**.

## Approval policy

Human approval is required before:

- publishing on third-party platforms;
- making material pricing, positioning, legal, medical, financial, or safety content;
- making comparative or superlative claims;
- publishing under a named person’s identity;
- deleting or redirecting pages with existing traffic or links;
- making customer, partner, certification, or performance claims;
- starting outreach or review-request campaigns;
- expanding autonomy to a new class of changes.

Low-risk owned-site changes may become autonomous only after the class has deterministic checks, proven rollback, and an explicit policy grant.

## Product principles

1. **Business outcomes over visibility theater.** A mention without qualified behavior is not success.
2. **Truth before optimization.** The system may make true information easier to discover; it may not manufacture consensus.
3. **Earliest blocker first.** Do not rewrite content while access or routing is broken.
4. **Exact surfaces, not blended scores.** Search, app, API, model, market, account, and session conditions remain separate.
5. **Evidence labels travel with recommendations.** Official controls outrank studies, correlations, vendor claims, and anecdotes.
6. **Owned execution before external promotion.** Build the best defensible answer before seeking corroboration.
7. **Draft public participation; automate owned systems.** Third-party communities are people and institutions, not link inventory.
8. **One coherent experiment at a time.** Preserve baselines, denominators, nulls, confounders, and rollback.
9. **No ranking guarantees.** Search and answer engines are stochastic and change without notice.
10. **Current capability must be stated honestly.** Planned software is never presented as shipped software.

## Deliberate non-goals

The project will not become:

- a spam bot;
- a fake-review or synthetic-consensus engine;
- a proprietary 0–100 GEO oracle;
- a page factory for every keyword permutation;
- an autonomous identity impersonator;
- another closed dashboard whose metrics cannot be re-derived;
- a requirement to publish `llms.txt`, AI-only endpoints, or arbitrary content chunks without a named consumer.

## North-Star success

The system succeeds when it can repeatedly produce audited, reviewable changes that increase qualified organic business outcomes while preserving factual integrity, policy compliance, maintainability, and rollback.

The complete release gates are defined in [`DEFINITION-OF-DONE.md`](DEFINITION-OF-DONE.md).