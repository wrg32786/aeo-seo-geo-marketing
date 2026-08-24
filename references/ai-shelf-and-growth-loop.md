# AI Shelf and Organic Growth Loop

Use this module when the task involves AI recommendations, product or service discovery, long-tail wedges, competitor concentration, content creation, source earning, or continuous organic growth.

## Purpose

The goal is not to make a model repeat a brand name once. The goal is to find a commercially useful question the business can answer truthfully, build the strongest owned asset for that question, earn legitimate corroboration, and determine whether the change improves qualified discovery.

## Core terms

- **AI shelf** — the small set of brands, products, services, pages, and sources repeatedly surfaced for a prompt family.
- **Shelf slot** — an observed mention or recommendation position under a specific surface and run condition.
- **Incumbent concentration** — how much of the observed recommendation set is controlled by the leading entity or small group.
- **Shelf openness** — the absence of stable consensus for a meaningful user constraint.
- **Wedge** — a narrow, defensible question where the offer has real fit and can provide better evidence than current answers.
- **Corroboration** — independent or appropriately disclosed third-party evidence that supports the owned asset.
- **Authority laundering** — a model restating seller-controlled claims in a neutral voice that makes them appear independently vetted.

## Evidence boundary

### Starmorph guide

The [Starmorph AEO/GEO guide](https://blog.starmorph.com/blog/aeo-geo-optimization-guide) is useful as a practitioner inventory of content, schema, sourcing, and tracking tactics. Treat fixed multipliers, universal formatting thresholds, and checklist weights as hypotheses unless supported by current official guidance or replicated evidence.

### Morrowen field observation

The Morrowen experiment, described in the project discussion and summarized in [independent coverage](https://www.dataiads.io/en/blog/chatgpt-product-recommendation-fake-brand), is a bounded field observation:

- a new seller-controlled site reportedly entered browsing-enabled ChatGPT recommendations for two narrow prompts;
- broad category prompts did not move;
- other tested engines did not reproduce the result;
- the product and favorable claims were fabricated for the experiment;
- the observation did not isolate the causal contribution of wording, indexing, supporting publication, freshness, competition, or personalization.

It supports the hypothesis that under-defended long-tail recommendation questions may be more movable than locked category shelves. It does **not** establish a 21-day rule, a universal Q&A tactic, a cross-engine effect, or permission to publish unverified claims.

### Recommendation manipulation research

The [SafeGEO recommendation-manipulation study](https://arxiv.org/html/2606.28356v1) supports treating seller-controlled recommendation content as an integrity risk and testing structured evidence checks. It does not provide a universal production ranking formula.

## Shelf-mapping workflow

### 1. Define the commercial decision

Start from a real user decision, not a keyword list:

- What is the person trying to choose, avoid, compare, repair, buy, book, or understand?
- What constraints materially change the answer?
- What outcome makes the visit valuable to the business?
- Does the offer genuinely satisfy the constraint?

Reject a prompt family when the only path to relevance is stretching or inventing the offer.

### 2. Build prompt families

Cover the decision from broad to narrow:

| Family | Example pattern |
|---|---|
| Category | best `[category]` |
| Use case | best `[category]` for `[job]` |
| Constraint | `[category]` without `[problematic attribute]` |
| Failure mode | what should I use if `[common option]` causes `[problem]` |
| Specification | `[ingredient/technology/compatibility]` `[category]` |
| Comparison | `[option A]` vs `[option B]` for `[job]` |
| Price | best `[category]` under `[budget]` |
| Trust | safest / most tested / best documented `[category]` |
| Local | `[category]` available in `[market]` |
| Exclusion | who should not use `[category/offer]` |
| Agentic | choose or reorder `[category]` under these constraints |

Do not create a separate webpage for every paraphrase. Prompts are measurement units; pages are user-value assets.

### 3. Preserve exact run conditions

For every observation, retain:

- platform;
- product surface;
- search or grounding mode;
- model/version when exposed;
- date and time;
- country, locale, and language;
- device;
- logged-in/account state;
- clean, persistent, or personalized session;
- prompt text and family;
- search activation and exposed grounding queries;
- answer text;
- recommendation order;
- cited domains and URLs;
- seller-controlled versus independent source type;
- target retrieval, citation, absorption, and fidelity fields.

Never pool web, app, API, Search, assistant, country, account, or session conditions silently.

### 4. Sample more than once

A single answer is an anecdote. Use repeated clean runs when permitted, preserve null and zero-result runs, and report denominators.

A practical baseline may use:

```text
5–20 high-value prompt families
× 3–5 paraphrases where materially distinct
× 3–5 repeated runs
× each target surface
```

The sample size is a planning default, not a ranking requirement. Adjust for cost, volatility, and business value.

### 5. Calculate inspectable shelf signals

Use transparent metrics rather than one proprietary score.

#### Mention rate

```text
target mentions / eligible runs
```

#### First-mentioned share

```text
runs where target is first / runs with recommendations
```

#### Recommendation share

```text
target recommendation appearances / total recommendation appearances
```

Exclude branded validation prompts from unbranded recommendation share.

#### Citation rate

```text
runs citing target / eligible runs
```

#### Absorption rate

```text
cited answers substantively using target claims / cited answers
```

#### Fidelity rate

```text
accurate target appearances / target appearances
```

#### Incumbent concentration

Use a visible concentration measure such as leading-brand share or Herfindahl-Hirschman Index. State the formula and the set of recommendations included.

#### Cross-surface agreement

Report how often surfaces return the same leading entities and source domains. Do not call disagreement an error automatically; it may identify open shelf space.

#### Volatility

Report how often the recommendation set or order changes across repeated comparable runs.

#### Constraint satisfaction

Record whether each recommendation actually satisfies the prompt’s material constraints.

### 6. Classify the shelf

Use evidence and judgment together:

| State | Typical evidence |
|---|---|
| Locked | high leading-brand concentration, low volatility, high cross-run agreement |
| Contested | recurring small set with meaningful order rotation |
| Fragmented | low cross-surface agreement and high set variation |
| Open | no stable leader for the specific constraint and weak existing answers |
| Unsafe | repeated factual errors, constraint violations, or authority laundering |
| Unknown | insufficient or incomparable observations |

Do not convert these classes into a promise that an open shelf is easy to win.

### 7. Select a wedge

A wedge must pass all gates:

1. meaningful user demand;
2. plausible qualified business value;
3. real offer fit;
4. supportable claims;
5. weak or incomplete current answers;
6. manageable competition and maintenance;
7. acceptable legal, policy, and reputational risk;
8. a controlled asset capable of answering the question better.

Prioritize with an inspectable model:

```text
opportunity priority =
qualified demand
× legitimate fit
× evidence strength
× shelf openness
× execution probability
÷ cost, risk, and maintenance
```

The factors may be ordinal. Expose every factor and rationale; do not present the result as an engine score.

## Truth gate before content generation

Before drafting a wedge asset, verify:

- the offer exists;
- availability and geography;
- current price and terms;
- ingredients, specifications, compatibility, or service scope;
- evidence for performance, safety, testing, and certification claims;
- known limitations, exclusions, and contraindications;
- seller-controlled versus independent evidence;
- permission to use customer, partner, expert, or organization names;
- agreement across visible copy, schema, feeds, and listings.

If a required fact is missing, create a fact-acquisition work order. Do not fill the gap with plausible prose.

## Build the owned wedge asset

Prefer one complete asset that serves the user over many near-duplicate pages.

A strong wedge page commonly includes:

- a direct answer early;
- the exact constraint and why it matters;
- who the option is for and not for;
- current verified specifications, availability, and price where relevant;
- fair comparison dimensions;
- original testing, examples, demonstrations, data, or first-hand experience when available;
- independent evidence and source attribution;
- material limitations and uncertainty;
- methodology and verification date;
- descriptive internal links to canonical product/service pages;
- a clear next step aligned with the user’s job.

Use schema only when it matches visible content and a real supported use case.

## Earn legitimate corroboration

After the owned answer is strong, map which external sources recur for that prompt family.

Possible actions:

- publish original data or a useful tool others can cite;
- correct or complete a legitimate directory profile;
- obtain real customer reviews through a neutral request process;
- contribute documentation or open-source work;
- provide an expert quote or editorial contribution;
- support partner/customer case studies with permission;
- demonstrate the product or method on video;
- answer a relevant community question completely.

Do not seek mentions merely because a domain is generally authoritative. The source should be relevant to the exact audience and question.

## Reddit and community operation

Reddit is an earned tactic only when the target source chain or audience evidence justifies it.

### Required record

```yaml
community: r/example
thread_or_topic: "..."
why_relevant: "..."
observed_source_role: citation | demand-language | referral | reputation | none
rules_checked_at: 2026-08-24
affiliation: "..."
link_needed: true | false
approval: pending | approved | rejected
```

### Draft standard

- Answer the actual question.
- Put the useful substance in the post or comment.
- Disclose material affiliation.
- Link only when the destination adds needed evidence, detail, or utility.
- Use the community’s language without impersonating its members.
- Adapt to the thread; do not paste a reusable promotional block.

### Prohibited automation

- account creation farms;
- fake personas or customer stories;
- mass posting;
- coordinated votes;
- undisclosed promotion;
- fake reviews;
- repeated exposure links;
- evasion of moderator or platform controls.

The agent may research, draft, and monitor. Public posting remains human-approved by default.

## Recommendation-integrity review

Before accepting a shelf gain as success, inspect whether the answer:

- cites the owned page accurately;
- distinguishes the seller from independent evidence;
- preserves limitations;
- satisfies the user’s constraints;
- avoids presenting unverified claims as vetted consensus;
- recommends an actually available option;
- does not displace a safer or more suitable option through misleading content.

A higher recommendation share with lower fidelity or constraint satisfaction is a regression.

## Observation cadence

Choose cadence from crawl/index latency, engine volatility, and business value. A common field plan is:

```text
baseline
→ technical acceptance immediately
→ day 7 directional check
→ day 21–30 primary check
→ day 60 durability check
→ day 90 retain/expand/retire decision
```

These dates are an experiment cadence, not a promise that results appear on day 21.

## Wedge expansion

Expand only after the initial asset shows evidence of useful discovery and factual stability.

1. Improve the same constraint where answers remain incomplete.
2. Address adjacent constraints on the same canonical asset or a genuinely distinct asset.
3. Add symmetric comparisons and alternatives.
4. Build use-case authority through evidence, tools, and case studies.
5. Attempt broader category shelves only when the business has accumulated real proof and source support.

## Required outputs

Use `references/output-contracts.md` to emit:

- shelf map;
- wedge opportunity record;
- truth/publication gate;
- owned-asset brief;
- corroboration plan;
- community contribution draft;
- experiment record;
- acceptance and measurement report;
- learning record.

## Anti-patterns

Do not:

- assume long-tail means low competition or high value;
- infer shelf openness from one run;
- manufacture the product or evidence;
- copy the Morrowen experiment as a tactic;
- publish one page per prompt paraphrase;
- equate first mention with durable rank;
- report browsing-enabled results as browsing-off model knowledge;
- generalize one engine to all engines;
- treat a model’s confident voice as independent validation;
- celebrate citations while traffic, conversion, fidelity, or safety declines.