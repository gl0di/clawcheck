"""State-directory and state-file permission tests (POSIX only).

Verifies that after a monitor snapshot or a history entry is written:
  - the state DIRECTORY is chmod 0o700 (owner-only)
  - the state FILE is chmod 0o600 (owner-only)

Skipped on Windows because POSIX permission bits are not meaningful there.
"""
from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest

from clawseccheck.monitor import save_state
from clawseccheck.history import record


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permissions not applicable on Windows")
def test_monitor_state_dir_is_owner_only(tmp_path):
    state_dir = tmp_path / ".clawseccheck"
    state_file = state_dir / "state.json"
    snap = {"version": 1, "score": 80, "grade": "B", "skills": {}, "bootstrap": {}, "checks": {}}

    save_state(state_file, snap)

    dir_mode = state_dir.stat().st_mode & 0o777
    assert dir_mode == 0o700, f"state dir mode should be 0o700, got {oct(dir_mode)}"


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permissions not applicable on Windows")
def test_monitor_state_file_is_owner_only(tmp_path):
    state_dir = tmp_path / ".clawseccheck"
    state_file = state_dir / "state.json"
    snap = {"version": 1, "score": 80, "grade": "B", "skills": {}, "bootstrap": {}, "checks": {}}

    save_state(state_file, snap)

    file_mode = state_file.stat().st_mode & 0o777
    assert file_mode == 0o600, f"state file mode should be 0o600, got {oct(file_mode)}"


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permissions not applicable on Windows")
def test_history_state_dir_is_owner_only(tmp_path):
    state_dir = tmp_path / ".clawseccheck"
    history_file = state_dir / "history.jsonl"
    score = SimpleNamespace(score=75, grade="C")

    record(score, path=str(history_file), when="2026-06-20")

    dir_mode = state_dir.stat().st_mode & 0o777
    assert dir_mode == 0o700, f"history dir mode should be 0o700, got {oct(dir_mode)}"


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permissions not applicable on Windows")
def test_history_state_file_is_owner_only(tmp_path):
    state_dir = tmp_path / ".clawseccheck"
    history_file = state_dir / "history.jsonl"
    score = SimpleNamespace(score=75, grade="C")

    record(score, path=str(history_file), when="2026-06-20")

    file_mode = history_file.stat().st_mode & 0o777
    assert file_mode == 0o600, f"history file mode should be 0o600, got {oct(file_mode)}"
