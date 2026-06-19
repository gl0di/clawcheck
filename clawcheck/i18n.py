"""Internationalisation support for ClawCheck.

Pure stdlib — no external dependencies. English is the canonical source of
truth (strings are copied verbatim from report.py); translations are additive.
Missing translations always fall back to English; missing keys return the key
itself. Functions never raise.
"""
from __future__ import annotations

LANGS = ("en", "he")
DEFAULT_LANG = "en"
RTL_LANGS = frozenset({"he"})


def is_rtl(lang: str) -> bool:
    """Return True iff *lang* is a right-to-left language."""
    return lang in RTL_LANGS


# ---------------------------------------------------------------------------
# UI / report strings (keys map to both "en" and "he")
# ---------------------------------------------------------------------------
STRINGS: dict[str, dict[str, str]] = {
    "report.title": {
        "en": "ClawCheck - OpenClaw Security Audit",
        "he": "ClawCheck - ביקורת אבטחה של OpenClaw",
    },
    "report.score_line": {
        "en": "Score: {score}/100   Grade: {grade}   Lethal Trifecta: {trifecta}",
        "he": "ציון: {score}/100   דירוג: {grade}   Lethal Trifecta: {trifecta}",
    },
    "report.capped": {
        "en": "(capped from {raw} - open {sev} finding)",
        "he": "(מוגבל מ-{raw} - ממצא {sev} פתוח)",
    },
    "report.no_issues": {
        "en": "No issues found by ClawCheck. Keep it that way. {ok}",
        "he": "ClawCheck לא מצא בעיות. שמור על זה. {ok}",
    },
    "report.to_fix": {
        "en": "{n} thing(s) to fix (ClawCheck) - most urgent first:",
        "he": "{n} דבר(ים) לתיקון (ClawCheck) - הדחופים ביותר קודם:",
    },
    "report.label_why": {
        "en": "why",
        "he": "מדוע",
    },
    "report.label_fix": {
        "en": "fix",
        "he": "תיקון",
    },
    "report.suppressed_count": {
        "en": "({n} finding(s) suppressed via .clawcheckignore)",
        "he": "({n} ממצא(ים) מושתקים באמצעות .clawcheckignore)",
    },
    "report.gov_warning": {
        "en": "WARNING: a CRITICAL finding ({id}) is suppressed via .clawcheckignore",
        "he": "אזהרה: ממצא קריטי ({id}) מושתק באמצעות .clawcheckignore",
    },
    "report.native_header": {
        "en": "--- Also from OpenClaw's built-in `security audit` ---",
        "he": "--- גם מביקורת `security audit` המובנית של OpenClaw ---",
    },
    "report.native_additional": {
        "en": "{n} additional finding(s) the platform's own audit reports:",
        "he": "{n} ממצא(ים) נוסף(ים) שביקורת הפלטפורמה מדווחת עליהם:",
    },
    "report.native_clean": {
        "en": "Clean — openclaw security audit found nothing.",
        "he": "נקי — ביקורת האבטחה של openclaw לא מצאה דבר.",
    },
    "report.native_not_included": {
        "en": "(not included: {note})",
        "he": "(לא נכלל: {note})",
    },
    "card.security_label": {
        "en": "OpenClaw Security",
        "he": "אבטחת OpenClaw",
    },
    "card.trifecta_label": {
        "en": "Lethal Trifecta",
        "he": "Lethal Trifecta",
    },
    "card.audited_by": {
        "en": "audited by ClawCheck",
        "he": "נבדק על ידי ClawCheck",
    },
    "monitor.title": {
        "en": "ClawCheck - Threat Monitor",
        "he": "ClawCheck - מנטור איומים",
    },
    "monitor.current": {
        "en": "Current: {score}/100  Grade: {grade}",
        "he": "נוכחי: {score}/100  דירוג: {grade}",
    },
    "monitor.baseline": {
        "en": "Baseline saved. Future runs will alert on what changes since now.",
        "he": "קו הבסיס נשמר. הרצות עתידיות יתריעו על שינויים מרגע זה.",
    },
    "monitor.no_threats": {
        "en": "No new threats since last check. {ok}",
        "he": "אין איומים חדשים מאז הבדיקה האחרונה. {ok}",
    },
    "monitor.changes": {
        "en": "{n} change(s) detected since last check:",
        "he": "{n} שינוי(ים) זוהה(ו) מאז הבדיקה האחרונה:",
    },
    "prompts.title": {
        "en": "ClawCheck - copy-paste fix prompts",
        "he": "ClawCheck - הנחיות תיקון להעתקה-הדבקה",
    },
    "prompts.intro": {
        "en": "Paste each into your OpenClaw agent to fix it:",
        "he": "הדבק כל אחת לסוכן OpenClaw שלך לתיקון:",
    },
    "prompts.nothing": {
        "en": "Nothing to fix. {ok}",
        "he": "אין מה לתקן. {ok}",
    },
    "html.title": {
        "en": "ClawCheck Security Audit Report",
        "he": "דוח ביקורת אבטחה של ClawCheck",
    },
    "html.h1": {
        "en": "🔍 ClawCheck Security Audit Report",
        "he": "🔍 דוח ביקורת אבטחה של ClawCheck",
    },
    "html.label_score": {
        "en": "Score:",
        "he": "ציון:",
    },
    "html.label_trifecta": {
        "en": "Lethal Trifecta:",
        "he": "Lethal Trifecta:",
    },
    "html.label_capped": {
        "en": "Capped:",
        "he": "מוגבל:",
    },
    "html.capped_detail": {
        "en": "from {raw} (open {sev} finding)",
        "he": "מ-{raw} (ממצא {sev} פתוח)",
    },
    "html.private_title": {
        "en": "⚠ Private Report",
        "he": "⚠ דוח פרטי",
    },
    "html.private_body": {
        "en": "This report contains detailed security findings and must <strong>NOT</strong> be shared publicly.",
        "he": "דוח זה מכיל ממצאי אבטחה מפורטים ו<strong>אסור</strong> לשתפו פומבית.",
    },
    "html.section_findings": {
        "en": "Findings",
        "he": "ממצאים",
    },
    "html.label_why2": {
        "en": "Why:",
        "he": "מדוע:",
    },
    "html.label_fix2": {
        "en": "Fix:",
        "he": "תיקון:",
    },
    "html.no_issues": {
        "en": "No issues found. Keep it that way.",
        "he": "לא נמצאו בעיות. שמור על זה.",
    },
}


