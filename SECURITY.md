# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| latest  | yes       |
| older   | best-effort patch on request |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities — use one of
the private channels below so the issue can be assessed and patched before public
disclosure.

**Preferred:** [GitHub Security Advisories](https://github.com/gl0di/clawseccheck/security/advisories/new)
(private, coordinated disclosure).

**Alternative:** email the maintainer via the address listed on the GitHub profile.

### What to include

- ClawSecCheck version (`clawseccheck --version`).
- Python version and OS.
- A clear description of the vulnerability and its impact.
- Steps to reproduce or a minimal proof-of-concept.

### What NOT to include

**Do not paste real secrets, API keys, tokens, passwords, or other credentials** in
issue reports, advisory drafts, or email. Redact all sensitive values before sharing.
If reproduction requires a config file, replace secret values with placeholders such
as `<REDACTED>` or `sk-XXXX`.

## Scope

ClawSecCheck is a **local, read-only** audit tool. It reads only the files it is
pointed at (OpenClaw config, bootstrap markdown, installed-skill text) and writes
nothing by default. It makes no network calls. Findings stay on your machine.

In-scope issues include:
- Logic bugs that produce false PASS results for genuinely unsafe configs.
- Output channels that could be exploited for prompt injection (e.g. `--prompts`).
- Any code path that reads, writes, or executes more than the documented scope.
- Dependency or supply-chain issues in the publish workflow.

Out of scope:
- Vulnerabilities in OpenClaw itself (report those to the OpenClaw project).
- Issues only reproducible by a malicious local user who already has filesystem access.

## Response timeline

We aim to acknowledge reports within 5 business days and to release a patch within 30
days for confirmed issues. Complex issues may take longer; we will communicate delays.
