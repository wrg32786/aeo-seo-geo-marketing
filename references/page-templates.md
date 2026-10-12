# Page and README Templates

Use this module when writing or rewriting an owner page: a README, a product page, a docs landing page or a tool page. The templates live in `templates/`:

- `templates/README-template.md` for a GitHub README;
- `templates/page-template.html` for a web page, with JSON-LD slots;
- `templates/jsonld/faqpage.json` and `templates/jsonld/softwareapplication.json`.

The short answer: open with one sentence that answers "what is this", put install and proof near the top, add a FAQ in the words people use, and say plainly what has not been shown.

## Section order

1. **Title.** The project name plus the category in plain words. "Organic Discovery: SEO, AEO and GEO Agent Skill" is clearer than "Organic Discovery".
2. **Direct-answer opener.** One sentence: what it is, who it is for, what it does. It should still make sense if quoted alone in an AI answer.
3. **One-line install** (tools only). A single command someone can paste.
4. **What it does, in plain English.** One short paragraph.
5. **Evidence and limits.** What was tested, on what, with links. What it is not. Known limitations. Release status.
6. **How to use it.** Each subsection opens with a one-sentence answer, then commands.
7. **What this changes on your machine** (tools only). Files written, network calls, how to undo.
8. **FAQ.** 5 to 10 questions phrased the way people ask them.
9. **Alternatives.** Neutral, short, with links.
10. **Reference material.** Structure, contracts, contributing, license.

## Writing rules

- Each answer section opens with one sentence that answers the heading. Detail follows.
- Use the canonical description from the entity record, word for word, in the opener or immediately after it.
- Plain human voice. Short sentences. No em dashes or en dashes; use a period, comma, colon or parentheses.
- No superlatives and no hype words. Replace "the best", "powerful", "revolutionary", "seamless", "blazing fast" with a checkable fact.
- Every number links to its source or states its method.
- Say "not shown" or "unknown" where that is the truth.
- Put the FAQ in visible text. Hidden or collapsed-only content is a poor basis for markup.

## The direct-answer opener

Pattern:

```text
{Name} is a {category} for {audience} that {does the main job}, {key differentiator or constraint}.
```

Checks:

- under 40 words;
- names the category in words people search;
- contains no claim you cannot support;
- reads naturally if quoted alone.

## The FAQ

- Take the questions from the question map, not from imagination.
- Phrase each as a person would type it into ChatGPT, Perplexity or Google.
- Answer the question in the first sentence, then add one to three sentences of detail.
- Include at least one honest "no" or "not yet" answer if one applies. It builds trust and it is often what people are checking.
- On a web page, mirror the visible FAQ in `FAQPage` JSON-LD using `templates/jsonld/faqpage.json`. On GitHub there is no JSON-LD; the Markdown FAQ is the whole thing.

## Evidence and limits

Four parts:

1. **What has been shown:** test, environment, sample size, date, link.
2. **What it is not:** the claims a reader might assume but you have not shown.
3. **Known limitations:** current defects or gaps, with issue links.
4. **Release status:** which version the evidence applies to.

Claims that can be checked get repeated and cited. Hype gets ignored or filtered.

## What this changes on your machine

A table with three columns: where, what is written or changed, how to undo it. Then a short "network and data" list naming every outbound call. If the tool makes no network calls by default, say so.

## Alternatives

List two to five real alternatives with one neutral sentence each on what they do and when someone might pick them. Do not disparage. Link to them. This section often answers the comparison questions people ask engines, and a fair one is more likely to be trusted.

## Before you publish

- Run `python scripts/check_front_page.py <file.md>` on Markdown front pages.
- Run `python scripts/od.py audit <file.html>` on HTML pages.
- Validate every fact through the registry.
- Check JSON-LD at validator.schema.org and confirm every marked-up question is visible.
