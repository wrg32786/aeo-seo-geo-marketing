"""Exact-surface AI shelf mapping and defensible wedge planning."""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from od_truth import (
    INDEPENDENT_TYPES,
    SELLER_CONTROLLED_TYPES,
    TruthError,
    fact_index,
    validate_fact_registry,
)

OBSERVATION_SCHEMA_VERSION = "organic-discovery/observations/1.0"
SHELF_SCHEMA_VERSION = "organic-discovery/shelf-map/1.0"
WEDGE_SCHEMA_VERSION = "organic-discovery/wedge-plan/1.0"

OBSERVATION_SCHEMA = "schemas/observation.schema.json"
SHELF_MAP_SCHEMA = "schemas/shelf-map.schema.json"
WEDGE_PLAN_SCHEMA = "schemas/wedge-plan.schema.json"

EXACT_DIMENSIONS = (
    "platform",
    "surface",
    "mode",
    "model",
    "market",
    "language",
    "device",
    "account_state",
    "session_state",
    "prompt_family",
    "target_entity_id",
    "branded",
)

MIN_CLASSIFICATION_RUNS = 4
UNSAFE_MIN_EVALUABLE = 3
LOCKED_TOP_FIRST_SHARE = 0.70
LOCKED_TOP_RECOMMENDATION_RATE = 0.75
LOCKED_AGREEMENT = 0.60
OPEN_RECOMMENDATION_COVERAGE = 0.80
OPEN_TOP_FIRST_SHARE = 0.40
OPEN_AGREEMENT = 0.35
FRAGMENTED_AGREEMENT = 0.50
UNSAFE_MIN_FIDELITY = 0.75
UNSAFE_MIN_CONSTRAINT_SATISFACTION = 0.75
UNSAFE_MAX_UNAVAILABLE_RATE = 0.20

ALLOWED_SOURCE_TYPES = {
    "first_party",
    "seller_controlled",
    "independent_editorial",
    "official_registry",
    "customer_authorized",
    "community",
    "internal_record",
    "other",
    "unknown",
}
SELLER_SOURCE_TYPES = {"first_party", "seller_controlled", "internal_record"}
INDEPENDENT_SOURCE_TYPES = {"independent_editorial", "official_registry", "customer_authorized"}


class ShelfError(RuntimeError):
    """Expected observation or planning error suitable for a concise CLI message."""


def _clean(value: Any) -> str:
    return "" if value is None else " ".join(str(value).strip().split())


def _round(value: float | None) -> float | None:
    return None if value is None else round(value, 4)


