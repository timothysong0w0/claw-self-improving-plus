#!/usr/bin/env python3
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "learning-promoter" / "scripts"


def run(*args):
    return subprocess.run(["python3", *map(str, args)], check=True, capture_output=True, text=True)


def test_score_and_targets(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    inbox = tmp_path / "inbox.jsonl"
    inbox.write_text(
        json.dumps({
            "type": "correction",
            "summary": "User prefers Simplified Chinese replies",
            "details": "Use Simplified Chinese by default in future responses",
            "evidence": "User explicitly stated this",
            "source": "chat",
            "status": "captured",
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "scored.jsonl"
    run(SCRIPTS / "score_learnings.py", inbox, "-o", out)
    rows = [json.loads(x) for x in out.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert rows[0]["reuse_value"] in {"medium", "high"}
    assert rows[0]["confidence"] in {"medium", "high"}
    assert "MEMORY.md" in rows[0]["promotion_target_candidates"]


def test_draft_uses_real_tools_anchor(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    scored = tmp_path / "scored.jsonl"
    scored.write_text(
        json.dumps({
            "id": "uv-policy",
            "timestamp": "2026-03-11T05:01:00+00:00",
            "source": "workspace",
            "type": "decision",
            "summary": "Use uv instead of pip for Python dependency management",
            "details": "Workspace policy says to use uv and the .venv Python path for scripts.",
            "evidence": "TOOLS.md documents the Python and UV policy",
            "status": "scored",
            "reuse_value": "high",
            "confidence": "high",
            "impact_scope": "workspace",
            "promotion_target_candidates": ["TOOLS.md"],
            "promotion_worthiness": "high"
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    out = tmp_path / "patches.json"
    run(SCRIPTS / "draft_patches.py", scored, "-o", out)
    data = json.loads(out.read_text(encoding="utf-8"))
    patch = data["patch_candidates"][0]
    assert patch["anchor"] == "## 🐍 Python & UV Policy"
    assert patch["target_file"] == "TOOLS.md"


def test_conflict_detector_finds_same_anchor(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    patches = tmp_path / "patches.json"
    patches.write_text(json.dumps({
        "patch_candidates": [
            {"id": "a", "target_file": "TOOLS.md", "anchor": "## Search Policy", "insert_mode": "after-anchor", "suggested_entry": "- one"},
            {"id": "b", "target_file": "TOOLS.md", "anchor": "## Search Policy", "insert_mode": "after-anchor", "suggested_entry": "- two"}
        ]
    }, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "conflicts.json"
    run(SCRIPTS / "detect_patch_conflicts.py", patches, "-o", out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["has_conflicts"] is True
    assert len(data["anchor_conflicts"]) == 1


def test_apply_dry_run_skips_duplicate_entry(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    base = tmp_path / "base"
    base.mkdir()
    tools = base / "TOOLS.md"
    tools.write_text("## 🐍 Python & UV Policy\n- existing\n", encoding="utf-8")
    patches = tmp_path / "patches.json"
    patches.write_text(json.dumps({
        "patch_candidates": [
            {
                "id": "dup",
                "target_file": "TOOLS.md",
                "anchor": "## 🐍 Python & UV Policy",
                "insert_mode": "after-anchor",
                "suggested_entry": "- existing",
                "approved": True
            }
        ]
    }, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "apply.json"
    run(SCRIPTS / "apply_approved_patches.py", patches, "--base-dir", base, "--dry-run", "-o", out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["results"][0]["status"] == "skipped"
    assert data["results"][0]["reason"] == "entry already present"


def test_merge_groups_near_duplicates(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    inbox = tmp_path / "near.jsonl"
    inbox.write_text(
        json.dumps({
            "id": "dup-1", "type": "decision", "summary": "Use uv instead of pip for Python installs",
            "details": "Workspace Python policy requires uv for package management.", "evidence": "TOOLS.md policy", "status": "captured"
        }, ensure_ascii=False) + "\n" +
        json.dumps({
            "id": "dup-2", "type": "decision", "summary": "Prefer uv over pip for Python dependency management",
            "details": "The workspace standard is uv plus the shared .venv.", "evidence": "TOOLS.md documents this rule", "status": "captured"
        }, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    scored = tmp_path / "scored.jsonl"
    merge = tmp_path / "merge.json"
    run(SCRIPTS / "score_learnings.py", inbox, "-o", scored)
    run(SCRIPTS / "merge_candidates.py", scored, "-o", merge)
    data = json.loads(merge.read_text(encoding="utf-8"))
    assert len(data["merge_groups"]) >= 1


def test_archive_batch_moves_file(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    inbox = tmp_path / "inbox.jsonl"
    inbox.write_text('{"id":"x"}\n', encoding="utf-8")
    archive_dir = tmp_path / "archive"
    run(SCRIPTS / "archive_batch.py", inbox, "--archive-dir", archive_dir)
    assert not inbox.exists()
    archived = list(archive_dir.glob("*-inbox.jsonl"))
    assert len(archived) == 1


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        test_score_and_targets(p / "t1")
        test_draft_uses_real_tools_anchor(p / "t2")
        test_conflict_detector_finds_same_anchor(p / "t3")
        test_apply_dry_run_skips_duplicate_entry(p / "t4")
        test_merge_groups_near_duplicates(p / "t5")
        test_archive_batch_moves_file(p / "t6")
        print("ok")
