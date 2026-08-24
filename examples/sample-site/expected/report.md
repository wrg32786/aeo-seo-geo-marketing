# Organic Discovery Audit — examples/sample-site/site/index.html

## Executive diagnosis

Earliest observable failing stage: **eligibility**. The audit found **2 P0** and **4 P1** findings. Technical eligibility is not proof of indexing, retrieval, citation, recommendation, traffic, or conversion. No opaque readiness score is calculated.

## Stage diagnosis

| Stage | Status | Confidence | Evidence |
|---|---|---|---|
| Activation | unknown | low | not observable from a deterministic page fetch |
| Eligibility | blocked | medium | deterministic initial-page audit |
| Retrieval | unknown | low | not observable from a deterministic page fetch |
| Context Allocation | unknown | low | not observable from a deterministic page fetch |
| Source Selection | unknown | low | not observable from a deterministic page fetch |
| Absorption | unknown | low | not observable from a deterministic page fetch |
| Fidelity | blocked | medium | deterministic initial-page audit |
| Behavior | unknown | low | not observable from a deterministic page fetch |

## Findings

| ID | Priority | Stage | Finding |
|---|---|---|---|
| F-001 | P0 | fidelity | **Hidden machine-targeted instructions were detected** — Hidden/comment/script content appears to instruct an AI or crawler how to rank, cite, or respond. |
| F-002 | P0 | eligibility | **Canonical conflicts with the audited local asset** — The local index fixture declares https://example.test/not-this-page. |
| F-003 | P1 | eligibility | **Core answer may require JavaScript** — Only 28 visible words were present in initial HTML while client scripts/framework roots were detected. |
| F-004 | P1 | eligibility | **AI search crawlers are blocked** — OAI-SearchBot, Claude-SearchBot cannot fetch the target path. |
| F-005 | P1 | fidelity | **Material claims lack visible provenance** — Numeric, superlative, certification, or performance claims appear without visible sourcing. |
| F-006 | P1 | fidelity | **Structured data contains unsupported visible facts** — Important schema values are absent from visible initial content. |
| F-007 | P2 | eligibility | **Multiple primary headings dilute page purpose** — Found 2 H1 elements. |
| F-008 | P2 | eligibility | **Images are missing alternative text** — Found 1 images without alt text. |
| F-009 | P2 | eligibility | **Links lack accessible descriptive text** — Found 1 non-empty links with no text or aria-label. |
| F-010 | P2 | eligibility | **Meta description is missing** — No meta description was found. |
| F-011 | P2 | eligibility | **Document language is missing** — The html element has no lang value. |
| F-012 | P2 | eligibility | **Audited page is absent from the sitemap fixture** — The sibling sitemap does not contain the represented index URL. |
| F-013 | P2 | fidelity | **Commercial offer omits a material price or availability fact** — The page presents an offer but no visible price or explicit availability path was detected. |
| F-014 | P3 | eligibility | **Viewport metadata is missing** — No viewport meta element was found. |
| F-015 | P3 | eligibility | **Heading levels skip hierarchy** — The heading outline jumps by more than one level. |

## Work orders

### OD-001 — P0 / fidelity

- **Root cause:** Hidden/comment/script content appears to instruct an AI or crawler how to rank, cite, or respond.
- **Owner:** security
- **Risk:** high
- **Change:**
  - remove the hidden instruction and review its origin
- **Acceptance:**
  - the pattern is absent from source and rendered output
- **Delayed observation:** fidelity_and_delayed_discovery / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore a clean known-good revision

### OD-002 — P0 / eligibility

- **Root cause:** The local index fixture declares https://example.test/not-this-page.
- **Owner:** engineering
- **Risk:** medium
- **Change:**
  - set the canonical to the deployed URL represented by this file
- **Acceptance:**
  - the canonical resolves to the intended deployed page
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore the previous canonical if the deployment mapping differs

### OD-003 — P1 / eligibility

- **Root cause:** Only 28 visible words were present in initial HTML while client scripts/framework roots were detected.
- **Owner:** engineering
- **Risk:** medium
- **Change:**
  - render the primary answer, offer facts, and links in initial HTML
- **Acceptance:**
  - initial HTML contains the same core facts available after rendering
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - revert to the prior rendering path if hydration or functionality regresses

### OD-004 — P1 / eligibility

- **Root cause:** OAI-SearchBot, Claude-SearchBot cannot fetch the target path.
- **Owner:** engineering
- **Risk:** medium
- **Change:**
  - allow only the search-answer crawlers the owner intentionally supports
