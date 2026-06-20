# Host-monitor detection signals (grounding for `hostwatch.py` / B50–B54)

ClawSecCheck's **Host Watch Posture** ring (checks B50–B54 + RISK-10) answers one
question read-only: *is anyone watching the machine this agent runs on?* This file
records the **grounded** detection signals so no path here is fabricated
(CLAUDE.md golden rule #4). Every signal is filesystem-only — **no subprocess, no
network**: a well-known config path, a binary name on `PATH` (`shutil.which` reads
`PATH`, it never executes), a systemd enable-symlink, a read-only config/plist
file, or a read-only Windows registry key.

**Confidence policy:** only **HIGH**-confidence signals (authoritative docs / man
pages / universally-stable standard paths) are used as positive detections in
`hostwatch.py`. **LOW**/unverified signals are intentionally *omitted* — an honest
`unknown` beats a wrong `present`/`absent`. The "could not verify" list at the
bottom is excluded from the detector by design.

> **active-signal** = a read-only indicator that a monitor is *enabled*, not merely
> installed. The systemd mechanism is generic: `systemctl enable <unit>` creates a
> symlink `/etc/systemd/system/<target>.wants/<unit>` → the unit file; its presence
> means enabled-at-boot. Source: freedesktop `systemd.unit(5)`.
> Caveat: enabled ≠ currently running, and a unit can run without an enable symlink,
> so *absence of the symlink is not proof of disabled* — we treat it as "installed,
> can't confirm enabled" (`active=None`/`False`), never as a FAIL.

## B50 — Network monitoring / IDS
| Signal | OS | Active? | Conf |
|---|---|---|---|
| `/etc/suricata/suricata.yaml`; bin `suricata`; unit `suricata.service` (+wants-symlink) | linux | yes (symlink) | HIGH |
| Zeek prefix `/opt/zeek/bin/zeek` or `/usr/local/zeek/bin/zeek`; bins `zeek`/`zeekctl` (not on default PATH) | linux | — | HIGH |
| Snort 3 `/etc/snort/snort.lua` or `/usr/local/etc/snort/snort.lua`; bin `snort` | linux | — | HIGH |
| Little Snitch `/Applications/Little Snitch.app`; LuLu `/Applications/LuLu.app` (required locations) | macos | — | HIGH |
| Sysmon service `Sysmon64`/`Sysmon`, driver key `SysmonDrv`; `C:\Windows\Sysmon64.exe` | windows | service-exists | HIGH (svc/key) / LOW (exe path) |

## B51 — Host audit / syscall logging
| Signal | OS | Active? | Conf |
|---|---|---|---|
| `/etc/audit/auditd.conf`, `/etc/audit/audit.rules`, `/etc/audit/rules.d/`; bin `auditctl`; unit `auditd.service` (+symlink) | linux | yes (symlink) | HIGH |
| OpenBSM `/etc/security/audit_control` (the real file, not `.example`) — **disabled by default since macOS 14** | macos | yes (file exists) | HIGH |
| Sysmon (see B50) doubles as the host event auditor | windows | service-exists | HIGH |

## B52 — File-integrity monitoring
| Signal | OS | Active? | Conf |
|---|---|---|---|
| AIDE: Debian `/etc/aide/aide.conf`, RHEL `/etc/aide.conf`; bin `aide`; DB `/var/lib/aide/aide.db[.gz]` ⇒ baseline initialised | linux | DB exists | HIGH |
| Tripwire `/etc/tripwire/tw.cfg` + `twcfg.txt`; bin `tripwire` | linux | — | HIGH |
| osquery `/etc/osquery/osquery.conf` (+ homebrew `/opt/homebrew/etc`, `/usr/local/etc`); bin `osqueryd` | linux/macos | — | HIGH |

## B53 — Endpoint protection / EDR / AV
| Signal | OS | Active? | Conf |
|---|---|---|---|
| Wazuh `/var/ossec/bin/wazuh-control`; OSSEC `/var/ossec/bin/ossec-control` or `/var/ossec/etc/ossec.conf` | linux | — | HIGH |
| CrowdStrike `/opt/CrowdStrike/falconctl`; bin `falconctl`; win service `CSFalconService` | linux/win | service-exists | HIGH |
| SentinelOne `/opt/sentinelone/bin/sentinelctl` | linux | — | HIGH |
| MS Defender for Endpoint `/opt/microsoft/mdatp`; bin `mdatp` | linux | — | HIGH |
| ClamAV `/etc/clamav/clamd.conf`; bins `clamscan`/`clamd` | linux | — | HIGH |
| macOS apps: `/Applications/Falcon.app`, `/Applications/Microsoft Defender.app`, Santa `/Applications/Santa.app` + `/var/db/santa` | macos | — | HIGH |
| Windows: `WinDefend` service / `ProgramData\Microsoft\Windows Defender`; `Program Files\CrowdStrike` | windows | service-exists | HIGH |

## B54 — Host firewall
| Signal | OS | Active? | Conf |
|---|---|---|---|
| ufw `/etc/ufw/ufw.conf` → **`ENABLED=yes`**; bin `ufw` | linux | yes (key) | HIGH |
| firewalld `/etc/firewalld/firewalld.conf`; bin `firewall-cmd`; unit `firewalld.service` (+symlink) | linux | yes (symlink) | HIGH |
| nftables `/etc/nftables.conf` — **presence ≠ enabled**; unit `nftables.service` (+symlink) is the real active signal | linux | yes (symlink) | HIGH |
| macOS ALF `/Library/Preferences/com.apple.alf.plist` key `globalstate` (0=off,1=on,2=block-all) — **gone on Sequoia 15+** ⇒ UNKNOWN when absent | macos | yes (key) | HIGH |
| Windows `EnableFirewall` REG_DWORD per profile under `…\SharedAccess\Parameters\FirewallPolicy\{Domain,Standard,Public}Profile` | windows | yes (DWORD) | HIGH |

## Deliberately treated as UNKNOWN (LOW / unverifiable — NOT used as positives)
- Snort 2 legacy `/etc/snort/snort.conf`; exact Snort binary path.
- Zeek systemd unit name (no canonical unit; zeekctl-managed).
- Sysmon binary install dir (varies with how `-i` was run — service/driver key used instead).
- LuLu config dir; ClamAV unit names; SentinelOne Windows service name; Santa config-plist path.
- iptables persistence (no universal file; `iptables-persistent`/`/etc/sysconfig/iptables` are optional add-ons).
- macOS pf state (`/etc/pf.conf` ships by default; presence ≠ enabled; live state needs `pfctl`).
- Windows advanced audit policy / Defender live (non-policy) real-time-protection state (tamper-protected).

## Structural caveats baked into the detector
- `/etc/nftables.conf` (linux) and `/etc/pf.conf` (macOS) **exist-but-disabled**: presence is not enablement.
- macOS ALF plist is **absent on Sequoia 15+**; OpenBSM is **disabled by default since macOS 14** — absence there is expected, reported as UNKNOWN/absent, never as "monitoring stripped".

_Sources (anchors): docs.suricata.io · docs.snort.org · docs.zeek.org · Red Hat
auditd & AIDE guides · osquery FIM docs · documentation.wazuh.com ·
learn.microsoft.com (Defender Linux/macOS, Sysmon) · docs.clamav.net ·
help.obdev.at / objective-see.org · freedesktop `systemd.unit(5)` · NSA Windows
Firewall audit baseline. Full URLs captured during the 2026-06 grounding pass._
