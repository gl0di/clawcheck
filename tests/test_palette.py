"""Screen 12 — full capability palette (F-045).

The load-bearing test is the drift guard: every cli._PRIMARY_MODES flag must be
represented in the palette (or explicitly exempt), so the palette and cli.py can't
silently diverge. Offline, deterministic, no writes.
"""
from __future__ import annotations

from pathlib import Path

from clawseccheck.cli import _PRIMARY_MODES
from clawseccheck.palette import (
    EXEMPT_FROM_PALETTE,
    _PALETTE,
    grounded_flags,
    render_palette,
)


# ── Drift guard (the point of the grounded registry) ─────────────────────────

class TestGrounding:
    def test_every_primary_mode_is_in_the_palette(self):
        grounded = grounded_flags()
        missing = [flag for _attr, flag, _kind in _PRIMARY_MODES
                   if flag not in EXEMPT_FROM_PALETTE and flag not in grounded]
        assert not missing, f"palette is missing capabilities from _PRIMARY_MODES: {missing}"

    def test_exemptions_are_real_modes(self):
        # An exemption that no longer names a real mode is dead weight — catch it.
        mode_flags = {flag for _a, flag, _k in _PRIMARY_MODES}
        stale = [f for f in EXEMPT_FROM_PALETTE if f not in mode_flags]
        assert not stale, f"EXEMPT_FROM_PALETTE names non-existent modes: {stale}"

    def test_grounded_flags_are_real_cli_flags(self):
        # Guard against a typo'd flag in the registry: every grounded flag must
        # actually appear in cli.py's source (where add_argument declares it).
        src = Path("clawseccheck/cli.py").read_text(encoding="utf-8")
        bogus = [f for f in grounded_flags() if f not in src]
        assert not bogus, f"palette grounds to flags not present in cli.py: {bogus}"


# ── Rendering ─────────────────────────────────────────────────────────────────

class TestRender:
    def test_all_category_titles_present(self):
        out = render_palette()
        for cat in _PALETTE:
            assert cat.title in out

    def test_readonly_and_live_tags_present(self):
        out = render_palette()
        assert "✅ read-only" in out
        assert "⚡" in out  # live-agent disclosure

    def test_modifiers_and_help_footer(self):
        out = render_palette()
        assert "Add to any:" in out
        assert '"private"' in out and "--no-history" in out
        assert 'say "help"' in out

    def test_check_count_substituted(self):
        assert "81 checks across your OpenClaw setup" in render_palette(n_checks=81)

    def test_check_count_falls_back_when_unknown(self):
        out = render_palette(n_checks=None)
        assert "all checks across your OpenClaw setup" in out
        assert "{n}" not in out  # placeholder never leaks

    def test_ascii_is_pure_ascii(self):
        out = render_palette(n_checks=81, ascii_only=True)
        assert out.isascii()
        assert "(live)" in out          # ⚡ folded, not dropped
        assert "🦞" not in out and "✅" not in out

    def test_every_entry_shows_its_flag_or_default(self):
        out = render_palette()
        for cat in _PALETTE:
            for e in cat.entries:
                token = "(default)" if (e.flag is None and not e.also) else e.flag
                assert token in out