- **Acceptance:**
  - approved AI search crawlers can fetch the path while training policy remains unchanged
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore the prior per-crawler rules

### OD-005 — P1 / fidelity

- **Root cause:** Numeric, superlative, certification, or performance claims appear without visible sourcing.
- **Owner:** content
- **Risk:** high
- **Change:**
  - verify each material claim and add visible source/method/limitations or remove it
- **Acceptance:**
  - every material claim has an approved source and visible qualification
- **Delayed observation:** fidelity_and_delayed_discovery / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - remove the unsupported claim if verification fails

### OD-006 — P1 / fidelity

- **Root cause:** Important schema values are absent from visible initial content.
- **Owner:** content
- **Risk:** high
- **Change:**
  - remove unsupported values or render the verified facts visibly
- **Acceptance:**
  - visible copy and structured data agree for every material value
- **Delayed observation:** fidelity_and_delayed_discovery / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - remove the changed markup if facts cannot be maintained

### OD-007 — P2 / eligibility

- **Root cause:** Found 2 H1 elements.
- **Owner:** content
- **Risk:** low
- **Change:**
  - retain one page-level H1 and demote subordinate headings
- **Acceptance:**
  - one descriptive H1 remains
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore previous heading levels if accessibility testing finds a regression

### OD-008 — P2 / eligibility

- **Root cause:** Found 1 images without alt text.
- **Owner:** content
- **Risk:** low
- **Change:**
  - add useful alt text or an explicit empty alt for decorative images
- **Acceptance:**
  - each image has an intentional alt value
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore prior markup if assistive-technology testing regresses

### OD-009 — P2 / eligibility

- **Root cause:** Found 1 non-empty links with no text or aria-label.
- **Owner:** engineering
- **Risk:** low
- **Change:**
  - add descriptive link text or an accessible name
- **Acceptance:**
  - every actionable link has an accessible name
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore the prior component if navigation behavior regresses

### OD-010 — P2 / eligibility

- **Root cause:** No meta description was found.
- **Owner:** content
- **Risk:** low
- **Change:**
  - add a truthful summary for search snippets
- **Acceptance:**
  - one visible-content-aligned description is present
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - remove it if the template duplicates or misstates the page

### OD-011 — P2 / eligibility

- **Root cause:** The html element has no lang value.
- **Owner:** engineering
- **Risk:** low
- **Change:**
  - set the correct BCP 47 language tag
- **Acceptance:**
  - the html element declares the page language
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore the prior language routing if locale detection regresses

### OD-012 — P2 / eligibility

- **Root cause:** The sibling sitemap does not contain the represented index URL.
- **Owner:** engineering
- **Risk:** low
- **Change:**
  - add the canonical deployed URL to the sitemap
- **Acceptance:**
  - the canonical target appears exactly once
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - remove the entry if the page should not be indexed

### OD-013 — P2 / fidelity

- **Root cause:** The page presents an offer but no visible price or explicit availability path was detected.
- **Owner:** content
- **Risk:** medium
- **Change:**
  - show current price/availability or clearly explain how to obtain it
- **Acceptance:**
  - the offer exposes accurate current commercial terms
- **Delayed observation:** fidelity_and_delayed_discovery / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore the prior copy if terms cannot be maintained

### OD-014 — P3 / eligibility

- **Root cause:** No viewport meta element was found.
- **Owner:** engineering
- **Risk:** low
- **Change:**
  - add a standard responsive viewport declaration
- **Acceptance:**
  - mobile layout remains usable and viewport metadata is present
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - remove the change if it breaks intentional embedded behavior

### OD-015 — P3 / eligibility

- **Root cause:** The heading outline jumps by more than one level.
- **Owner:** content
- **Risk:** low
- **Change:**
  - make heading levels reflect document hierarchy
- **Acceptance:**
  - the heading outline has no unexplained jumps
- **Delayed observation:** technical_acceptance / immediate technical check; 28d delayed outcome where applicable
- **Rollback:**
  - restore previous levels if component semantics require another hierarchy

## Limitations

- Initial HTML parser; no browser rendering or index/citation observation.
- Heuristic claim and hidden-instruction checks require human review.

## Deliberately not done

- No opaque readiness score.
- No claim that crawler access equals indexing, retrieval, citation, or recommendation.
- No automatic content generation, community posting, outreach, or publishing.
- No recommendation to create `llms.txt` without a named consumer.
