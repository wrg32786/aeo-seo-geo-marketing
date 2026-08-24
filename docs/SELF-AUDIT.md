# Self-Audit: Organic Discovery Repository

**Controlled asset:** `https://github.com/wrg32786/aeo-seo-geo-marketing`  
**Audit date:** 2026-08-23  
**Goal:** Improve discovery, comprehension, trust, installation, and accurate citation for queries about SEO, AEO, GEO, AI search optimization, and Agent Skills.

## Executive diagnosis

The repository was publicly crawlable and had a substantive skill, but the landing surface under-explained the product. The H1 was only “Organic Discovery,” installation was absent above the fold, GitHub topics were empty, host-specific metadata was missing, and there was no CI, citation file, contribution policy, security policy, or public example of the system auditing itself.

An exact-name web search did not surface the repository at baseline. That is not proof of an indexing defect—the repository was new—but it means visibility must remain `unknown/weak` until later observation rather than being declared successful.

The highest-leverage owned-asset fix was one coherent bundle: make the repository’s category identity explicit, expose installation and use cases, add machine-readable host/citation metadata, add deterministic validation, populate relevant GitHub metadata, and publish this audit.

## Discovery brief

- **Entity:** Organic Discovery
- **Type:** Open-source Agent Skill
- **Repository owner:** `wrg32786`
- **Primary jobs:** audit, implement, and measure SEO/AEO/GEO improvements
- **Audience:** developers, technical marketers, publishers, agencies, founders, SEO teams, and AI-agent operators
- **Primary markets/language:** global / English
- **Conversion goals:** install, star, fork, cite, contribute, and use the skill
- **Controlled surfaces:** repository files and README
- **Configured GitHub metadata:** About description and repository topics
- **Partially controlled surfaces:** website, social preview, Pages settings, and external indexing
- **Unknowns:** GitHub traffic analytics, clone counts, search impressions, AI citations, downstream installs

## Eight-stage diagnosis

| Stage | Status at baseline | Evidence | Confidence | Finding |
|---|---|---|---|---|
| Activation | unknown | external search | low | Search products do not expose whether this exact repo query triggered retrieval |
| Eligibility | healthy | public GitHub surface | high | Repository and README were publicly reachable |
| Retrieval | weak/unknown | exact-name search | medium | Exact-name web search did not surface the repo at audit time |
| Context allocation | unknown | not exposed | low | No reliable evidence of reranking or context position |
| Source selection | unknown | no controlled prompt baseline | low | No citation baseline existed |
| Absorption | unknown | no cited-answer corpus | low | No evidence that answers used repository doctrine |
| Fidelity | weak | owned page review | high | Core doctrine was accurate, but category identity and installability were under-specified |
| Behavior | unknown | no first-party analytics supplied | low | Installs, stars, clones, referrals, and conversions were unavailable |

## Root causes

1. **Entity/category ambiguity:** “Organic Discovery” alone did not state SEO, AEO, GEO, Agent Skill, or supported answer surfaces.
2. **Installation friction:** Users and agents could not see where the skill belongs in Codex or Claude Code.
3. **Trust gap:** No visible CI badge or contributor/security contract.
4. **Machine-readable identity gap:** No `agents/openai.yaml` or `CITATION.cff`.
5. **Evidence gap:** The project claimed evidence discipline but did not expose a self-audit.
6. **Repository metadata gap:** GitHub topics were empty at baseline and required a separate repository-settings write.

## Implemented work orders

### OD-SELF-001 — Clarify the category and direct answer

- **Priority:** P0
- **Stage:** fidelity / retrieval
- **Asset:** `README.md`
- **Change:** keyword-specific H1, answer-first definition, supported platforms, use cases, differentiation, outputs, and clear internal navigation
- **Acceptance:** a new visitor can identify what the repo is, who it is for, and what it produces from the opening section
- **Status:** complete

### OD-SELF-002 — Remove installation ambiguity

- **Priority:** P0
- **Stage:** behavior
- **Asset:** `README.md`
- **Change:** official-path manual installs for Codex and Claude Code plus invocation examples
- **Acceptance:** commands place the repository at a documented host skill location
- **Status:** complete

### OD-SELF-003 — Add deterministic trust signals

- **Priority:** P1
- **Stage:** fidelity / behavior
- **Assets:** `.github/workflows/validate.yml`, `scripts/validate_skill.py`
- **Change:** validate on pushes and pull requests under Python 3.11 and 3.13; surface badge in README
- **Acceptance:** workflow executes the same local validator documented for contributors
- **Status:** complete; first pull-request run passed on both configured Python versions

