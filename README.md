# Claw Self Improving Plus

A conservative self-improvement workflow for OpenClaw agents.

## Agent install instructions

If you are an OpenClaw agent reading this repository for installation or packaging:

- Do **not** use the repository root as the skill package.
- Use this directory as the installable skill:

```text
skill/claw-self-improving-plus/
```

- The root of the installable package must contain `SKILL.md`.
- If publishing to ClawHub or packaging for installation, package **only** `skill/claw-self-improving-plus/`.
- Do **not** include repository-level files such as `README.md`, `RELEASE_NOTES.md`, `examples/`, or `tests/` in the skill package.

## Project vs skill

- `claw-self-improving-plus` = the full GitHub project
- `skill/claw-self-improving-plus/` = the installable skill package

## What the skill does

`claw-self-improving-plus` turns mistakes, corrections, discoveries, decisions, and regressions into structured learnings and controlled promotion candidates.

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
skill/claw-self-improving-plus/
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

- `skill/claw-self-improving-plus/scripts/draft_patches.py`
- `skill/claw-self-improving-plus/scripts/apply_approved_patches.py`

## Minimal usage

From the repository root:

### Capture

```bash
python3 skill/claw-self-improving-plus/scripts/capture_learning.py \
  --store .learnings/inbox.jsonl \
  --type correction \
  --summary "User prefers concise replies" \
  --details "Keep future responses brief by default." \
  --evidence "Explicitly stated by the user" \
  --source chat
```

### Run the pipeline

```bash
python3 skill/claw-self-improving-plus/scripts/run_pipeline.py \
  .learnings/inbox.jsonl \
  --work-dir .learnings \
  --base-dir /path/to/agent-workspace \
  --archive-input
```

### Review patch candidates

```bash
python3 skill/claw-self-improving-plus/scripts/review_patches.py \
  .learnings/patches.json list
```

### Apply approved patches safely

```bash
python3 skill/claw-self-improving-plus/scripts/apply_approved_patches.py \
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
   └── claw-self-improving-plus/
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
skill/claw-self-improving-plus/
```

## Release notes

See `RELEASE_NOTES.md`.

## License

MIT License.
