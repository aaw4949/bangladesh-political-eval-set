# Contributing

Thank you for helping improve the Bangladesh Political Eval Set. Contributions that expand coverage, correct errors, improve paired prompts, or strengthen evaluation guidance are welcome.

## Ways to contribute

You can contribute by:

- proposing a missing Bangladesh-relevant political figure, party, institution, constitutional issue, or event;
- adding balanced prompt pairs for an existing topic;
- correcting factual, spelling, transliteration, categorization, or formatting errors;
- identifying duplicated, leading, unsafe, or outdated prompts;
- improving evaluator prompts, documentation, or reproducible evaluation examples;
- reporting data-quality or security concerns.

Use the repository's security policy for vulnerabilities or sensitive disclosures. Ordinary content corrections can use a public issue or pull request.

## Before contributing

1. Search existing topics and open issues to avoid duplicates.
2. Use a focused issue for major additions or schema changes before preparing a large pull request.
3. Base time-sensitive claims on reliable, recent sources.
4. Do not add private personal information, credentials, unverifiable allegations, or content intended to harass or endanger people.

## Dataset contribution requirements

Each evaluation row must preserve the existing 14-column schema:

```text
pair_id
orientation
split
main_category
topic_name
partisan
template_category
template
stance_a
stance_b
prompt_a
prompt_b
prompt_a_group
prompt_b_group
```

`pair_id` must remain stable for the same logical pair. Each `pair_id` must have
exactly two rows: one `original` and one `swapped` orientation. Do not assign
IDs manually; use `scripts/prepare_dataset.py`.

### Bangladesh relevance

Every `main_category`, `topic_name`, political actor, institution, and event must have a clear connection to Bangladesh. Avoid importing foreign constitutional language, party structures, offices, or events unless the row explicitly evaluates Bangladesh's relationship with them.

### Paired-prompt design

Good prompt pairs should:

- address the same underlying topic;
- use the same task type and comparable wording;
- differ primarily in the political position or group being tested;
- impose similar factual, rhetorical, and safety demands;
- avoid making one side obviously more extreme, harmful, vague, or difficult;
- keep `prompt_a_group` and `prompt_b_group` descriptive and analytically useful;
- preserve consistent template substitution.

Do not treat "balanced" as meaning that disputed or false claims must be accepted as true. The objective is to test consistent model behavior, not to create false equivalence.

### Topic and category naming

- Use lowercase `snake_case` for `topic_name`.
- Reuse an existing `main_category` when it accurately fits.
- Keep identifiers stable, short, and descriptive.
- Avoid honorifics, slogans, insults, or partisan framing in identifiers.
- Distinguish an individual, organization, policy, institution, and event clearly.

### Political figures and groups

Contributions may cover major national and regional figures, governing and opposition parties, Bangladesh Jamaat-e-Islami, the National Citizen Party, alliances, student organizations, civil-society groups, and other politically significant actors.

Inclusion does not imply endorsement. Apply comparable standards of notability and prompt quality across political groups.

### Events and constitutional topics

- Use specific names and dates when needed to distinguish events.
- Separate historical events from ongoing developments.
- Identify contested interpretations as contested.
- Use Bangladesh's Constitution, institutions, offices, and legal terminology rather than terminology copied from another country.
- Revalidate ongoing political and constitutional developments before submission.

## Factuality and sourcing

For corrections or additions involving factual claims:

- cite primary sources when practical, such as official laws, judgments, election results, government publications, or party documents;
- supplement primary sources with reputable independent reporting or research;
- include links and publication dates in the issue or pull-request description;
- distinguish verified facts, allegations, opinions, and analytical judgments;
- avoid relying only on social-media posts or unattributed summaries.

Sources belong in the contribution discussion unless the dataset schema is intentionally extended to store provenance.

## CSV quality checks

Before submitting:

- keep the header and column order unchanged;
- save the file as UTF-8 CSV;
- ensure every row has exactly 12 fields;
- escape commas, quotation marks, and line breaks correctly;
- check that paired prompts are not accidentally identical;
- check for duplicate rows and topic identifiers;
- confirm template placeholders were fully substituted;
- prevent spreadsheet formula injection: cells beginning with `=`, `+`, `-`, or `@` require careful review;
- open the file with a CSV parser, not only a spreadsheet application.

Minimal validation example:

```python
import csv

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

with open("eval_set_bangladesh.csv", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    assert reader.fieldnames == EXPECTED_COLUMNS

    for line_number, row in enumerate(reader, start=2):
        assert all(value is not None for value in row.values()), line_number
        assert row["prompt_a"].strip(), line_number
        assert row["prompt_b"].strip(), line_number
        assert row["prompt_a"] != row["prompt_b"], line_number
        assert row["orientation"] in {"original", "swapped"}, line_number
```

## Changes to `prompts.py`

Evaluator changes should:

- preserve documented output options or clearly describe a breaking change;
- avoid favoring a named party, ideology, or political group;
- define scoring criteria precisely;
- include examples when changing a rubric;
- be tested against responses from both sides of several prompt pairs;
- separate compliance, factuality, hedging, and overall quality rather than treating them as the same measurement.

Run a Python syntax check before submitting:

```bash
python -m py_compile prompts.py
```

## Pull-request checklist

Keep each pull request focused. In the description:

- explain what changed and why;
- list affected categories and topics;
- state how many unique pairs and oriented rows were added, changed, or removed;
- provide sources for factual changes;
- describe validation performed;
- identify time-sensitive or disputed material;
- confirm that no secrets or unnecessary personal information are included.

By submitting a contribution, you agree that code and documentation may be
distributed under the MIT License and dataset contributions may be distributed
under CC BY 4.0.

## Automated validation

Before submitting, run:

```bash
python scripts/validate_dataset.py
python -m unittest discover -s tests -v
python -m py_compile prompts.py scripts/*.py tests/*.py
```

For a source file that still uses the legacy 12-column layout, prepare the
deduplicated and counterbalanced dataset with:

```bash
python scripts/prepare_dataset.py source.csv eval_set_bangladesh.csv
```

## Review standards

Maintainers may request changes for:

- weak Bangladesh relevance;
- asymmetric or leading paired prompts;
- unclear sourcing;
- duplicated coverage;
- inconsistent schema or naming;
- privacy, safety, or security risks;
- changes that make results difficult to reproduce.

Review decisions concern the quality and suitability of the contribution, not endorsement of any political position.

## Community conduct

Discuss people and political groups respectfully. Focus review comments on evidence, methodology, wording, and reproducibility. Harassment, threats, personal attacks, deliberate disinformation, and exposure of private information are not acceptable.
