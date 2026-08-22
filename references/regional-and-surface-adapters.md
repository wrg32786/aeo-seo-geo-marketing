# Regional and Surface Adapters

Use this module when results vary by country, language, device, app, browser, API, model mode, account state, or platform ecosystem—or when the business has no owned website.

The same prompt text does not define the same experiment across surfaces. Preserve the complete condition.

## 1. Surface identity

Represent each observation as:

```yaml
engine: ""
product: ""
mode: "search|grounded|ungrounded|agent|standard|unknown"
model_or_version: "reported-or-unknown"
terminal: "web|mobile-app|desktop-app|api|serp|assistant|unknown"
device: "desktop|mobile|tablet|api|unknown"
web_retrieval_enabled: true
account_state: "logged-out|logged-in|enterprise|unknown"
personalization_state: "off|on|unknown"
country: ""
locale: ""
language: ""
conversation_state: "new|continued"
timestamp_utc: ""
sampling_method: "manual-browser|official-api|third-party-provider|first-party-report|server-log"
```

Never silently pool observations whose identity differs.

## 2. API is not the consumer product

An API response may test model knowledge, a developer retrieval stack, or a provider-specific search tool. It is not automatically equivalent to the public web or app product.

Keep separate rows for:

- ungrounded model knowledge;
- API with search or grounding enabled;
- consumer web search mode;
- mobile or desktop app;
- enterprise or authenticated product;
- Google AI Overviews, Google AI Mode, and Gemini;
- Bing search results and Copilot;
- user-triggered fetches and autonomous/search crawlers.

Label the evidence produced by each condition. A non-search API run cannot prove that a newly published page is retrievable.

## 3. Branded validation versus unbranded discovery

A prompt that names the brand is expected to make the brand easier to mention. Do not let branded validation inflate unbranded category visibility.

Classify every prompt:

- `unbranded-discovery` — category, problem, recommendation, best-for, vendor, or use-case prompt without the target entity;
- `comparison` — target versus named competitor or alternative;
- `branded-validation` — asks what the target is, whether it is legitimate, its price, features, reviews, or facts;
- `narrative-correction` — tests a known stale, disputed, or inaccurate claim;
- `support` — troubleshooting or existing-customer use.

Use `branded-validation` primarily for factual accuracy, entity recognition, and narrative drift. Compute unbranded mention or recommendation rates only from eligible unbranded cells.

## 4. Query libraries by market

For each target market, build native prompts across:

- recommendation;
- comparison;
- alternatives;
- pricing and procurement;
- risk, safety, trust, and drawbacks;
- brand validation;
- use case and scenario;
- troubleshooting and support where relevant.

Do not translate one query library mechanically. Use the language, product vocabulary, units, currency, regulation, buying process, and constraints of that market.

Maintain separate:

- prompt portfolio;
- competitor set;
- source-chain map;
- canonical pages or localized assets;
- business-value weights;
- metrics and denominators.

Cross-market totals are usually uninterpretable. Compare markets only after normalizing the question, sampling condition, and business meaning.

## 5. Native-language and regional implementation

When a business targets multiple regions:

- use stable language or region URLs when an owned site exists;
- implement correct canonical and `hreflang` relationships;
- keep translated pages indexable and internally discoverable;
- use native-language editing rather than raw machine translation for important pages;
- localize units, currencies, availability, legal disclaimers, contact details, examples, and conversion paths;
- use current local profiles, maps, merchants, directories, review systems, and feeds where the vertical depends on them;
- preserve one entity identity while allowing legitimate regional offers and names.

A localized page is not complete merely because the words were translated.

## 6. Platform ecosystems are empirical, not universal

Some markets and products retrieve disproportionately from platform-native ecosystems, publisher networks, review sites, marketplaces, maps, forums, social content, video, or list sites. Other engines draw more broadly from conventional web search.

Determine source priority from the target condition:

1. run the relevant prompt portfolio;
2. record recurring cited or retrieved domains and source types;
3. separate web and app observations;
4. identify whether sources cluster inside a platform owner’s ecosystem;
5. compare competitor presence and factual quality;
6. pursue only legitimate inclusion paths that help the source’s audience.

GeoLook’s referenced CN-GEO snapshot is a useful bounded example: it reports strong platform and terminal differences in one Chinese citation dataset. Treat that as evidence that ecosystem effects can be large—not as a permanent ranking table or a reason to buy placements on listed domains. Re-run current source recon for the actual category and surface.

## 7. Source-chain actions by region

Potential source classes include:

- owned canonical pages and documentation;
- government, regulatory, academic, and standards sources;
- news and industry publishers;
- comparison, review, marketplace, and directory platforms;
- maps, business profiles, booking systems, and merchant feeds;
- GitHub, package registries, API documentation, and technical communities;
- Reddit, forums, Q&A, social platforms, and video;
- platform-native publishing ecosystems.

For every action, verify:

- the source actually recurs for the target condition;
- the brand or asset qualifies for inclusion;
- disclosure, conflict-of-interest, and editorial rules;
- the contribution is useful without a promotional link;
- the source can represent the facts accurately;
- success and stop rules are defined.

No region justifies fake reviews, paid-undisclosed lists, astroturfing, account farms, or copied articles.

## 8. No-owned-site mode

A business can have meaningful organic and AI discovery without an owned website.

Choose the actual controlled surface:

- marketplace or retailer product page;
- app store listing;
- Google Business Profile, Bing Places, Apple Business Connect, or regional map profile;
- GitHub repository or package registry;
- booking, ticketing, directory, or portfolio profile;
- publisher, association, or institutional page.

Then:

1. build the canonical fact card;
2. mark website-only checks `not-applicable`;
3. audit the controlled surface’s indexing, content, data fields, media, reviews, and conversion path;
4. map independent sources that recur in answers;
5. correct official records and earn audience-useful third-party coverage;
6. measure referral and conversion on the available surface.

Do not recommend building a new site unless it solves a demonstrated ownership, conversion, data-control, or eligibility gap.

## 9. Sampling matrix

Use a matrix rather than one global run:

| Prompt ID | Query class | Engine | Product/mode | Terminal | Country | Locale/language | Account/personalization | Sample method | Valid runs | Notes |
|---|---|---|---|---|---|---|---|---|---:|---|

Prioritize cells by business value. Do not multiply every prompt across every possible surface without a decision need.

## 10. Reporting and pooling rules

Report separately by:

- platform and product mode;
- API versus consumer product;
- web versus app or SERP;
- market, country, locale, and language;
- branded versus unbranded query class;
- new versus continued conversation;
- first-party actual, manual sample, and third-party tracker.

A roll-up MAY be shown for executive readability only when:

- component metrics remain visible;
- weights have a documented business basis;
- missing or inapplicable cells are not converted to zero;
- the roll-up is labeled a reporting index, not a platform ranking score.

## Definition of done

The adapter work is complete when:

- every observation has a fully specified surface identity;
- API, web, app, Search, assistant, and training-knowledge results are not conflated;
- branded validation is separated from unbranded discovery;
- prompt libraries, competitors, sources, and metrics are market-specific;
- regional source priorities come from current target-condition evidence;
- website-only checks are `not-applicable` for businesses without an owned site;
- any executive roll-up preserves the underlying platform and market results.
