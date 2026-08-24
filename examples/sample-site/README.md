# Offline auditor example

This fixture is intentionally broken. It proves the v0.4 deterministic auditor from a clean checkout without network access.

Run from the repository root:

```bash
python scripts/od.py audit examples/sample-site/site/index.html \
  --output /tmp/organic-discovery-example
```

The committed `expected/` directory is regenerated with the same command and is compared byte-for-byte in `tests/test_od.py`.

## Intentional failures

- canonical points to the wrong deployed path;
- ChatGPT and Claude search crawlers are blocked while conventional search crawlers remain allowed;
- the core explanation is injected only after JavaScript runs;
- Product JSON-LD contains a product name, price, rating, and review count absent from visible HTML;
- numeric, performance, and trust claims have no visible provenance;
- hidden content and an HTML comment contain prompt-like manipulation instructions;
- the sitemap omits the canonical target;
- duplicate H1s, heading-level skips, an unnamed link, a missing image alt, missing language, missing description, and missing viewport metadata demonstrate lower-priority checks.

The result must preserve retrieval, context allocation, source selection, absorption, and behavior as `unknown`. A local page audit cannot prove those downstream outcomes.
