# Contributing

Contributions are welcome when they make Organic Discovery more accurate, executable, portable, safe, or easier to verify.

## Good contributions

- Current official crawler, indexing, preview, product-feed, or reporting changes
- Reproducible bugs in the auditor, fact validator, shelf mapper, wedge planner, skill router, validator, references, or output contracts
- Better schemas, exact-surface grouping, null handling, hard gates, metrics, or deterministic reports
- Controlled experiments with raw observations, denominators, fidelity checks, and explicit boundaries
- New vertical or regional adapters with clear limits
- Better examples, accessibility, security, tests, or installation documentation
- Removal or downgrading of unsupported folklore

## Evidence requirements

Every material tactic or platform claim must identify:

- source URL or primary document;
- evidence class from `references/evidence-and-tactics.md`;
- platform and exact surface;
- date checked;
- market, language, mode, and model when relevant;
- what the evidence establishes;
- what it does **not** establish.

A vendor score, Reddit post, repository README, benchmark, or correlation cannot become a universal requirement.

## Deterministic contract rules

- Preserve `null` and `unknown`; do not manufacture denominators.
- Keep exact-surface dimensions separate.
- Exclude branded validation from unbranded recommendation share.
- Keep seller-controlled and independent evidence distinguishable.
- Do not soften a hard rejection into a lower planning score.
- Any schema change must update its fixture, tests, docs, and version boundary.
- Legacy v0.4 audit artifacts remain versioned independently unless their own contract changes.

## Workflow

1. Create a focused branch.
2. Make the smallest coherent change.
3. Update the relevant reference and `references/source-register.md` when doctrine changes.
4. Update `CHANGELOG.md` for material user-facing changes.
5. Run:

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
```

6. Open a pull request describing the root cause, contract changes, evidence boundary, validation, and rollback.

## Pull-request checklist

- [ ] The change solves a documented problem rather than adding speculative scope.
- [ ] Official platform behavior was rechecked when relevant.
- [ ] New claims have provenance and limits.
- [ ] Exact surfaces remain isolated.
- [ ] Branded prompts remain excluded from unbranded share.
- [ ] Unsupported, unavailable, unsafe, prohibited, or locked opportunities still fail hard gates.
- [ ] No ranking, citation, recommendation, traffic, revenue, or timing guarantee was added.
- [ ] No fabricated statistics, reviews, quotes, dates, products, or consensus were added.
- [ ] Local links, schemas, JSON, and JSONL are valid.
- [ ] Both offline examples reproduce byte-for-byte.
- [ ] Trigger evals include positive and negative cases.
- [ ] Python 3.11 and 3.13 CI pass.

## Security issues

Do not publish exploit details in a normal issue. Follow [`SECURITY.md`](SECURITY.md).
