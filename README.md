# claw-self-improving-plus

A conservative self-improvement workflow for OpenClaw agents, powered by the `learning-promoter` skill.

## Agent install instructions

If you are an OpenClaw agent reading this repository for installation or packaging:

- Do **not** use the repository root as the skill package.
- Use this directory as the installable skill:

```text
skill/learning-promoter/
```

- The root of the installable package must contain `SKILL.md`.
- If publishing to ClawHub or packaging for installation, package **only** `skill/learning-promoter/`.
- Do **not** include repository-level files such as `README.md`, `RELEASE_NOTES.md`, `examples/`, or `tests/` in the skill package.

## Project vs skill

- `claw-self-improving-plus` = the full GitHub project
- `learning-promoter` = the actual skill and core promotion engine

## What the skill does

`learning-promoter` turns mistakes, corrections, discoveries, decisions, and regressions into structured learnings and controlled promotion candidates.

Core flow:

1. capture raw learnings
2. score reuse, confidence, scope, and promotion worthiness
3. detect likely duplicates
4. consolidate repeated patterns
5. build and age a prioritized backlog
6. draft anchored patches for long-term files
7. detect conflicts and existing promotions
8. require human approval before apply
9. apply only approved patches

## Installable layout

```text
skill/learning-promoter/
├── SKILL.md
├── scripts/
└── references/
```

## Default promotion targets

The default targets are:

- `SOUL.md`
- `AGENTS.md`
- `TOOLS.md`
- `MEMORY.md`

If your workspace uses different files, update the routing and anchor rules in:

- `skill/learning-promoter/scripts/draft_patches.py`
- `skill/learning-promoter/scripts/apply_approved_patches.py`

## Minimal usage

From the repository root:

### Capture

```bash
python3 skill/learning-promoter/scripts/capture_learning.py \
  --store .learnings/inbox.jsonl \
  --type correction \
  --summary "User prefers concise replies" \
  --details "Keep future responses brief by default." \
  --evidence "Explicitly stated by the user" \
  --source chat
```

### Run the pipeline

```bash
python3 skill/learning-promoter/scripts/run_pipeline.py \
  .learnings/inbox.jsonl \
  --work-dir .learnings \
  --base-dir /path/to/agent-workspace \
  --archive-input
```

### Review patch candidates

```bash
python3 skill/learning-promoter/scripts/review_patches.py \
  .learnings/patches.json list
```

### Apply approved patches safely

```bash
python3 skill/learning-promoter/scripts/apply_approved_patches.py \
  .learnings/patches.json \
  --base-dir /path/to/agent-workspace \
  --dry-run \
  -o .learnings/apply-report.json
```

## Pipeline outputs

Recommended working directory:

```text
.learnings/
├── inbox.jsonl
├── scored.jsonl
├── merge.json
├── consolidated.jsonl
├── backlog.json
├── backlog-aged.json
├── patches.json
├── conflicts.json
├── existing-promotions.json
├── apply-report.json
└── archive/
```

## Repository layout

```text
.
├── README.md
├── LICENSE
├── RELEASE_NOTES.md
├── examples/
├── tests/
└── skill/
   └── learning-promoter/
      ├── SKILL.md
      ├── scripts/
      └── references/
```

## Tests

Run:

```bash
python3 tests/test_learning_promoter.py
```

## Packaging

If your platform expects a skill package, package this directory only:

```text
skill/learning-promoter/
```

## Release notes

See `RELEASE_NOTES.md`.

## License

MIT License.
