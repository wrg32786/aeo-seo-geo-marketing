# Evidence and Tactic Doctrine

Use this reference before recommending an optimization tactic. Its purpose is to prevent unsupported folklore from becoming a mandatory checklist.

## 1. Evidence hierarchy

| Label | Evidence type | What it can justify | What it cannot justify |
|---|---|---|---|
| [O] | Current official platform documentation or policy | Platform controls, eligibility requirements, reporting surfaces, prohibited behavior | A guaranteed ranking or citation outcome |
| [A] | Controlled live-engine test, natural experiment, or matched control | A bounded causal or quasi-causal claim for the tested surface and period | Universal transfer to another engine, vertical, locale, or date |
| [B] | Repeated live-engine observation at useful scale | Prioritization, hypotheses, source-pattern reconnaissance | Causation |
| [C] | Fixed-context, post-retrieval, RAG, benchmark, or lab experiment | Whether content presentation can alter use after retrieval | Organic discovery, durable citation, clicks, or revenue |
| [D] | Cross-sectional correlation | Which variables deserve investigation | “Do more of X and citations will rise” |
| [F] | Practitioner, Reddit, vendor, or anecdotal report | Edge cases, operational ideas, test design | General rules |
| [X] | Emerging protocol or unverified tactic | A contained experiment with owner and rollback | A score requirement or default implementation |

### Application rules

1. Prefer the highest applicable class.
2. A tactic is **default** only when it is independently useful to people or required by an official platform.
3. A tactic is **conditional** when benefit depends on intent, page type, source chain, or platform.
4. A tactic is **experimental** when no named consuming system or reliable outcome exists.
5. A tactic is **rejected** when it is deceptive, policy-violating, unsupported, or likely to reduce trust.
6. Record the exact tested engine, mode, date, locale, query family, denominator, and outcome before promoting a local experiment into reusable strategy memory.

## 2. How to interpret the research

### Foundational GEO paper

The 2023/2024 GEO paper showed that edits such as adding relevant citations, quotations, and statistics could improve source visibility in its benchmark, with reported relative gains up to roughly 40 percent. The crucial limitation is that the source was already present in a fixed or supplied context. The study established that presentation can change downstream use; it did not establish durable organic retrieval, universal ranking lift, or traffic.

Use it to generate **[C] hypotheses**, not fixed impact promises. Never reproduce its techniques by inventing evidence.

### 2026 critical survey

The survey of 45 studies models GEO as a pipeline rather than one ranking task. Its strongest practical conclusions are:

- topical relevance and context position are more reproducible than generic formatting recipes;
- citation, absorption, fidelity, and behavior are different outcomes;
- engine and run variance are substantial;
- citation-oriented rewriting can harm retrieval in end-to-end settings;
- no reviewed tactic demonstrated stable, longitudinal, cross-platform causal lift in organic discoverability and downstream behavior.

The operating implication is simple: diagnose and test each stage. Do not award a page a single “AI-ready” score and declare success.

### Later controlled work

- Citation-absorption research supports measuring whether a cited page actually contributes claims or evidence, not only whether its URL appears.
- Competitive RAG and ranking studies repeatedly find query-document relevance and context position important; fresh timestamps or prices may help when materially relevant.
- Structure can help extraction in some environments, but fixed recipes and formatting-only edits generalize poorly.
- Multi-agent GEO research supports engine-specific strategy memory only after controlled validation and fidelity checks.

These findings are useful for experiment design. They do not override live platform policies or prove organic traffic impact.

## 3. Tactic registry

### Default: useful even without an AI-citation effect

