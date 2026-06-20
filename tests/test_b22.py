"""B22 Self-modification risk tests."""
from pathlib import Path

from clawseccheck.checks import check_self_modification
from clawseccheck.collector import Context


def _ctx(cfg=None, home="/x"):
    c = Context(home=Path(home))
    c.config = cfg or {}
    c.bootstrap = {}
    return c


def _make_workspace(tmp_path, soul_mode=0o644, ws_mode=0o755, skills_mode=None):
    """Create a minimal workspace with SOUL.md and optionally a skills dir."""
    ws = tmp_path / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    ws.chmod(ws_mode)
    soul = ws / "SOUL.md"
    soul.write_text("I am the agent.")
    soul.chmod(soul_mode)
    if skills_mode is not None:
        sk = ws / "skills"
        sk.mkdir(exist_ok=True)
        sk.chmod(skills_mode)
    return ws


def _cfg_with_tools(approval=None):
    """Config with fs_write tool present."""
    cfg = {"tools": {"allow": ["fs_write", "shell"]}}
    if approval is not None:
        cfg["tools"]["requireApproval"] = approval
    return cfg


# ---- condition (a): no tools -> UNKNOWN ----
def test_b22_no_tools_is_unknown(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    c = _ctx({}, home=str(tmp_path))
    assert check_self_modification(c).status == "UNKNOWN"


# ---- condition (b): tools present but no writable targets -> UNKNOWN ----
def test_b22_tools_but_tight_perms_is_unknown(tmp_path):
    _make_workspace(tmp_path, soul_mode=0o600, ws_mode=0o700)
    c = _ctx(_cfg_with_tools(), home=str(tmp_path))
    assert check_self_modification(c).status == "UNKNOWN"


# ---- FAIL: tools + writable workspace dir + no approval ----
def test_b22_world_writable_ws_dir_no_approval_fails(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    c = _ctx(_cfg_with_tools(), home=str(tmp_path))
    result = check_self_modification(c)
    assert result.status == "FAIL"
    assert result.id == "B22"


# ---- FAIL: tools + group-writable SOUL.md + no approval ----
def test_b22_group_writable_soul_no_approval_fails(tmp_path):
    _make_workspace(tmp_path, soul_mode=0o664, ws_mode=0o700)
    c = _ctx(_cfg_with_tools(), home=str(tmp_path))
    assert check_self_modification(c).status == "FAIL"


# ---- FAIL: tools + world-writable skills dir + no approval ----
def test_b22_world_writable_skills_dir_no_approval_fails(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o700, skills_mode=0o777)
    # Also need a top-level skills dir (outside workspace)
    sk = tmp_path / "skills"
    sk.mkdir(exist_ok=True)
    sk.chmod(0o777)
    c = _ctx(_cfg_with_tools(), home=str(tmp_path))
    assert check_self_modification(c).status == "FAIL"


# ---- WARN: tools + writable target + approval present ----
def test_b22_writable_with_approval_warns(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    c = _ctx(_cfg_with_tools(approval=True), home=str(tmp_path))
    assert check_self_modification(c).status == "WARN"


# ---- WARN: elevated.requireApproval counts as approval ----
def test_b22_elevated_approval_counts(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    cfg = {"tools": {"allow": ["fs_write"], "elevated": {"requireApproval": True}}}
    c = _ctx(cfg, home=str(tmp_path))
    assert check_self_modification(c).status == "WARN"


# ---- approval=False must not suppress FAIL ----
def test_b22_approval_false_still_fails(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    c = _ctx(_cfg_with_tools(approval=False), home=str(tmp_path))
    assert check_self_modification(c).status == "FAIL"


# ---- approval="never" must not suppress FAIL ----
def test_b22_approval_never_still_fails(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    c = _ctx(_cfg_with_tools(approval="never"), home=str(tmp_path))
    assert check_self_modification(c).status == "FAIL"


# ---- elevated tools trigger condition (a) ----
def test_b22_elevated_tools_count(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    cfg = {"tools": {"elevated": {"allowFrom": ["owner@example.com"]}}}
    c = _ctx(cfg, home=str(tmp_path))
    assert check_self_modification(c).status == "FAIL"


# ---- no workspace at all -> UNKNOWN (no writable targets found) ----
def test_b22_no_workspace_is_unknown(tmp_path):
    c = _ctx(_cfg_with_tools(), home=str(tmp_path))
    assert check_self_modification(c).status == "UNKNOWN"


# ---- Windows (non-POSIX) -> UNKNOWN ----
def test_b22_windows_is_unknown(monkeypatch, tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    from clawseccheck import checks
    monkeypatch.setattr(checks, "_is_posix", lambda: False)
    c = _ctx(_cfg_with_tools(), home=str(tmp_path))
    assert check_self_modification(c).status == "UNKNOWN"


# ---- finding metadata ----
def test_b22_finding_has_correct_severity(tmp_path):
    _make_workspace(tmp_path, ws_mode=0o777)
    c = _ctx(_cfg_with_tools(), home=str(tmp_path))
    result = check_self_modification(c)
    assert result.severity == "HIGH"
    assert result.scored is True
