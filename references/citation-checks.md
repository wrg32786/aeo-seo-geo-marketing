# Citation Checks

Use this module to find out whether AI answers cite you for the target questions, and to keep a record that shows change over time. The short answer: ask each target question on each engine the same way, log every run including misses, and pair the log with first-party traffic and referrer data.

This is the lightweight, manual layer. For exact-surface grouping, shelf states and wedge selection over many runs, export the same observations as JSONL and use `python scripts/od.py shelf map` with the contracts in `references/output-contracts.md`. For full experiment design, see `references/measurement-protocol.md`.

## 1. What to check

For each target question from the question map:

- **Shown:** did the engine produce an AI answer at all? AI Overviews often do not trigger.
- **Mentioned:** is the project named in the answer text?
- **Cited:** is a URL you control (repo, site, docs) listed as a source?
- **Position:** where in the source list.
- **Accurate:** does the answer describe the project correctly, with the current description and limits?
- **Who else:** which competitors and which sources were cited instead.

Mentioned and cited are different results. So are cited and clicked. Keep them in separate columns.

## 2. How to run a check

1. Use the canonical question text from the question map, not a paraphrase.
2. Record the engine, mode (for example ChatGPT with search, Perplexity default, Google AI Overview, Google AI Mode, Copilot), whether you were signed in, country and language.
3. Use a clean session where you can: signed out or a fresh profile, no prior conversation. Answers vary by account and history.
4. Ask each question at least three times per engine per check date. Answers vary between runs; one run is an anecdote.
5. Save the answer: a screenshot, a share link or a copy of the text and source list.
6. Log every run, including runs where nothing about you appeared. Zero results are data.
7. Keep branded questions ("What is {name}?") flagged as branded. They test accuracy, not discovery, and never count toward unbranded share.

## 3. Cadence

- Baseline before any change.
- After a change ships: one week, four weeks and twelve weeks.
- Monthly after that for the active target list.
- Re-baseline after a major engine change you hear about, and note it in the log.

## 4. First-party data to pair with it

GitHub keeps traffic data for 14 days, so save it on every check:

```bash
gh api repos/{owner}/{repo}/traffic/views > traffic-views-$(date +%F).json
gh api repos/{owner}/{repo}/traffic/clones > traffic-clones-$(date +%F).json
gh api repos/{owner}/{repo}/traffic/popular/referrers > traffic-referrers-$(date +%F).json
gh api repos/{owner}/{repo}/traffic/popular/paths > traffic-paths-$(date +%F).json
```

On a site:

- Search Console Performance report for the target queries and pages. Google counts AI Overview and AI Mode appearances inside the normal "Web" search type. [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- Analytics referrers such as `chatgpt.com`, `perplexity.ai`, `copilot.microsoft.com` and `gemini.google.com`. ChatGPT search links have carried `utm_source=chatgpt.com`; confirm in your own logs rather than assuming.
- Server or CDN logs for crawler visits (OAI-SearchBot, PerplexityBot, Googlebot, Bingbot), verified by published IP ranges where the vendor publishes them.

## 5. Reading the results

- A citation that appears once and never again is noise until it repeats.
- A rise in mentions with worse accuracy is a regression.
- If you are cited but get no referrals, the answer may already satisfy the question. That can still be useful for awareness. Record it as such; do not call it traffic.
- If nothing moves after twelve weeks on a narrow question, check the earlier stages: is the page indexed, is it the canonical owner, does it actually answer the question better than what is cited?
- Do not convert this log into a single score. Report the counts with their denominators: "cited in 4 of 9 runs on Perplexity, 0 of 9 on ChatGPT, AI Overview shown in 3 of 9".

## 6. Template

`templates/citation-log.csv` columns:

```text
check_date, question_id, question_text, branded, engine, surface_mode, signed_in,
market, language, run_number, ai_answer_shown, project_mentioned, project_cited,
cited_url, cited_position, description_accurate, competitors_cited, sources_cited,
screenshot_or_export_path, notes
```

Use `yes`, `no` or `unknown` for the yes/no columns. Unknown is not no.

## 7. Limits of this method

- Manual checks are small samples. They show direction, not market share.
- Consumer apps, APIs and signed-in sessions can give different answers. Do not mix them in one rate.
- Paid trackers automate this at larger scale. Their scores are their own heuristics; keep their raw observations and ignore any single "visibility score".