| Tactic | Evidence | Main stages | Guardrail |
|---|---|---|---|
| Make the page crawlable, renderable, indexable, canonical, and snippet-eligible | [O] | Eligibility, retrieval | Eligibility never guarantees serving |
| Create unique, people-first, non-commodity content | [O] | Retrieval through behavior | “Unique” must be substantively useful, not merely differently worded |
| Align page purpose, title, H1, introduction, headings, and body | [O]/[B] | Retrieval, selection | Avoid exact-match stuffing and page-per-query fan-out |
| Provide first-hand evidence, original data, demonstrations, or primary documentation | [O]/[B] | Retrieval, selection, absorption | Publish methodology, scope, limitations, and dates |
| State precise entities, units, versions, prices, dates, and applicability conditions | [O]/[C] | Retrieval, absorption, fidelity | Only where relevant and maintained |
| Cite primary sources near supported claims | [O]/[C] | Trust, absorption, fidelity | Sources must actually support the claim |
| Use clear semantic HTML and accessible interaction patterns | [O] | Eligibility, agent use | Accessibility is not an optional GEO hack |
| Maintain internal links, canonical ownership, breadcrumbs, and sitemaps | [O] | Discovery, retrieval | Sitemaps are hints; avoid internal-link spam |
| Keep source systems, visible content, schema, profiles, and feeds consistent | [O] | Eligibility, fidelity | Establish one data owner |
| Use supported structured data that matches visible content | [O] | Understanding, rich results | Do not claim a direct AI-citation boost |
| Instrument referrals, citations, recommendations, and conversions separately | [O]/research | Behavior, measurement | Preserve denominators and zero-result runs |

### Conditional: use when intent or evidence warrants it

| Tactic | Evidence | Trigger | Failure mode |
|---|---|---|---|
| Answer or summary near the beginning | [O]/[C] | User needs a direct answer before detail | Oversimplifies nuance or becomes generic boilerplate |
| Question headings and FAQs | [O]/[C] | Users genuinely ask separable questions | Repetitive keyword pages or invented FAQs |
| Lists and tables | [O]/[C] | Comparison, procedure, specification, eligibility, or decision criteria | Formatting without useful facts |
| Comparison and alternatives pages | [B]/[F] | Commercial prompts and source map show comparison sources | Self-serving claims, competitor misinformation, legal risk |
| Author/reviewer pages and credentials | [O] | Expertise or accountability matters | Decorative biographies unrelated to the claim |
| Frequent updates | [O]/[B] | Facts, availability, price, regulation, or news change | Fake freshness and date churn |
| Video, images, diagrams, and transcripts | [O] | Visual proof, demonstrations, products, locations, procedures | Key information exists only in media |
| Original benchmarks, calculators, datasets, or tools | [B]/[F] | Audience has a recurring decision or calculation | Thin lead magnets without methodology |
| Earned third-party mentions or links | [D]/[F] | Target source chain relies on external corroboration | Manufacturing mentions or confusing correlation with causation |
| Reddit/community participation | [B]/[F] | The platform appears in the actual source chain and community fit is real | Spam, bans, negative sentiment, negligible citation on the target engine |
| IndexNow | [O] | Bing/participating-engine freshness matters | Treated as ranking submission rather than change notification |
| Product/local/publisher feeds and profiles | [O] | Vertical and platform support them | Stale or conflicting data |

### Experimental: never a blocker by default

| Tactic | Evidence | Allowed use | Required control |
|---|---|---|---|
| `llms.txt` | [X]/[B] | Documentation or agent navigation for a named consumer | Version control, request-log monitoring, security review, maintenance owner |
| Markdown page alternates | [X] | Documentation systems known to consume them | Canonical strategy and parity checks |
| AI manifests or custom `/ai/*.json` endpoints | [X] | Named integration with a documented contract | Schema owner, versioning, authentication if needed |
| Fixed “answer capsule” word counts | [C]/[F] | A/B test for a specific surface | Human readability and full-chain measurement |
| Engine-specific stylistic rewrites | [C] | Controlled twin-branch test | Fidelity gate and rollback |
| Self-promotional listicles | [A]/[F] | Small disclosed experiment where source gap is documented | Recommendation-backfire measurement and maintenance tax |

### Rejected

