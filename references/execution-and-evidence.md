# Execution and Evidence

Use this reference when turning reconnaissance into implementation work. It exists to prevent a common failure mode: good observations becoming vague recommendations with no fact discipline, acceptance criteria, or rollback.

## 1. Build a fact registry first

Before generating copy, schema, feeds, profile text, comparisons, community responses, or off-site listings, establish one canonical registry for the material facts the system is allowed to assert.

Recommended fields:

| Field | Purpose |
|---|---|
| `entity` | Brand, product, person, location, service, or dataset the claim describes |
| `canonical_name` | Exact public name |
| `aliases` | Legitimate alternate names, former names, common misspellings, model names |
| `claim` | Canonical factual statement |
| `value` / `unit` | Structured value when applicable |
| `source` | Primary document/URL/system of record |
| `verified_at` | Date checked |
| `evidence_grade` | Strength of support |
| `publish_status` | public / internal / requires approval / prohibited |
| `expires_at` | Date or event that forces review |
| `owner` | Person/system responsible for maintenance |

### Fact evidence grades

- **A — authoritative primary source**: controlled system, contract, product database, official filing, maintained docs, original dataset.
- **B — strong independent corroboration**: reliable third party with direct evidence.
- **C — internal statement awaiting external verification or publication approval.**
- **D — unresolved / inferred / stale.** Do not turn into a strong public claim.
- **E — prohibited or known false.** Never publish.

Do not let a writing model silently promote C/D facts to A/B wording.

## 2. Separate recommendation evidence from observation evidence

Two grades answer different questions:

1. **Recommendation label** (`[O]`, `[A]`…`[X]`) says how strongly a tactic is supported.
2. **Observation grade** says how trustworthy a specific result is.

Observation grades:

| Grade | Observation |
|---|---|
| **A** | Controlled live-product sample with raw response, source URLs/screenshots/export, timestamp, exact surface, clean environment, and query |
| **B** | Reproducible API/product sample with version/mode and whether retrieval/grounding was enabled documented |
| **C** | Synthetic benchmark, vendor simulation, replay, or inferred extraction |
| **D** | Anecdote, remembered result, screenshot with missing context, or unverified report |

Never call an API response “what ChatGPT says” if the target is ChatGPT Search in the consumer product. Never merge browser, app, API, and grounded/un-grounded runs as if they were equivalent.

## 3. Dependency-layer repair order

Use four implementation layers:

### Layer 1 — Access

Can the relevant system fetch usable public content?

Check:

- HTTP status and redirect chain;
- robots policy using correct matching semantics;
- `X-Robots-Tag` plus HTML robots directives;
- WAF/CDN response differences for relevant crawler identities;
- static HTML versus JS-only shell;
- authentication/cookie/geofence barriers;
- response size and accidental truncation where relevant.

If access is blocked, downstream optimization is secondary.

### Layer 2 — Routing

Can engines consistently identify the correct canonical owner of the information?

Check:

- canonical URL;
- redirects and duplicate protocols/hosts/slashes/parameters;
- sitemap membership and truthful `lastmod`;
- internal discovery;
- pagination/facets;
- hreflang and locale routing;
- duplicate and near-duplicate pages;
- broken links from machine-readable navigation files if they exist.

### Layer 3 — Understanding

Can the page and entity be interpreted correctly?

Check:

- visible entity definition;
- canonical name and legitimate aliases;
- product/service category;
- native-market language;
- consistent descriptions across visible copy, schema, feeds, and owned profiles;
- supported structured data;
- organization/product/person relationships;
- dates, versions, units, geography, price, availability where relevant.

### Layer 4 — Citability / usefulness

Does the asset contain material worth selecting and reusing?

Check:

- direct relevance to target user jobs;
- self-contained factual sections;
- original/primary evidence;
- definitions and scope;
- comparisons with consistent dimensions;
- procedures with verification;
- dates/versions where volatility matters;
- limitations and exceptions;
- transparent sources and methodology;
- human usefulness and conversion path.

## 4. Browser-versus-crawler observability

Robots access does not prove delivery. A CDN or WAF can serve different status codes, challenges, or HTML to automated identities.

When relevant and allowed, compare:

```text
normal browser-like request
relevant search/citation crawler request
generic bot request
```

Record:

- status;
- final URL;
- headers;
- content length/hash;
- title/H1/body extraction;
- challenge/interstitial text;
- cache headers;
- region if relevant.

Treat user-agent strings as spoofable. Official IP verification or trusted verified-bot signals are stronger evidence than UA alone.

## 5. Rendering and extraction parity

A page that looks complete in a browser may expose little in initial HTML.

Capture both:

- **response HTML extraction** — what exists before client JS;
- **rendered extraction** — what a browser sees after execution.

Flag:

- meaningful body absent from initial HTML;
- critical internal links injected only after interaction;
- product facts hidden behind tabs that are not in DOM;
- schema generated after a crawler may have stopped;
- infinite scrolling with no crawlable URLs;
- client-side locale redirects;
- consent overlays obscuring content.