def t(key: str, lang: str = "en", **kw: object) -> str:
    """Look up a UI string by *key* for *lang*.

    Lookup order:
      1. STRINGS[key][lang]
      2. STRINGS[key]["en"]  (language fallback)
      3. *key* itself        (key fallback)

    Then format with **kw if provided. On any formatting error fall back to the
    English template formatted (and if that also fails, return the raw template).
    Never raises.
    """
    entry = STRINGS.get(key)
    if entry is None:
        return key

    template = entry.get(lang) or entry.get("en") or key

    if not kw:
        return template

    try:
        return template.format(**kw)
    except (KeyError, IndexError):
        # Try English template as fallback
        en_template = entry.get("en") or key
        try:
            return en_template.format(**kw)
        except (KeyError, IndexError):
            return template


# ---------------------------------------------------------------------------
# Check-title translations (indexed by check id, "he" key only)
# ---------------------------------------------------------------------------
TITLES: dict[str, dict[str, str]] = {
    "A1": {"he": "Lethal Trifecta (קלט לא מהימן × נתונים רגישים × יציאה החוצה)"},
    "B1": {"he": "סודות בקובץ תצורה / קבצי אתחול בטקסט גלוי"},
    "B2": {"he": "חשיפת ה-Gateway ואימות ערוצים"},
    "B3": {"he": "הרשאות מינימליות (כלים מוגברים / רשימות היתר)"},
    "B4": {"he": "ארגז חול להרצה"},
    "B5": {"he": "שלמות שרשרת אספקה של תוספים / מיומנויות"},
    "B6": {"he": "משטח הזרקה בקובצי האתחול (SOUL.md/AGENTS.md/TOOLS.md)"},
    "B7": {"he": "משטח הרעלת זיכרון (MEMORY.md / ספריית זיכרון)"},
    "B8": {"he": "אישור אנושי לפעולות הרסניות"},
    "B9": {"he": "דלף הנחיית מערכת / סוד בפלט כלי"},
    "B10": {"he": "יומן ביקורת ועמדה רגישה"},
    "B11": {"he": "TLS בתעבורה והגנה במנוחה"},
    "B12": {"he": "עדיפות למקומי והיגיינת מודל"},
    "B13": {"he": "בטיחות מיומנויות / תוספים מותקנים (הורד, לא עשוי בעצמך)"},
    "B14": {"he": "משטח יציאה (היכן הסוכן יכול לפנות החוצה)"},
    "B15": {"he": "גבולות אמון שרת MCP"},
    "B16": {"he": "ניטור איומים / זיהוי פעיל"},
    "B17": {"he": "אוטונומיה / פעולות פעימת לב"},
    "B18": {"he": "האצלה לסוכנות משנה"},
    "B19": {"he": "הגנת נתונים במנוחה (זיכרון/יומנים)"},
    "B20": {"he": "הגנת כתיבה על קבצי האתחול / הזיכרון"},
    "B21": {"he": "גבול אמון פלט-כלי / תוכן-מאוחזר"},
    "B22": {"he": "סיכון שינוי עצמי (קבצי זהות/מיומנות ניתנים לכתיבה + כלים פעילים)"},
    "B23": {"he": "הנחיות עקיפת אישור בקובצי האתחול"},
    "B24": {"he": "הקשחת שרת MCP"},
    "B25": {"he": "היגיינת עדכון / הצמדת גרסאות"},
    "C3": {"he": "גיבויים של SOUL.md / זיכרון"},
    "C4": {"he": "גרסת OpenClaw / היגיינת עדכון"},
    "C5": {"he": "בטיחות PATH של בינארי מקומי"},
}


