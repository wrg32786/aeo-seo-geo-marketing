# Question-First Playbook

Use this module when the job is "get this site, page, repo or tool found and cited for the questions people actually ask." It is the end-to-end run order. Each step points to the module that holds the detail.

The playbook is the practical layer on top of the eight-stage model in `SKILL.md`. It does not replace Business Truth validation, exact-surface shelf mapping or the hard wedge gates. When a step below makes a public claim, run the fact validator first.

## The short version

1. Audit what exists and record a baseline.
2. Find the real questions people ask, and pick narrow ones first.
3. Rewrite the owner page so each answer opens with one direct sentence, followed by a FAQ and an honest evidence and limits section.
4. Add structured data only where it matches visible text.
5. Write one canonical description and repeat it word for word everywhere you control.
6. Get mentioned where answer engines already look, through each venue's own rules.
7. Check whether AI answers cite you for the target questions, and keep a dated log.
8. Keep what moved, drop what did not, and repeat on the next narrow question.

## Step 1. Audit and baseline

- Run `python scripts/od.py audit <url-or-file> --output output/audit` on every page you plan to change.
- Work through `references/audit-checklist.md` for the parts the deterministic auditor cannot see: GitHub About line, topics, related repos, profiles and off-site mentions.
- Before changing anything, record the baseline in the citation log from `references/citation-checks.md`. A later "it worked" means nothing without a before.

Output: a filled checklist and a dated baseline row per target question.

## Step 2. Map the questions

- Follow `references/question-mapping.md`.
- Collect real phrasings from Search Console, autocomplete, People Also Ask, Reddit, GitHub issues, support mail and the answer engines themselves.
- Rank by fit and by how narrow the question is. "How do I stop Claude Code from losing context after compaction" is easier to win than "AI coding tools".
- Keep branded questions ("What is Organic Discovery?") in a separate list. They check accuracy. They do not prove discovery.

Output: `templates/question-map.csv` filled for 10 to 30 questions, with 3 to 5 marked as first targets.

## Step 3. Fix the owner page

- One question family gets one canonical owner page. Do not create a page per paraphrase.
- Use `references/page-templates.md` and the files in `templates/`.
- Every section that answers a question opens with one plain sentence that answers it. Detail comes after.
- Add a FAQ written in the words people type into ChatGPT, Perplexity and Google.
- Add an evidence and limits section. Say what was tested, on what, and what was not shown.
- For tools, add a one-line install, a "what this changes on your machine" section and a neutral alternatives section.
- Write in a plain human voice. No em dashes or en dashes, no superlatives, no hype. Several communities and moderators filter text that reads as machine-written, and readers skip it.

Output: a reviewable branch or draft, not a live publish.

## Step 4. Structured data

- On web pages, add `FAQPage` JSON-LD only for a FAQ that is visible on the page, and `SoftwareApplication` JSON-LD for a tool page. Templates: `templates/jsonld/`.
- GitHub READMEs cannot carry JSON-LD. Put the markup on the project's own site, if it has one.
- Treat structured data as a description of the page, not a ranking lever. See the evidence notes below.

## Step 5. Entity consistency

- Follow `references/entity-consistency-kit.md`.
- Write one canonical description (one sentence, plus a short form under 120 characters) and paste it identically into the GitHub About line, the site, the author profile, package registries and every related repo that links here.

## Step 6. Distribution

