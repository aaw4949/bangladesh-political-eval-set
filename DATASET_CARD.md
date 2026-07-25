# Dataset Card

## Overview

The Bangladesh Political Eval Set is a paired-prompt dataset for measuring
whether language models respond consistently to opposing positions in
Bangladesh's political context.

It is an evaluation instrument, not a factual knowledge base, opinion poll,
news source, or ranking of political groups.

## Unit of analysis

The logical unit is a prompt pair identified by `pair_id`. Each pair is
published twice:

- `original`: the source A/B ordering;
- `swapped`: the same stances, prompts, and group labels in reverse order.

Results should be aggregated at the unique-pair level so the two orientations
do not count as independent evidence.

## Composition

- 1,836 unique prompt pairs
- 3,672 oriented rows
- 122 topics
- 6 main categories
- 9 reusable task templates

The dataset includes political figures, parties and groups, constitutional
questions, public policy, social and identity issues, public health, foreign
relations, and historical or current events.

## Intended uses

- paired refusal and compliance evaluation;
- comparative response-quality evaluation;
- hedging and caveat analysis;
- regression testing across models or system prompts;
- consistency testing in sourced news-briefing pipelines.

## Out-of-scope uses

Do not use the dataset:

- as proof that a stance or allegation is true;
- as a comprehensive list of Bangladeshi political actors;
- to infer public opinion or electoral support;
- to make decisions about individuals;
- as a substitute for current, independently retrieved sources.

## Construction and quality controls

Rows use matched templates with opposing stances. Exact duplicate source rows
were removed. Prompts were regenerated from their stored template and stance.
Each logical pair was counterbalanced across A/B orientation.

Automated validation checks:

- schema and required fields;
- stable pair identifiers and orientation integrity;
- exact duplicates and identical paired prompts;
- template substitution;
- accepted categorical values;
- topic naming;
- spreadsheet formula-injection prefixes;
- known malformed prompt constructions.

## Known limitations

- Coverage is intentionally broad but not exhaustive.
- Political relevance and officeholding change over time.
- Category and topic distributions are not population weights.
- Nine reusable templates cannot represent every real user request.
- Counterbalancing reduces order effects but does not eliminate evaluator bias.
- Topic-level provenance is incomplete where
  `metadata/topics.csv` records `sources_needed`.
- Some stances concern disputed interpretations that require attribution and
  current source review.

## Recommended evaluation practice

- keep model settings identical across paired requests;
- evaluate both orientations but aggregate them under one `pair_id`;
- randomize presentation order;
- use blinded or multiple evaluators;
- retain full prompts, responses, model settings, timestamps, and evaluator
  outputs;
- report sample sizes and uncertainty by topic and category;
- manually review large disparities and consequential claims.

## Maintenance

Topic provenance and review status are tracked in `metadata/topics.csv`.
Substantive updates should include authoritative sources and an `as_of` or
review date. Dataset releases should record changes in `CHANGELOG.md`.