- Keyword stuffing, entity stuffing, and repetitive query variants.
- Fabricated statistics, quotes, reviews, experts, awards, users, or test results.
- Fake `dateModified`, false urgency, stale prices, or unsupported superlatives.
- Hidden text, white-on-white text, tiny text, invisible Unicode, HTML-comment instructions, or prompt injection.
- Cloaking or serving materially different claims to bots and people.
- Fake FAQ or review schema; schema for content users cannot see.
- Mass AI-generated pages with no distinct audience value.
- Site reputation abuse, parasite SEO, doorway pages, expired-domain exploitation, or third-party pages published chiefly to borrow host authority.
- Reddit astroturfing, bought accounts, coordinated votes, duplicate posts, undisclosed affiliation, or “helpful” comments whose real purpose is a link.
- Repeatedly prompting a model in an attempt to “train” it on a brand.
- Adding every known AI bot to an allowlist without a policy decision and IP verification.
- Treating a one-run answer or one vendor score as proof of visibility.

## 4. Content transformation patterns

Choose patterns by user job, not by a universal GEO template.

### Definition/reference

Use when the page should define a concept or entity.

- definition or identity near the top;
- scope and exclusions;
- named properties/components;
- examples and non-examples;
- primary references;
- last-reviewed information when time-sensitive.

### Procedure/how-to

- explicit outcome and prerequisites;
- numbered steps;
- verification after major steps;
- edge cases and failure modes;
- expected output;
- relevant safety or rollback notes.

### Comparison/evaluation

- disclose methodology and commercial relationship;
- compare all options on the same dimensions;
- distinguish facts, tests, opinions, and estimates;
- include limitations and who should not choose each option;
- date volatile facts such as price and availability;
- link to primary sources.

### Product/service

- state exactly what it is, for whom, and what it does;
- expose price, availability, requirements, geography, model/version, and support facts where relevant;
- show primary proof: demos, specifications, cases, benchmarks, documentation;
- explain meaningful limitations;
- keep merchant/profile/schema data consistent with visible content.

### Original research/data page

- research question;
- methodology;
- population/sample/time period;
- definitions;
- findings with units and confidence/limitations where applicable;
- downloadable or inspectable data when possible;
- citation guidance and contact/maintainer.

### Local service

- exact service and geography;
- evidence of real local operation;
- hours, phone, address/service area, appointment path;
- qualifications/licenses only when verifiable;
- prices/ranges only when accurate;
- Business Profile and directory consistency.

## 5. Claim discipline

For every number or objective claim, answer:

1. What exactly is being claimed?
2. Who or what does it apply to?
3. What date/version does it describe?
4. What source supports it?
5. Does the source support this exact wording?
6. Is the fact still current?
7. Is it visible to humans, not merely schema or hidden markup?

If the source is missing, downgrade the wording or remove the claim.

## 6. What counts as “fresh”

Freshness is not “change the date.” Classify facts:

- **Evergreen** — definition, stable procedure, historical fact: review periodically but do not churn dates.
- **Slow-changing** — product capability, team, policy: event-driven plus scheduled review.
- **Fast-changing** — price, inventory, regulation, versions, rankings, availability, news: explicit owner and refresh SLA.

Use a truthful `dateModified` only when the visible page materially changed.

## 7. What counts as authority

Do not reduce authority to Domain Rating or a backlink count. Examine:

- first-hand experience or primary responsibility;
- identifiable expertise and accountability;
- direct access to the facts being discussed;
- transparent methodology;
- independent corroboration;
- source reputation for the specific topic;
- consistency across time and surfaces;
- corrections policy and maintenance.

A small primary source may be better evidence than a large aggregator.

## 8. Page-vs-site decisions

Do not try to make every page answer every question.

Create a new page only when there is a distinct user job, durable information need, and meaningful content that should have its own canonical URL. Otherwise:

- expand the existing owner page;
- merge overlaps;
- redirect obsolete pages;
- use anchors/internal links;
- keep a single canonical answer where duplication would create retrieval ambiguity.
