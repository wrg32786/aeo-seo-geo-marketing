# Question Mapping

Use this module to find the questions people actually ask before writing or rewriting anything. The output is a ranked question map that drives the owner page, the FAQ and the citation checks.

The short answer: collect real phrasings from at least four sources, group them by job, and start with narrow questions where your project is a clear, honest fit.

## 1. Start from the job, not the keyword

Write down, in one sentence each:

- what the project does;
- who uses it;
- what they were trying to do just before they would need it;
- what they would type if they did not know the project existed.

That last line is the seed list. It should contain no brand names.

## 2. Collect real phrasings

Use at least four of these sources. Record where each question came from.

| Source | How to collect | What it is good for |
|---|---|---|
| Google autocomplete and People Also Ask | Type the seed phrases into a clean browser session and copy the suggestions and PAA questions | How people phrase a question to Google |
| Search Console queries | Performance report, filter for queries with "how", "what", "why", "vs", "best way", "can I" | Questions that already bring impressions |
| Reddit | Search the topic in relevant subreddits, sort by top and new, read titles and the top comments | Problem language, objections, and comparisons people make |
| GitHub issues and discussions | Search issues in your repo and in competing repos for "how do I", "is there a way", "does it support" | Concrete technical questions |
| Hacker News | Search `hn.algolia.com` for the topic | Skeptical framing, alternatives people mention |
| The answer engines themselves | Ask ChatGPT, Perplexity and Google AI Mode the seed question, then note the follow-up questions they suggest and the sub-queries they show | How the engines expand a question |
| Support mail, sales calls, chat logs | Pull the first message of each conversation | The exact words of people who already needed you |
| Stack Overflow and Discord | Search the topic and error messages | Error-message questions, which are narrow and often unanswered |

Do not invent questions to fill a list. A question nobody asked is a doorway page.

## 3. Write each question the way people type it

People ask answer engines in full sentences. Keep the wording close to the source:

- "how do I get my github repo to show up in chatgpt answers"
- "does llms.txt actually do anything"
- "is faq schema still worth adding in 2026"
- "claude code skill for seo audit"

Keep one canonical phrasing per question and list the variants under it. Variants share one answer.

## 4. Classify

For each question, record:

- **Intent:** definition, how-to, troubleshooting, comparison, recommendation, evaluation, install, cost.
- **Breadth:** narrow (one specific job, constraint or error), medium, or broad (a head term such as "SEO tools").
- **Fit:** strong (the project answers it directly), partial, or none. Drop questions with no fit.
- **Branded:** yes or no. Branded questions go to accuracy checks, not discovery targets.
- **Current owner:** who answer engines cite today, from one or two quick checks.
- **Evidence you can offer:** a test, a number with a source, a working example, a limit.

## 5. Pick first targets

Choose 3 to 5 first targets that are:

1. narrow;
2. a strong fit;
3. answerable with evidence you already have;
4. not owned by one dominant source today (if one source owns it in every run, it is a later target).

Broad head terms come later, after several nearby narrow questions hold. This mirrors the wedge logic in `references/ai-shelf-and-growth-loop.md`; when you have exact-surface observations, run `python scripts/od.py shelf map` and `python scripts/od.py wedge plan` to make the choice with hard gates.

## 6. Map questions to places

| Question type | Where the answer lives |
|---|---|
| "What is X" and the one-line pitch | First paragraph of the README or home page |
| How-to and install | A section with a one-sentence answer and a command |
| Troubleshooting | FAQ entry or a docs page titled with the error |
| Comparison and alternatives | A neutral alternatives section |
| "Does it really work" | Evidence and limits section |
| Questions with a strong community angle | A draft reply for an existing Reddit or forum thread (human-approved) |

## 7. Output

Fill `templates/question-map.csv`. Columns:

```text
question_id, canonical_question, variants, source, source_url, intent, breadth,
fit, branded, current_owner, evidence_available, owner_page, owner_section,
first_target, notes
```

Re-run the collection every quarter, or after a release that changes what the project does.
