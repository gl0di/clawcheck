"""clean_taint_argv_listform: caller input -> fixed-program argv list (shell=False).

The smyx-payment pattern: the tainted value is an isolated argv element passed to a
hardcoded interpreter/module, shell=False. Not command injection — vet must PASS.
"""

import subprocess
import sys


def query_after_payment(phone):
    """phone is caller-supplied; passed as one argv element to a fixed module."""
    return subprocess.run(
        [sys.executable, "-m", "scripts.query", phone],
        capture_output=True,
        text=True,
    )