def title_for(check_id: str, default: str, lang: str = "en") -> str:
    """Return the translated title for *check_id* in *lang*.

    For English (or any unknown language without a translation entry) the
    *default* (the English title from CATALOG) is returned verbatim.
    """
    if lang == "en":
        return default
    return TITLES.get(check_id, {}).get(lang, default)


# ---------------------------------------------------------------------------
# Gettext-style phrase map for common static fix/detail strings
# ---------------------------------------------------------------------------
PHRASES: dict[str, dict[str, str]] = {
    "Keep redaction on.": {
        "he": "השאר את הסינון פעיל.",
    },
    "Keep sandbox.mode enabled.": {
        "he": "השאר את sandbox.mode מופעל.",
    },
    "Keep auth on and channels on allowlist.": {
        "he": "השאר את האימות פעיל והערוצים ברשימת ההיתר.",
    },
    "Keep least privilege: explicit allowlists only.": {
        "he": "שמור על הרשאות מינימליות: רשימות היתר מפורשות בלבד.",
    },
    "Keep audit + redaction on.": {
        "he": "השאר את הביקורת והסינון פעילים.",
    },
    "Keep data local where possible.": {
        "he": "שמור נתונים מקומיים ככל האפשר.",
    },
    "Keep it enabled and make sure its alerts actually reach you.": {
        "he": "השאר פעיל וודא שהתראותיו אכן מגיעות אליך.",
    },
    "Keep bootstrap files free of language that weakens human approval gates.": {
        "he": "שמור קבצי אתחול נקיים משפה המחלישה שערי אישור אנושי.",
    },
    "Keep all entries pinned and review updates manually.": {
        "he": "השאר את כל הרשומות מוצמדות ובדוק עדכונים ידנית.",
    },
    "Keep a trusted/untrusted separation rule in SOUL.md.": {
        "he": "שמור כלל הפרדה בין מהימן/לא-מהימן ב-SOUL.md.",
    },
    "Keep approval gating on all high-impact tools.": {
        "he": "השאר שערי אישור על כל הכלים בעלי השפעה גבוהה.",
    },
    "Keep transport encrypted and credential files locked down.": {
        "he": "השאר את התעבורה מוצפנת וקבצי האישורים נעולים.",
    },
}


def tp(text: str, lang: str = "en") -> str:
    """Gettext-style phrase lookup for static detail/fix strings.

    If *lang* is ``"en"`` or *text* is empty, return *text* unchanged.
    Otherwise look up *text* in PHRASES and return the translation for *lang*,
    falling back to *text* itself if no entry exists.
    """
    if lang == "en" or not text:
        return text
    return PHRASES.get(text, {}).get(lang, text)
