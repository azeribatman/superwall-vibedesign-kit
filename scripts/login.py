#!/usr/bin/env python3
"""Authenticate with Superwall. Two methods:

1. Console snippet (recommended):
   - Open superwall.com in Chrome, open DevTools Console
   - Paste the snippet we print, it copies 2 tokens to clipboard
   - Paste them here

2. Full cURL paste (fallback):
   - DevTools Network → any /api/trpc/ request → Copy as cURL → paste here

Usage:
    python3 scripts/login.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRETS = ROOT / ".secrets"

CONSOLE_SNIPPET = """copy(`accounts_superwall_token=${document.cookie.match(/accounts_superwall_token=([^;]+)/)[1]}\\npaywall_sAntiCsrfToken=${document.cookie.match(/paywall_sAntiCsrfToken=([^;]+)/)[1]}`)"""


def parse_token_paste(text: str) -> tuple[str, str] | None:
    """Parse the 2-line token paste from the console snippet."""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    token = None
    csrf = None
    for line in lines:
        if line.startswith("accounts_superwall_token="):
            token = line.split("=", 1)[1]
        elif line.startswith("paywall_sAntiCsrfToken="):
            csrf = line.split("=", 1)[1]
    if token and csrf:
        return token, csrf
    return None


def parse_curl(text: str) -> tuple[str, str] | None:
    """Extract the 2 tokens from a full cURL paste."""
    # Find cookie string
    m = re.search(r"(?:-b|--cookie)\s+['\"]([^'\"]+)['\"]", text)
    if not m:
        m = re.search(r"-H\s+['\"]cookie:\s*([^'\"]+)['\"]", text, re.IGNORECASE)
    if not m:
        return None

    cookie = m.group(1)
    t = re.search(r"accounts_superwall_token=([^;]+)", cookie)
    c = re.search(r"paywall_sAntiCsrfToken=([^;]+)", cookie)
    if t and c:
        return t.group(1).strip(), c.group(1).strip()
    return None


def save_and_test(token: str, csrf: str) -> bool:
    """Save tokens + smoke test."""
    SECRETS.mkdir(exist_ok=True)

    # Build minimal cookie string (only what we need)
    cookie = f"accounts_superwall_token={token}; paywall_sAntiCsrfToken={csrf}"
    cookie_path = SECRETS / "cookie.txt"
    cookie_path.write_text(cookie)
    cookie_path.chmod(0o600)

    # Remove stale csrf.txt if present
    csrf_path = SECRETS / "csrf.txt"
    if csrf_path.exists():
        csrf_path.unlink()

    print(f"\nSaved to {cookie_path}")
    print(f"Token: {token[:20]}...")
    print(f"CSRF:  {csrf}")

    print("\nTesting connection...")
    sys.path.insert(0, str(ROOT / "src"))
    from superwall_kit import SuperwallClient

    try:
        c = SuperwallClient()
        user = c.query("user.getSelf", {})
        uid = user.get("user", {}).get("id", user.get("id", "?"))
        print(f"Logged in as user {uid}")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        print("The token might be expired or from a different workspace.")
        return False


def main():
    print("=" * 50)
    print("  Superwall Login")
    print("=" * 50)
    print()
    print("Step 1: Open superwall.com in Chrome and log in")
    print("Step 2: Open DevTools (Cmd+Opt+I) → Console tab")
    print("Step 3: Paste this snippet and press Enter:")
    print()
    print(f"  {CONSOLE_SNIPPET}")
    print()
    print('Step 4: It copies 2 tokens to your clipboard.')
    print("        Paste them below and press Ctrl+D:")
    print()

    text = sys.stdin.read().strip()
    if not text:
        print("Nothing pasted.")
        sys.exit(1)

    # Try token paste first, then cURL fallback
    result = parse_token_paste(text)
    if result:
        token, csrf = result
        print("Detected: token paste (2 values)")
    else:
        result = parse_curl(text)
        if result:
            token, csrf = result
            print("Detected: cURL paste (extracted 2 tokens from cookie)")
        else:
            print("\nCouldn't find tokens in what you pasted.")
            print("Expected either:")
            print("  - 2 lines: accounts_superwall_token=... and paywall_sAntiCsrfToken=...")
            print("  - A full Copy-as-cURL from DevTools")
            sys.exit(1)

    ok = save_and_test(token, csrf)
    if ok:
        print("\nYou're all set. Start editing paywalls!")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