def _rate(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else _round(numerator / denominator)


def _mean(values: Iterable[float]) -> float | None:
    items = list(values)
    return None if not items else _round(sum(items) / len(items))


def _pairwise_jaccard(sets: list[set[str]]) -> float | None:
    if len(sets) < 2:
        return None
    scores: list[float] = []
    for index, left in enumerate(sets):
        for right in sets[index + 1 :]:
            union = left | right
            scores.append(1.0 if not union else len(left & right) / len(union))
    return _mean(scores)


def _parse_timestamp(value: Any, *, run_id: str, errors: list[str]) -> str | None:
    text = _clean(value)
    if not text:
        errors.append(f"{run_id}: timestamp is required")
        return None
    # A strict-enough ISO boundary without introducing a dependency.
    candidate = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        from datetime import datetime

        return datetime.fromisoformat(candidate).isoformat().replace("+00:00", "Z")
    except ValueError:
        errors.append(f"{run_id}: timestamp must be ISO 8601")
        return None


def _bool_or_none(value: Any, *, field: str, run_id: str, errors: list[str]) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    errors.append(f"{run_id}: {field} must be boolean or null")
    return None


def _list_or_none(value: Any, *, field: str, run_id: str, errors: list[str]) -> list[Any] | None:
    if value is None:
        return None
    if isinstance(value, list):
        return value
    errors.append(f"{run_id}: {field} must be an array or null")
    return None


def _domain(url: str) -> str | None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None
    return parsed.hostname.casefold().removeprefix("www.")


def _normalize_recommendations(value: Any, *, run_id: str, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        errors.append(f"{run_id}: recommendations must be an array")
        return []
    output: list[dict[str, Any]] = []
    positions: set[int] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{run_id}: recommendation {index} must be an object")
            continue
        entity_id = _clean(item.get("entity_id") or item.get("entity"))
        if not entity_id:
            errors.append(f"{run_id}: recommendation {index} requires entity_id")
            continue
        position = item.get("position")
        if not isinstance(position, int) or isinstance(position, bool) or position < 1:
            errors.append(f"{run_id}: recommendation {index} position must be a positive integer")
            continue
        if position in positions:
            errors.append(f"{run_id}: recommendation positions must be unique")
            continue
        positions.add(position)
        constraint_satisfied = _bool_or_none(
            item.get("constraint_satisfied"),
            field=f"recommendations[{index}].constraint_satisfied",
            run_id=run_id,
            errors=errors,
        )
        available = _bool_or_none(
            item.get("available"),
            field=f"recommendations[{index}].available",
            run_id=run_id,
            errors=errors,
        )
        output.append(
            {
                "entity_id": entity_id,
                "entity": _clean(item.get("entity")) or entity_id,
                "position": position,
                "constraint_satisfied": constraint_satisfied,
                "available": available,
            }
        )
    return sorted(output, key=lambda item: (item["position"], item["entity_id"]))


def _normalize_citations(value: Any, *, run_id: str, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        errors.append(f"{run_id}: citations must be an array")
        return []
    output: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{run_id}: citation {index} must be an object")
            continue
        url = _clean(item.get("url"))
        domain = _domain(url)
        if domain is None:
            errors.append(f"{run_id}: citation {index} requires a public http(s) URL")
            continue
        source_type = _clean(item.get("source_type") or "unknown").casefold()
        if source_type not in ALLOWED_SOURCE_TYPES:
            errors.append(f"{run_id}: citation {index} has unsupported source_type {source_type!r}")
            continue
        position = item.get("position")
        if position is not None and (not isinstance(position, int) or isinstance(position, bool) or position < 1):
            errors.append(f"{run_id}: citation {index} position must be a positive integer or null")
            position = None
        output.append(
            {
                "url": url,
                "domain": domain,
                "source_type": source_type,
                "entity_id": _clean(item.get("entity_id")) or None,
                "position": position,
            }
        )
    return sorted(output, key=lambda item: (item["position"] is None, item["position"] or 0, item["url"]))


def normalize_observation(raw: dict[str, Any], *, line_number: int) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    run_id = _clean(raw.get("run_id")) or f"line-{line_number}"
    required_strings = (
        "run_id",
        "platform",
        "surface",
        "mode",
        "market",
        "language",
        "device",
        "account_state",
        "session_state",
        "prompt_id",
        "prompt_family",
        "prompt",
        "target_entity_id",
    )
    values: dict[str, str] = {}
    for field in required_strings:
        values[field] = _clean(raw.get(field))
        if not values[field]:
            errors.append(f"{run_id}: {field} is required")
    if not isinstance(raw.get("branded"), bool):
        errors.append(f"{run_id}: branded must be boolean")

    timestamp = _parse_timestamp(raw.get("timestamp"), run_id=run_id, errors=errors)
    recommendations = _normalize_recommendations(raw.get("recommendations"), run_id=run_id, errors=errors)
    citations = _normalize_citations(raw.get("citations"), run_id=run_id, errors=errors)

    fidelity_issues = _list_or_none(raw.get("fidelity_issues"), field="fidelity_issues", run_id=run_id, errors=errors)
    constraint_violations = _list_or_none(
        raw.get("constraint_violations"),
        field="constraint_violations",
        run_id=run_id,
        errors=errors,
    )
    target_claims_used = _list_or_none(
        raw.get("target_claims_used"),
        field="target_claims_used",
        run_id=run_id,
        errors=errors,
    )
    search_queries = _list_or_none(raw.get("search_queries"), field="search_queries", run_id=run_id, errors=errors)

    normalized = {
        "run_id": values["run_id"],
        "timestamp": timestamp,
        "platform": values["platform"].casefold(),
        "surface": values["surface"].casefold(),
        "mode": values["mode"].casefold(),
        "model": _clean(raw.get("model")) or None,
        "market": values["market"],
        "language": values["language"].casefold(),
        "device": values["device"].casefold(),
        "account_state": values["account_state"].casefold(),
        "session_state": values["session_state"].casefold(),
        "prompt_id": values["prompt_id"],
        "prompt_family": values["prompt_family"],
        "prompt": values["prompt"],
        "intent": _clean(raw.get("intent")).casefold() or None,
        "branded": raw.get("branded") if isinstance(raw.get("branded"), bool) else None,
        "target_entity_id": values["target_entity_id"],
        "search_triggered": _bool_or_none(
            raw.get("search_triggered"),
            field="search_triggered",
            run_id=run_id,
            errors=errors,
        ),
        "search_queries": [_clean(item) for item in search_queries] if search_queries is not None else None,
        "recommendations": recommendations,
        "citations": citations,
        "target_retrieved": _bool_or_none(
            raw.get("target_retrieved"),
            field="target_retrieved",
            run_id=run_id,
            errors=errors,
        ),
        "target_cited": _bool_or_none(
            raw.get("target_cited"),
            field="target_cited",
            run_id=run_id,
            errors=errors,
        ),
        "target_claims_used": [_clean(item) for item in target_claims_used] if target_claims_used is not None else None,
        "fidelity_issues": [_clean(item) for item in fidelity_issues] if fidelity_issues is not None else None,
        "constraint_violations": [_clean(item) for item in constraint_violations] if constraint_violations is not None else None,
        "answer": raw.get("answer") if isinstance(raw.get("answer"), str) else None,
        "notes": _clean(raw.get("notes")) or None,
        "line_number": line_number,
    }
    return (None if errors else normalized), errors


def load_observations(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        raise ShelfError(f"cannot read observations {path}: {exc}") from exc
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(raw, dict):
            errors.append(f"line {line_number}: observation must be an object")
            continue
        record, row_errors = normalize_observation(raw, line_number=line_number)
        errors.extend(row_errors)
        if record is None:
            continue
        if record["run_id"] in seen:
            errors.append(f"{record['run_id']}: run_id must be unique")
            continue
        seen.add(record["run_id"])
        records.append(record)
    if errors:
        preview = "\n".join(f"- {message}" for message in errors[:20])
        suffix = "" if len(errors) <= 20 else f"\n- ... {len(errors) - 20} more"
        raise ShelfError(f"observation validation failed:\n{preview}{suffix}")
    if not records:
        raise ShelfError("observation file contains no records")
    return sorted(records, key=lambda item: item["run_id"])


def _group_id(dimensions: dict[str, Any]) -> str:
    payload = json.dumps(dimensions, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    return f"surface-{digest}"


def _group_dimensions(record: dict[str, Any]) -> dict[str, Any]:
    return {dimension: record[dimension] for dimension in EXACT_DIMENSIONS}


def _confidence(run_count: int) -> str:
    if run_count >= 12:
        return "high"
    if run_count >= 6:
        return "medium"
    return "low"


def _classify(metrics: dict[str, Any], *, branded: bool) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if branded:
        return "unknown", ["branded validation group; excluded from unbranded shelf classification"]

    runs = metrics["runs"]
    fidelity = metrics["fidelity"]
    constraints = metrics["constraint_satisfaction"]
    availability = metrics["recommendation_availability"]

    if (
        fidelity["denominator"] >= UNSAFE_MIN_EVALUABLE
        and fidelity["rate"] is not None
        and fidelity["rate"] < UNSAFE_MIN_FIDELITY
    ):
        reasons.append(
            f"fidelity rate {fidelity['rate']:.2f} is below {UNSAFE_MIN_FIDELITY:.2f}"
        )
    if (
        constraints["denominator"] >= UNSAFE_MIN_EVALUABLE
        and constraints["rate"] is not None
        and constraints["rate"] < UNSAFE_MIN_CONSTRAINT_SATISFACTION
    ):
        reasons.append(
            f"constraint satisfaction {constraints['rate']:.2f} is below {UNSAFE_MIN_CONSTRAINT_SATISFACTION:.2f}"
        )
    if (
        availability["denominator"] >= UNSAFE_MIN_EVALUABLE
        and availability["unavailable_rate"] is not None
        and availability["unavailable_rate"] > UNSAFE_MAX_UNAVAILABLE_RATE
    ):
        reasons.append(
            f"unavailable recommendation rate {availability['unavailable_rate']:.2f} exceeds {UNSAFE_MAX_UNAVAILABLE_RATE:.2f}"
        )
    if reasons:
        return "unsafe", reasons

    if runs < MIN_CLASSIFICATION_RUNS:
        return "unknown", [f"{runs} runs; at least {MIN_CLASSIFICATION_RUNS} required for classification"]

    coverage = metrics["recommendation_coverage"]["rate"]
    top_first = metrics["incumbent_concentration"]["top_first_mentioned_share"]
    top_recommendation = metrics["incumbent_concentration"]["top_entity_recommendation_rate"]
    agreement = metrics["recommendation_set_agreement"]
    unique_first = metrics["incumbent_concentration"]["unique_first_entities"]

    if (
        top_first is not None
        and top_recommendation is not None
        and agreement is not None
        and top_first >= LOCKED_TOP_FIRST_SHARE
        and top_recommendation >= LOCKED_TOP_RECOMMENDATION_RATE
        and agreement >= LOCKED_AGREEMENT
    ):
        return "locked", [
            f"top first-mentioned share={top_first:.2f}",
            f"top entity recommendation rate={top_recommendation:.2f}",
            f"set agreement={agreement:.2f}",
        ]

    if coverage is not None and coverage < OPEN_RECOMMENDATION_COVERAGE:
        return "open", [
            f"recommendation coverage={coverage:.2f}",
            f"top first-mentioned share={(top_first or 0.0):.2f}",
            f"set agreement={(agreement or 0.0):.2f}",
        ]

    if unique_first >= 3 and agreement is not None and agreement < FRAGMENTED_AGREEMENT:
        return "fragmented", [
            f"{unique_first} distinct first-mentioned entities",
            f"set agreement={agreement:.2f}",
        ]

    if (
        coverage is not None
        and (top_first or 0.0) < OPEN_TOP_FIRST_SHARE
        and (agreement if agreement is not None else 0.0) < OPEN_AGREEMENT
    ):
        return "open", [
            f"recommendation coverage={coverage:.2f}",
            f"top first-mentioned share={(top_first or 0.0):.2f}",
            f"set agreement={(agreement or 0.0):.2f}",
        ]

    if metrics["incumbent_concentration"]["unique_recommended_entities"] >= 2:
        return "contested", [
            f"{metrics['incumbent_concentration']['unique_recommended_entities']} entities recur without a locked leader"
        ]

    return "unknown", ["insufficient recommendation diversity or observable evidence"]


def _fact_support(
    *,
    facts_report: dict[str, Any] | None,
    target_entity_id: str,
    prompt_family: str,
) -> dict[str, Any]:
    if facts_report is None:
        return {
            "status": "unknown",
            "publishable_fact_ids": [],
            "blocked_fact_ids": [],
            "independent_fact_ids": [],
            "seller_controlled_fact_ids": [],
            "offer_exists": None,
            "availability": None,
            "limitations_present": None,
            "gate_failures": ["no fact registry supplied"],
        }
    facts = [
        fact
        for fact in facts_report.get("facts", [])
        if fact["entity_id"] == target_entity_id
        and (not fact["prompt_families"] or prompt_family in fact["prompt_families"])
    ]
    publishable_ids = set(facts_report.get("publishable_fact_ids", []))
    publishable = [fact for fact in facts if fact["claim_id"] in publishable_ids]
    blocked = [fact for fact in facts if fact["claim_id"] not in publishable_ids]
    existence = [fact for fact in publishable if fact["claim_type"] == "existence"]
    availability_facts = [fact for fact in publishable if fact["claim_type"] == "availability"]
    fit = [
        fact
        for fact in publishable
        if fact["claim_type"]
        in {
            "offer_fit",
            "feature",
            "ingredient",
            "compatibility",
            "service_area",
            "performance",
            "price",
        }
    ]
    gate_failures: list[str] = []
    offer_exists = any(fact["offer_exists"] is True for fact in existence or publishable)
    available_values = {fact["availability"] for fact in availability_facts or publishable}
    availability = (
        "available"
        if "available" in available_values
        else "limited"
        if "limited" in available_values
        else "preorder"
        if "preorder" in available_values
        else "unavailable"
        if "unavailable" in available_values
        else "unknown"
    )
    if not offer_exists:
        gate_failures.append("no publishable fact confirms that the offer exists")
    if availability not in {"available", "limited", "preorder"}:
        gate_failures.append("no publishable fact confirms current availability")
    if not fit:
        gate_failures.append("no publishable fact establishes fit for this prompt family")
    prohibited = [fact for fact in blocked if fact["publish_status"] == "prohibited"]
    if prohibited:
        gate_failures.append("one or more prompt-family facts are prohibited")
    return {
        "status": "pass" if not gate_failures else "blocked",
        "publishable_fact_ids": sorted(fact["claim_id"] for fact in publishable),
        "blocked_fact_ids": sorted(fact["claim_id"] for fact in blocked),
        "independent_fact_ids": sorted(
            fact["claim_id"] for fact in publishable if fact["source_control"] == "independent"
        ),
        "seller_controlled_fact_ids": sorted(
            fact["claim_id"] for fact in publishable if fact["source_control"] == "seller_controlled"
        ),
        "offer_exists": offer_exists,
        "availability": availability,
        "limitations_present": any(bool(fact["limitations"]) for fact in publishable),
        "gate_failures": gate_failures,
    }


def _group_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    runs = len(records)
    recommendation_sets = [
        {item["entity_id"] for item in record["recommendations"]} for record in records
    ]
    citation_domain_sets = [{item["domain"] for item in record["citations"]} for record in records]
    coverage_n = sum(bool(items) for items in recommendation_sets)

    recommended_run_counts: Counter[str] = Counter()
    first_counts: Counter[str] = Counter()
    positions: defaultdict[str, list[int]] = defaultdict(list)
    for record in records:
        seen: set[str] = set()
        for item in record["recommendations"]:
            positions[item["entity_id"]].append(item["position"])
            seen.add(item["entity_id"])
        recommended_run_counts.update(seen)
        if record["recommendations"]:
            first = min(record["recommendations"], key=lambda item: item["position"])
            first_counts[first["entity_id"]] += 1

    entity_ids = sorted(recommended_run_counts)
    entity_stats = []
    for entity_id in entity_ids:
        entity_stats.append(
            {
                "entity_id": entity_id,
                "recommendation_runs": recommended_run_counts[entity_id],
                "recommendation_rate": _rate(recommended_run_counts[entity_id], runs),
                "first_mentioned_runs": first_counts[entity_id],
                "first_mentioned_share": _rate(first_counts[entity_id], runs),
                "mean_position": _round(statistics.fmean(positions[entity_id])),
            }
        )
    entity_stats.sort(
        key=lambda item: (
            -(item["first_mentioned_share"] or 0.0),
            -(item["recommendation_rate"] or 0.0),
            item["entity_id"],
        )
    )
    top = entity_stats[0] if entity_stats else None

    search_known = [record["search_triggered"] for record in records if record["search_triggered"] is not None]
    retrieved_known = [record["target_retrieved"] for record in records if record["target_retrieved"] is not None]
    cited_known = [record["target_cited"] for record in records if record["target_cited"] is not None]
    fidelity_known = [record["fidelity_issues"] for record in records if record["fidelity_issues"] is not None]
    constraint_known = [
        record["constraint_violations"]
        for record in records
        if record["constraint_violations"] is not None
    ]
    recommendation_constraint_values = [
        item["constraint_satisfied"]
        for record in records
        for item in record["recommendations"]
        if item["constraint_satisfied"] is not None
    ]
    availability_values = [
        item["available"]
        for record in records
        for item in record["recommendations"]
        if item["available"] is not None
    ]

    source_mix: Counter[str] = Counter(
        item["source_type"] for record in records for item in record["citations"]
    )
    citation_total = sum(source_mix.values())
    seller_citations = sum(source_mix[source] for source in SELLER_SOURCE_TYPES)
    independent_citations = sum(source_mix[source] for source in INDEPENDENT_SOURCE_TYPES)
    target_entity_id = records[0]["target_entity_id"]
    target_recommendation_n = sum(
        any(item["entity_id"] == target_entity_id for item in record["recommendations"])
        for record in records
    )
    target_first_n = sum(
        bool(record["recommendations"])
        and min(record["recommendations"], key=lambda item: item["position"])["entity_id"]
        == target_entity_id
        for record in records
    )

    agreement = _pairwise_jaccard(recommendation_sets)
    return {
        "runs": runs,
        "recommendation_coverage": {
            "numerator": coverage_n,
            "denominator": runs,
            "rate": _rate(coverage_n, runs),
        },
        "search_activation": {
            "numerator": sum(value is True for value in search_known),
            "denominator": len(search_known),
            "rate": _rate(sum(value is True for value in search_known), len(search_known)),
        },
        "target_retrieval": {
            "numerator": sum(value is True for value in retrieved_known),
            "denominator": len(retrieved_known),
            "rate": _rate(sum(value is True for value in retrieved_known), len(retrieved_known)),
        },
        "target_citation": {
            "numerator": sum(value is True for value in cited_known),
            "denominator": len(cited_known),
            "rate": _rate(sum(value is True for value in cited_known), len(cited_known)),
        },
        "target_recommendation": {
            "numerator": target_recommendation_n,
            "denominator": runs,
            "rate": _rate(target_recommendation_n, runs),
        },
        "target_first_mentioned": {
            "numerator": target_first_n,
            "denominator": runs,
            "rate": _rate(target_first_n, runs),
        },
        "fidelity": {
            "numerator": sum(not issues for issues in fidelity_known),
            "denominator": len(fidelity_known),
            "rate": _rate(sum(not issues for issues in fidelity_known), len(fidelity_known)),
        },
        "constraint_satisfaction": {
            "numerator": sum(not issues for issues in constraint_known),
            "denominator": len(constraint_known),
            "rate": _rate(sum(not issues for issues in constraint_known), len(constraint_known)),
        },
        "recommendation_constraint_satisfaction": {
            "numerator": sum(value is True for value in recommendation_constraint_values),
            "denominator": len(recommendation_constraint_values),
            "rate": _rate(
                sum(value is True for value in recommendation_constraint_values),
                len(recommendation_constraint_values),
            ),
        },
        "recommendation_availability": {
            "available_numerator": sum(value is True for value in availability_values),
            "unavailable_numerator": sum(value is False for value in availability_values),
            "denominator": len(availability_values),
            "available_rate": _rate(sum(value is True for value in availability_values), len(availability_values)),
            "unavailable_rate": _rate(sum(value is False for value in availability_values), len(availability_values)),
        },
        "recommendation_set_agreement": agreement,
        "volatility": None if agreement is None else _round(1.0 - agreement),
        "citation_source_overlap": _pairwise_jaccard(citation_domain_sets),
        "source_mix": dict(sorted(source_mix.items())),
        "seller_controlled_source_share": _rate(seller_citations, citation_total),
        "independent_source_share": _rate(independent_citations, citation_total),
        "incumbent_concentration": {
            "top_entity_id": top["entity_id"] if top else None,
            "top_first_mentioned_share": top["first_mentioned_share"] if top else None,
            "top_entity_recommendation_rate": top["recommendation_rate"] if top else None,
            "unique_first_entities": len(first_counts),
            "unique_recommended_entities": len(entity_stats),
            "first_mention_hhi": _round(
                sum((count / runs) ** 2 for count in first_counts.values())
            )
            if runs
            else None,
        },
        "entities": entity_stats,
    }


def build_shelf_map(
    records: list[dict[str, Any]],
    *,
    observation_source: str,
    facts_report: dict[str, Any] | None = None,
    facts_source: str | None = None,
) -> dict[str, Any]:
    groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    dimensions_by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        dimensions = _group_dimensions(record)
        group_id = _group_id(dimensions)
        dimensions_by_id[group_id] = dimensions
        groups[group_id].append(record)

    output_groups: list[dict[str, Any]] = []
    excluded_branded = 0
    for group_id in sorted(groups):
        group_records = sorted(groups[group_id], key=lambda item: item["run_id"])
        dimensions = dimensions_by_id[group_id]
        metrics = _group_metrics(group_records)
        state, reasons = _classify(metrics, branded=bool(dimensions["branded"]))
        if dimensions["branded"]:
            excluded_branded += len(group_records)
        fact_support = _fact_support(
            facts_report=facts_report,
            target_entity_id=dimensions["target_entity_id"],
            prompt_family=dimensions["prompt_family"],
        )
        integrity_issues: list[str] = []
        if state == "unsafe":
            integrity_issues.extend(reasons)
        if fact_support["status"] == "blocked":
            integrity_issues.extend(fact_support["gate_failures"])
        output_groups.append(
            {
                "group_id": group_id,
                "dimensions": dimensions,
                "observation_ids": [record["run_id"] for record in group_records],
                "runs": len(group_records),
                "shelf_state": state,
                "classification_confidence": _confidence(len(group_records)),
                "classification_reasons": reasons,
                "eligible_for_unbranded_recommendation_share": not dimensions["branded"],
                "metrics": metrics,
                "fact_support": fact_support,
                "integrity_issues": sorted(set(integrity_issues)),
            }
        )

    families: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for group in output_groups:
        families[group["dimensions"]["prompt_family"]].append(group)
    family_summaries = []
    for family in sorted(families):
        family_groups = families[family]
        unbranded = [
            group for group in family_groups if group["eligible_for_unbranded_recommendation_share"]
        ]
        states = Counter(group["shelf_state"] for group in unbranded)
        family_summaries.append(
            {
                "prompt_family": family,
                "surface_group_ids": sorted(group["group_id"] for group in family_groups),
                "unbranded_surface_group_ids": sorted(group["group_id"] for group in unbranded),
                "state_counts": dict(sorted(states.items())),
                "cross_surface_state": (
                    next(iter(states))
                    if len(states) == 1
                    else "mixed"
                    if states
                    else "unknown"
                ),
                "note": "Rates remain per exact surface group; this summary does not pool recommendation share.",
            }
        )

    return {
        "schema_version": SHELF_SCHEMA_VERSION,
        "record_schema": OBSERVATION_SCHEMA,
        "shelf_map_schema": SHELF_MAP_SCHEMA,
        "source": {
            "observations": observation_source,
            "facts": facts_source,
            "observation_count": len(records),
            "observation_sha256": hashlib.sha256(
                "\n".join(
                    json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                    for record in records
                ).encode("utf-8")
            ).hexdigest(),
        },
        "group_dimensions": list(EXACT_DIMENSIONS),
        "classification_thresholds": {
            "minimum_runs": MIN_CLASSIFICATION_RUNS,
            "unsafe_minimum_evaluable": UNSAFE_MIN_EVALUABLE,
            "locked_top_first_share": LOCKED_TOP_FIRST_SHARE,
            "locked_top_recommendation_rate": LOCKED_TOP_RECOMMENDATION_RATE,
            "locked_set_agreement": LOCKED_AGREEMENT,
            "open_recommendation_coverage": OPEN_RECOMMENDATION_COVERAGE,
            "open_top_first_share": OPEN_TOP_FIRST_SHARE,
            "open_set_agreement": OPEN_AGREEMENT,
            "fragmented_set_agreement": FRAGMENTED_AGREEMENT,
            "unsafe_minimum_fidelity": UNSAFE_MIN_FIDELITY,
            "unsafe_minimum_constraint_satisfaction": UNSAFE_MIN_CONSTRAINT_SATISFACTION,
            "unsafe_maximum_unavailable_rate": UNSAFE_MAX_UNAVAILABLE_RATE,
        },
        "branded_exclusion": {
            "excluded_observation_count": excluded_branded,
            "rule": "Branded validation observations are grouped separately and excluded from unbranded recommendation-share denominators.",
        },
        "groups": output_groups,
        "prompt_families": family_summaries,
        "notes": [
            "No exact-surface rates are silently pooled.",
            "Missing fields remain null and are excluded from their metric denominator.",
            "Shelf classifications are transparent operational rules, not platform ranking scores.",
            "No classification implies a fixed time to shelf entry.",
        ],
    }


def write_shelf_outputs(
    output_dir: Path,
    records: list[dict[str, Any]],
    shelf_map: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized = "\n".join(
        json.dumps(record, sort_keys=True, ensure_ascii=False) for record in records
    ) + "\n"
    (output_dir / "normalized-observations.jsonl").write_text(normalized, encoding="utf-8")
    (output_dir / "shelf-map.json").write_text(
        json.dumps(shelf_map, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "shelf-report.md").write_text(render_shelf_report(shelf_map), encoding="utf-8")


def render_shelf_report(shelf_map: dict[str, Any]) -> str:
    lines = [
        "# Organic Discovery AI Shelf Map",
        "",
        "Exact surfaces are reported separately. Branded validation is excluded from unbranded recommendation-share denominators. No opaque GEO score or fixed time-to-shelf promise is produced.",
        "",
        "## Surface groups",
        "",
        "| Group | Prompt family | Surface | Market | Branded | Runs | State | Confidence |",
        "|---|---|---|---|---:|---:|---|---|",
    ]
    for group in shelf_map["groups"]:
        dimensions = group["dimensions"]
        surface = f"{dimensions['platform']} / {dimensions['surface']} / {dimensions['mode']}"
        lines.append(
            f"| `{group['group_id']}` | {dimensions['prompt_family']} | {surface} | "
            f"{dimensions['market']} / {dimensions['language']} | {str(dimensions['branded']).lower()} | "
            f"{group['runs']} | **{group['shelf_state']}** | {group['classification_confidence']} |"
        )
    lines += ["", "## Classification rationale", ""]
    for group in shelf_map["groups"]:
        lines.append(f"### {group['group_id']} — {group['shelf_state']}")
        for reason in group["classification_reasons"]:
            lines.append(f"- {reason}")
        metrics = group["metrics"]
        lines.append(
            f"- Recommendation coverage: {metrics['recommendation_coverage']['numerator']}/"
            f"{metrics['recommendation_coverage']['denominator']} "
            f"({metrics['recommendation_coverage']['rate']})"
        )
        lines.append(f"- Set agreement: {metrics['recommendation_set_agreement']}")
        lines.append(f"- Volatility: {metrics['volatility']}")
        lines.append(f"- Fidelity: {metrics['fidelity']['numerator']}/{metrics['fidelity']['denominator']} ({metrics['fidelity']['rate']})")
        lines.append(
            f"- Constraint satisfaction: {metrics['constraint_satisfaction']['numerator']}/"
            f"{metrics['constraint_satisfaction']['denominator']} ({metrics['constraint_satisfaction']['rate']})"
        )
        if group["integrity_issues"]:
            lines.append("- Integrity issues:")
            lines.extend(f"  - {issue}" for issue in group["integrity_issues"])
        lines.append("")
    lines += [
        "## Boundary",
        "",
        "- Technical or observational readiness is not a ranking, citation, traffic, or conversion guarantee.",
        "- Seller-controlled evidence is counted separately from independent evidence.",
        "- Unknown values are not converted to false or zero.",
        "",
    ]
    return "\n".join(lines)


def _load_candidates(path: Path | None, *, shelf_map: dict[str, Any], facts_report: dict[str, Any]) -> list[dict[str, Any]]:
    if path is not None:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ShelfError(f"cannot read candidates {path}: {exc}") from exc
        candidates = payload.get("candidates") if isinstance(payload, dict) else payload
        if not isinstance(candidates, list):
            raise ShelfError("candidate file must be an array or an object containing candidates")
        normalized: list[dict[str, Any]] = []
        seen_candidate_ids: set[str] = set()
        for index, item in enumerate(candidates):
            if not isinstance(item, dict):
                raise ShelfError(f"candidate {index} must be an object")
            candidate_id = _clean(item.get("candidate_id"))
            prompt_family = _clean(item.get("prompt_family"))
            target_entity_id = _clean(item.get("target_entity_id"))
            if not candidate_id or not prompt_family or not target_entity_id:
                raise ShelfError(f"candidate {index} requires candidate_id, prompt_family, and target_entity_id")
            if candidate_id in seen_candidate_ids:
                raise ShelfError(f"candidate_id must be unique: {candidate_id}")
            seen_candidate_ids.add(candidate_id)
            factors = item.get("factors") or {}
            if not isinstance(factors, dict):
                raise ShelfError(f"candidate {candidate_id}: factors must be an object")
            normalized_factors: dict[str, float | None] = {}
            for key in (
                "qualified_demand",
                "conversion_value",
                "execution_probability",
                "source_attainability",
                "implementation_cost",
                "maintenance_cost",
                "risk",
            ):
                value = factors.get(key)
                if value is None:
                    normalized_factors[key] = None
                elif isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= float(value) <= 1:
                    normalized_factors[key] = float(value)
                else:
                    raise ShelfError(f"candidate {candidate_id}: factor {key} must be between 0 and 1 or null")
            normalized.append(
                {
                    "candidate_id": candidate_id,
                    "prompt_family": prompt_family,
                    "target_entity_id": target_entity_id,
                    "user_constraint": _clean(item.get("user_constraint")) or None,
                    "controlled_asset": _clean(item.get("controlled_asset")) or None,
                    "required_fact_ids": sorted(
                        {_clean(value) for value in item.get("required_fact_ids", []) if _clean(value)}
                    ),
                    "surface_group_ids": sorted(
                        {_clean(value) for value in item.get("surface_group_ids", []) if _clean(value)}
                    ),
                    "factors": normalized_factors,
                    "notes": _clean(item.get("notes")) or None,
                    "source": "provided",
                }
            )
        return sorted(normalized, key=lambda item: item["candidate_id"])

    candidates: list[dict[str, Any]] = []
    family_targets = {
        (group["dimensions"]["prompt_family"], group["dimensions"]["target_entity_id"])
        for group in shelf_map["groups"]
        if not group["dimensions"]["branded"]
    }
    facts = facts_report.get("facts", [])
    for prompt_family, target_entity_id in sorted(family_targets):
        required = sorted(
            fact["claim_id"]
            for fact in facts
            if fact["entity_id"] == target_entity_id
            and prompt_family in fact["prompt_families"]
        )
        candidates.append(
            {
                "candidate_id": f"wedge-{target_entity_id}-{prompt_family}",
                "prompt_family": prompt_family,
                "target_entity_id": target_entity_id,
                "user_constraint": None,
                "controlled_asset": None,
                "required_fact_ids": required,
                "surface_group_ids": [],
                "factors": {
                    "qualified_demand": None,
                    "conversion_value": None,
                    "execution_probability": None,
                    "source_attainability": None,
                    "implementation_cost": None,
                    "maintenance_cost": None,
                    "risk": None,
                },
                "notes": "Auto-generated from exact-surface observations and prompt-family fact tags.",
                "source": "inferred",
            }
        )
    return candidates


def _planning_index(factors: dict[str, float | None], shelf_openness: float, evidence_strength: float) -> tuple[float | None, list[str]]:
    missing = [key for key, value in factors.items() if value is None]
    if missing:
        return None, missing
    positives = [
        factors["qualified_demand"],
        factors["conversion_value"],
        factors["execution_probability"],
        factors["source_attainability"],
        shelf_openness,
        evidence_strength,
    ]
    burdens = [
        factors["implementation_cost"],
        factors["maintenance_cost"],
        factors["risk"],
    ]
    numerator = sum(float(value) for value in positives) / len(positives)
    denominator = 1.0 + sum(float(value) for value in burdens) / len(burdens)
    return _round(numerator / denominator), []


def _shelf_openness(state: str) -> float:
    return {
        "open": 1.0,
        "fragmented": 0.8,
        "contested": 0.55,
        "locked": 0.0,
        "unsafe": 0.0,
        "unknown": 0.0,
    }.get(state, 0.0)


def plan_wedges(
    shelf_map: dict[str, Any],
    facts_report: dict[str, Any],
    *,
    candidates_path: Path | None = None,
) -> dict[str, Any]:
    if shelf_map.get("schema_version") != SHELF_SCHEMA_VERSION:
        raise ShelfError("unsupported shelf-map schema version")
    if not facts_report.get("valid"):
        raise ShelfError("fact registry is invalid; repair Business Truth before wedge planning")

    candidates = _load_candidates(candidates_path, shelf_map=shelf_map, facts_report=facts_report)
    facts_by_id = fact_index(facts_report)
    publishable = set(facts_report.get("publishable_fact_ids", []))
    groups = {group["group_id"]: group for group in shelf_map["groups"]}
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for candidate in candidates:
        gate_failures: list[str] = []
        required_ids = candidate["required_fact_ids"]
        missing_ids = [claim_id for claim_id in required_ids if claim_id not in facts_by_id]
        blocked_ids = [claim_id for claim_id in required_ids if claim_id in facts_by_id and claim_id not in publishable]
        if missing_ids:
            gate_failures.append("required facts are missing: " + ", ".join(missing_ids))
        if blocked_ids:
            gate_failures.append("required facts are not publishable: " + ", ".join(blocked_ids))

        fact_support = _fact_support(
            facts_report=facts_report,
            target_entity_id=candidate["target_entity_id"],
            prompt_family=candidate["prompt_family"],
        )
        gate_failures.extend(fact_support["gate_failures"])

        eligible_groups = [
            group
            for group in shelf_map["groups"]
            if group["dimensions"]["prompt_family"] == candidate["prompt_family"]
            and group["dimensions"]["target_entity_id"] == candidate["target_entity_id"]
            and not group["dimensions"]["branded"]
        ]
        if candidate["surface_group_ids"]:
            unknown_group_ids = [group_id for group_id in candidate["surface_group_ids"] if group_id not in groups]
            if unknown_group_ids:
                gate_failures.append("unknown surface groups: " + ", ".join(unknown_group_ids))
            eligible_groups = [
                group for group in eligible_groups if group["group_id"] in candidate["surface_group_ids"]
            ]
        if not eligible_groups:
            gate_failures.append("no matching unbranded exact-surface groups")

        surface_opportunities: list[dict[str, Any]] = []
        surface_rejections: list[dict[str, Any]] = []
        evidence_strength = min(
            1.0,
            0.45
            + 0.12 * len(fact_support["independent_fact_ids"])
            + 0.05 * len(fact_support["seller_controlled_fact_ids"]),
        )
        for group in eligible_groups:
            state = group["shelf_state"]
            surface_failure = None
            if state == "unsafe":
                surface_failure = "unsafe shelf: recommendation integrity must be repaired before growth planning"
            elif state == "unknown":
                surface_failure = "unknown shelf: collect enough exact-surface observations"
            elif state == "locked":
                surface_failure = "locked shelf: broad displacement is not an approved v0.5 wedge"
            if group["fact_support"]["status"] == "blocked":
                surface_failure = "surface fact gate is blocked"
            planning_index, missing_factors = _planning_index(
                candidate["factors"],
                _shelf_openness(state),
                evidence_strength,
            )
            record = {
                "group_id": group["group_id"],
                "dimensions": group["dimensions"],
                "shelf_state": state,
                "shelf_confidence": group["classification_confidence"],
                "shelf_openness": _shelf_openness(state),
                "planning_index": planning_index,
                "missing_business_factors": missing_factors,
            }
            if surface_failure:
                record["rejection_reason"] = surface_failure
                surface_rejections.append(record)
            else:
                surface_opportunities.append(record)

        if eligible_groups and not surface_opportunities:
            gate_failures.append("every matching surface group is locked, unsafe, unknown, or fact-blocked")

        base = {
            "candidate_id": candidate["candidate_id"],
            "prompt_family": candidate["prompt_family"],
            "target_entity_id": candidate["target_entity_id"],
            "user_constraint": candidate["user_constraint"],
            "controlled_asset": candidate["controlled_asset"],
            "candidate_source": candidate["source"],
            "required_fact_ids": required_ids,
            "fact_support": fact_support,
            "factors": candidate["factors"],
            "surface_opportunities": sorted(
                surface_opportunities,
                key=lambda item: (
                    -(item["planning_index"] if item["planning_index"] is not None else -1.0),
                    item["group_id"],
                ),
            ),
            "rejected_surfaces": sorted(surface_rejections, key=lambda item: item["group_id"]),
            "notes": candidate["notes"],
        }
        if gate_failures:
            base["status"] = "rejected"
            base["gate_failures"] = sorted(set(gate_failures))
            rejected.append(base)
        else:
            base["status"] = (
                "approved_for_planning"
                if all(not surface["missing_business_factors"] for surface in surface_opportunities)
                else "approved_pending_business_priority_inputs"
            )
            base["gate_failures"] = []
            actions = []
            if not fact_support["independent_fact_ids"]:
                actions.append("seek independent corroboration before representing seller claims as consensus")
            if any(surface["missing_business_factors"] for surface in surface_opportunities):
                actions.append("supply qualified demand, conversion value, cost, maintenance, execution, source, and risk factors")
            base["required_actions"] = actions
            accepted.append(base)

    accepted.sort(
        key=lambda item: (
            -max(
                (
                    surface["planning_index"]
                    for surface in item["surface_opportunities"]
                    if surface["planning_index"] is not None
                ),
                default=-1.0,
            ),
            item["candidate_id"],
        )
    )
    rejected.sort(key=lambda item: item["candidate_id"])
    return {
        "schema_version": WEDGE_SCHEMA_VERSION,
        "wedge_plan_schema": WEDGE_PLAN_SCHEMA,
        "source": {
            "shelf_map_schema_version": shelf_map.get("schema_version"),
            "fact_registry_schema_version": facts_report.get("schema_version"),
            "candidates": str(candidates_path) if candidates_path else None,
        },
        "summary": {
            "candidate_count": len(candidates),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "opaque_geo_score": None,
        },
        "accepted": accepted,
        "rejected": rejected,
        "hard_gates": [
            "offer existence and current availability",
            "publishable prompt-family fact support",
            "no prohibited required facts",
            "matching unbranded exact-surface observations",
            "surface state is not locked, unsafe, or unknown",
        ],
        "notes": [
            "Planning indexes are transparent business-prioritization aids, not search-engine scores.",
            "Unsafe or unsupported opportunities are rejected rather than merely ranked lower.",
            "No accepted candidate carries a fixed time-to-shelf promise.",
            "Exact-surface opportunity records remain separate.",
        ],
    }


def write_wedge_plan(path: Path, plan: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
