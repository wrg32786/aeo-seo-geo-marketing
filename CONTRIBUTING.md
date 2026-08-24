# Contributing

Contributions are welcome when they make Organic Discovery more accurate, executable, portable, or easier to verify.

## Good contributions

- Current official crawler, indexing, preview, product-feed, or reporting changes
- Reproducible bugs in the skill router, validator, references, or output contracts
- New vertical or regional adapters with clear boundaries
- Controlled experiments with raw observations, denominators, and fidelity checks
- Better trigger evals, examples, accessibility, security, or installation documentation
- Removal or downgrading of unsupported folklore

## Evidence requirements

Every material tactic or platform claim must identify:

- source URL or primary document;
- evidence class used by `references/evidence-and-tactics.md`;
- platform and exact surface;
- date checked;
- market, language, mode, and model when relevant;
- what the evidence establishes;
- what it does **not** establish.

A vendor score, Reddit post, repository README, or cross-sectional correlation cannot be promoted into a universal requirement.

## Workflow

1. Create a focused branch.
2. Make the smallest coherent change.
3. Update the relevant reference and `references/source-register.md` when doctrine changes.
4. Update `CHANGELOG.md` for material user-facing changes.
5. Run:

```bash
python scripts/validate_skill.py
```

6. Open a pull request describing the root cause, evidence boundary, validation, and rollback.

## Pull-request checklist

- [ ] The change solves a documented problem rather than adding speculative scope.
- [ ] Official platform behavior was rechecked when relevant.
- [ ] New claims have provenance and limits.
- [ ] API, web, app, Search, and assistant observations remain isolated.
- [ ] No ranking, citation, recommendation, or traffic guarantee was added.
- [ ] No fabricated statistics, reviews, quotes, dates, or consensus were added.
- [ ] Local links and referenced files resolve.
- [ ] Trigger evals still include positive and negative cases.
- [ ] `python scripts/validate_skill.py` passes.

## Security issues

Do not publish exploit details in a normal issue. Follow [`SECURITY.md`](SECURITY.md).
