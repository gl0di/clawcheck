# ClawSecCheck vs NVIDIA SkillSpector — comparison & what we adopted

Grounding pass: 2026-06 against the real repo (github.com/nvidia/skillspector, v2.2.3,
Apache-2.0). This documents what SkillSpector does, and exactly what ClawSecCheck adopted
from it — and what it deliberately did **not**, and why (our project laws: stdlib-only,
zero-network, no-LLM, no fabricated facts).

## They solve a different half of the problem
- **SkillSpector** = *input validation* — "is this skill artifact safe to install?" It scans a
  third-party artifact (skill dir / git repo / zip / SKILL.md / scripts).
- **ClawSecCheck** = *configuration validation* — "is my own agent set up safely?" A posture
  audit of the user's OpenClaw install (config, bootstrap, MCP, installed skills, host).

The only real overlap is skill/MCP vetting (`--vet` / `--vet-mcp` / B13), where SkillSpector goes
deeper. 0.21.0 closes the biggest part of that gap.

## SkillSpector — grounded capabilities (v2.2.3)
- **64 patterns / 16 categories.** Methods: regex (`re`), **Python AST** (`ast`), **taint tracking**
  (`ast`), **YARA** (`yara-python`), **live CVE** (OSV.dev API), **optional LLM** semantic analysis
  (OpenAI / Anthropic / NVIDIA via LangChain/LangGraph).
- Offline mode (`--no-llm`); OSV.dev falls back to a static list when unreachable.
- Output: terminal / JSON / Markdown / SARIF. Targets Claude Code, Codex, Gemini, Cursor.
- Cites a paper (Liu et al., 2026: "Agent Skills in the Wild") with 42,447 skills, 26.1% vulnerable,
  5.2% malicious. **Not verifiable from the repo** — treat as their cited figure, not ours.

## What ClawSecCheck adopted (0.21.0 "Deeper Vetting")
All additions are **stdlib-only, offline, read-only** and obey the zero-false-positive-FAIL law.

| Adopted | Their analog | Our implementation |
|---|---|---|
| **Python AST analysis** of skill `.py` files | Behavioral AST (AST1–AST8) | `clawseccheck/skillast.py` — `ast.parse` only (never compile/exec). High-confidence crit: obfuscated `exec`/`eval` of decoded strings, `getattr(...)()` indirection, `__import__(...).system()`. Info-only sinks (subprocess/os.system/pickle.loads) escalate only alongside a cred/exfil signal. |
| **Injection directives inside a vetted skill** | Prompt Injection (P1–P8) | `_SKILL_INJECTION` in `checks.py` — agent-manipulation prose (ignore-instructions, exfiltrate-secrets, hide-from-user). HIGH; deliberately narrow so ordinary setup prose stays clean. |
| **Richer evidence surfacing** | per-finding evidence | `--vet` now prints the `file:line — reason` evidence list (was suppressed in plain text). |

## What we deliberately did NOT adopt (and why)
- **YARA rules** (YR1–YR4) — requires the `yara-python` C extension; violates *stdlib-only / zero
  runtime deps*. Our regex + AST cover the obfuscation/malware-indicator space without it.
- **Live OSV.dev CVE lookups** (SC4) — a network call; violates *local-only / zero-network*. (Our
  B33 uses a static, curated advisory table instead — same idea, no network.)
- **LLM semantic analysis** — requires a network call **and** ships the skill's contents to a third-
  party model; violates *zero-network* and *no-exfiltration*. Out of scope for a trust-first tool.
- **Taint/dataflow tracking** (TT1–TT5) — adoptable on stdlib `ast`, but FP-delicate (a legit skill
  reading `OPENAI_API_KEY` and POSTing to api.openai.com would false-positive). Deferred to 0.22.0
  with conservative gating (escalate existing cred/exfil signals only, never FAIL on its own).
- Non-Python AST (JS / shell / Go) — our AST layer is **Python-only**; those languages stay on the
  regex engine. Honest limitation, documented in the README.

## Net effect
`--vet` / B13 now catch the obfuscation class that pure regex misses — `exec(base64.b64decode(...))`,
`getattr(os, "sys"+"tem")(...)`, `__import__("os").system(...)` — while keeping zero false-positive
FAILs on real fleet configs (verified). Attribution: techniques inspired by NVIDIA SkillSpector
(Apache-2.0); no SkillSpector code was copied.
