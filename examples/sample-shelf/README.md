# Sample AI Shelf Fixture

This fixture proves the executable v0.5 Business Truth, exact-surface shelf mapping, and wedge-planning contracts without calling any external service.

The names and domains are synthetic. They are not product recommendations.

## Inputs

- `fact-registry.csv` — approved, approval-required, prohibited, independent, seller-controlled, unavailable, and nonexistent-offer cases.
- `observations.jsonl` — 22 preserved observations across separate ChatGPT Search and Gemini-style fixture surfaces.
- `candidates.json` — two defensible candidates and three candidates that must be rejected.

The observation set intentionally contains:

- an **open** narrow shelf;
- the same prompt family **locked** on another surface;
- a **locked** broad category shelf;
- a **fragmented** travel shelf;
- an **unsafe** health-related shelf;
- branded validation runs that must not enter unbranded recommendation-share denominators.

## Reproduce

```bash
python scripts/od.py facts validate examples/sample-shelf/fact-registry.csv \
  --output /tmp/od-shelf/facts.json

python scripts/od.py shelf map examples/sample-shelf/observations.jsonl \
  --facts examples/sample-shelf/fact-registry.csv \
  --output /tmp/od-shelf

python scripts/od.py wedge plan /tmp/od-shelf/shelf-map.json \
  --facts examples/sample-shelf/fact-registry.csv \
  --candidates examples/sample-shelf/candidates.json \
  --output /tmp/od-shelf/wedge-plan.json
```

Compare the generated files with `expected/`.

## Expected decisions

- `wedge-kindroot-sensitive-skin` — accepted on the open ChatGPT fixture surface; the locked Gemini fixture surface remains rejected.
- `wedge-kindroot-travel` — accepted for planning, with independent corroboration still required.
- `wedge-kindroot-broad` — rejected because the exact shelf is locked.
- `wedge-kindroot-eczema` — rejected because the shelf is unsafe and the required safety claim is prohibited.
- `wedge-ghost-product` — rejected because the offer does not exist, is unavailable, and has no matching shelf evidence.

No output contains an opaque GEO score or a fixed time-to-shelf promise.
