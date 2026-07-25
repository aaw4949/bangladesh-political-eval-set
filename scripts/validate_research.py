"""Validate research-integration JSON and CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
MEDIA_PATH = ROOT / "data" / "media_outlets.csv"
EVIDENCE_PATH = ROOT / "data" / "evidence" / "media_assessments.csv"
SCHEMA_PATH = ROOT / "schemas" / "media_rating.schema.json"

MEDIA_COLUMNS = [
    "outlet_id", "outlet_name", "url", "country", "medium", "ownership",
    "assessment_start", "assessment_end", "party_alignment",
    "geopolitical_scores", "sociocultural_score", "governance_score",
    "reliability_score", "confidence", "evidence_count", "review_status",
    "last_reviewed", "methodology_version", "notes",
]
EVIDENCE_COLUMNS = [
    "evidence_id", "outlet_id", "published_at", "article_url",
    "content_type", "subject_actor", "axis", "observed_frame", "coded_value",
    "evidence_excerpt_or_summary", "coder", "second_coder_reviewed",
    "archive_url", "notes",
]
ALLOWED_MEDIA = {
    "print", "online", "television", "radio", "wire", "multiplatform"
}
ALLOWED_STATUS = {
    "unreviewed", "in_review", "provisional", "reviewed",
    "insufficient_evidence", "stale",
}


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate() -> list[str]:
    errors: list[str] = []
    json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    with MEDIA_PATH.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != MEDIA_COLUMNS:
            return ["media_outlets.csv header mismatch"]
        rows = list(reader)

    ids: set[str] = set()
    for line, row in enumerate(rows, start=2):
        outlet_id = row["outlet_id"]
        if outlet_id in ids:
            errors.append(f"media line {line}: duplicate outlet_id")
        ids.add(outlet_id)
        if not outlet_id.startswith("bdmo_"):
            errors.append(f"media line {line}: invalid outlet_id")
        if row["country"] != "Bangladesh":
            errors.append(f"media line {line}: country must be Bangladesh")
        if row["medium"] not in ALLOWED_MEDIA:
            errors.append(f"media line {line}: invalid medium")
        if row["review_status"] not in ALLOWED_STATUS:
            errors.append(f"media line {line}: invalid review_status")
        if row["url"] and not is_url(row["url"]):
            errors.append(f"media line {line}: invalid URL")
        if row["review_status"] == "unreviewed":
            rated = [
                row["party_alignment"], row["geopolitical_scores"],
                row["sociocultural_score"], row["governance_score"],
                row["reliability_score"], row["confidence"],
            ]
            if any(rated) or row["evidence_count"] != "0":
                errors.append(
                    f"media line {line}: unreviewed record contains ratings"
                )

    with EVIDENCE_PATH.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != EVIDENCE_COLUMNS:
            errors.append("media_assessments.csv header mismatch")
        for line, row in enumerate(reader, start=2):
            if row["outlet_id"] not in ids:
                errors.append(f"evidence line {line}: unknown outlet_id")
            if not is_url(row["article_url"]):
                errors.append(f"evidence line {line}: invalid article_url")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(f"ERROR: {problem}" for problem in problems))
        raise SystemExit(1)
    print("Research integration validation passed")
