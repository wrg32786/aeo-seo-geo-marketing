# Source Register

**Research cutoff:** 2026-08-22  
**Purpose:** provenance, conflict resolution, and update tracking for the Organic Discovery skill.

This register is not a decorative bibliography. Before relying on a tactic, identify what the source actually establishes, what it does not establish, and whether a newer platform document supersedes it.

## Source classes

| Class | Meaning | Default use |
|---|---|---|
| O | Official platform specification, policy, product documentation, or announcement | Governs platform controls and compliance |
| A | Peer-reviewed or strong controlled evidence in a live or causally relevant setting | Supports bounded causal claims |
| B | Repeated observational evidence from live systems | Prioritization and hypothesis generation |
| C | Controlled fixed-context, post-retrieval, benchmark, or RAG evidence | Content-selection or absorption experiments only |
| D | Correlational industry study | Recon and prioritization, never causation |
| F | Practitioner or community field report | Discover tactics, failure modes, and terminology |
| X | Proposal, informal protocol, or emerging implementation | Optional experiment with named consumer and owner |

## Agent Skills standard

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | O | `SKILL.md` frontmatter, folder naming, progressive disclosure, optional scripts/references/assets, validation expectations | Any SEO or GEO tactic | 2026-08-22 |
| [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) | O | Concise runtime instructions, modular references, deterministic templates, practical validation | Search-engine behavior | 2026-08-22 |
| [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) | O | Activation-focused descriptions and trigger evaluation | Ranking or citation lift | 2026-08-22 |
| [OpenAI Codex skills guide](https://developers.openai.com/codex/build-skills) | O | OpenAI implementation of the Agent Skills standard | Search visibility | 2026-08-22 |
| [OpenAI API skills guide](https://developers.openai.com/api/docs/guides/tools-skills) | O | Progressive disclosure and skill packaging in OpenAI tooling | Search visibility | 2026-08-22 |

## Google Search and generative AI features

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [Optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | O | Core SEO remains the foundation; Search index and quality systems matter; unique non-commodity people-first content; Merchant Center and Business Profiles; Search Console measurement; Google Search ignores `llms.txt` and does not require special chunking or manufactured mentions | A guaranteed ranking, citation, or universal rule for non-Google engines | 2026-08-22 |
| [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) | O | Normal technical eligibility and preview controls apply to AI Overviews and AI Mode | That eligibility produces inclusion | 2026-08-22 |
| [People-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | O | First-hand expertise, clear authorship, reliable sourcing, substantive updates, and people-first intent | A fixed E-E-A-T score or citation formula | 2026-08-22 |
| [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | O | Prohibitions on scaled abuse, link spam, cloaking, site-reputation abuse, misleading functionality, and other manipulation | That compliant content will rank | 2026-08-22 |
| [Structured data introduction](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | O | Supported JSON-LD can aid understanding and rich-result eligibility; markup must match visible content | A direct AI-citation boost | 2026-08-22 |
| [Robots.txt introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro) | O | Crawl directives and their limits | Deindexing through crawl blocking | 2026-08-22 |
| [Block indexing with `noindex`](https://developers.google.com/search/docs/crawling-indexing/block-indexing) | O | Correct use of `noindex`; crawler needs access to observe it | Immediate removal from every cache or external system | 2026-08-22 |
| [Snippet and preview controls](https://developers.google.com/search/docs/appearance/snippet) | O | `nosnippet`, `max-snippet`, and `data-nosnippet` controls | Inclusion or ranking gains | 2026-08-22 |
| [Sitemaps overview](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview) | O | Discovery hints and canonical URL inventory | Crawl, index, or rank guarantees | 2026-08-22 |
| [Common crawlers](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers) | O | Current Google crawler identities and verification paths | That a user-agent string alone is authentic | 2026-08-22 |
| [Google-Extended](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers#google-extended) | O | Separate control for Gemini model improvement/grounding uses; not a Google Search inclusion or ranking control | Control over Googlebot or Search AI features | 2026-08-22 |
| [Succeeding in AI search](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) | O | Accessible/indexable content, preview controls, visible-data/schema agreement, multimodal support | A separate GEO ranking system | 2026-08-22 |

## Bing, Copilot, and IndexNow

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [AI Performance in Bing Webmaster Tools](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) | O | Citation, cited-page, grounding-query, and trend reporting for Microsoft AI experiences | A complete cross-platform view or causal attribution | 2026-08-22 |
| [Optimizing content for AI search answers](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers) | O | SEO foundation, clear modular HTML, evidence, freshness, title/H1 alignment, and content accessibility | Guaranteed Bing/Copilot inclusion | 2026-08-22 |
| [Bing `data-nosnippet` support](https://blogs.bing.com/webmaster/October-2025/Bing-Introduces-Support-for-the-data-nosnippet-HTML-Attribute) | O | Selective exclusion of visible page regions from snippets and AI answers | Rank improvement | 2026-08-22 |
| [IndexNow](https://www.indexnow.org/) and [protocol documentation](https://www.indexnow.org/documentation) | O | Fast notification of URL additions, updates, and deletions to participating engines | Crawl, index, citation, or ranking guarantee | 2026-08-22 |

## OpenAI / ChatGPT Search

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [OpenAI crawler overview](https://developers.openai.com/api/docs/bots) | O | `OAI-SearchBot` for search visibility, `GPTBot` for training, `ChatGPT-User` for user-triggered visits; published IP ranges; separate controls | That allowance guarantees retrieval or citation | 2026-08-22 |
| [Publishers and developers FAQ](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq) | O | Public-site inclusion basics, crawl/snippet controls, referral attribution, and `noindex` behavior | A page-level citation formula | 2026-08-22 |
| [Product discovery in ChatGPT](https://openai.com/chatgpt/search-product-discovery/) | O | Optional product-feed controls can improve product-data freshness and accuracy | Organic recommendation, placement, or sales guarantees | 2026-08-22 |

## Anthropic / Claude

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [Anthropic web-crawler controls](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) | O | `Claude-SearchBot` for web search, `Claude-User` for user-directed fetches, `ClaudeBot` for training-related crawling; robots controls | That `ClaudeBot` controls Claude search citations | 2026-08-22 |

## Perplexity

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [Perplexity crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers) | O | `PerplexityBot` for search/linking and `Perplexity-User` for user-requested fetching; official IP ranges | Citation, rank, or recommendation guarantees | 2026-08-22 |

## Reddit policy and community operation

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [Reddit spam policy](https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam) | O | Repeated or unsolicited mass engagement, deceptive behavior, and spam are prohibited | That any allowed link gains search or AI visibility | 2026-08-22 |
| [Keeping spam out of a community](https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community) | O | Community-level enforcement and anti-spam expectations | Uniform rules across subreddits | 2026-08-22 |
| [Growing your community](https://support.reddithelp.com/hc/en-us/articles/15484256976148-Growing-your-community) | O | Relevant, authentic participation and community-specific norms | Permission for undisclosed promotion | 2026-08-22 |

## Academic GEO and answer-source research

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [Critical survey of GEO, 2023–2026](https://arxiv.org/abs/2607.14035) | A/B synthesis | Multistage model; stochasticity; evidence hierarchy; retrieval and context position as recurring levers; citation rewrites can harm retrieval; no reviewed universal longitudinal cross-platform causal tactic for organic discovery or business behavior | That no tactic can ever work, or that all engines behave identically | 2026-08-22 |
| [Foundational GEO paper](https://arxiv.org/abs/2311.09735) | C | In fixed-context experiments, content transformations can change visibility/citation metrics after source inclusion | Organic crawl, retrieval, durable rank, traffic, or conversion lift | 2026-08-22 |
| [Citation selection and absorption framework](https://arxiv.org/html/2604.25707v2) | A/C | Citation selection and answer absorption are distinct outcomes requiring separate metrics | Universal engine behavior outside the evaluated conditions | 2026-08-22 |
| [SAGEO end-to-end evaluation](https://arxiv.org/html/2602.12187v2) | A/C | Need to evaluate retrieval, citation, and downstream answer effects together | Guaranteed transfer to every commercial engine | 2026-08-22 |
| [MAGEO reusable strategy optimization](https://arxiv.org/html/2604.19516v1) | C/X | Engine- and task-specific strategies, reusable memory, and fidelity-aware testing | A stable public ranking recipe | 2026-08-22 |
| [GEO governance and ecosystem risks](https://arxiv.org/abs/2606.12439) | A | Manipulation, distributional, governance, and disclosure risks | Specific rank factors | 2026-08-22 |

## Industry observational research

These sources are useful because they observe commercial engines at scale. They remain vendor-produced, compositional, and usually non-causal.

| Source | Class | Supports | Does not prove | Checked |
|---|---:|---|---|---|
| [Why ChatGPT cites pages](https://ahrefs.com/blog/why-chatgpt-cites-pages/) | B/D | Large-sample source-pattern recon; search-grounded source selection; title/query relevance; source-type composition including Reddit | Causal effect of any isolated page edit | 2026-08-22 |
| [Self-promotional AI SEO experiment](https://ahrefs.com/blog/self-promotional-content-ai-seo-experiment/) | A/B | Direct self-promotion can sometimes change mentions; citations and recommendations can diverge; established brands may depend more on third-party sources; intermittent results | That promotional pages reliably improve recommendations or traffic | 2026-08-22 |
| [Schema and AI citations study](https://ahrefs.com/blog/schema-ai-citations/) | B | Matched observational evidence found little or no clear citation lift from schema alone | That schema is useless for understanding or rich-result eligibility | 2026-08-22 |
| [`llms.txt` usage study](https://ahrefs.com/blog/llmstxt-study/) | B | Most observed `llms.txt` files showed little crawler consumption; format is not a robots directive | That no named agent, documentation tool, or future consumer can use it | 2026-08-22 |
| [AI Overview brand correlations](https://ahrefs.com/blog/ai-overview-brand-correlation/) | D | Candidate brand-presence signals worth testing | Causation or a prescription to manufacture mentions | 2026-08-22 |
| [AI brand visibility correlations](https://ahrefs.com/blog/ai-brand-visibility-correlations/) | D | Cross-web presence and visibility associations | That buying or spamming mentions causes visibility | 2026-08-22 |

## GitHub implementation recon

| Repository | Class | Useful material | Important correction or limit | Checked |
|---|---:|---|---|---|
| [Auriti-Labs/geo-optimizer-skill](https://github.com/Auriti-Labs/geo-optimizer-skill) | F/X | Broad audit surface, CLI ideas, logs, bot tests, reports, MCP packaging, citation monitoring | Its score overweights speculative files and custom AI endpoints; its published skill has historically conflated some search/training crawlers; fixed “impact” numbers should not be generalized | 2026-08-22 |
| [coreyhaines31/marketingskills AI SEO](https://github.com/coreyhaines31/marketingskills/blob/main/skills/ai-seo/SKILL.md) | F | Activation language, marketer-oriented workflow, cross-engine surface inventory | Practitioner doctrine, not platform specification or causal evidence | 2026-08-22 |
| [SNLabat/SEO-GEO-AEO-Skill](https://github.com/SNLabat/SEO-GEO-AEO-Skill) | F | Compact audit structure and report packaging | Uses generic category scoring; category scores must not substitute for stage evidence | 2026-08-22 |
| [rampstackco/claude-skills GEO skill](https://github.com/rampstackco/claude-skills/blob/main/skills/seo-aeo-geo/SKILL.md) | F | Trigger coverage and implementation prompts | Must be reconciled against current official crawler controls | 2026-08-22 |
| [AgricIDaniel/claude-seo](https://github.com/AgricIDaniel/claude-seo) | F | Modular orchestration and vertical detection | Tooling depth does not establish tactic effectiveness | 2026-08-22 |
| [AnswerDotAI/llms-txt](https://github.com/AnswerDotAI/llms-txt) | X | Informal `llms.txt` proposal for agent/documentation context | Not a Google Search requirement or universal crawler standard | 2026-08-22 |
| [Wu-beining/MAGEO](https://github.com/Wu-beining/MAGEO) | C/X | Research implementation for reusable GEO strategy optimization | Research code is not a production ranking oracle | 2026-08-22 |
| [danishashko/geo-aeo-tracker](https://github.com/danishashko/geo-aeo-tracker) | F | Cross-engine prompt hub, country segmentation, raw answer/citation capture, grounding-query and SERP joins, competitor citation gaps, scheduled historical tracking | Its SRO/visibility scores are heuristics, not platform ranking models | 2026-08-22 |
| [onvoyage-ai/gtm-engineer-skills](https://github.com/onvoyage-ai/gtm-engineer-skills) | F | Prompt taxonomy, Reddit language mining, strict artifact contracts, deterministic audit versus LLM judgment, source-opportunity workflow | Several fixed citation multipliers, mandatory `llms.txt`, and “one mention can trigger citation” claims are not universal rules | 2026-08-22 |
| [indranilbanerjee/digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro) | F | Fact/claim governance, canonical AEO audit, narrative drift, recurring monitoring, first-party reconciliation, acceptance gates, multi-platform packaging | Plugin-specific scores and surface assumptions must be revalidated against current first-party docs | 2026-08-22 |
| [aigclink/geolook](https://github.com/aigclink/geolook) | F/B | Claim-block operating unit, evidence-grade fact cards, API/web/app isolation, no-site mode, market-specific source maps, attribution discipline, acceptance work orders | Fixed content thresholds and market source rankings are bounded to their cited datasets/surfaces and should not be universalized | 2026-08-22 |

## Reddit field recon

Reddit is evidence of practitioner beliefs, observed source behavior, community rules, and failure modes—not a ranking specification. Validate every tactic independently.

| Thread | Class | Useful signal | Limit | Checked |
|---|---:|---|---|---|
| [Understanding AEO/GEO](https://www.reddit.com/r/SEO/comments/1tbik3o/understanding_aeogeo/) | F | Current practitioner vocabulary, source-overlap discussion, and skepticism | Claims and percentages may be second-hand or selectively cited | 2026-08-22 |
| [What signals are you actually measuring?](https://www.reddit.com/r/bigseo/comments/1vfh7h7/what_signals_are_you_actually_measuring_for/) | F | Intent coverage, recommendation share, framing, dependency, stability, and gap mapping | Community recommendations are not validated standards | 2026-08-22 |
| [74k AI citations and Reddit](https://www.reddit.com/r/aeo/comments/1u0g4am/had_74k_ai_citations_sitting_in_my_logs_reddit/) | F | Example dataset suggesting Reddit contribution varied sharply by engine | One tracker sample; no universal source-share conclusion | 2026-08-22 |
| [Local SEO and Reddit](https://www.reddit.com/r/localseo/comments/1pdroyd/local_seo_and_reddit/) | F | Help-first participation and local/community relevance | No proof that Reddit links create local or AI rank | 2026-08-22 |
| [Prompt tracking can mislead](https://www.reddit.com/r/SEO/comments/1q8j251/ai_prompt_tracking_can_fool_you_into_thinking/) | F | Search state, listicle dependence, and volatility can distort “visibility” dashboards | Anecdotal example, not population estimate | 2026-08-22 |
| [AEO agency skepticism](https://www.reddit.com/r/SEO/comments/1ulu7h5/spent_4200_on_an_aeo_agency_for_a_pool_business/) | F | Common failure mode: selling opaque scores and generic schema instead of tracing sources | Individual experience and discussion | 2026-08-22 |
| [Sustainably growing brand mentions](https://www.reddit.com/r/AISEOforBeginners/comments/1tthdno/how_do_you_sustainably_grow_brand_mentions_for_ai/) | F | “Citation supply chain” as a practical recon heuristic | Community self-promotion rules and possible vendor bias | 2026-08-22 |

## Conflict-resolution rules

1. Current official platform documentation overrides tools, repositories, vendor studies, and community advice for crawler, indexing, preview, feed, and product controls.
2. A fixed-context benchmark may justify a post-retrieval content experiment; it does not justify an organic-ranking promise.
3. Correlations identify places to investigate. They never justify manufactured mentions, links, reviews, or dates.
4. A tactic observed on one engine, mode, locale, vertical, or date remains platform-specific until replicated.
5. A tactic is promoted from `EARNED` only when the target query family and target platform show a repeatable need and the change survives retrieval, citation, fidelity, and business checks.
6. When sources conflict, record the conflict, verification date, affected platform, and chosen behavior in the audit rather than silently averaging them.

## Maintenance procedure

At least quarterly—or immediately after a platform crawler, Search Console, Webmaster Tools, feed, schema, or policy update:

1. re-open every official source relevant to the changed platform;
2. update crawler names, purposes, IP-verification guidance, and controls;
3. move unsupported tactics down the evidence ladder rather than preserving legacy scores;
4. add new controlled studies with their exact experimental boundary;
5. run the trigger evals and validator;
6. increment the skill version and research cutoff;
7. document material doctrine changes in the repository release notes.
