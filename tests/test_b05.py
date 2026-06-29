"""B5 — supply-chain integrity tests.

Grounded against check_supply_chain (checks.py:778).

B5 is advisory-only and always returns UNKNOWN — it never PASS, FAIL, or WARN because
per-manifest pinning/integrity metadata is not recorded in openclaw.json. Two code paths:
1. No plugins/skills declared in config  -> UNKNOWN "No plugins/skills declared"
2. Plugins/skills present in config      -> UNKNOWN "cannot assess supply-chain integrity"
"""
from pathlib import Path

from clawseccheck.catalog import UNKNOWN
from clawseccheck.checks import check_supply_chain
from clawseccheck.collector import Context


def _ctx(cfg: dict) -> Context:
    c = Context(home=Path("/nonexistent"))
    c.config = cfg
    return c


# ---- UNKNOWN: no plugins/skills declared ----

def test_b05_empty_config_unknown():
    f = check_supply_chain(_ctx({}))
    assert f.status == UNKNOWN
    assert "plugins" in f.detail.lower() or "skills" in f.detail.lower()


def test_b05_unrelated_config_no_plugins_unknown():
    cfg = {"gateway": {"bind": "127.0.0.1:8080"}}
    f = check_supply_chain(_ctx(cfg))
    assert f.status == UNKNOWN


# ---- UNKNOWN: plugins/skills present (integrity not in openclaw.json) ----

def test_b05_plugins_entries_present_unknown():
    cfg = {"plugins": {"entries": {"slack": {}}}}
    f = check_supply_chain(_ctx(cfg))
    assert f.status == UNKNOWN
    assert "integrity" in f.detail.lower() or "assess" in f.detail.lower()


def test_b05_skills_entries_present_unknown():
    cfg = {"skills": {"entries": {"my-skill": {}}}}
    f = check_supply_chain(_ctx(cfg))
    assert f.status == UNKNOWN


def test_b05_bare_plugins_dict_unknown():
    # plugins key present but without entries sub-key — cfg.get("plugins") is still truthy
    cfg = {"plugins": {"allow": ["slack"]}}
    f = check_supply_chain(_ctx(cfg))
    assert f.status == UNKNOWN


# ---- B5 is never PASS, FAIL, or WARN ----

def test_b05_never_pass_fail_warn():
    for cfg in (
        {},
        {"plugins": {"entries": {"slack": {}}}},
        {"skills": {"entries": {"my-skill": {}}}},
    ):
        result = check_supply_chain(_ctx(cfg))
        assert result.status not in ("PASS", "FAIL", "WARN"), (
            f"B5 should never return PASS/FAIL/WARN; got {result.status} for cfg={cfg}"
        )
