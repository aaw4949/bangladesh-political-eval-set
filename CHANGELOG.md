# Changelog

## Unreleased

### Changed

- Removed 72 exact duplicate source rows.
- Added stable `pair_id` values and original/swapped orientations.
- Counterbalanced every prompt pair to reduce A/B ordering effects.
- Replaced malformed analysis prompts with `Assess the claim that {stance}`.
- Consolidated overlapping social and historical category names.
- Redesigned evaluator prompts to separate untrusted inputs and return JSON.
- Added a sourced factuality and citation-support evaluator.

### Added

- Automated dataset validation and evaluator-template tests.
- GitHub Actions validation workflow.
- Topic-level provenance and review-status scaffold.
- Dataset card, data license, changelog, and CODEOWNERS.
