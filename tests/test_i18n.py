"""Tests for clawcheck/i18n.py — pure stdlib i18n module."""
from __future__ import annotations

from clawcheck.catalog import CATALOG
from clawcheck.i18n import LANGS, RTL_LANGS, STRINGS, TITLES, PHRASES
from clawcheck.i18n import is_rtl, t, title_for, tp


# ---------------------------------------------------------------------------
# is_rtl
# ---------------------------------------------------------------------------
class TestIsRtl:
    def test_he_is_rtl(self):
        assert is_rtl("he") is True

    def test_en_is_not_rtl(self):
        assert is_rtl("en") is False

    def test_unknown_lang_is_not_rtl(self):
        assert is_rtl("fr") is False
        assert is_rtl("") is False

    def test_rtl_langs_frozenset(self):
        assert isinstance(RTL_LANGS, frozenset)
        assert "he" in RTL_LANGS
        assert "en" not in RTL_LANGS


# ---------------------------------------------------------------------------
# t() — basic lookup
# ---------------------------------------------------------------------------
class TestTLookup:
    def test_en_returns_en_value(self):
        result = t("report.title", lang="en")
        assert result == "ClawCheck - OpenClaw Security Audit"

    def test_he_returns_nonempty_string(self):
        result = t("report.title", lang="he")
        assert result
        assert isinstance(result, str)

    def test_he_differs_from_en(self):
        en_val = t("report.title", lang="en")
        he_val = t("report.title", lang="he")
        assert he_val != en_val

    def test_several_keys_have_he(self):
        keys = [
            "report.score_line",
            "report.no_issues",
            "report.to_fix",
            "monitor.title",
            "html.title",
        ]
        for key in keys:
            he_val = t(key, lang="he")
            en_val = t(key, lang="en")
            assert he_val, f"Empty Hebrew for {key}"
            assert he_val != en_val, f"Hebrew same as English for {key}"

    def test_unknown_key_returns_key(self):
        assert t("no.such.key") == "no.such.key"
        assert t("no.such.key", lang="he") == "no.such.key"

    def test_unknown_lang_falls_back_to_en(self):
        # An unknown language should fall back to English value
        result = t("report.title", lang="zz")
        assert result == "ClawCheck - OpenClaw Security Audit"

    def test_default_lang_is_en(self):
        assert t("report.title") == t("report.title", lang="en")


# ---------------------------------------------------------------------------
# t() — placeholder formatting
# ---------------------------------------------------------------------------
class TestTFormatting:
    def test_en_formats_placeholders(self):
        result = t("report.score_line", lang="en", score=85, grade="B", trifecta="2/3")
        assert "85" in result
        assert "B" in result
        assert "2/3" in result

    def test_he_formats_placeholders(self):
        result = t("report.score_line", lang="he", score=85, grade="B", trifecta="2/3")
        assert "85" in result
        assert "B" in result
        assert "2/3" in result

    def test_missing_placeholder_does_not_raise(self):
        # Passing no kwargs for a template that has {score} etc. — must not raise
        result = t("report.score_line", lang="en")
        assert isinstance(result, str)

    def test_extra_placeholder_does_not_raise(self):
        # Extra kwargs are ignored by str.format — must not raise
        result = t("report.title", lang="en", extra="ignored")
        assert result == "ClawCheck - OpenClaw Security Audit"

    def test_partial_placeholder_does_not_raise(self):
        # Only some placeholders provided — must not raise, returns something
        result = t("report.score_line", lang="he", score=90)
        assert isinstance(result, str)

    def test_capped_formatting(self):
        result = t("report.capped", lang="en", raw=95, sev="CRITICAL")
        assert "(capped from 95 - open CRITICAL finding)" == result

    def test_monitor_current_he(self):
        result = t("monitor.current", lang="he", score=70, grade="C")
        assert "70" in result
        assert "C" in result


