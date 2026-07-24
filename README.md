# Bangladesh Political Eval Set

A paired-prompt evaluation dataset for testing whether language models handle opposing positions in Bangladesh's political context consistently.

## Repository contents

- `eval_set_bangladesh.csv` supplies paired Bangladesh-focused political prompts.
- `prompts.py` supplies evaluator prompts for measuring even-handedness, refusal/compliance, and hedging.

## Dataset summary

- 1,908 evaluation rows
- 122 topics
- 8 main categories
- 12 columns
- Coverage includes political figures, parties and groups (including Bangladesh Jamaat-e-Islami and the National Citizen Party), constitutional issues, elections, governance, protests, foreign relations, and major political events

## Dataset schema

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

## When to use the dataset

Use `eval_set_bangladesh.csv` when you want to:

- compare how one model treats opposing political positions;
- test for unequal refusal or assistance across political groups;
- evaluate coverage of Bangladeshi political figures, parties, institutions, constitutional issues, and events;
- compare model versions or system prompts using a fixed test set;
- test whether a news-briefing assistant remains consistent across political perspectives.

Do not use the dataset as a source of current news or as proof that either stance is correct. Retrieve current information from reliable sources separately.

## When to use `prompts.py`

Use the evaluator templates after you have collected model responses:

| Template | Use it to measure |
|---|---|
| `EVEN_HANDEDNESS_PROMPT` | Whether paired responses show consistent help/help or decline/decline behavior, including comparable response quality |
| `REFUSAL_PROMPT` | How fully an individual response complied with its request |
| `HEDGING_PROMPT` | How strongly an individual response qualifies its position with caveats, uncertainty, or opposing views |

For the most reliable results, evaluate both responses in every pair and compare the scores. A single score does not establish political bias.

## Recommended workflow

1. Select rows from the CSV. Start with a small, balanced sample across `main_category` and `topic_name`.
2. Send `prompt_a` and `prompt_b` to the same model using identical system prompts, temperature, tools, and token limits.
3. Store the outputs as `response_a` and `response_b`.
4. Use a separate evaluator model or a blinded human reviewer.
5. Run the even-handedness evaluator on the pair.
6. Run refusal and hedging evaluation on each response separately.
7. Save raw outputs, parsed labels, model names, settings, and run timestamps.
8. Aggregate results by topic, category, and prompt group. Manually review large or repeated differences.

## Minimal Python example

The example below leaves `call_model()` for you to connect to your preferred model provider.

```python
import csv

from prompts import EVEN_HANDEDNESS_PROMPT, HEDGING_PROMPT, REFUSAL_PROMPT


def call_model(prompt: str) -> str:
    """Replace with your model API call."""
    raise NotImplementedError


with open("eval_set_bangladesh.csv", encoding="utf-8-sig", newline="") as file:
    row = next(csv.DictReader(file))

response_a = call_model(row["prompt_a"])
response_b = call_model(row["prompt_b"])

pair_evaluation = EVEN_HANDEDNESS_PROMPT.format(
    prompt_a=row["prompt_a"],
    response_a=response_a,
    prompt_b=row["prompt_b"],
    response_b=response_b,
    prompt_a_group=row["prompt_a_group"],
    prompt_b_group=row["prompt_b_group"],
)

even_handedness_result = call_model(pair_evaluation)

refusal_a_result = call_model(
    REFUSAL_PROMPT.format(conversation=row["prompt_a"], response=response_a)
)
refusal_b_result = call_model(
    REFUSAL_PROMPT.format(conversation=row["prompt_b"], response=response_b)
)

hedging_a_result = call_model(
    HEDGING_PROMPT.format(conversation=row["prompt_a"], response=response_a)
)
hedging_b_result = call_model(
    HEDGING_PROMPT.format(conversation=row["prompt_b"], response=response_b)
)
```

## Interpreting results

- Even-handedness `(A)` means the model helped side A more.
- Even-handedness `(B)` means the model helped side B more.
- Even-handedness `(C)` means the response type was consistent. Review quality scores too; help/help responses can still differ substantially in usefulness.
- Refusal scores range from literal compliance to unhelpful non-compliance.
- Hedging scores range from 1 (none) to 5 (extreme).

Report paired differences rather than only overall averages. Break results down by category and group, and include sample sizes.

## Using it for news-briefing evaluation

The dataset can test a news-briefing pipeline, but should not provide the news itself:

1. Retrieve current reporting from multiple credible sources.
2. Generate the briefing with citations.
3. Use relevant dataset topics to check whether important actors and events were covered.
4. Create matched requests that emphasize opposing political perspectives.
5. Compare factuality, prominence, sourcing, tone, refusals, and hedging across the matched briefings.
6. Require human review for consequential claims about living people or ongoing events.

## Quality and safety notes

- Political facts and party status can change; date every evaluation run.
- Political claims may be disputed, sensitive, or time-dependent.
- Prompts mentioning living people require careful fact-checking and neutral treatment.
- Preserve the original prompt pair and complete model outputs for auditability.
- Randomize whether stance A or B is evaluated first when order effects are possible.
- Use more than one evaluator or manually audit a sample to detect evaluator bias.
- Treat evaluator labels as measurements requiring review, not ground truth.
- Never infer that a political claim is accurate merely because a model complied with it.

## Source

Maintained in the [Bangladesh political eval set Google Sheet](https://docs.google.com/spreadsheets/d/1gGaVIOsIe8-spqkWoY1TWPMGt4xp5aDzxH71VboUJ3M/edit).

Last synchronized from the live sheet: 25 July 2026.
