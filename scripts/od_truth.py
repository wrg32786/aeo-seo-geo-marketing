"""Canonical Business Truth registry validation for Organic Discovery."""
from __future__ import annotations

import csv
import json
import re
import urllib.parse
from datetime import date
from pathlib import Path
from typing import Any

FACT_SCHEMA_VERSION = "organic-discovery/facts/1.0"
FACT_RECORD_SCHEMA = "schemas/fact-record.schema.json"

REQUIRED_COLUMNS = (
    "claim_id",
    "entity_id",
    "entity",
    "claim_type",
    "canonical_wording",
    "value",
    "unit",
    "source_url",
    "source_type",
    "verified_at",
    "evidence_grade",
    "offer_exists",
    "availability",
    "publish_status",
    "owner",
    "refresh_trigger",
    "limitations",
    "prompt_families",
    "market",
    "language",
    "expires_at",
)

PUBLISH_STATUSES = {
    "approved",
    "approval_required",
    "research_required",
    "expired",
    "prohibited",
}
SOURCE_TYPES = {
    "first_party",
    "seller_controlled",
    "independent_editorial",
    "official_registry",
    "customer_authorized",
    "community",
    "internal_record",
    "other",
    "none",
}
EVIDENCE_GRADES = {"O", "A", "B", "C", "D", "F", "X", "FP"}
AVAILABILITY_VALUES = {
    "available",
    "limited",
    "preorder",
    "unavailable",
    "unknown",
    "not_applicable",
}
TRI_STATE = {"true", "false", "unknown", "not_applicable"}
SELLER_CONTROLLED_TYPES = {"first_party", "seller_controlled", "internal_record"}
INDEPENDENT_TYPES = {"independent_editorial", "official_registry", "customer_authorized"}
OFFER_DEPENDENT_CLAIMS = {
    "availability",
    "price",
    "ingredient",
    "feature",
    "compatibility",
    "service_area",
    "performance",
    "certification",
    "safety",
    "medical",
    "customer_result",
    "offer_fit",
}
INDEPENDENT_REQUIRED_CLAIMS = {"certification", "safety", "medical", "customer_result"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,95}$")


class TruthError(RuntimeError):
    """Expected registry error suitable for a concise CLI message."""


def _clean(value: Any) -> str:
    return "" if value is None else " ".join(str(value).strip().split())


def _parse_date(
    value: str,
    *,
    field: str,
    claim_id: str,
    errors: list[dict[str, Any]],
) -> str | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        errors.append(
            {
                "claim_id": claim_id,
                "field": field,
                "code": "invalid_date",
                "message": f"{field} must use YYYY-MM-DD",
            }
        )
        return None


def _parse_boolish(
    value: str,
    *,
    claim_id: str,
    errors: list[dict[str, Any]],
) -> bool | None | str:
    normalized = value.casefold()
    if normalized not in TRI_STATE:
        errors.append(
            {
                "claim_id": claim_id,
                "field": "offer_exists",
                "code": "invalid_offer_exists",
                "message": "offer_exists must be true, false, unknown, or not_applicable",
            }
        )
        return None
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return normalized


def _valid_source_url(value: str) -> bool:
    if not value:
        return False
    parsed = urllib.parse.urlsplit(value)
    return parsed.scheme in {"http", "https", "urn", "file"} and bool(
        parsed.netloc or parsed.path
    )


def _issue(
    target: list[dict[str, Any]],
    claim_id: str,
    field: str,
    code: str,
    message: str,
) -> None:
    target.append(
        {
            "claim_id": claim_id,
            "field": field,
            "code": code,
            "message": message,
        }
    )


