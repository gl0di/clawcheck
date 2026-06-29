"""B10 — audit-log observability (check_audit_log).

OpenClaw exposes no config field to toggle audit logging; audit is a CLI command
only. B10 is purely observational: it reports WARN when redaction is disabled
(logs may expose secrets/PII) and UNKNOWN for everything else.

Verdicts:
  WARN    : logging.redactSensitive == "off"
  UNKNOWN : any other config (including absent / other values)
  (NEVER PASS or FAIL)
"""
from pathlib import Path

from clawseccheck.catalog import FAIL, PASS, UNKNOWN, WARN
from clawseccheck.checks import check_audit_log
from clawseccheck.collector import Context


def _ctx(cfg: dict) -> Context:
    c = Context(home=Path("/nonexistent"))
    c.config = cfg
    return c


# ---- WARN: redaction explicitly disabled ----

def test_b10_redact_off_warns():
    f = check_audit_log(_ctx({"logging": {"redactSensitive": "off"}}))
    assert f.status == WARN


def test_b10_redact_off_detail_mentions_redact():
    f = check_audit_log(_ctx({"logging": {"redactSensitive": "off"}}))
    assert "redact" in f.detail.lower() or "off" in f.detail.lower()


# ---- UNKNOWN: everything else ----

def test_b10_empty_config_unknown():
    assert check_audit_log(_ctx({})).status == UNKNOWN


def test_b10_redact_tools_set_unknown():
    # redaction enabled -> cannot infer audit state -> UNKNOWN (not a PASS)
    assert check_audit_log(_ctx({"logging": {"redactSensitive": "tools"}})).status == UNKNOWN


def test_b10_logging_absent_unknown():
    assert check_audit_log(_ctx({"gateway": {"port": 19001}})).status == UNKNOWN


def test_b10_logging_empty_dict_unknown():
    assert check_audit_log(_ctx({"logging": {}})).status == UNKNOWN


def test_b10_unexpected_redact_value_unknown():
    assert check_audit_log(_ctx({"logging": {"redactSensitive": "all"}})).status == UNKNOWN


# ---- NEVER PASS or FAIL ----

def test_b10_never_pass_or_fail():
    for cfg in (
        {},
        {"logging": {"redactSensitive": "off"}},
        {"logging": {"redactSensitive": "tools"}},
        {"logging": {"redactSensitive": "all"}},
        {"logging": {}},
        {"gateway": {"port": 19001}},
    ):
        result = check_audit_log(_ctx(cfg))
        assert result.status not in (PASS, FAIL), (
            f"B10 must never return PASS/FAIL; got {result.status!r} for {cfg}"
        )
