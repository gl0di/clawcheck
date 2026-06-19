"""Baseline suppression via .clawcheckignore."""
from clawcheck import audit
from clawcheck.baseline import apply, fingerprint, load_ignore
from clawcheck.catalog import CRITICAL, FAIL, HIGH, PASS, WARN, Finding
from clawcheck.report import render_report
from clawcheck.scoring import compute


def _f(cid, severity, status, detail="d"):
    return Finding(cid, "t", severity, status, detail, "fix", "fw")


def test_fingerprint_stable_and_detail_sensitive():
    assert fingerprint(_f("B14", WARN, WARN, "same")) == fingerprint(_f("B14", WARN, WARN, "same"))
    assert fingerprint(_f("B14", WARN, WARN, "a")) != fingerprint(_f("B14", WARN, WARN, "b"))
    assert fingerprint(_f("B14", WARN, WARN)).startswith("B14:")


def test_load_ignore_parsing(tmp_path):
    (tmp_path / ".clawcheckignore").write_text("# comment\n\nB14\nB2:ab12cd34\n  B7  \n")
    assert load_ignore(tmp_path) == {"B14", "B2:ab12cd34", "B7"}
    assert load_ignore(tmp_path / "nope") == set()


def test_apply_by_id_and_by_fingerprint():
    a, b = _f("B14", "MEDIUM", WARN), _f("B2", CRITICAL, FAIL, "x")
    apply([a, b], {"B14"})
    assert a.suppressed and not b.suppressed
    c = _f("B9", "MEDIUM", WARN, "y")
    apply([c], {fingerprint(c)})
    assert c.suppressed


def test_suppressed_critical_does_not_cap_score():
    keep = _f("B3", HIGH, PASS)
    supp = _f("B2", CRITICAL, FAIL, "x")
    supp.suppressed = True
    r = compute([keep, supp])
    assert r.score == 100 and r.capped is False


def test_suppressed_excluded_from_report():
    supp = _f("B2", CRITICAL, FAIL, "x")
    supp.suppressed = True
    out = render_report([supp], compute([supp]))
    assert "No issues found" in out
    assert "1 finding(s) suppressed via .clawcheckignore" in out


def test_audit_applies_clawcheckignore(tmp_path):
    (tmp_path / "openclaw.json").write_text("{}")
    _, findings, _ = audit(tmp_path)
    target = next(f for f in findings if f.status == WARN)
    (tmp_path / ".clawcheckignore").write_text(target.id + "\n")
    _, findings2, _ = audit(tmp_path)
    assert next(f for f in findings2 if f.id == target.id).suppressed
