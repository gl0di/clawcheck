"""RISK-10 — powerful agent on a host with no detection monitoring.

Fires only on POSITIVE evidence that all four visibility classes (network IDS /
audit / FIM / EDR) are ABSENT, AND the agent is high-privilege (exec/write +
reachable by untrusted input). An 'unknown' probe or any present monitor yields
no chain (zero-false-positive doctrine). Firewall is irrelevant (prevention,
not detection).
"""
from __future__ import annotations

from pathlib import Path

from clawseccheck.collector import Context
from clawseccheck.risk import risk_paths

_VIS = ("network_ids", "host_audit", "file_integrity", "edr_av")

_POWERFUL = {"tools": {"exec": {"mode": "auto"}},
             "channels": {"telegram": {"dmPolicy": "open"}}}
_WEAK = {"tools": {}}


def _host(supported=True, **overrides):
    classes = {}
    for c in (*_VIS, "firewall"):
        classes[c] = overrides.get(c, {"status": "absent", "found": [], "active": None})
    return {"system": "Linux", "supported": supported, "classes": classes}


def _ctx(cfg, host):
    c = Context(home=Path("/nonexistent"))
    c.config = cfg
    c.host = host
    return c


def _ids(ctx):
    return {p.id for p in risk_paths(ctx, [])}


def test_risk10_fires_powerful_agent_blind_host():
    assert "RISK-10" in _ids(_ctx(_POWERFUL, _host()))


def test_risk10_silent_for_weak_agent():
    assert "RISK-10" not in _ids(_ctx(_WEAK, _host()))


def test_risk10_silent_when_one_visibility_monitor_present():
    host = _host(edr_av={"status": "present", "found": ["Wazuh"], "active": None})
    assert "RISK-10" not in _ids(_ctx(_POWERFUL, host))


def test_risk10_silent_when_a_visibility_class_is_unknown():
    # an inconclusive probe is NOT positive evidence of absence -> no chain
    host = _host(host_audit={"status": "unknown", "found": [], "active": None})
    assert "RISK-10" not in _ids(_ctx(_POWERFUL, host))


def test_risk10_silent_when_host_not_scanned():
    assert "RISK-10" not in _ids(_ctx(_POWERFUL, None))


def test_risk10_silent_on_unsupported_host():
    assert "RISK-10" not in _ids(_ctx(_POWERFUL, _host(supported=False)))


def test_risk10_ignores_firewall_only_presence():
    # a firewall present but all detection classes absent still fires (firewall is
    # prevention, not detection)
    host = _host(firewall={"status": "present", "found": ["ufw"], "active": True})
    assert "RISK-10" in _ids(_ctx(_POWERFUL, host))


def test_risk10_severity_is_medium():
    paths = risk_paths(_ctx(_POWERFUL, _host()), [])
    r10 = next(p for p in paths if p.id == "RISK-10")
    assert r10.severity == "MEDIUM"
