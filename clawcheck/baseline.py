"""Baseline suppression via .clawcheckignore.

Entries are either a bare check id (e.g. ``B14``) or a full fingerprint
(e.g. ``B14:ab12cd34``).  Suppressed findings are excluded from the score,
the report, and the monitor snapshot.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def fingerprint(finding) -> str:
    """Stable identifier: ``<id>:<sha1-8>`` of the finding detail string."""
    digest = hashlib.sha1(
        finding.detail.encode("utf-8", "replace")
    ).hexdigest()[:8]
    return f"{finding.id}:{digest}"


def load_ignore(home: Path | str) -> set[str]:
    """Read ``<home>/.clawcheckignore`` and return the set of entries.

    Each non-blank, non-comment line is one entry (bare id or fingerprint).
    Returns an empty set when the file is absent.
    """
    p = Path(home).expanduser() / ".clawcheckignore"
    if not p.is_file():
        return set()
    entries: set[str] = set()
    try:
        for raw in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if line and not line.startswith("#"):
                entries.add(line)
    except OSError:
        pass
    return entries


def apply(findings, ignore: set[str]) -> None:
    """Set ``finding.suppressed = True`` for every finding matched by *ignore*.

    A finding is matched when its bare id *or* its full fingerprint is in the
    ignore set.  Modifies findings in-place; returns nothing.
    """
    if not ignore:
        return
    for f in findings:
        if f.id in ignore or fingerprint(f) in ignore:
            f.suppressed = True
