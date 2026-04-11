#!/usr/bin/env python3
"""Paste a Copy-as-cURL from Superwall DevTools. We extract cookie + csrf.

Usage:
    python3 scripts/login.py

Then paste a cURL command copied from Chrome/Safari DevTools (Network tab,
any request to superwall.com/api/trpc/...). Press Ctrl+D when done.

We parse out the cookie string and save it to .secrets/cookie.txt. The
anti-csrf token is inside the cookie itself, so you only need one file.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRETS = ROOT / ".secrets"


def extract_cookie_from_curl(curl_text: str) -> str | None:
    """Find the cookie value from a curl command.

    Handles both:
        -b 'cookie_string'
        --cookie 'cookie_string'
        -H 'cookie: cookie_string'
    """
    # -b or --cookie flag
    m = re.search(r"(?:-b|--cookie)\s+['\"]([^'\"]+)['\"]", curl_text)
    if m:
        return m.group(1)

    # Cookie as -H header (case-insensitive)
    m = re.search(
        r"-H\s+['\"]cookie:\s*([^'\"]+)['\"]",
        curl_text,
        re.IGNORECASE,
    )
    if m:
        return m.group(1)

    return None


def extract_csrf_from_cookie(cookie: str) -> str | None:
    m = re.search(r"paywall_sAntiCsrfToken=([^;]+)", cookie)
    return m.group(1).strip() if m else None


def main():
    print("Paste a Copy-as-cURL from Superwall DevTools.")
    print("(Network tab → any /api/trpc/ request → right-click → Copy → Copy as cURL)")
    print("Press Ctrl+D (or Ctrl+Z on Windows) when done:\n")

    curl_text = sys.stdin.read()

    cookie = extract_cookie_from_curl(curl_text)
    if not cookie:
        print("\n❌ Could not find a cookie in the pasted cURL.")
        print("   Make sure the cURL includes a -b 'cookie=...' or -H 'cookie: ...' flag.")
        sys.exit(1)

    csrf = extract_csrf_from_cookie(cookie)
    if not csrf:
        print("\n❌ Found a cookie, but no paywall_sAntiCsrfToken inside.")
        print("   Make sure you're logged into Superwall in your browser.")
        sys.exit(1)

    SECRETS.mkdir(exist_ok=True)
    cookie_path = SECRETS / "cookie.txt"
    cookie_path.write_text(cookie)
    cookie_path.chmod(0o600)

    # Remove stale csrf.txt if present (we auto-extract now)
    csrf_path = SECRETS / "csrf.txt"
    if csrf_path.exists():
        csrf_path.unlink()

    print(f"\n✅ Saved to {cookie_path}")
    print(f"   CSRF auto-extracted: {csrf[:12]}...")

    # Smoke test
    print("\n🔍 Testing connection...")
    sys.path.insert(0, str(ROOT / "src"))
    from superwall_kit import SuperwallClient

    try:
        c = SuperwallClient()
        # Light query: get user
        user = c.query("user.getSelf", {})
        print(f"✅ Logged in as user id {user.get('id', '?')}")
    except Exception as e:
        print(f"❌ Test call failed: {e}")
        print("   The cookie might be from a different workspace than the paywall you want to edit.")
        sys.exit(1)


if __name__ == "__main__":
    main()
