# Organic Discovery: SEO, AEO and GEO Agent Skill for Claude Code and Codex

[![Validate skill](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml/badge.svg)](https://github.com/wrg32786/aeo-seo-geo-marketing/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-open%20standard-111827)](https://agentskills.io/)
[![Version](https://img.shields.io/badge/version-0.5.0-2563eb)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a)](LICENSE)

Organic Discovery is an MIT-licensed Agent Skill and Python CLI that helps you or your AI agent get a website or GitHub repo found and cited by Google, ChatGPT search and Perplexity, using checks you can verify.

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git ~/.claude/skills/organic-discovery && python3 ~/.claude/skills/organic-discovery/scripts/validate_skill.py
```

[Install](#install) · [Playbook](#the-question-first-playbook) · [Evidence and limits](#evidence-and-limits) · [What it changes](#what-this-changes-on-your-machine) · [FAQ](#faq) · [Alternatives](#alternatives) · [CLI reference](#cli-reference) · [Roadmap](docs/ROADMAP.md)

## What it does, in plain English

It covers conventional search engine optimization (**SEO**), answer engine optimization (**AEO**) and generative engine optimization (**GEO**). You point it at a page, a README or a project. The bundled CLI audits the page for crawl, index, canonical, metadata and structured-data problems and writes plain work orders. The skill then walks your agent through a question-first playbook: find the questions people actually ask, rewrite the owner page so each answer opens with a direct sentence, add a FAQ and an honest evidence and limits section, keep one description consistent everywhere, get mentioned where answer engines already look, and check whether AI answers cite you. It never gives you a single made-up "GEO score", and it never posts anywhere on its own.

It follows the chain from facts to results:

```text
business truth → access → understanding → retrieval → citation
→ source use → factual fidelity → recommendation → traffic → conversion
```

## Install

Requires Python 3.11 or newer and git. No Python packages to install.

### Claude Code

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git ~/.claude/skills/organic-discovery && python3 ~/.claude/skills/organic-discovery/scripts/validate_skill.py
```

The last line of output should start with `OK: organic-discovery validated`. A project-only install can go in `.claude/skills/organic-discovery/` inside the project instead.

### ChatGPT and Codex

Ask `$skill-installer` to install:

```text
https://github.com/wrg32786/aeo-seo-geo-marketing
```

Or install by hand:

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
cd aeo-seo-geo-marketing
python scripts/validate_skill.py
mkdir -p ~/.agents/skills
ln -s "$PWD" ~/.agents/skills/organic-discovery
```

A repository-local install can use `.agents/skills/organic-discovery/`.

## The question-first playbook

The playbook is the end-to-end run order an agent follows. Start with [`references/playbook.md`](references/playbook.md).

| Step | What happens | Module |
|---|---|---|
| 1. Audit | Run the CLI audit and work the checklist, then record a baseline | [Audit checklist](references/audit-checklist.md) |
| 2. Map questions | Collect real phrasings from search, Reddit, issues and the engines; pick narrow ones first | [Question mapping](references/question-mapping.md) |
| 3. Fix the owner page | Direct-answer opener, FAQ, evidence and limits, install, alternatives | [Page templates](references/page-templates.md), [`templates/`](templates/) |
| 4. Structured data | `FAQPage` and `SoftwareApplication` JSON-LD, only where it matches visible text | [`templates/jsonld/`](templates/jsonld/) |
| 5. Entity consistency | One description, repeated word for word on every surface | [Entity kit](references/entity-consistency-kit.md) |
| 6. Distribution | Reddit by subreddit rules, awesome-lists by their own process, Show HN, dev.to and Medium with canonical URLs, GitHub topics | [Distribution playbook](references/distribution-playbook.md) |
| 7. Measure | Ask each target question on each engine, log every run, pair with traffic and referrers | [Citation checks](references/citation-checks.md) |

Ask your agent:

```text
Use Organic Discovery on this repo. Run the audit checklist, map the questions
people ask about this kind of tool, rewrite the README with a direct-answer opener,
FAQ and evidence and limits, draft a canonical description and topics, draft
distribution posts for my review, and set up a citation log. Do not post anything.
```

For a full business run with fact governance and AI shelf mapping:

```text
Use Organic Discovery on this business and website.

Run the deterministic audit. Build and validate Business Truth. Preserve exact
AI observations, map each shelf separately, reject unsafe or unsupported wedges,
and choose the highest-value legitimate opening. Implement approved owned-site
changes on a branch, prepare reviewable earned-source drafts, validate the revision,
and define measurement, stop rules, and rollback.
```

## Evidence and limits

- **What has been shown:** the CLI is deterministic. CI runs 20 unit tests and regenerates two offline examples byte for byte on Python 3.11 and 3.13 for every push and pull request. The README you are reading passes the bundled front-page check.
- **What it is not:** there is no published evidence yet that using this skill gets a site or repo cited by any AI engine. This repo has not yet measured its own citation results. The playbook treats each tactic as an experiment to measure, not a guarantee.
- **Where the playbook comes from:** current platform documentation (Google Search Central, OpenAI's crawler docs), published studies and field reports, each labeled by evidence class in [`references/source-register.md`](references/source-register.md) and the evidence notes in [`references/playbook.md`](references/playbook.md). Studies of AI citations disagree, often because they count differently; the docs say so where it matters.
- **Known limitations:** the audit checks one page at a time. There is no live multi-engine scheduler; citation checks are run by hand or exported from another tracker.
- **Release status:** the latest tagged release is v0.5.0. The playbook modules and the front-page check were added after that tag and are listed under Unreleased in the [changelog](CHANGELOG.md).

The repository does **not yet ship** a live multi-model scheduler, Search Console or analytics connector, CMS publisher, dashboard, database, hosted SaaS, or automatic Reddit/community poster. Those remain explicit later phases in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## What this changes on your machine

| Where | What it does | How to undo |
|---|---|---|
| `~/.claude/skills/organic-discovery/` (or the folder you choose) | The git clone. Your agent reads `SKILL.md` and the reference files from here. | Delete the folder |
| `~/.agents/skills/organic-discovery` (Codex manual install) | A symlink to your clone | `rm ~/.agents/skills/organic-discovery` |
| `.validation-output/` inside the clone | `validate_skill.py` writes test output here and deletes it before it exits | Nothing to undo |
| The `--output` path you pass | `od.py` writes JSON and Markdown reports only there | Delete the output folder |

**Network and data.** Install uses git to clone from GitHub. `validate_skill.py`, `check_front_page.py` and the `facts`, `shelf` and `wedge` commands make no network calls. `od.py audit <url>` fetches that URL, its `/robots.txt` and one sitemap, with timeouts, size limits and a block on private network addresses. Nothing is sent anywhere else, and there is no telemetry. Your agent's own web searches and its model provider are outside this tool.

## FAQ

### What is the difference between SEO, AEO and GEO?

SEO is getting a page to rank in classic search results; AEO and GEO are getting it used and cited inside AI answers from Google AI Overviews, ChatGPT search, Perplexity and similar tools. In practice they overlap heavily: Google says AI Overviews use the same indexing and snippet eligibility as normal Search. This skill treats them as stages of one chain and checks each stage separately.

### How do I get my GitHub repo to show up in ChatGPT or Perplexity answers?

Start with a narrow question your repo clearly answers, make the README open with a one-sentence answer to it, and get the repo mentioned in places those engines already cite. The playbook covers each step, including GitHub topics, awesome-lists and Reddit. Then check by asking the question several times and logging the result. Nothing guarantees a citation.

### Does llms.txt help with AI search citations?

Not much, based on current evidence. Google says Google Search does not use llms.txt, and an Ahrefs study found that 97% of the llms.txt files it observed got no requests in May 2026. It is cheap to add for tools that read it, so the playbook treats it as housekeeping, not a citation driver.

### Is FAQ schema still worth adding after Google dropped FAQ rich results?

Only as an accurate description of a FAQ people can see. Google stopped showing FAQ rich results on May 7, 2026, so there is no Google display benefit. `FAQPage` is still valid schema.org markup that other systems may read. Write the FAQ for readers first.

### Do I need special schema or files to appear in Google AI Overviews?

No. Google says there are no extra technical requirements, no special schema and no AI text files needed; the page must be indexed and eligible to show with a snippet. Structured data still helps search systems understand a page when it matches the visible content.

### How do I check whether AI answers cite my site?

Ask each target question on each engine, at least three times, in a clean session, and log whether you were shown, mentioned, cited and described accurately. Save GitHub traffic and referrer data on the same day, because GitHub keeps only 14 days. [`references/citation-checks.md`](references/citation-checks.md) has the method and a CSV template.

### Will it post to Reddit or Hacker News for me?

No. It drafts posts and submissions for you to review and publish yourself, after checking each venue's rules. Fake accounts, vote requests and undisclosed promotion are out of scope.

### Does it work without Claude Code or Codex?

Yes. The CLI runs on its own with Python 3.11 or newer, and the reference files are plain Markdown you can follow by hand or load into another agent that supports Agent Skills.

## Alternatives

- [Google Search Console](https://search.google.com/search-console) and [Bing Webmaster Tools](https://www.bing.com/webmasters): free first-party data on indexing, queries and clicks, including AI Overview traffic inside Search Console's Web report. Use them alongside any tool.
- Commercial AI visibility trackers such as [Profound](https://www.tryprofound.com/), [Peec AI](https://peec.ai/) and [Otterly.AI](https://otterly.ai/): automated prompt tracking across engines at a larger scale than manual checks. Their visibility scores are their own heuristics.
- [Screaming Frog SEO Spider](https://www.screamingfrog.co.uk/seo-spider/): a desktop crawler for whole-site technical audits, where this CLI audits one page at a time.
- Other open-source agent skills for the same job, for example [geo-optimizer-skill](https://github.com/Auriti-Labs/geo-optimizer-skill), [claude-seo](https://github.com/AgricIDaniel/claude-seo) and the [AI SEO skill in marketingskills](https://github.com/coreyhaines31/marketingskills/blob/main/skills/ai-seo/SKILL.md). [`references/source-register.md`](references/source-register.md) notes what each is useful for and where its approach differs.

## CLI reference

Version `0.5.0` ships four commands and a front-page check:

1. **Webpage audit**: bounded technical and content inspection for a URL or local HTML file.
2. **Business Truth validation**: deterministic claim, provenance, existence, availability, and publication gates.
3. **AI Shelf mapping**: exact-surface observation normalization, metrics, and transparent shelf classification.
4. **Wedge planning**: hard rejection of locked, unsafe, unsupported, unavailable, or fabricated opportunities.
5. **Front-page check**: `python scripts/check_front_page.py README.md` checks a Markdown front page for a direct-answer opener, FAQ, evidence and limits, install, machine changes, alternatives, dashes and superlatives.

It also ships stable JSON Schemas for normalized facts, observations, shelf maps, and wedge plans; two offline fixtures with committed expected outputs; 20 focused regression tests; Python 3.11 and 3.13 CI; and the playbook templates in [`templates/`](templates/).

Quick start from a clone:

```bash
git clone https://github.com/wrg32786/aeo-seo-geo-marketing.git
cd aeo-seo-geo-marketing
python scripts/validate_skill.py
```

### Deterministic webpage auditor

```bash
python scripts/od.py audit https://example.com --output output/audit
python scripts/od.py audit ./page.html --output output/audit
```

The auditor writes:

```text
output/audit/
├── audit.json
├── work-orders.json
└── report.md
```

It checks bounded HTTP behavior, crawler controls, index directives, canonicalization, initial HTML, metadata, headings, links, images, sitemaps, JSON-LD, visible/schema agreement, claim provenance, and hidden prompt-like instructions. Public URL fetching rejects private-network destinations, revalidates redirects, pins the validated public IP, and enforces timeout, byte, and redirect limits.

It does not treat technical eligibility as indexing, retrieval, citation, traffic, or conversion success. Unobservable stages remain `unknown`; `opaque_score` remains `null`.

See [`examples/sample-site/`](examples/sample-site/).

### Business Truth validator

A fact registry is the publication boundary between an LLM and public claims.

```bash
python scripts/od.py facts validate fact-registry.csv --output facts.json
```

Example with the bundled fixture:

```bash
python scripts/od.py facts validate examples/sample-shelf/fact-registry.csv \
  --output output/facts.json
```

The canonical CSV contract records:

```text
claim_id, entity_id, entity, claim_type, canonical_wording, value, unit,
source_url, source_type, verified_at, evidence_grade, offer_exists,
availability, publish_status, owner, refresh_trigger, limitations,
prompt_families, market, language, expires_at
```

The validator:

- requires stable IDs and valid dates;
- distinguishes seller-controlled, independent, community, and unknown evidence;
- blocks approved claims without provenance, verification, ownership, or refresh rules;
- blocks offer-dependent claims when existence or availability is not confirmed;
- requires independent evidence for certification, safety, medical, and customer-result claims;
- keeps `approval_required`, `research_required`, `expired`, and `prohibited` facts out of publication-ready copy;
- preserves seller-controlled facts while preventing them from being represented as independent consensus.

The normalized record contract is [`schemas/fact-record.schema.json`](schemas/fact-record.schema.json).

### AI Shelf Mapper

An AI shelf is the small recommendation set produced for one prompt family on one exact product surface. Organic Discovery never silently pools:

```text
platform + surface + mode + model + market + language + device
+ account state + session state + prompt family + target entity + branded state
```

```bash
python scripts/od.py shelf map examples/sample-shelf/observations.jsonl \
  --facts examples/sample-shelf/fact-registry.csv \
  --output output/shelf
```

The command writes:

```text
output/shelf/
├── normalized-observations.jsonl
├── shelf-map.json
└── shelf-report.md
```

For every exact-surface group it reports:

- recommendation coverage and target participation;
- first-mentioned share and recommendation order;
- incumbent concentration;
- recommendation-set agreement and volatility;
- citation-domain overlap;
- seller-controlled and independent source share;
- retrieval and citation rates when observable;
- fidelity, constraint satisfaction, and recommendation availability;
- the numerator and denominator behind every rate.

Shelf states are transparent operational classifications:

- **locked**: one entity dominates repeatedly;
- **contested**: a recurring set competes without one locked leader;
- **fragmented**: recommendations rotate with low agreement;
- **open**: recommendations are absent or unstable enough to warrant a narrow test;
- **unsafe**: fidelity, constraint satisfaction, or availability falls below the declared guardrail;
- **unknown**: evidence is insufficient or the group is branded validation.

Branded validation is grouped separately and excluded from unbranded recommendation-share denominators. Missing fields stay `null` and stay out of their metric denominator.

The contracts are [`schemas/observation.schema.json`](schemas/observation.schema.json) and [`schemas/shelf-map.schema.json`](schemas/shelf-map.schema.json).

### Truthful wedge planner

```bash
python scripts/od.py wedge plan output/shelf/shelf-map.json \
  --facts examples/sample-shelf/fact-registry.csv \
  --candidates examples/sample-shelf/candidates.json \
  --output output/wedge-plan.json
```

A wedge must pass hard gates before prioritization:

- the offer exists and is currently available;
- required facts are publishable;
- the prompt family has legitimate offer fit;
- the observations are unbranded and exact-surface;
- the shelf is not `locked`, `unsafe`, or `unknown`;
- no required fact is prohibited or unsupported.

Unsafe and unsupported opportunities are rejected, not merely scored lower. Optional business factors produce a transparent planning index; it is not an engine score and it carries no fixed time-to-shelf promise.

The contract is [`schemas/wedge-plan.schema.json`](schemas/wedge-plan.schema.json).

### Offline AI-shelf proof

[`examples/sample-shelf/`](examples/sample-shelf/) contains 22 synthetic observations across six exact-surface groups. The fixture proves:

- one narrow prompt family is open in the ChatGPT fixture but locked in the Gemini fixture;
- branded runs are excluded;
- a broad category shelf is locked;
- a travel shelf is fragmented;
- a health-related shelf is unsafe;
- a nonexistent product and a prohibited claim are rejected;
- two legitimate wedges pass the hard gates.

Every generated artifact is compared byte-for-byte in CI.

## How it differs from score-based tools

| Common SEO/GEO tooling | Organic Discovery |
|---|---|
| One proprietary readiness score | Observable stages, exact metrics, facts, gates, and `null` for unknowns |
| Seller copy treated as neutral evidence | Seller-controlled and independent evidence remain distinct |
| Branded prompts inflate visibility | Branded validation is excluded from unbranded share |
| API and consumer surfaces pooled | Every material surface condition is part of the grouping key |
| Broad head-term queries first | Narrow, legitimate wedges are tested before locked category shelves |
| Unsafe opportunities ranked lower | Unsupported, unavailable, unsafe, and prohibited opportunities are rejected |
| Advice without execution contracts | Deterministic files, schemas, examples, acceptance checks, and rollback |
| Visibility as the final KPI | Retrieval, citation, fidelity, qualified traffic, conversion, and revenue stay separate |

Public third-party posting remains human-approved by default. The skill never authorizes fake identities, fake reviews, coordinated votes, undisclosed promotion, or mass link posting.

## Evidence posture

- Current official platform controls outrank vendor claims and community advice.
- Benchmarks and field reports justify bounded experiments, not ranking guarantees.
- Correlations do not justify manufactured mentions, reviews, links, or dates.
- A result remains bounded to its exact surface, market, prompt family, and observation window until replicated.
- A recommendation-share increase with worse fidelity or constraint satisfaction is a regression.
- No output promises a fixed time to rank, citation, recommendation, traffic, or revenue.

## Repository structure

```text
.
├── SKILL.md
├── README.md
├── references/      playbook, checklist, question mapping, templates guide,
│                    entity kit, distribution, citation checks, doctrine
├── templates/       README and page templates, JSON-LD, entity record, CSV logs
├── schemas/
│   ├── fact-record.schema.json
│   ├── observation.schema.json
│   ├── shelf-map.schema.json
│   └── wedge-plan.schema.json
├── examples/
│   ├── sample-site/
│   └── sample-shelf/
├── scripts/
│   ├── od.py
│   ├── od_audit.py
│   ├── od_fetch.py
│   ├── od_truth.py
│   ├── od_shelf.py
│   ├── check_front_page.py
│   └── validate_skill.py
├── tests/
├── docs/
├── agents/
└── evals/
```

## Roadmap

```text
v0.4 deterministic auditor: shipped
v0.5 Business Truth + AI Shelf Mapper: shipped
→ v0.6 GitHub-backed implementation operator
→ v0.7 content + earned-source queue
→ v0.8 measurement adapters
→ v0.9 CMS + bounded autonomy
→ v1.0 continuous loop
```

## Validate

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/check_front_page.py README.md
```

The CI workflow additionally regenerates both offline examples and compares every expected artifact on Python 3.11 and 3.13.

## Project documents

- Playbook: [`references/playbook.md`](references/playbook.md)
- Product vision: [`docs/PRODUCT-VISION.md`](docs/PRODUCT-VISION.md)
- Roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)
- Definition of done: [`docs/DEFINITION-OF-DONE.md`](docs/DEFINITION-OF-DONE.md)
- Output contracts: [`references/output-contracts.md`](references/output-contracts.md)
- Evidence register: [`references/source-register.md`](references/source-register.md)
- Self-audit: [`docs/SELF-AUDIT.md`](docs/SELF-AUDIT.md)
- Contributing: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security: [`SECURITY.md`](SECURITY.md)
- Citation: [`CITATION.cff`](CITATION.cff)
- License: [`LICENSE`](LICENSE)