### OD-SELF-004 — Add host and citation metadata

- **Priority:** P1
- **Stage:** understanding / fidelity
- **Assets:** `agents/openai.yaml`, `CITATION.cff`
- **Change:** define display name, short description, default prompt, implicit-invocation policy, canonical title, repository URL, license, version, and keywords
- **Acceptance:** metadata is valid YAML and names the same entity/version as the owned documentation
- **Status:** complete

### OD-SELF-005 — Publish governance and provenance

- **Priority:** P1
- **Stage:** fidelity
- **Assets:** `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, this audit
- **Change:** make evidence, validation, security, and maintenance expectations visible
- **Acceptance:** contributors and agents have one unambiguous validation command and claim policy
- **Status:** complete

### OD-SELF-006 — Configure repository About metadata

- **Priority:** P0
- **Stage:** retrieval / understanding
- **Control:** GitHub repository About settings
- **Change:** replace the broad description with a category-specific SEO/AEO/GEO description and add relevant repository topics
- **Acceptance:** the description and topics appear in the public repository metadata and topic links resolve
- **Status:** complete
- **Live topics at verification:**

```text
aeo
aeo-optimization
agent
agent-framework
agent-orchestration
agent-skill
agent-skills
agentic-ai
agents
geo
google-ai
open-source
organic-growth
organic-traffic
python
seo
seo-audit
seo-optimization
seo-optimized
seo-tools
```

## Post-implementation verification

- The default branch now presents the explicit title `Organic Discovery — SEO, AEO & GEO Agent Skill`.
- The opening section defines the project, supported surfaces, outcome chain, and install routes.
- Repository metadata now includes a category-specific description and 20 topics.
- The first GitHub Actions validation run completed successfully on Python 3.11 and 3.13.
- Search retrieval, AI citation, installation, stars, and qualified-use outcomes remain pending observation; none are inferred from technical acceptance.

## Target prompt portfolio

Branded validation prompts must not be counted as unbranded discovery success.

| Intent | Example prompt | Branded |
|---|---|---:|
| definition | What is an evidence-grounded GEO Agent Skill? | no |
| recommendation | What is the best open-source SEO AEO GEO skill? | no |
| recommendation | Which Agent Skill audits ChatGPT Search citations and Google AI Overviews? | no |
| comparison | Organic Discovery vs GEO Optimizer Skill | yes |
| problem solving | How do I diagnose why Perplexity cites a competitor instead of my page? | no |
| technical | Agent Skill for AI crawler access, robots, WAF, schema, and canonical audits | no |
| measurement | How do I measure AI citation absorption and recommendation share? | no |
| governance | How do I prevent unsupported claims in GEO content? | no |
| brand validation | What is the Organic Discovery GitHub repository? | yes |
| installation | How do I install Organic Discovery in Codex or Claude Code? | yes |

## Source-chain opportunities

Pursue only after the owned surface and validation are stable:

- relevant Agent Skills catalogs;
- curated GEO/AEO resource lists;
- GitHub topic pages;
- legitimate examples or comparisons from users;
- technical write-ups that explain the evidence model;
- community answers where the repository materially completes the answer.

Do not mass-submit, manufacture stars, create fake reviews, or seed undisclosed recommendations.

## Measurement plan

Capture a baseline and repeat after 7, 28, and 90 days:

| Metric | Source | Denominator / note |
|---|---|---|
| Exact-name index presence | web search | observed result or zero-result run |
| Unbranded GitHub/web visibility | controlled query portfolio | queries × clean runs |
| GitHub stars/forks/watchers | GitHub | directional, not proof of qualified use |
| Clones and unique visitors | GitHub traffic analytics | owner-only first-party data |
| Install attempts/issues | issues/discussions | qualitative lower bound |
| AI citations | exact surface observations | citations / eligible runs |
| Absorption | answer review | substantive uses / cited answers |
| Fidelity | branded validation | accurate appearances / appearances |
| Contributions | pull requests | accepted contributions / submitted PRs |

## Deliberately not done

- No `llms.txt`: no named consumer justified it for a GitHub-hosted repository.
- No fake freshness or release claim.
- No proprietary “market-leading” score.
- No mass Reddit, Quora, Hacker News, or awesome-list submission.
- No duplicate keyword pages.
- No claim that README changes guarantee indexing, citation, stars, or installs.
