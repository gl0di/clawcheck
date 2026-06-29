"""B3 — least-privilege / tool-reachability tests.

Grounded against check_least_privilege (checks.py:581).

Verdict map:
- FAIL: '*' in tools.elevated.allowFrom (flat string, flat list, or per-provider dict
        string/list value), OR total entries in allowFrom > 25.
- WARN: tools.profile != 'minimal' (non-empty value), OR plugins.entries present
        without a plugins.allow reachability allowlist.
- PASS: no elevated wildcard, entries <= 25, minimal/absent profile, plugins constrained.
No UNKNOWN path exists.
"""
from pathlib import Path

from clawseccheck.catalog import FAIL, PASS, WARN
from clawseccheck.checks import check_least_privilege
from clawseccheck.collector import Context


def _ctx(cfg: dict) -> Context:
    c = Context(home=Path("/nonexistent"))
    c.config = cfg
    return c


# ---- PASS ----

def test_b03_empty_config_pass():
    assert check_least_privilege(_ctx({})).status == PASS


def test_b03_small_allowfrom_dict_pass():
    cfg = {"tools": {"elevated": {"allowFrom": {"discord": ["user-123", "user-456"]}}}}
    assert check_least_privilege(_ctx(cfg)).status == PASS


def test_b03_minimal_profile_pass():
    cfg = {"tools": {"profile": "minimal"}}
    assert check_least_privilege(_ctx(cfg)).status == PASS


def test_b03_plugins_entries_with_allow_passes():
    cfg = {"plugins": {"entries": {"slack": {}}, "allow": ["slack"]}}
    assert check_least_privilege(_ctx(cfg)).status == PASS


# ---- FAIL: wildcard in tools.elevated.allowFrom ----

def test_b03_flat_wildcard_string_allowfrom_fail():
    """Legacy / hypothetical flat wildcard string."""
    cfg = {"tools": {"elevated": {"allowFrom": "*"}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == FAIL


def test_b03_flat_wildcard_list_allowfrom_fail():
    """Flat list containing '*'."""
    cfg = {"tools": {"elevated": {"allowFrom": ["*"]}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == FAIL


def test_b03_dict_wildcard_string_value_fail():
    """Per-provider dict where the value is the bare string '*'."""
    cfg = {"tools": {"elevated": {"allowFrom": {"discord": "*"}}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == FAIL


def test_b03_dict_wildcard_in_list_value_fail():
    """Per-provider dict where the list value contains '*'."""
    cfg = {"tools": {"elevated": {"allowFrom": {"telegram": ["*"]}}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == FAIL


def test_b03_wildcard_evidence_populated_on_fail():
    cfg = {"tools": {"elevated": {"allowFrom": {"discord": ["*"]}}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == FAIL
    assert len(f.evidence) >= 1


# ---- FAIL: too many entries in allowFrom ----

def test_b03_dict_total_entries_over_25_fail():
    """26 total entries across two providers (>25 threshold)."""
    cfg = {"tools": {"elevated": {"allowFrom": {
        "discord": ["u" + str(i) for i in range(20)],
        "telegram": ["v" + str(i) for i in range(6)],
    }}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == FAIL


def test_b03_flat_list_over_25_entries_fail():
    """Flat list with 26 entries."""
    cfg = {"tools": {"elevated": {"allowFrom": ["u" + str(i) for i in range(26)]}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == FAIL


def test_b03_dict_exactly_25_entries_pass():
    """Exactly 25 entries — boundary: does NOT exceed the threshold."""
    cfg = {"tools": {"elevated": {"allowFrom": {
        "discord": ["u" + str(i) for i in range(25)],
    }}}}
    assert check_least_privilege(_ctx(cfg)).status == PASS


# ---- WARN: profile broader than minimal ----

def test_b03_profile_coding_warns():
    cfg = {"tools": {"profile": "coding"}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == WARN
    assert any("profile" in e.lower() for e in f.evidence)


def test_b03_profile_full_warns():
    cfg = {"tools": {"profile": "full"}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == WARN


# ---- WARN: plugins.entries present without plugins.allow ----

def test_b03_plugins_entries_without_allow_warns():
    cfg = {"plugins": {"entries": {"slack": {}}}}
    f = check_least_privilege(_ctx(cfg))
    assert f.status == WARN
    assert any("plugins" in e.lower() for e in f.evidence)


# ---- FAIL takes priority over WARN when both conditions fire ----

def test_b03_wildcard_plus_broad_profile_still_fail():
    cfg = {
        "tools": {
            "elevated": {"allowFrom": {"discord": ["*"]}},
            "profile": "coding",
        }
    }
    assert check_least_privilege(_ctx(cfg)).status == FAIL
