# Platform Adapters

Use this reference before changing crawler controls, Search settings, feeds, structured data, or platform-specific behavior. Platform policies and crawler identities change; verify official documentation at execution time.

## 1. Google Search and generative features

Core principle: Google’s generative Search features still depend on standard Search eligibility and quality systems.

### Treat as first-class

- Googlebot crawlability and rendering;
- indexability and snippet eligibility;
- canonicalization;
- people-first, useful content;
- supported structured data matching visible content;
- product/local/publisher feeds and profiles where relevant;
- Search Console actuals when available.

### Do not make mandatory

- `llms.txt`;
- AI-only schema;
- fixed “LLM chunks”;
- custom AI manifests;
- manufactured third-party mentions.

### Separate controls

- Google Search inclusion: Googlebot, indexing/snippet directives.
- Other Google AI uses controlled by `Google-Extended`: separate from Search ranking/indexing.

Do not tell users that blocking or allowing `Google-Extended` directly controls AI Overview ranking.

## 2. OpenAI / ChatGPT

Keep three functions distinct:

- **OAI-SearchBot** — search/discovery citation crawling for ChatGPT Search surfaces.
- **ChatGPT-User** — user-triggered fetching in supported experiences.
- **GPTBot** — training/model improvement crawler.

A site can choose to allow search citation access while blocking training. Verify current OpenAI documentation and published IP ranges before policy changes.

Do not treat GPTBot access as required for ChatGPT Search citations.

## 3. Anthropic / Claude

Anthropic exposes separate crawler identities for different purposes. Verify current names at execution time; current doctrine distinguishes:

- search-oriented crawling;
- user-triggered fetching;
- training/general crawling.

Do not collapse them into one `ClaudeBot` policy without checking current official docs.

## 4. Perplexity

Separate automatic discovery/search crawling from user-triggered fetching where Perplexity documents separate identities.

Measure actual citations on the target surface. A robots audit proves only access policy, not serving/citation.

## 5. Bing / Microsoft Copilot

For Bing-grounded discovery:

- verify Bingbot access and Bing indexing;
- use Bing Webmaster Tools when available;
- keep canonical/sitemap/indexing fundamentals healthy;
- consider IndexNow for timely change notification when appropriate;
- track Copilot and Bing/AI surfaces separately when their interfaces differ.

Do not assume Google indexing implies Bing/Copilot visibility.

## 6. Crawlers versus WAF/CDN

Robots rules are only one layer. Compare actual HTTP behavior for relevant crawler identities because managed bot systems may challenge or block them independently.

Check:

- status code;
- final URL;
- challenge page;
- extracted text;
- cache/geography effects;
- verified crawler IP where possible.

Never weaken general abuse protection more than necessary.

## 7. Structured data

Structured data is useful when:

- the vocabulary is supported by the target search platform or downstream consumer;
- values match visible page content;
- it improves eligibility for real rich-result/product/local/event/etc. features;
- it reduces entity ambiguity.

It is not a magic universal AI citation signal.

Priorities:

1. factual consistency;
2. correct supported type;
3. required/recommended properties where applicable;
4. stable identifiers/URLs;
5. correct authorship/date/product/location relationships.

Inspect nested `@graph` and list-valued `@type` correctly; do not falsely report missing schema that exists inside a graph.

## 8. `llms.txt` and AI-readable files

Treat `llms.txt` as optional/experimental unless a named consumer or documentation workflow justifies it.

If used:

- keep it concise and maintained;
- link only to canonical, public, useful pages;
- verify every linked URL is live and crawlable;
- avoid publishing private/internal information;
- monitor request logs to see whether any relevant agent actually consumes it.

Do not award ranking credit merely for file presence.

Custom `.well-known/ai.txt`, `/ai/summary.json`, `/ai/faq.json`, etc. are not universal standards. Use only for explicit integrations.

## 9. Search Console / first-party reporting

When Google exposes generative-search performance reporting for a property, treat it as first-party actual exposure within its documented scope.

Keep separate:

- impressions/exposure;
- cited pages;
- clicks/referrals;
- conversions.

If click data is absent from a report, reconcile with analytics/logs rather than inferring clicks.

## 10. Local discovery

For local businesses, prioritize platform-owned entity data:

- Google Business Profile;
- Bing Places where relevant;
- Apple/business directories where user journey warrants;
- accurate NAP/service area/hours;
- reviews and responses;
- local landing pages only when they provide unique local value.

Do not generate thin city pages at scale.

## 11. Ecommerce/product discovery

Keep these synchronized:

- product page visible facts;
- Product structured data;
- Merchant Center/feed data;
- inventory/price/availability;
- identifiers such as GTIN/MPN/brand when legitimately available;
- images and variant relationships.

Conflict between feed, schema, and page is a data-quality issue before it is an SEO issue.

## 12. News/editorial discovery

For publishers:

- truthful publication/update times;
- author/editor accountability;
- original reporting and primary documents;
- correction policy;
- canonical ownership/syndication controls;
- News sitemap/feed surfaces where supported;
- clear separation of reporting, opinion, and sponsored content.

Do not update timestamps without substantive changes.

## 13. Documentation/developer discovery

High-value patterns:

- stable canonical URLs;
- server-rendered/referenceable text;
- version-specific docs;
- code examples that compile/run;
- explicit prerequisites/errors;
- changelog/release links;
- GitHub/source links;
- OpenAPI or other documented machine interfaces when the product actually has them.

`llms.txt` may be more reasonable here than on a generic marketing site because the content has a clear machine-navigation use case; still measure consumption.

## 14. Preview/snippet controls

Understand the distinction between:

- `noindex` — prevents indexing;
- `nosnippet` — limits snippets/use in Search features per platform documentation;
- `max-snippet` / `data-nosnippet` — granular preview controls;
- crawler-specific robots rules — control fetching;
- training-specific opt-outs — do not necessarily affect Search.

Never remove legal/privacy/paywall controls solely for GEO.

## 15. Feeds, profiles, and APIs as source-of-truth surfaces

Where a platform provides a structured submission/profile system, prefer maintaining it over inventing an AI file:

- Merchant Center;
- Business Profile;
- publisher feeds;
- app stores;
- product catalogs;
- Bing Webmaster/IndexNow;
- marketplace listings;
- official APIs/docs.

These are real platform contracts and often more operationally important than speculative GEO markup.

## 16. Agent-action readiness

When users expect AI agents to do more than answer—book, buy, call, calculate, submit, install—optimize the underlying human-accessible action path first:

- semantic labels/forms;
- accessible names;
- predictable URLs/actions;
- clear prerequisites and confirmation states;
- secure authentication boundaries;
- documented APIs/tools where they genuinely exist.

Do not expose unsafe write actions merely to appear “agent-ready.”
