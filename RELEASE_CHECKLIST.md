# Release Checklist

Pre-tag/publish checklist for ClawSecCheck stable releases.

## Version consistency

- [ ] `clawseccheck/__init__.py` `__version__` matches the intended tag.
- [ ] `SKILL.md` frontmatter `version:` matches `__version__`.
- [ ] `CHANGELOG.md` has an entry for this version.
- [ ] `README.md` status/version block reflects the release.

## Test suite

- [ ] `python3 -m pytest -q` — all tests pass, zero failures.
- [ ] `/home/glodi/pulse/.venv/bin/ruff check .` (or `ruff check .`) — clean.
- [ ] `python3 -m compileall clawseccheck/` — no syntax errors.

## CLI smoke tests

- [ ] `python3 audit.py --json --no-native` — exits 0, valid JSON.
- [ ] `python3 audit.py --verify-self` — exits 0, prints hash.
- [ ] `python3 audit.py --vet .` — exits 0.
- [ ] `python3 audit.py --prompts --no-native` — exits 0.

## Documentation honesty

- [ ] No "zero false positives" claim anywhere in README or docs.
- [ ] No "proves your agent is safe" or "checks everything" claim.
- [ ] README has a "Limitations" section stating heuristic nature and manual-review requirement.
- [ ] SECURITY.md present and asks reporters not to paste secrets.
- [ ] Release notes explicitly say "heuristic audit, not proof of safety".

## Security gates

- [ ] No `shell=True` reachable from untrusted config or skill content.
- [ ] No network calls by default (grep for `requests`, `urllib`, `socket`, `httpx`).
- [ ] No writes to disk by default; writes only under explicit CLI flags.
- [ ] Secret values redacted in all output channels.
- [ ] `UNKNOWN` states never mapped to `PASS`.
- [ ] Suppressed CRITICAL findings remain visible in suppressions section.

## Publish pipeline

- [ ] CI green on supported Python versions (3.9, 3.12) before tagging.
- [ ] Publish workflow uses a pinned `clawhub` version (not `@latest`).
- [ ] Stable publish requires manual approval / environment protection gate.
- [ ] `CLAWHUB_TOKEN` has minimum required scope; not echoed in logs.
- [ ] Tag format: `vX.Y.Z`.
