# Contributing

Contributions are welcome when they make Organic Discovery more accurate, executable, portable, secure, or easier to verify.

## Good contributions

- Reproducible auditor bugs with a small HTML fixture
- Safer bounded-fetch behavior and redirect/private-network tests
- Deterministic checks that map to a real user or platform failure
- Current official crawler, indexing, preview, feed, or reporting changes
- Better output contracts, trigger evals, examples, accessibility, or installation documentation
- Controlled experiments with raw observations, denominators, and fidelity checks
- Removal or downgrading of unsupported folklore

## Evidence requirements

Every material tactic or platform claim identifies its source, evidence class, exact platform/surface, date checked, market or mode when relevant, what it establishes, and what it does not establish.

A vendor score, Reddit post, repository README, or correlation cannot become a universal requirement.

## Workflow

1. Create a focused branch.
2. Make the smallest coherent change.
3. Add or update one fixture/test for non-trivial auditor logic.
4. Regenerate expected artifacts through `scripts/od.py`; do not hand-edit them.
5. Update the relevant reference and `references/source-register.md` when doctrine changes.
6. Update every versioned artifact for a release.
7. Run:

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/od.py audit examples/sample-site/site/index.html --output /tmp/od-example
```

8. Open a pull request describing root cause, evidence boundary, security impact, validation, delayed outcomes, and rollback.

## Pull-request checklist

- [ ] The change solves a documented problem rather than adding speculative scope.
- [ ] Standard library or existing code was reused before adding a dependency.
- [ ] Remote fetch safety is preserved when networking changes.
- [ ] New deterministic logic has one focused check.
- [ ] Expected artifacts were regenerated and intentionally reviewed.
- [ ] Official platform behavior was rechecked when relevant.
- [ ] New claims have provenance and limits.
- [ ] API, web, app, Search, and assistant observations remain isolated.
- [ ] No ranking, citation, recommendation, or traffic guarantee was added.
- [ ] No fabricated statistics, reviews, quotes, dates, or consensus were added.
- [ ] Local links and referenced files resolve.
- [ ] Trigger evals still include positive and negative cases.
- [ ] Validation, tests, and the offline example pass.

## Security issues

Do not publish exploit details in a normal issue. Follow [`SECURITY.md`](SECURITY.md).
