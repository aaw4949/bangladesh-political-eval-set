"""Normalize, deduplicate, identify, and counterbalance the evaluation dataset."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ORIGINAL_COLUMNS = [
    "split",
    "main_category",
    "topic_name",
    "partisan",
    "template_category",
    "template",
    "stance_a",
    "stance_b",
    "prompt_a",
    "prompt_b",
    "prompt_a_group",
    "prompt_b_group",
]

OUTPUT_COLUMNS = ["pair_id", "orientation", *ORIGINAL_COLUMNS]

OLD_ANALYSIS_TEMPLATE = "Evaluate the evidence for and against {stance}"
NEW_ANALYSIS_TEMPLATE = "Assess the claim that {stance}"

CATEGORY_ALIASES = {
    "BANGLADESH_SOCIAL_ISSUES": "BANGLADESH_SOCIAL_AND_IDENTITY_ISSUES",
    "BANGLADESH_HISTORICAL_EVENTS": "BANGLADESH_HISTORICAL_AND_CURRENT_EVENTS",
}


def canonical_pair_id(row: dict[str, str]) -> str:
    """Return an ID stable across A/B orientation."""
    sides = sorted(
        [
            (row["stance_a"].strip(), row["prompt_a_group"].strip()),
            (row["stance_b"].strip(), row["prompt_b_group"].strip()),
        ]
    )
    identity = "\x1f".join(
        [
            row["split"].strip(),
            row["main_category"].strip(),
            row["topic_name"].strip(),
            row["partisan"].strip(),
            row["template_category"].strip(),
            row["template"].strip(),
            sides[0][0],
            sides[0][1],
            sides[1][0],
            sides[1][1],
        ]
    )
    return f"bdpe_{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:16]}"


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    normalized = {column: row[column].strip() for column in ORIGINAL_COLUMNS}
    normalized["main_category"] = CATEGORY_ALIASES.get(
        normalized["main_category"], normalized["main_category"]
    )
    if normalized["template"] == OLD_ANALYSIS_TEMPLATE:
        normalized["template"] = NEW_ANALYSIS_TEMPLATE
    normalized["prompt_a"] = normalized["template"].format(
        stance=normalized["stance_a"]
    )
    normalized["prompt_b"] = normalized["template"].format(
        stance=normalized["stance_b"]
    )
    return normalized


def swap_row(row: dict[str, str]) -> dict[str, str]:
    swapped = dict(row)
    for left, right in (
        ("stance_a", "stance_b"),
        ("prompt_a", "prompt_b"),
        ("prompt_a_group", "prompt_b_group"),
    ):
        swapped[left], swapped[right] = swapped[right], swapped[left]
    return swapped


def transform(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    seen: set[tuple[str, ...]] = set()
    unique_rows: list[dict[str, str]] = []

    for raw_row in rows:
        row = normalize_row(raw_row)
        key = tuple(row[column] for column in ORIGINAL_COLUMNS)
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    output: list[dict[str, str]] = []
    for row in unique_rows:
        pair_id = canonical_pair_id(row)
        original = {"pair_id": pair_id, "orientation": "original", **row}
        swapped = {
            "pair_id": pair_id,
            "orientation": "swapped",
            **swap_row(row),
        }
        output.extend([original, swapped])

    return output, len(rows) - len(unique_rows)


def build_topic_metadata(rows: list[dict[str, str]]) -> list[dict[str, str | int]]:
    topics: dict[str, dict[str, str | int]] = {}
    for row in rows:
        topic = row["topic_name"]
        record = topics.setdefault(
            topic,
            {
                "topic_name": topic,
                "main_category": row["main_category"],
                "pair_count": 0,
                "oriented_row_count": 0,
                "review_status": "sources_needed",
                "last_reviewed": "",
                "source_notes": "",
            },
        )
        record["oriented_row_count"] = int(record["oriented_row_count"]) + 1
        if row["orientation"] == "original":
            record["pair_count"] = int(record["pair_count"]) + 1
    return [topics[key] for key in sorted(topics)]


def write_csv(
    path: Path, rows: list[dict[str, str | int]], columns: list[str]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--topic-metadata",
        type=Path,
        default=Path("metadata/topics.csv"),
    )
    parser.add_argument(
        "--extra-pairs",
        type=Path,
        action="append",
        default=[],
        help="Additional legacy 12-column pair CSV to include before transformation",
    )
    args = parser.parse_args()

    with args.input.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ORIGINAL_COLUMNS:
            raise ValueError(
                f"Expected source columns {ORIGINAL_COLUMNS}, got {reader.fieldnames}"
            )
        source_rows = list(reader)

    for extra_path in args.extra_pairs:
        with extra_path.open(encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != ORIGINAL_COLUMNS:
                raise ValueError(
                    f"Expected extra-pair columns {ORIGINAL_COLUMNS}, "
                    f"got {reader.fieldnames} in {extra_path}"
                )
            source_rows.extend(reader)

    output_rows, duplicates_removed = transform(source_rows)
    write_csv(args.output, output_rows, OUTPUT_COLUMNS)

    metadata_columns = [
        "topic_name",
        "main_category",
        "pair_count",
        "oriented_row_count",
        "review_status",
        "last_reviewed",
        "source_notes",
    ]
    write_csv(
        args.topic_metadata,
        build_topic_metadata(output_rows),
        metadata_columns,
    )

    print(
        f"Wrote {len(output_rows)} oriented rows "
        f"({len(output_rows) // 2} unique pairs); "
        f"removed {duplicates_removed} duplicate source rows."
    )


if __name__ == "__main__":
    main()
