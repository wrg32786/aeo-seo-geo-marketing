# Audit Checklist

Use this checklist at the start and end of a playbook run. Mark each line `pass`, `fail`, `unknown` or `n/a`, with a one-line note on the evidence. Unknown is a valid answer; do not mark it pass.

The deterministic auditor (`python scripts/od.py audit`) covers much of section A for HTML pages. The rest needs a person or an agent with a browser and the GitHub CLI.

## A. Access and eligibility

- [ ] The page returns 200 to a normal request and is not behind a login, cookie wall or bot challenge.
- [ ] robots.txt allows Googlebot, Bingbot and OAI-SearchBot, unless there is a written policy decision not to. Training crawlers (GPTBot, Google-Extended, ClaudeBot) are a separate decision.
- [ ] The CDN or WAF does not block those crawlers (check server or CDN logs, not just robots.txt).
- [ ] No `noindex`, `nosnippet` or restrictive `max-snippet` unless intended.
- [ ] One canonical URL per page; duplicates point to it.
- [ ] The main content is in the initial HTML, not only after JavaScript runs.
- [ ] The page is in the sitemap, and the sitemap returns XML, not an HTML fallback.
- [ ] Search Console and Bing Webmaster Tools are verified for the site, if it is a site.

## B. The front page or owner page

- [ ] The first sentence under the title says what this is, who it is for and what it does, in plain words.
- [ ] Each section that answers a question opens with a one-sentence answer.
- [ ] There is a FAQ written as people phrase questions to ChatGPT, Perplexity and Google.
- [ ] There is an evidence and limits section: what was tested, on what, and what was not shown.
- [ ] For a tool: a one-line install near the top.
- [ ] For a tool: a "what this changes on your machine" section listing files written, network calls and how to undo.
- [ ] A neutral alternatives section names other options fairly.
- [ ] Every number has a source or a stated method.
- [ ] No em dashes, en dashes or superlatives ("best", "ultimate", "leading", "revolutionary", "world-class"). Run `python scripts/check_front_page.py README.md` on a Markdown front page.
- [ ] Facts on the page match the fact registry (`python scripts/od.py facts validate`).

## C. Structured data (web pages only)

- [ ] `FAQPage` JSON-LD exists only where the same questions and answers are visible on the page.
- [ ] Tool pages carry `SoftwareApplication` JSON-LD with name, description, category, OS, offer price and a link to the code.
- [ ] Organization or Person markup names the same entity, with the same name and URL, as the profile and repo.
- [ ] The markup parses in the Schema Markup Validator (validator.schema.org).
- [ ] Nobody expects a Google FAQ rich result. Google stopped showing them on May 7, 2026.

## D. Entity consistency

- [ ] One canonical description exists in `templates/entity-record.yaml` or the project's own copy of it.
- [ ] The GitHub About line matches it word for word.
- [ ] The site's meta description and first paragraph match it.
- [ ] The author profile (GitHub bio, X, LinkedIn, personal site) uses the same project name and short form.
- [ ] Related repos by the same author link to this one with the same name and short form.
- [ ] Package registries (npm, PyPI, marketplace listings) use the same text.
- [ ] `CITATION.cff`, host metadata such as `agents/openai.yaml`, and the README H1 use the same project name.

## E. GitHub repository specifics

- [ ] The About line is set and under 350 characters.
- [ ] The website field points to a real project page, not back to the repo itself.
- [ ] Topics are 20 or fewer, each matches a term people search, and none are generic filler. Check a topic's size with `gh api "search/repositories?q=topic:<name>" -q .total_count`.
- [ ] A license is detected by GitHub.
- [ ] CI is green on the default branch and the badge links to it.
- [ ] There is a tagged release, and the README states which version the evidence refers to.
- [ ] The social preview image is set (repository settings; owner action).

## F. Off-site presence

- [ ] Searched Reddit for the target questions; noted which subreddits discuss them and their self-promotion rules.
- [ ] Listed curated awesome-lists that cover the category and read each one's contribution rules.
- [ ] Checked whether the project has ever been posted to Hacker News (`site:news.ycombinator.com <name>`).
- [ ] Any cross-posted articles on dev.to or Medium set a canonical URL back to the original.
- [ ] No fake accounts, vote requests, undisclosed affiliation or duplicate posts anywhere.

## G. Measurement baseline

- [ ] A citation log exists with at least one dated row per target question per engine (`templates/citation-log.csv`).
- [ ] GitHub traffic baseline saved: `gh api repos/<owner>/<repo>/traffic/views`, `.../traffic/clones` and `.../traffic/popular/referrers`. GitHub keeps only 14 days, so save it each time.
- [ ] Analytics or Search Console baseline saved for the site, if there is one.
- [ ] llms.txt status noted. It is optional housekeeping and is not scored here.

## Reporting

Report the checklist as a table with the section, item, status and evidence. List the failing items in the order of the repair layers in `references/execution-and-evidence.md`: access first, then routing, understanding and citability. A FAQ cannot fix a page that crawlers cannot reach.
