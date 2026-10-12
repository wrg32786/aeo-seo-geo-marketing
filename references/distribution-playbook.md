# Distribution Playbook

Use this module after the owner page is fixed and the canonical description is set. The short answer: get the project mentioned, accurately and with disclosure, in the places answer engines and people already read, and follow each venue's own written rules every time.

Every public post or submission in this module is drafted by the agent and published by a human. Record each one in `templates/distribution-log.csv`. Do not post the same text to several venues; write for each audience.

The ethical rules in `references/source-earning.md` apply in full: no fake accounts, no bought or borrowed accounts, no vote requests, no undisclosed affiliation, no near-duplicate posts.

## 0. Order of work

1. Owner page and canonical description first. A link to a weak page wastes the mention.
2. GitHub topics, because they cost nothing and are owner-controlled.
3. Long-form write-up on your own site or blog, then dev.to and Medium copies with a canonical URL.
4. Answers in existing Reddit and forum threads where the project genuinely answers the question.
5. Show HN once the project is something people can run in a few minutes.
6. Awesome-list submissions when the project meets each list's stated bar.

## 1. GitHub topics

- GitHub allows up to 20 topics per repository; names are lowercase letters, numbers and hyphens, 50 characters or fewer. [GitHub Docs](https://docs.github.com/articles/classifying-your-repository-with-topics)
- Pick topics people actually browse and search. Check the size of a topic before choosing it:

```bash
gh api "search/repositories?q=topic:generative-engine-optimization" -q .total_count
```

- Prefer specific terms that match your category ("generative-engine-optimization", "claude-code-skills") over generic ones ("agents", "open-source").
- Watch for ambiguous topics. "geo" is also used by geospatial projects.
- Topics are a repository setting. Propose them in the pull request; the owner applies them with `gh repo edit --add-topic` and `--remove-topic`.

## 2. Reddit, by subreddit rules

Reddit's role in AI answers varies a lot by engine and over time (see the evidence notes in `references/playbook.md`). Use it because the audience is there, and treat any citation effect as a bonus to be measured.

Before any post or comment:

1. Read the subreddit's sidebar rules, wiki and pinned posts. Note self-promotion rules, link rules, required flair and any "showcase" day or weekly thread.
2. Search the subreddit for the target question. An answer in an existing thread is usually better than a new post.
3. Check whether the account has a real history in that community. A new account that only posts its own link reads as spam.
4. If the rules ban self-promotion, do not post the project. You can still answer the question without the link.

A good contribution:

- answers the question in the comment itself, so it is useful even if nobody clicks;
- says plainly "I made this" or "I maintain this";
- links once, to the canonical URL, without tracking parameters unless the community allows them;
- mentions limits and alternatives;
- is written by a person in their own voice. Several subreddits remove text that reads as machine-written, and readers downvote it.

Record the subreddit, rule checked, URL, date, and whether moderators kept or removed it.

## 3. Curated awesome-lists, through their own process

Each list sets its own bar and its own submission path. Read the list's `CONTRIBUTING.md` and issue templates before submitting, every time; they change.

Examples checked on 2026-10-11 (re-check before use):

| List | How to submit | Stated bar |
|---|---|---|
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Web UI issue form only; PRs are not the path | At least 14 days old with signs of active development, or at least 100 stars; one resource at a time |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Pull request | About 10 stars or more ("social proof"); PRs must not be explicitly AI-generated or AI-submitted |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | Pull request titled `Add skill: author/skill-name` | Real community usage; brand-new skills are declined; description of 10 words or fewer |
| [amplifying-ai/awesome-generative-engine-optimization](https://github.com/amplifying-ai/awesome-generative-engine-optimization) | The README asks for pull requests and links a CONTRIBUTING.md that was missing from the repo when checked | No written bar found; ask in an issue first if unsure |

Rules for this repo's own submissions:

- one list at a time, one entry per submission;
- use the list's exact entry format and the canonical short description;
- if the project does not meet the bar yet, do not submit. Come back when it does;
- a list maintained by the same author is not independent corroboration. It is fine to list the project there, but do not count it as an earned mention.

## 4. Hacker News

- Show HN is for something people can run or hold. Blog posts, sign-up pages and lists are not Show HN; post them as regular submissions. Do not ask friends to upvote or comment. [Show HN guidelines](https://news.ycombinator.com/showhn.html)
- The post title starts with "Show HN:" and says what it is in plain words.
- Be around to answer comments for the first few hours. Answer criticism with facts and limits.
- Minor version bumps are generally not substantive enough for a new Show HN.
- One submission. If it does not take off, do not resubmit the same link repeatedly.

## 5. dev.to and Medium with canonical URLs

Publish the full write-up on your own site first, then syndicate.

- **dev.to:** in the Markdown front matter add `canonical_url: https://your-site/original-post`. In the rich editor, the canonical URL is in the post settings. [DEV editor guide](https://dev.to/p/editor_guide)
- **Medium:** use Medium's "Import a story" feature, which sets the canonical link to the original URL, or set the original URL in the story's advanced settings. Check the published page source for `rel="canonical"` after publishing.
- Keep the opening paragraph identical to the owner page opener, so the canonical description repeats.
- End with a link to the repo and the site, using the canonical name.

If there is no site, the README can be the canonical source, but a site page that carries JSON-LD is a stronger home.

## 6. Other places worth checking

Only where the audience is real and the rules allow it: Stack Overflow answers (no link-only answers), relevant Discord or Slack communities (read the promotion channel rules), the project's own GitHub Discussions, newsletters in the niche, and podcasts. Agent Skill catalogs and marketplaces are listings; keep their text identical to the entity record.

## 7. Distribution log

Fill `templates/distribution-log.csv` for every draft and post:

```text
date, venue, community_or_list, rule_checked_url, rule_summary, draft_path,
approved_by, published_url, disclosure_included, canonical_url_used,
moderator_outcome, referrals_7d, cited_in_ai_answer, notes
```

A post that was removed, ignored or drew no referrals is still a row. Failed attempts are how you learn which venues are worth the time.
