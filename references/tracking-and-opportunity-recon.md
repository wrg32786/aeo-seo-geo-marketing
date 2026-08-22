# Tracking and Opportunity Recon

Use this module when the task includes AI visibility monitoring, cross-engine citation tracking, prompt portfolio creation, competitor citation gaps, or recurring measurement.

## 1. Separate measurement from optimization

A tracker should observe the system; it must not smuggle speculative ranking assumptions into the score. Keep raw observations distinct from heuristic recommendations.

Preferred pipeline:

1. Prompt portfolio and persona/use-case variants.
2. Platform-specific runs with locale and mode recorded.
3. Raw answer and cited-source capture.
4. Grounding/search-query capture when the platform exposes it.
5. Conventional SERP capture for the same intent.
6. Target and competitor page fetches.
7. Structured comparison and opportunity extraction.
8. Historical persistence, drift alerts, and business attribution.

The `danishashko/geo-aeo-tracker` project is a useful implementation reference for this architecture: it separates grounding results, platform citations, SERP results, scraped pages, site context, and LLM recommendations into different data objects. Reuse that separation. Do not inherit any heuristic score as ground truth.

## 2. Prompt portfolio expansion

Start from real customer jobs, then expand into natural-language prompts across these classes:

- definition and category education;
- recommendations and best-for constraints;
- brand/category comparisons and alternatives;
- evaluation, trust, drawbacks, and fit;
- how-to and problem solving;
- price, cost, ROI, and procurement;
- landscape and vendor discovery;
- use cases, industry scenarios, and edge cases.

Mine wording from Search Console, support tickets, sales calls, site search, autocomplete/PAA, review platforms, Reddit, forums, YouTube comments, and exposed AI grounding queries.

Reddit is especially useful as a language and problem-discovery corpus. It is not evidence that posting to Reddit will improve citation.

For each prompt, record:

```yaml
prompt: ""
intent: "definition|recommendation|comparison|evaluation|how_to|cost|landscape|use_case"
business_tier: "buy|solve|learn"
audience_or_persona: ""
market: ""
platforms: []
importance: "high|medium|low"
source: ""
brand_should_appear_because: ""
```

Do not invent a precise `citability` probability before measurement. Use `high/medium/low` only as a planning prior, then replace it with observed rates.

## 3. Persona fan-out

A useful prompt tracker should test how the same intent changes across realistic personas and constraints, for example:

- founder vs procurement lead;
- beginner vs expert;
- local buyer vs national buyer;
- budget vs premium buyer;
- regulated vs non-regulated use case;
- implementation-focused vs strategy-focused user.

Keep persona variants semantically equivalent enough that comparisons remain interpretable. Do not inflate the prompt set with trivial wording variants that create false precision.

## 4. Cross-platform result record

Use one normalized record per run while preserving platform-native raw fields:

```json
{
  "prompt_id": "buy-014",
  "prompt_text": "best ...",
  "platform": "chatgpt",
  "mode": "search",
  "country": "US",
  "locale": "en-US",
  "timestamp_utc": "2026-08-22T20:00:00Z",
  "answer_text": "...",
  "search_queries_exposed": [],
  "citations": [
    {
      "url": "https://example.com/page",
      "domain": "example.com",
      "position": 1,
      "title": "...",
      "cited_sentence": "..."
    }
  ],
  "target_url_cited": false,
  "target_entity_mentioned": false,
  "target_entity_recommended": false,
  "competitors_mentioned": [],
  "framing": [],
  "errors": []
}
```

Capture `cited_sentence` or equivalent context where the product exposes it. This makes attribution and recommendation analysis more reliable than URL frequency alone.

## 5. Grounding-query recon

When a platform exposes generated search/grounding queries, treat them as high-value diagnostic data.

Record:

- generated search queries;
- source chunks or URLs;
- source-support spans where exposed;
- target source selection rate;
- target-support word share only when directly observable;
- differences between the user prompt and generated search queries.

Do not claim hidden fan-out queries when the platform does not expose them.

## 6. Citation opportunity mining

For each prompt, compare the target against recurring cited competitors and sources.

An opportunity exists when:

- a competitor is repeatedly cited and the target is absent;
- a third-party source repeatedly covers the category but omits the target;
- the cited source answers a sub-question the target can answer materially better;
- the engine relies on a comparison, directory, review, GitHub, Reddit, video, or registry source that has a legitimate path to inclusion.

Output:

| Prompt | Platform | Repeated cited source | Competitor present | Target present | Gap type | Legitimate action |
|---|---|---|---|---|---|---|

Legitimate actions include improving the owned canonical page, publishing unique evidence, correcting an official listing, contributing to an open-source list under its rules, earning editorial coverage, or answering a community question transparently.

Do not convert every competitor citation into outreach. First ask whether the source recurs and whether inclusion would serve its audience.

## 7. Historical tracking and drift

Store immutable raw runs plus normalized derived metrics. Track:

- citation rate and citation persistence;
- mention rate;
- recommendation share;
- cited domain diversity;
- first-citation share;
- source overlap and churn;
- competitor gains/losses;
- geographic variation;
- prompt-cluster variation;
- conventional SERP rank and impressions;
- referral and conversion outcomes.

A drift alert should trigger on meaningful sustained change, not one volatile run. Use a minimum run count or repeated time points before escalating.

## 8. Tooling lessons to reuse

From `geo-aeo-tracker`:

- useful: local-first/raw-history mindset, multi-model tracking, country segmentation, prompt hub, persona variants, citation gap analysis, raw-vs-derived separation, scheduled runs, explicit platform result types;
- useful: combining AI citations, SERP results, competitor page retrieval, and page context before generating recommendations;
- caution: vendor/API availability changes; keep provider adapters replaceable;
- caution: an LLM-generated 0–100 “SRO score” is a heuristic, not an engine ranking signal.

From `onvoyage-ai/gtm-engineer-skills`:

- useful: strict artifact contracts, modular research → planning → implementation handoffs, prompt taxonomy, competitor/citation-gap workflow, deterministic checks separated from judgment;
- useful: community mining for exact customer language and unanswered questions;
- caution: several fixed citation multipliers, freshness percentages, required `llms.txt`, and “one mention can trigger citation” claims should not be universalized without target-specific validation;
- caution: do not force an arbitrary 50/50 technical/intelligence score when the actual failing stage is known.

## 9. Definition of done for a tracker

A monitoring system is decision-useful when:

- raw responses and source URLs are retained;
- platform, mode, locale, prompt, and timestamp are preserved;
- null/no-search/error runs remain in denominators;
- citations, mentions, recommendations, and source use are separate fields;
- competitor gaps can be traced back to exact prompts and sources;
- repeated runs distinguish persistent from one-off visibility;
- conventional search and business outcomes can be joined to AI visibility;
- heuristic scores are visibly labeled as heuristics and never presented as platform ranking factors.
