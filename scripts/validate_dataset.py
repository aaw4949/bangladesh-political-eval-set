"""Fail-fast validation for the Bangladesh Political Eval Set."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


EXPECTED_COLUMNS = [
    "pair_id",
    "orientation",
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

ALLOWED_ORIENTATIONS = {"original", "swapped"}
ALLOWED_PARTISAN = {"True", "False"}
ALLOWED_TEMPLATE_CATEGORIES = {
    "analysis",
    "formal_writing",
    "humor",
    "narratives",
    "question_analytical",
    "question_opinion",
    "reasoning",
}
ALLOWED_MAIN_CATEGORIES = {
    "BANGLADESH_CONSTITUTION",
    "BANGLADESH_HISTORICAL_AND_CURRENT_EVENTS",
    "BANGLADESH_POLITICAL_FIGURES_AND_PARTIES",
    "BANGLADESH_PUBLIC_POLICY",
    "BANGLADESH_SCIENCE_AND_PUBLIC_HEALTH",
    "BANGLADESH_SOCIAL_AND_IDENTITY_ISSUES",
}

TOPIC_PATTERN = re.compile(r"[a-z0-9]+(?:_[a-z0-9]+)*")
PAIR_ID_PATTERN = re.compile(r"bdpe_[0-9a-f]{16}")
MALFORMED_PATTERN = re.compile(
    r"Evaluate the evidence for and against the evidence", re.IGNORECASE
)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != EXPECTED_COLUMNS:
            return [
                f"Header mismatch: expected {EXPECTED_COLUMNS}, got {reader.fieldnames}"
            ]
        rows = list(reader)

    if not rows:
        return ["Dataset contains no rows"]

    exact_rows: Counter[tuple[str, ...]] = Counter()
    composite_keys: Counter[tuple[str, str]] = Counter()
    by_pair: dict[str, list[tuple[int, dict[str, str]]]] = defaultdict(list)

    for line_number, row in enumerate(rows, start=2):
        empty = [column for column in EXPECTED_COLUMNS if not row[column].strip()]
        if empty:
            errors.append(f"Line {line_number}: empty required fields {empty}")

        if not PAIR_ID_PATTERN.fullmatch(row["pair_id"]):
            errors.append(f"Line {line_number}: invalid pair_id {row['pair_id']!r}")
        if row["orientation"] not in ALLOWED_ORIENTATIONS:
            errors.append(
                f"Line {line_number}: invalid orientation {row['orientation']!r}"
            )
        if row["partisan"] not in ALLOWED_PARTISAN:
            errors.append(
                f"Line {line_number}: invalid partisan value {row['partisan']!r}"
            )
        if row["template_category"] not in ALLOWED_TEMPLATE_CATEGORIES:
            errors.append(
                f"Line {line_number}: invalid template_category "
                f"{row['template_category']!r}"
            )
        if row["main_category"] not in ALLOWED_MAIN_CATEGORIES:
            errors.append(
                f"Line {line_number}: invalid main_category "
                f"{row['main_category']!r}"
            )
        if not TOPIC_PATTERN.fullmatch(row["topic_name"]):
            errors.append(
                f"Line {line_number}: topic_name is not lowercase snake_case"
            )
        if row["prompt_a"] == row["prompt_b"]:
            errors.append(f"Line {line_number}: paired prompts are identical")
        if row["prompt_a"] != row["template"].format(stance=row["stance_a"]):
            errors.append(f"Line {line_number}: prompt_a does not match template")
        if row["prompt_b"] != row["template"].format(stance=row["stance_b"]):
            errors.append(f"Line {line_number}: prompt_b does not match template")
        if MALFORMED_PATTERN.search(row["prompt_a"]) or MALFORMED_PATTERN.search(
            row["prompt_b"]
        ):
            errors.append(f"Line {line_number}: malformed analysis prompt")

        for column in EXPECTED_COLUMNS:
            value = row[column].lstrip()
            if value.startswith(("=", "+", "-", "@")):
                errors.append(
                    f"Line {line_number}: formula-like prefix in {column}"
                )

        exact_rows[tuple(row[column] for column in EXPECTED_COLUMNS)] += 1
        composite_keys[(row["pair_id"], row["orientation"])] += 1
        by_pair[row["pair_id"]].append((line_number, row))

    duplicate_rows = sum(count - 1 for count in exact_rows.values() if count > 1)
    if duplicate_rows:
        errors.append(f"Found {duplicate_rows} exact duplicate rows")

    duplicate_keys = [
        key for key, count in composite_keys.items() if count != 1
    ]
    if duplicate_keys:
        errors.append(
            f"Found {len(duplicate_keys)} non-unique pair_id/orientation keys"
        )

    for pair_id, pair_rows in by_pair.items():
        if len(pair_rows) != 2:
            errors.append(f"{pair_id}: expected 2 orientations, got {len(pair_rows)}")
            continue
        mapped = {row["orientation"]: row for _, row in pair_rows}
        if set(mapped) != ALLOWED_ORIENTATIONS:
            errors.append(f"{pair_id}: missing original or swapped orientation")
            continue
        original = mapped["original"]
        swapped = mapped["swapped"]
        swap_checks = [
            ("stance_a", "stance_b"),
            ("stance_b", "stance_a"),
            ("prompt_a", "prompt_b"),
            ("prompt_b", "prompt_a"),
            ("prompt_a_group", "prompt_b_group"),
            ("prompt_b_group", "prompt_a_group"),
        ]
        if any(original[left] != swapped[right] for left, right in swap_checks):
            errors.append(f"{pair_id}: swapped orientation is inconsistent")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset",
        nargs="?",
        type=Path,
        default=Path("eval_set_bangladesh.csv"),
    )
    args = parser.parse_args()
    errors = validate(args.dataset)
    if errors:
        for error in errors[:100]:
            print(f"ERROR: {error}")
        if len(errors) > 100:
            print(f"...and {len(errors) - 100} more errors")
        raise SystemExit(1)
    print(f"Validation passed: {args.dataset}")


if __name__ == "__main__":
    main()
