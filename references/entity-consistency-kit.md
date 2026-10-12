# Entity Consistency Kit

Use this module to make every surface you control describe the project the same way. The short answer: write one canonical description, store it in one file, and paste it word for word into the GitHub About line, the site, the profile and every related repo.

Answer engines and search systems combine what many pages say about an entity. When the repo says one thing, the site another and the profile a third, the summary they build is vaguer and more likely to be wrong. Consistency does not create authority by itself. It removes a cause of confusion and makes accurate descriptions easier to repeat. See also section 6 of `references/source-earning.md`, which this kit extends.

## 1. Write the canonical record

Copy `templates/entity-record.yaml` into the project and fill it. The fields that matter most:

- `name`: one project name. Pick it once. If the repo slug differs, record the slug as an alternate name.
- `canonical_description`: one sentence, under 350 characters (the GitHub About limit). It says what it is, for whom, and the main job.
- `short_description`: under 120 characters, for bios, social cards, package registries and host metadata.
- `category_terms`: three to six words people search for, in their words.
- `canonical_url`: the one URL you want cited. For a project with a site, use the site page. For a repo-only project, use the repo URL.
- `author`: the name exactly as it appears on the profile.
- `surfaces`: every place the description should appear, with its current text and status.

Run the record past the fact registry. The description is a public claim like any other.

## 2. Write the description

Pattern:

```text
{Name}: {category} for {audience}. It {does the main job} {with the main constraint}. {License}, {runtime or install fact}.
```

Rules:

- no superlatives, no "AI-powered" filler, no em dashes;
- name the category in searched terms (for example "SEO, AEO and GEO" and "Agent Skill");
- state one checkable fact (license, runtime, what it writes);
- the same sentence everywhere. Do not paraphrase per surface.

## 3. Surfaces to update

| Surface | Field | Who can change it |
|---|---|---|
| GitHub repo | About description | Owner, in repository settings or `gh repo edit --description` |
| GitHub repo | Website field | Owner |
| GitHub repo | Topics | Owner, `gh repo edit --add-topic` |
| README | H1 and first paragraph | Pull request |
| Project site | `<title>`, meta description, first paragraph, `SoftwareApplication.description` | Site deploy |
| Author profile | GitHub bio, pinned repo, X, LinkedIn, personal site | Owner |
| Related repos | Any README section that links here | Pull request in each repo |
| Package registries | npm, PyPI, marketplace, skill catalogs | Publish step |
| Repo metadata | `CITATION.cff` title and abstract, host files such as `agents/openai.yaml` | Pull request |
| Articles | dev.to, Medium, blog posts that introduce the project | Author edit |

Repository settings, profiles and third-party listings are changes outside the repo. An agent drafts them; the owner applies them.

## 4. Check for drift

Each quarter, or after a rename or a major release:

1. Fetch each surface and copy its current text into the `surfaces` list.
2. Mark each `match`, `drift` or `missing`.
3. Fix drift at the source of truth first (the entity record), then propagate.
4. Ask each target engine the branded question ("What is {name}?") and check that the answer uses the current description. Log it in the citation log as a branded accuracy check.

## 5. Related repos and cross-links

- Each related repo by the same author should mention this one with the same name and short description, in a "Related projects" section.
- Link with descriptive text ("Organic Discovery, an SEO, AEO and GEO Agent Skill"), not "click here".
- Do not add cross-links where the projects have nothing to do with each other.

## 6. What not to do

- Do not stuff the description with every keyword. One sentence, the real category.
- Do not invent alternate names to capture more queries.
- Do not create profiles or listings you will not maintain. A stale listing is a source of wrong facts.
