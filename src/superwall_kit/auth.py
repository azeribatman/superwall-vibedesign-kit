"""Load Superwall auth from local .secrets/ files.

We don't touch the system cookie jar. Paste your session cookie once into
.secrets/cookie.txt — the anti-csrf token is extracted from inside the
cookie string automatically.
"""
from __future__ import annotations
import re
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[2]
SECRETS = ROOT / ".secrets"


@dataclass
class Auth:
    cookie: str
    csrf: str

    def headers(self) -> dict:
        return {
            "cookie": self.cookie,
            "anti-csrf": self.csrf,
            "content-type": "application/json",
            "accept": "*/*",
            "origin": "https://superwall.com",
            "referer": "https://superwall.com/editor/",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/146.0.0.0 Safari/537.36"
            ),
        }


def _extract_csrf_from_cookie(cookie: str) -> str | None:
    m = re.search(r"paywall_sAntiCsrfToken=([^;]+)", cookie)
    return m.group(1).strip() if m else None


def load_auth() -> Auth:
    cookie_path = SECRETS / "cookie.txt"
    csrf_path = SECRETS / "csrf.txt"

    if not cookie_path.exists():
        raise FileNotFoundError(
            f"Missing {cookie_path}.\n"
            f"Run `python3 scripts/login.py` and paste a Copy-as-cURL from "
            f"DevTools, or paste your cookie string directly into cookie.txt."
        )

    cookie = cookie_path.read_text().strip()

    # Prefer explicit csrf.txt if present (back-compat), else auto-extract
    if csrf_path.exists():
        csrf = csrf_path.read_text().strip()
    else:
        csrf = _extract_csrf_from_cookie(cookie)
        if not csrf:
            raise ValueError(
                "Could not find paywall_sAntiCsrfToken in cookie string. "
                "Make sure you pasted a full Cookie: header from a logged-in "
                "Superwall session."
            )

    return Auth(cookie=cookie, csrf=csrf)
