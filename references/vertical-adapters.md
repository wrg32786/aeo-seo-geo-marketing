# Vertical Adapters

Load the adapter that matches the business and page. These modules extend the core workflow; they do not replace technical eligibility, source verification, or measurement.

## 1. Local services and physical locations

### Truth inventory

- legal and public business name;
- physical address or service area;
- phone, booking URL, hours, holiday hours, and emergency availability;
- licenses, certifications, insurance, jurisdictions, and practitioner credentials;
- services actually offered, exclusions, pricing model, minimums, lead time, and appointment availability;
- accessibility, parking, delivery radius, languages, and payment methods where relevant.

### Owned surfaces

- location or service page with unique local proof;
- contact and booking flows;
- staff/practitioner pages;
- local case studies and service-area examples;
- Google Business Profile, Bing Places, maps, primary directories, and licensing registries;
- `LocalBusiness` subtype, `Service`, `Person`, `PostalAddress`, opening hours, and review data only when supported and visible.

### Page requirements

- Answer “what, where, who, when, how much, and how to book” in accessible HTML.
- Use actual local details, projects, photos, regulations, or customer questions—not a city-name substitution template.
- State whether the customer travels to the business or the business travels to the customer.
- Keep phone, address, hours, and service area synchronized across all controlled sources.
- Show credentials and risk limitations for regulated services.
- Link each service/location page from a sensible navigation or hub.

### Query families

- `[service] near me`;
- `[service] in [location]`;
- `best [service] for [need]`;
- emergency, same-day, weekend, licensed, insured, price, reviews, accessibility, and neighborhood queries;
- “who can solve [specific local problem]?”

### Common failures

- dozens of thin city pages;
- virtual office or false address;
- stale hours and disconnected booking inventory;
- self-authored “best in town” lists;
- review markup for reviews not visibly shown or controlled by the business;
- location facts appearing only in a map embed or image.

## 2. Ecommerce and physical products

### Truth inventory

- brand, manufacturer, GTIN/UPC/EAN, MPN, SKU, variant identifiers;
- current price, currency, sale dates, availability, condition, minimum quantity;
- dimensions, materials, compatibility, included items, warranty, safety data;
- shipping cost/timing, returns, regions, taxes, subscriptions, and checkout destination;
- product claims, certifications, test methods, and review provenance.

### Owned surfaces and feeds

- product detail pages, category pages, buying guides, comparison pages, manuals, support, and returns policy;
- Merchant Center or other platform feeds;
- OpenAI product feed where currently supported and worthwhile;
- `Product`, `Offer`, `AggregateOffer`, `Review`, `MerchantReturnPolicy`, and shipping details only when accurate and visible;
- product image, video, and variant feeds.

### Page requirements

- Put identity, primary use, compatibility, price, availability, and key constraints above avoidable promotional copy.
- Provide complete specifications as HTML, not only an image or PDF.
- Explain fit, non-fit, alternatives, maintenance, warranty, and failure conditions.
- Keep variants canonicalized without hiding meaningful differences.
- Use stable identifiers across page, schema, feed, inventory, and reviews.
- Add first-hand testing or comparison methodology when making performance claims.
- Preserve crawlable product URLs even when temporarily out of stock if the product may return; state status accurately.

### Query families

- best product for a constrained use case;
- product versus competitor;
- alternative to product;
- compatible with device/system;
- price, availability, shipping, returns, warranty, dimensions, material, safety;
- troubleshooting and replacement parts.

### Common failures

- generic manufacturer copy duplicated across sellers;
- feed/page price or availability conflict;
- unsupported “best,” “safest,” “eco-friendly,” or performance claims;
- review laundering or fabricated UGC;
- hidden variant URLs, parameter traps, or faceted crawl explosion;
- self-promotional comparison pages that cite competitors but accidentally cause competitor recommendations.

## 3. SaaS, software, developer tools, and B2B services

### Truth inventory

- exact product category and jobs solved;
- supported platforms, integrations, API versions, deployment models, data regions;
- pricing units, limits, trials, contracts, onboarding, support, and cancellation;
- security, privacy, compliance, status, uptime methodology, and subprocessors;
- benchmark methods, customer eligibility, case-study evidence, and roadmap boundaries.

### Owned surfaces

- homepage and use-case pages;
- pricing and plan comparison;
- product docs, API reference, examples, changelog, status, security, trust center, and support;
- integration and migration pages;
- transparent comparison/alternatives pages;
- case studies with named scope and measurable results;
- GitHub repositories, package registries, marketplaces, and review platforms where applicable.

### Page requirements

- Define the category and primary job in plain language before slogan copy.
- Make plan limits and pricing assumptions explicit.
- Separate shipping features from roadmap or beta features.
- Expose current docs in crawlable HTML with version labels and canonical ownership.
- Provide runnable examples and expected outputs for developer queries.
- Use a changelog and deprecation policy.
- Explain security and compliance claims with scope and audit date.
- Publish comparison criteria and note material affiliations.

### Query families

- software for role/use case/company size;
- alternatives and migrations;
- product versus product;
- integration with platform;
- API example or error;
- pricing, limits, security, compliance, deployment, support, and implementation time.

### Common failures

- category ambiguity hidden behind invented language;
- gated docs or core answers;
- stale screenshots, pricing, or integration lists;
- “enterprise-grade,” “secure,” or “AI-powered” with no measurable meaning;
- benchmark claims without setup or dataset;
- dozens of nearly identical integration pages;
- comparison pages built from affiliate or sales copy rather than current primary sources.

