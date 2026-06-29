"""B9 — sensitive-data redaction in tool output / logs (check_leak).

Verdicts:
  PASS : logging.redactSensitive == "tools"
  FAIL : logging.redactSensitive == "off"
  WARN : field absent (None) OR unexpected value
  (no UNKNOWN)
"""
from pathlib import Path

from clawseccheck.catalog import FAIL, PASS, UNKNOWN, WARN
from clawseccheck.checks import check_leak
from clawseccheck.collector import Context


def _ctx(cfg: dict) -> Context:
    c = Context(home=Path("/nonexistent"))
    c.config = cfg
    return c


# ---- PASS ----

def test_b09_redact_tools_passes():
    f = check_leak(_ctx({"logging": {"redactSensitive": "tools"}}))
    assert f.status == PASS


# ---- FAIL ----

def test_b09_redact_off_fails():
    f = check_leak(_ctx({"logging": {"redactSensitive": "off"}}))
    assert f.status == FAIL
    assert "off" in f.detail.lower() or "redact" in f.detail.lower()


# ---- WARN: field absent ----

def test_b09_field_absent_warns():
    # logging key missing entirely
    assert check_leak(_ctx({})).status == WARN


def test_b09_logging_present_but_field_absent_warns():
    # logging dict exists but redactSensitive is not set
    assert check_leak(_ctx({"logging": {}})).status == WARN


# ---- WARN: unexpected value ----

def test_b09_unexpected_value_all_warns():
    f = check_leak(_ctx({"logging": {"redactSensitive": "all"}}))
    assert f.status == WARN


def test_b09_unexpected_value_full_warns():
    assert check_leak(_ctx({"logging": {"redactSensitive": "full"}})).status == WARN


def test_b09_unexpected_value_true_warns():
    assert check_leak(_ctx({"logging": {"redactSensitive": True}})).status == WARN


# ---- never UNKNOWN ----

def test_b09_never_unknown():
    for cfg in (
        {},
        {"logging": {"redactSensitive": "tools"}},
        {"logging": {"redactSensitive": "off"}},
        {"logging": {"redactSensitive": "all"}},
        {"logging": {}},
    ):
        assert check_leak(_ctx(cfg)).status != UNKNOWN, f"unexpected UNKNOWN for {cfg}"