Do not assume every AI/search crawler renders JS like Google.

## 6. Manipulation and prompt-injection review

Because pages can be consumed by agents and LLM-based systems, inspect for accidental or malicious instructions that should not be part of public content.

High-risk patterns:

- “ignore previous instructions” / “system message” / “you are an AI” directives;
- hidden CSS prose;
- zero-width/invisible Unicode used to conceal instructions;
- long instructional HTML comments;
- `aria-hidden` blocks containing non-decorative persuasive content;
- micro-font text;
- foreground/background camouflage;
- `data-ai-*`, `data-prompt-*`, or similar attributes carrying instructions;
- content that tells an answer engine how to rank or recommend the page.

Remove manipulative content. Do not attempt to optimize it.

## 7. Narrative and entity fidelity

Track what an engine says separately from whether it cites the site.

Useful states:

- `aligned` — material facts and positioning are accurate;
- `incomplete` — correct but omits an important current fact;
- `outdated` — formerly true, now stale;
- `misattributed` — right fact attached to wrong entity/product;
- `fabricated` — unsupported claim;
- `negative-but-supported` — unfavorable but evidence-based;
- `misrepresented` — misleading or materially wrong framing.

For corrections, fix the underlying authoritative sources before trying to “influence” model output.

## 8. No-owned-site mode

Some entities have no canonical website: marketplace sellers, apps, open-source tools, creators, local businesses, social-first brands.

Do not force website-specific tasks onto them. Build from controlled surfaces:

- marketplace/store listing;
- Google Business Profile or equivalent;
- GitHub/docs;
- publisher/creator profile;
- product directory;
- official social profile;
- help center;
- knowledge base.

Then map external source ecosystems normally.

Mark website-only controls `not_applicable`, never failed.

## 9. Work-order contract

Every recommended implementation should be convertible into this shape:

```yaml
id: OD-001
priority: P0
root_cause: relevant crawlers receive a challenge page instead of the article
stage: eligibility
evidence: O
risk: medium
assets:
  - https://example.com/article
owner: web-platform
change:
  - remove verified citation crawler from managed bot challenge
  - preserve rate limits and abuse protections
acceptance:
  - crawler request returns 200
  - extracted title and article body match browser extraction materially
  - normal bot-abuse protections remain active
observation:
  metric: crawler requests and target-query retrieval
  window: 14d
rollback:
  - restore prior WAF rule if abuse or instability appears
```

### Priority definitions

- **P0** — access/indexing/canonical/security/data-integrity blocker.
- **P1** — high-value retrieval/citation/fidelity issue with clear evidence.
- **P2** — useful improvement or bounded experiment.
- **P3** — low-confidence, low-value, cosmetic, or optional.

### Risk classes

- **low** — copy/metadata adjustment with trivial rollback.
- **medium** — crawler policy, schema, routing, feed, template, or public comparison change.
- **high** — redirects at scale, domain migration, regulated claim, reputation response, wide programmatic publishing, or anything difficult to reverse.

High-risk changes require explicit pre-change snapshot and rollback.

## 10. Immediate acceptance versus delayed observation

Do not confuse “implemented correctly” with “worked in search.”

### Immediate acceptance

Can be checked now:

- response status/header changed correctly;
- canonical points to intended URL;
- schema validates and matches visible facts;
- sitemap/internal link includes intended URL;
- content exists in initial/rendered HTML;
- profile/feed reflects source-of-truth data;
- no hidden/manipulative text;
- tests/build pass.

### Delayed observation

Requires later samples:

- indexed/crawled status;
- rankings/impressions;
- retrieval rate;
- citation share;
- factual absorption;
- recommendation position;
- referral traffic;
- conversion.

A work order may be technically accepted while its outcome remains `pending_observation`.

## 11. Actual-versus-synthetic reconciliation

Prefer first-party actuals when the platform provides them, but do not discard synthetic probes.

Use both for different purposes:

- first-party reports/logs: actual exposure or crawling within their scope;
- controlled probes: diagnostic coverage for specific prompts;
- API sampling: reproducible model behavior in that API mode;
- vendor trackers: comparative convenience, not platform truth.

When they disagree:

- actual exposure high, probes low → prompt portfolio is too narrow or poorly representative;
- probes high, actual exposure low → prompts may have little real demand or synthetic environment overstates visibility;
- citations high, referrals low → citation does not imply clicks; inspect placement and user intent;
- referrals high, tracked citations low → missing prompt coverage, app/browser attribution differences, or untracked surfaces.

Do not average disagreement away.

## 12. Deterministic observability

Leave artifacts that let the next operator reproduce what happened.

At minimum preserve:

- raw URL/page snapshot or git commit;
- response headers;
- test query set;
- raw AI/search outputs where legally/technically possible;
- source/citation URLs;
- before/after timestamp;
- changed files or CMS entries;
- acceptance result;
- observation status;
- owner and next review date.

For programmatic changes, add the smallest runnable regression check that catches the failure class.