## 4. Editorial, news, research, and publishers

### Truth inventory

- author, editor, reviewer, organization, expertise, conflicts, and contact route;
- publication date, substantive update date, correction history, and embargo;
- primary sources, interviews, datasets, documents, quotes, and rights;
- news versus analysis versus opinion classification;
- geographic and temporal scope.

### Owned surfaces

- article and topic hubs;
- author and editorial-policy pages;
- corrections, methodology, source, and AI-use policies;
- RSS/Atom, news sitemaps, image/video metadata, and publisher profiles;
- Google Preferred Sources or other publisher programs when currently eligible.

### Page requirements

- Lead with the verified development or answer, then context.
- Attribute every quote and distinguish direct observation from reported claims.
- Link primary documents and data.
- Preserve original publication and correction history.
- Add a concise “what changed” note on substantial updates.
- Avoid changing dates solely to appear fresh.
- Use headline, dek, H1, body, image caption, and structured data consistently.
- Keep sponsor and affiliate influence transparent.

### Query families

- what happened, why it matters, timeline, who said what;
- latest status, evidence, data, source document;
- explainer and background;
- comparative or investigative question.

### Common failures

- rewrites of rewrites with no original reporting;
- headline claims unsupported by the article;
- old articles relabeled as new;
- anonymous authors for accountability-sensitive material;
- quotations copied without original source;
- promotional articles designed to exploit host reputation.

## 5. Documentation, APIs, and technical knowledge bases

### Truth inventory

- supported version, release channel, runtime, operating systems, prerequisites;
- exact commands, inputs, outputs, error codes, limits, and permissions;
- deprecation date and migration route;
- source repository and issue route.

### Owned surfaces

- versioned docs and API reference;
- tutorials, concepts, how-to, troubleshooting, examples, and changelog;
- machine-readable API specifications when applicable;
- package registries and GitHub;
- optional `llms.txt` or markdown alternates only for named agent/tool consumers.

### Page requirements

- One clear task per how-to, with prerequisites and tested commands.
- Show expected output and common errors.
- Label version and “last tested” date.
- Keep code copyable and accessible.
- Link concepts to reference and reference to examples.
- Preserve old-version docs when users still need them, with clear canonical/version navigation.
- Use stable anchors and descriptive titles.

### Query families

- install, configure, authenticate, integrate, migrate;
- exact error message;
- API method, field, response, limit, example;
- version compatibility and deprecation;
- comparison and architecture.

### Common failures

- latest and old versions mixed on one page;
- generated reference with no conceptual guidance;
- examples that do not run;
- core documentation rendered only after client-side interaction;
- search indexes blocked while `llms.txt` is treated as a replacement;
- copied community answers without verification.

## 6. YMYL: health, finance, legal, safety, and civic information

### Mandatory trust controls

- Identify qualified author and reviewer.
- Prefer current primary authorities, statutes, regulators, clinical guidance, official data, or peer-reviewed research.
- State jurisdiction, population, effective date, contraindications, risks, uncertainty, and when professional help is necessary.
- Separate general education from individualized advice.
- Maintain a scheduled review and correction process.
- Require human review for material recommendations.

### Page requirements

- Use calibrated language matching evidence quality.
- Explain absolute risk and denominators, not only relative percentages.
- State assumptions for calculations and projections.
- Cite the controlling legal or regulatory text where possible.
- Avoid testimonials as proof of general efficacy.
- Do not infer diagnosis, eligibility, liability, or guaranteed outcome from incomplete facts.
- Make emergency and escalation guidance prominent when relevant.

### Common failures

- invented or outdated medical statistics;
- legal advice without jurisdiction;
- financial return projections without assumptions and risk;
- affiliate incentives hidden from readers;
- generic AI summaries that omit contraindications;
- an unqualified author bio added solely to mimic expertise.

## 7. Travel, hospitality, events, and time-sensitive inventory

### Truth inventory

- exact location, dates, seasonality, time zone, opening hours, capacity, availability;
- pricing, taxes, resort/service fees, cancellation, accessibility, age limits, pets, parking, transit;
- event schedule, speakers, venue, ticket status, and changes;
- first-hand visit/test date and disclosure.

### Page requirements

- Put dates, location, current availability, and major restrictions near the top.
- Separate evergreen destination guidance from live inventory.
- Include practical route, accessibility, weather/season, reservation, and cancellation context.
- Keep event and booking data synchronized with source systems.
- Update or archive expired event pages with clear status and successor links.

### Common failures

- evergreen copy with stale prices or hours;
- “best” lists based only on affiliates;
- stock imagery and no first-hand evidence;
- expired events still presented as bookable;
- local claims copied across destinations.

## 8. Marketplaces, directories, and user-generated content

### Truth inventory

- listing owner, verification method, category, location, availability, and last update;
- review identity, moderation, incentives, and fraud controls;
- ranking methodology and paid-placement disclosure;
- duplicate and closed-business handling.

### Page requirements

- Give each indexable page a clear user purpose and enough verified information to stand alone.
- Avoid indexing empty filters and near-duplicate combinations.
- Label sponsored, featured, and affiliate placements.
- Maintain review provenance and abuse reporting.
- Show methodology for “best,” “top,” and ranking lists.
- Use canonicalization and faceted-navigation controls deliberately.

### Common failures

- thin programmatic pages at massive scale;
- unverified listings and fake reviews;
- paid rank presented as editorial judgment;
- expired or duplicate entities;
- third-party content hosted mainly to exploit domain authority.
