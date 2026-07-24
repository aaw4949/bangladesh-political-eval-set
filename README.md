# Bangladesh Political Eval Set

A paired-prompt evaluation dataset for testing whether language models handle opposing positions in Bangladesh's political context consistently.

## Dataset summary

- 1,908 evaluation rows
- 122 topics
- 8 main categories
- 12 columns
- Coverage includes political figures, parties and groups (including Bangladesh Jamaat-e-Islami and the National Citizen Party), constitutional issues, elections, governance, protests, foreign relations, and major political events

## Schema

| Column | Description |
|---|---|
| `split` | Dataset split |
| `main_category` | Broad Bangladesh-relevant category |
| `topic_name` | Normalized topic identifier |
| `partisan` | Whether the prompt pair represents opposing political positions |
| `template_category` | Type of task requested |
| `template` | Reusable prompt template |
| `stance_a` | First position |
| `stance_b` | Opposing position |
| `prompt_a` | Prompt generated from the first position |
| `prompt_b` | Prompt generated from the opposing position |
| `prompt_a_group` | Analytical label for the first position |
| `prompt_b_group` | Analytical label for the opposing position |

## How to use it

1. Run `prompt_a` and `prompt_b` separately through the same model and settings.
2. Save both responses with the row's topic and group labels.
3. Score each response using the same rubric—for example factuality, source quality, completeness, tone, uncertainty, and refusal behavior.
4. Compare the paired scores. Large unexplained differences can indicate inconsistent treatment of opposing positions.
5. Aggregate results by `main_category`, `topic_name`, or prompt group to identify patterns.

This dataset can also help evaluate a news-briefing system, but it is not itself a news source. For briefing tests, retrieve current reporting separately, require citations, and use these rows as coverage and consistency checks.

## Important limitations

- Political claims may be disputed, sensitive, or time-dependent.
- Prompts mentioning living people require careful fact-checking and neutral treatment.
- The dataset measures model behavior and consistency; it does not establish which political position is true.
- Revalidate names, party status, constitutional developments, and event descriptions before time-sensitive use.

## Source

Maintained in the [Bangladesh political eval set Google Sheet](https://docs.google.com/spreadsheets/d/1gGaVIOsIe8-spqkWoY1TWPMGt4xp5aDzxH71VboUJ3M/edit).

Last synchronized from the live sheet: 25 July 2026.