# ---------------------------------------------------------------------------
# STRINGS completeness
# ---------------------------------------------------------------------------
class TestStringsCompleteness:
    def test_all_keys_have_en_and_he(self):
        for key, translations in STRINGS.items():
            assert "en" in translations, f"Missing 'en' for key {key!r}"
            assert "he" in translations, f"Missing 'he' for key {key!r}"

    def test_en_strings_match_report_literals(self):
        """Spot-check a few en strings are byte-identical to report.py literals."""
        assert STRINGS["report.title"]["en"] == "ClawCheck - OpenClaw Security Audit"
        assert STRINGS["report.label_why"]["en"] == "why"
        assert STRINGS["report.label_fix"]["en"] == "fix"
        assert STRINGS["report.native_clean"]["en"] == "Clean — openclaw security audit found nothing."
        assert STRINGS["html.no_issues"]["en"] == "No issues found. Keep it that way."
        assert STRINGS["html.h1"]["en"] == "🔍 ClawCheck Security Audit Report"
        assert STRINGS["html.title"]["en"] == "ClawCheck Security Audit Report"
        assert STRINGS["html.label_score"]["en"] == "Score:"
        assert STRINGS["html.label_trifecta"]["en"] == "Lethal Trifecta:"
        assert STRINGS["html.label_capped"]["en"] == "Capped:"
        assert STRINGS["html.private_title"]["en"] == "⚠ Private Report"
        assert STRINGS["html.section_findings"]["en"] == "Findings"
        assert STRINGS["html.label_why2"]["en"] == "Why:"
        assert STRINGS["html.label_fix2"]["en"] == "Fix:"
        assert STRINGS["report.native_header"]["en"] == "--- Also from OpenClaw's built-in `security audit` ---"
        assert STRINGS["card.security_label"]["en"] == "OpenClaw Security"
        assert STRINGS["card.trifecta_label"]["en"] == "Lethal Trifecta"
        assert STRINGS["card.audited_by"]["en"] == "audited by ClawCheck"
        assert STRINGS["monitor.title"]["en"] == "ClawCheck - Threat Monitor"
        assert STRINGS["monitor.baseline"]["en"] == "Baseline saved. Future runs will alert on what changes since now."
        assert STRINGS["prompts.title"]["en"] == "ClawCheck - copy-paste fix prompts"
        assert STRINGS["prompts.intro"]["en"] == "Paste each into your OpenClaw agent to fix it:"


# ---------------------------------------------------------------------------
# title_for
# ---------------------------------------------------------------------------
class TestTitleFor:
    def test_en_returns_default(self):
        default = "Lethal Trifecta (untrusted input × sensitive data × outbound)"
        assert title_for("A1", default, lang="en") == default

    def test_he_known_id_returns_hebrew(self):
        default = "Lethal Trifecta (untrusted input × sensitive data × outbound)"
        result = title_for("A1", default, lang="he")
        assert result != default
        assert result  # non-empty

    def test_he_unknown_id_returns_default(self):
        default = "Some unknown check title"
        assert title_for("Z99", default, lang="he") == default

    def test_unknown_lang_returns_default(self):
        default = "Execution sandbox"
        assert title_for("B4", default, lang="fr") == default

    def test_b4_he_translation_present(self):
        default = "Execution sandbox"
        result = title_for("B4", default, lang="he")
        assert result != default

    def test_all_catalog_ids_have_he_title(self):
        """Every check id in CATALOG must have a 'he' entry in TITLES."""
        for meta in CATALOG:
            assert meta.id in TITLES, f"TITLES missing entry for {meta.id!r}"
            assert "he" in TITLES[meta.id], f"TITLES[{meta.id!r}] missing 'he' key"
            assert TITLES[meta.id]["he"], f"TITLES[{meta.id!r}]['he'] is empty"


# ---------------------------------------------------------------------------
# tp() — gettext-style phrase lookup
# ---------------------------------------------------------------------------
class TestTp:
    def test_en_returns_input_unchanged(self):
        text = "Keep redaction on."
        assert tp(text, lang="en") == text

    def test_empty_string_returns_unchanged(self):
        assert tp("", lang="he") == ""

    def test_unknown_text_returns_input(self):
        text = "Some text with no translation entry."
        assert tp(text, lang="he") == text

    def test_known_phrase_returns_hebrew(self):
        text = "Keep redaction on."
        result = tp(text, lang="he")
        assert result != text
        assert result  # non-empty

    def test_known_phrase_en_passthrough(self):
        # Even a phrase in PHRASES returns unchanged for lang="en"
        text = "Keep sandbox.mode enabled."
        assert tp(text, lang="en") == text

    def test_phrases_keys_are_exact_strings(self):
        """All PHRASES keys must be non-empty strings."""
        for k, v in PHRASES.items():
            assert isinstance(k, str) and k, f"Empty key in PHRASES: {k!r}"
            assert "he" in v, f"PHRASES[{k!r}] missing 'he'"
            assert v["he"], f"PHRASES[{k!r}]['he'] is empty"

    def test_audit_redaction_phrase(self):
        text = "Keep audit + redaction on."
        result = tp(text, lang="he")
        assert result != text

    def test_unknown_lang_returns_input(self):
        # tp only knows about PHRASES keys; an unknown lang has no entry
        text = "Keep redaction on."
        result = tp(text, lang="fr")
        assert result == text


# ---------------------------------------------------------------------------
# LANGS / DEFAULT_LANG constants
# ---------------------------------------------------------------------------
class TestConstants:
    def test_langs_contains_en_and_he(self):
        assert "en" in LANGS
        assert "he" in LANGS

    def test_default_lang_is_en(self):
        from clawcheck.i18n import DEFAULT_LANG
        assert DEFAULT_LANG == "en"
