# Media Evaluation Protocol

## Scope

This protocol supports transparent, repeatable assessment of political framing
and factual reliability in Bangladeshi news media. It must not be used to
blacklist outlets or infer the beliefs of individual journalists.

## Required evidence

An outlet assessment should normally include:

- ownership and beneficial-control records;
- publicly documented political roles held by owners or senior managers;
- a stratified sample of at least 30 political items across at least 90 days;
- news, headline, image, source-selection, and opinion-page observations;
- corrections, retractions, and relevant independent fact-check findings;
- evidence from more than one type of source;
- an assessment period and archive link where legally and ethically possible.

A smaller sample must remain `provisional` and display its limitations.

## Sampling

1. Define the assessment start and end dates before selecting content.
2. Include major political actors and events from across the period.
3. Separate straight news, editorials, opinion columns, and talk shows.
4. Avoid sampling only viral, controversial, or search-ranked items.
5. Preserve the query, inclusion rules, and excluded-item count.

## Coding

Each observation is stored in `data/evidence/media_assessments.csv`.

Coders should record:

- the actor or issue covered;
- the relevant analytical axis;
- the observed framing;
- a bounded coded value;
- the evidence URL and publication date;
- a short quotation or paraphrase within copyright limits;
- whether a second coder reviewed the observation.

At least 20% of observations should be double-coded. Report agreement and
adjudicate material disagreements before publishing an outlet label.

## Rating states

- `unreviewed`: no completed content audit;
- `in_review`: sampling or coding is underway;
- `provisional`: evidence exists but the minimum standard is incomplete;
- `reviewed`: the stated protocol and review requirements are satisfied;
- `insufficient_evidence`: available evidence cannot support a rating;
- `stale`: the review window is no longer representative.

## Labels and scores

Scores are derived summaries, not primary evidence. Party-alignment values are
independent rather than zero-sum. A label may be produced only when:

- the minimum evidence count is met;
- the assessment period is recorded;
- confidence is above the published threshold;
- contradictory evidence is summarized;
- a reviewer approves the result.

Political orientation and reliability must be reported separately. Accurate
reporting can have a viewpoint, and viewpoint-neutral reporting can still be
factually weak.

## Sensitive claims

Claims about living people, covert influence, corruption, propaganda,
misinformation, or foreign control require especially strong sourcing. Use
neutral wording, identify allegations as allegations, and include responses or
contrary evidence where available.

## Updating assessments

Review an outlet after:

- a national election or change of government;
- a major ownership or editorial-leadership change;
- a sustained change in editorial policy;
- twelve months since the last review.

Retain historical versions instead of overwriting them.
