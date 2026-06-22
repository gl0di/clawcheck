"""CI guard: no FAIL/WARN finding leaks an untranslated English detail into the
Hebrew report.

This permanently closes the recurring "forgot the he DETAIL_RULES for a new
check" gap (it has recurred at C5 -> B45 -> B47, and was found again here for
B9/B26/B30/B32/B38/B39/B41). The report renders a finding's detail through
``tp(detail, "he")`` (report.py); if a check ships prose with no matching entry
in ``i18n.DETAIL_RULES`` / ``PHRASES``, ``tp`` falls back to the English input
and the Hebrew report shows an English line.

For every FAIL/WARN finding produced across all fixture homes, the Hebrew
rendering of its detail must contain at least one Hebrew character whenever the
English detail carries prose. This is the whole-detail unit the user actually
sees on one report line; it is deterministic and has no false-positive risk from
Latin config identifiers (a translated line still contains Hebrew).

Offline, read-only, stdlib only.
"""
from __future__ import annotations

import re
from pathlib import Path

from clawseccheck import audit
from clawseccheck.i18n import tp

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"

# Hebrew block (U+0590–U+05FF) and a "has real English prose" signal.
_HEBREW = re.compile(r"[֐-׿]")
_PROSE = re.compile(r"[A-Za-z]{4,}")


def _fixture_homes() -> list[Path]:
    """Every fixture OpenClaw home: anything with an openclaw.json plus the
    conventional home_/bad_/clean_ top-level dirs."""
    homes: set[Path] = set()
    for cfg in FIXTURES.rglob("openclaw.json"):
        homes.add(cfg.parent)
    for d in FIXTURES.iterdir():
        if d.is_dir() and d.name.startswith(("home_", "bad_", "clean_")):
            homes.add(d)
    return sorted(homes)


def _prose_findings():
    """Yield (home, finding) for every FAIL/WARN finding whose detail is prose."""
    for home in _fixture_homes():
        try:
            _, findings, _ = audit(home, include_native=False)
        except Exception:  # noqa: BLE001 — a broken fixture is a separate concern
            continue
        for f in findings:
            if f.status not in ("FAIL", "WARN"):
                continue
            detail = (f.detail or "").strip()
            if detail and _PROSE.search(detail):
                yield home, f


def test_fixture_homes_discovered():
    """Guard against a vacuously-green suite if fixture discovery breaks."""
    assert _fixture_homes(), "no fixture homes found"


def test_some_findings_exercised():
    """The guard is only meaningful if fixtures actually fire prose findings."""
    assert any(True for _ in _prose_findings()), "no FAIL/WARN prose findings fired"


def test_every_failwarn_detail_is_localized_he():
    """No FAIL/WARN detail may render fully in English in the Hebrew report.

    If this fails, a check ships evidence prose with no matching he entry in
    i18n.DETAIL_RULES (or PHRASES). Add the Hebrew rule in the SAME change as the
    check (CLAUDE.md evidence-i18n rule).
    """
    leaks: dict[str, str] = {}
    for _home, f in _prose_findings():
        if not _HEBREW.search(tp(f.detail.strip(), "he")):
            leaks.setdefault(f.id, f.detail.strip())

    assert not leaks, (
        "FAIL/WARN findings whose detail is NOT localized to Hebrew "
        "(missing he DETAIL_RULES / PHRASES entry — add it in the same change):\n"
        + "\n".join(f"  {cid}: {txt[:100]}" for cid, txt in sorted(leaks.items()))
    )


def test_en_detail_is_byte_identical():
    """tp(detail, 'en') is always a no-op — the English path must never mutate."""
    for _home, f in _prose_findings():
        assert tp(f.detail, "en") == f.detail