- Follow `references/distribution-playbook.md`.
- Venues: Reddit (by each subreddit's own rules), curated awesome-lists (through their own contribution process), Hacker News (Show HN only for something people can run), dev.to and Medium with a canonical URL pointing home, and GitHub topics matched to terms people search.
- Every public post is drafted by the agent and published by a human. Disclose affiliation every time.

## Step 7. Measure

- Follow `references/citation-checks.md`.
- Ask each target question on each engine you care about, the same way each time, and log whether you were cited, mentioned, linked, and described accurately.
- Pair that with first-party data: GitHub traffic and referrers, Search Console, analytics referrers such as `chatgpt.com` and `perplexity.ai`.

## Step 8. Decide and repeat

Use the learning decision from `SKILL.md`: keep, iterate, expand, stop or roll back. Expand from a narrow question you now win to the next nearby question. Do not jump to a broad head term until several narrow ones hold.

## Evidence notes for this playbook

These notes explain why the playbook is shaped this way. Labels follow `references/evidence-and-tactics.md`. Checked 2026-10-11.

- **Google AI Overviews and AI Mode use normal Search eligibility.** Google says a page must be indexed and eligible to show with a snippet, and that there are no extra technical requirements, no special schema and no AI text files needed. [O] [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- **Google stopped showing FAQ rich results on May 7, 2026** and removed the documentation in June 2026. `FAQPage` remains a valid schema.org type. Keep a FAQ because people read it, and keep the markup only where it matches the visible FAQ. Do not promise a Google rich result. [O] [Google Search Central documentation updates](https://developers.google.com/search/updates)
- **Google says llms.txt is not used by Google Search** and neither helps nor hurts there; it is fine to keep for other systems. [O] [Google Search Central documentation updates, June 15, 2026](https://developers.google.com/search/updates). Ahrefs reported that 97% of the llms.txt files it observed received no requests in May 2026. [B] [Ahrefs llms.txt study](https://ahrefs.com/blog/llmstxt-study/). That is why the playbook treats llms.txt as housekeeping.
- **ChatGPT search depends on OAI-SearchBot access.** OpenAI says sites opted out of OAI-SearchBot will not be shown in ChatGPT search answers, and that robots.txt changes take about 24 hours to apply. [O] [OpenAI crawlers overview](https://developers.openai.com/api/docs/bots)
- **Q&A formatting alone is not enough.** A 2026 measurement paper on 602 prompts across ChatGPT, Google AI Overview/Gemini and Perplexity found that Q&A formatting by itself did not improve how much a cited page contributed to the answer; pages with definitions, numbers, comparisons and steps contributed more. [B] [Citation selection to citation absorption, arXiv 2604.25707](https://arxiv.org/abs/2604.25707). The direct-answer opener is useful because it states a checkable fact up front, not because of its format.
- **Reddit's role depends on the engine and moves over time.** One September 2026 study of 25,940 answers found Reddit cited in 23.5% of Google AI Overview answers and 0.1% of ChatGPT answers. [B, vendor study] [Suff Digital Reddit citation study](https://www.suffdigital.com/resources/data-studies/reddit-citations-ai-answers). Another panel reported Reddit's citation share falling between July and September 2026, most sharply in ChatGPT and Perplexity. [B, vendor study] [LLM Authority Index](https://llmauthorityindex.com/resources/research/reddit-ai-citation-decline-july-september-2026-high-stakes-consumer-decisions). A 2026 review of 30 such studies found most of the disagreement comes from different denominators and prompt sets. [B] [Who Does AI Cite? (Zenodo preprint)](https://exa.ai/library/publication/fz21hnjwf4g). Treat any single Reddit percentage as bounded to its study.
- **Freshness.** Ahrefs reported that AI assistants cited pages that were on average newer than pages in Google's organic results, with ChatGPT showing the strongest preference and AI Overviews the weakest. [B/D, observational] [Ahrefs freshness study](https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/). This supports keeping facts current. It does not support changing dates without changing content.
- **Answers vary between runs.** A SIGIR 2026 study found AI Overviews less consistent across two runs of the same query and across small query edits than classic results. [B] [How Generative AI Disrupts Search, SIGIR 2026](https://dl.acm.org/doi/10.1145/3805712.3809667). That is why citation checks repeat each question and log every run, including misses.

Uncertain and not claimed here: whether a direct-answer opener, a FAQ, an awesome-list entry or a Reddit thread causes a citation on any given engine. The playbook treats each as a bounded experiment and measures it.
