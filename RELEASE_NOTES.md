# Release Notes

## v0.2.0 — Phase 3 foundation

This release turns `learning-promoter` from a conservative promotion pipeline into a stronger long-term learning workflow.

### Added

- structured scoring with promotion worthiness
- stronger duplicate detection and consolidation
- prioritized backlog generation
- backlog aging for periodic review
- cleaner review rendering
- patch conflict detection
- existing-promotion checks before apply
- archive support for processed input batches
- one-shot pipeline orchestration
- expanded example data and test coverage

### Improved

- patch drafting now matches real workspace anchors more reliably
- apply flow supports safer dry-run verification
- consolidated learnings preserve combined evidence and related patterns
- README now explains the workflow more clearly for first-time users

### Why this matters

The project now supports a more realistic self-improvement loop:

1. capture raw lessons
2. rank and compress them into stronger knowledge
3. review the highest-value items first
4. apply only explicit, approved promotions

That keeps long-term memory cleaner while still letting the system compound useful experience over time.

---

## v0.1.0 — Initial conservative pipeline

Initial public foundation for `learning-promoter`.

### Added

- capture structured learning records in JSONL
- score learnings by reuse value, confidence, and scope
- group likely duplicates before promotion
- draft anchored patch candidates for long-term files
- review candidates with approve, reject, or skip actions
- apply only explicitly approved patches

### Design stance

This project is intentionally conservative.
It does not auto-rewrite long-term memory or behavior files by default.
The goal is to make self-improvement useful without letting permanent rules drift into noise.

### Notes

- repository content is English-first
- skill scripts avoid hardcoded local workspace paths
- `--base-dir` is the main runtime input when checking or applying promotions