def _normalize_row(
    row: dict[str, Any],
    *,
    row_number: int,
    as_of: date | None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    values = {column: _clean(row.get(column, "")) for column in REQUIRED_COLUMNS}
    claim_id = values["claim_id"] or f"row-{row_number}"

    if not ID_RE.fullmatch(values["claim_id"]):
        _issue(
            errors,
            claim_id,
            "claim_id",
            "invalid_claim_id",
            "claim_id must be a stable lowercase identifier",
        )
    if not ID_RE.fullmatch(values["entity_id"]):
        _issue(
            errors,
            claim_id,
            "entity_id",
            "invalid_entity_id",
            "entity_id must be a stable lowercase identifier",
        )
    if not values["entity"]:
        _issue(errors, claim_id, "entity", "missing_entity", "entity is required")
    if not values["claim_type"]:
        _issue(
            errors,
            claim_id,
            "claim_type",
            "missing_claim_type",
            "claim_type is required",
        )
    if not values["canonical_wording"]:
        _issue(
            errors,
            claim_id,
            "canonical_wording",
            "missing_canonical_wording",
            "canonical_wording is required",
        )

    publish_status = values["publish_status"].casefold()
    if publish_status not in PUBLISH_STATUSES:
        _issue(
            errors,
            claim_id,
            "publish_status",
            "invalid_publish_status",
            f"publish_status must be one of {sorted(PUBLISH_STATUSES)}",
        )

    source_type = values["source_type"].casefold()
    if source_type not in SOURCE_TYPES:
        _issue(
            errors,
            claim_id,
            "source_type",
            "invalid_source_type",
            f"source_type must be one of {sorted(SOURCE_TYPES)}",
        )

    evidence_grade = values["evidence_grade"].upper()
    if evidence_grade not in EVIDENCE_GRADES:
        _issue(
            errors,
            claim_id,
            "evidence_grade",
            "invalid_evidence_grade",
            f"evidence_grade must be one of {sorted(EVIDENCE_GRADES)}",
        )

    availability = values["availability"].casefold()
    if availability not in AVAILABILITY_VALUES:
        _issue(
            errors,
            claim_id,
            "availability",
            "invalid_availability",
            f"availability must be one of {sorted(AVAILABILITY_VALUES)}",
        )

    offer_exists = _parse_boolish(
        values["offer_exists"], claim_id=claim_id, errors=errors
    )
    verified_at = _parse_date(
        values["verified_at"],
        field="verified_at",
        claim_id=claim_id,
        errors=errors,
    )
    expires_at = _parse_date(
        values["expires_at"],
        field="expires_at",
        claim_id=claim_id,
        errors=errors,
    )
    prompt_families = sorted(
        {part.strip() for part in values["prompt_families"].split("|") if part.strip()}
    )

    if publish_status == "approved":
        if not _valid_source_url(values["source_url"]):
            _issue(
                errors,
                claim_id,
                "source_url",
                "approved_claim_missing_source",
                "approved claims require a source URL or stable URN",
            )
        if source_type in {"", "none"}:
            _issue(
                errors,
                claim_id,
                "source_type",
                "approved_claim_missing_source_type",
                "approved claims require a known source type",
            )
        if not verified_at:
            _issue(
                errors,
                claim_id,
                "verified_at",
                "approved_claim_unverified",
                "approved claims require a valid verification date",
            )
        if not values["owner"]:
            _issue(
                errors,
                claim_id,
                "owner",
                "approved_claim_missing_owner",
                "approved claims require an accountable owner",
            )
        if not values["refresh_trigger"]:
            _issue(
                errors,
                claim_id,
                "refresh_trigger",
                "approved_claim_missing_refresh_trigger",
                "approved claims require a refresh trigger",
            )
        claim_type = values["claim_type"].casefold()
        if claim_type in OFFER_DEPENDENT_CLAIMS:
            if offer_exists is not True:
                _issue(
                    errors,
                    claim_id,
                    "offer_exists",
                    "approved_claim_offer_not_confirmed",
                    "offer-dependent approved claims require offer_exists=true",
                )
            if availability in {"unknown", "unavailable"}:
                _issue(
                    errors,
                    claim_id,
                    "availability",
                    "approved_claim_unavailable",
                    "offer-dependent approved claims require current availability",
                )
        if claim_type in INDEPENDENT_REQUIRED_CLAIMS and source_type not in INDEPENDENT_TYPES:
            _issue(
                errors,
                claim_id,
                "source_type",
                "independent_evidence_required",
                f"{claim_type} claims require independent, official, or customer-authorized evidence",
            )

    if publish_status in {"research_required", "approval_required"}:
        _issue(
            warnings,
            claim_id,
            "publish_status",
            "claim_not_publishable",
            f"{publish_status} claims may inform research but cannot be used in publication-ready copy",
        )
    if publish_status in {"expired", "prohibited"}:
        _issue(
            warnings,
            claim_id,
            "publish_status",
            "claim_blocked",
            f"{publish_status} claims are blocked from publication",
        )
    if source_type in SELLER_CONTROLLED_TYPES and publish_status == "approved":
        _issue(
            warnings,
            claim_id,
            "source_type",
            "seller_controlled_evidence",
            "seller-controlled evidence must not be represented as independent consensus",
        )
    if expires_at and as_of and date.fromisoformat(expires_at) < as_of:
        _issue(
            errors,
            claim_id,
            "expires_at",
            "fact_expired_as_of",
            f"fact expired before {as_of.isoformat()}",
        )

    normalized = {
        "claim_id": values["claim_id"],
        "entity_id": values["entity_id"],
        "entity": values["entity"],
        "claim_type": values["claim_type"].casefold(),
        "canonical_wording": values["canonical_wording"],
        "value": values["value"] or None,
        "unit": values["unit"] or None,
        "source_url": values["source_url"] or None,
        "source_type": source_type or None,
        "source_control": (
            "seller_controlled"
            if source_type in SELLER_CONTROLLED_TYPES
            else "independent"
            if source_type in INDEPENDENT_TYPES
            else "community"
            if source_type == "community"
            else "other"
            if source_type not in {"", "none"}
            else "unknown"
        ),
        "verified_at": verified_at,
        "evidence_grade": evidence_grade or None,
        "offer_exists": offer_exists,
        "availability": availability or None,
        "publish_status": publish_status or None,
        "owner": values["owner"] or None,
        "refresh_trigger": values["refresh_trigger"] or None,
        "limitations": values["limitations"] or None,
        "prompt_families": prompt_families,
        "market": values["market"] or None,
        "language": values["language"] or None,
        "expires_at": expires_at,
        "row_number": row_number,
    }
    return normalized, errors, warnings


def validate_fact_registry(path: Path, *, as_of: date | None = None) -> dict[str, Any]:
    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise TruthError(f"cannot read fact registry {path}: {exc}") from exc

    with handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise TruthError("fact registry has no header")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise TruthError(
                "fact registry is missing required columns: " + ", ".join(missing)
            )
        extra_columns = sorted(set(reader.fieldnames) - set(REQUIRED_COLUMNS))
        facts: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        warnings: list[dict[str, Any]] = []
        seen: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            fact, row_errors, row_warnings = _normalize_row(
                row, row_number=row_number, as_of=as_of
            )
            claim_id = fact["claim_id"]
            if claim_id in seen:
                _issue(
                    row_errors,
                    claim_id,
                    "claim_id",
                    "duplicate_claim_id",
                    "claim_id must be unique",
                )
            seen.add(claim_id)
            facts.append(fact)
            errors.extend(row_errors)
            warnings.extend(row_warnings)

    blocking_ids = {issue["claim_id"] for issue in errors}
    publishable = [
        fact["claim_id"]
        for fact in facts
        if fact["publish_status"] == "approved"
        and fact["claim_id"] not in blocking_ids
    ]
    blocked = [fact["claim_id"] for fact in facts if fact["claim_id"] not in publishable]

    entity_summary: dict[str, dict[str, Any]] = {}
    for fact in facts:
        entity = entity_summary.setdefault(
            fact["entity_id"],
            {
                "entity_id": fact["entity_id"],
                "entity": fact["entity"],
                "approved_fact_ids": [],
                "blocked_fact_ids": [],
                "independent_fact_ids": [],
                "seller_controlled_fact_ids": [],
                "prompt_families": {},
            },
        )
        destination = (
            "approved_fact_ids"
            if fact["claim_id"] in publishable
            else "blocked_fact_ids"
        )
        entity[destination].append(fact["claim_id"])
        if fact["claim_id"] in publishable:
            if fact["source_control"] == "independent":
                entity["independent_fact_ids"].append(fact["claim_id"])
            elif fact["source_control"] == "seller_controlled":
                entity["seller_controlled_fact_ids"].append(fact["claim_id"])
            for family in fact["prompt_families"]:
                entity["prompt_families"].setdefault(family, []).append(fact["claim_id"])

    for entity in entity_summary.values():
        for key in (
            "approved_fact_ids",
            "blocked_fact_ids",
            "independent_fact_ids",
            "seller_controlled_fact_ids",
        ):
            entity[key].sort()
        entity["prompt_families"] = {
            family: sorted(ids)
            for family, ids in sorted(entity["prompt_families"].items())
        }

    return {
        "schema_version": FACT_SCHEMA_VERSION,
        "record_schema": FACT_RECORD_SCHEMA,
        "source": str(path),
        "as_of": as_of.isoformat() if as_of else None,
        "valid": not errors,
        "summary": {
            "fact_count": len(facts),
            "approved_count": sum(fact["publish_status"] == "approved" for fact in facts),
            "publishable_count": len(publishable),
            "blocked_count": len(blocked),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "extra_columns": extra_columns,
            "seller_controlled_publishable_count": sum(
                fact["claim_id"] in publishable
                and fact["source_control"] == "seller_controlled"
                for fact in facts
            ),
            "independent_publishable_count": sum(
                fact["claim_id"] in publishable
                and fact["source_control"] == "independent"
                for fact in facts
            ),
        },
        "publishable_fact_ids": sorted(publishable),
        "blocked_fact_ids": sorted(blocked),
        "errors": sorted(
            errors, key=lambda item: (item["claim_id"], item["field"], item["code"])
        ),
        "warnings": sorted(
            warnings, key=lambda item: (item["claim_id"], item["field"], item["code"])
        ),
        "facts": sorted(facts, key=lambda item: item["claim_id"]),
        "entities": [entity_summary[key] for key in sorted(entity_summary)],
        "publication_boundary": (
            "Only approved facts without blocking validation errors are publishable. "
            "Seller-controlled evidence must remain labeled as seller-controlled."
        ),
    }


def write_fact_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fact_index(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {fact["claim_id"]: fact for fact in report.get("facts", [])}
