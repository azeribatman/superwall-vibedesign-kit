"""Load Superwall auth from local .secrets/ files.

We don't touch the system cookie jar. Paste your session cookie once into
.secrets/cookie.txt and the CSRF token into .secrets/csrf.txt, and that's it.
"""
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


def load_auth() -> Auth:
    cookie_path = SECRETS / "cookie.txt"
    csrf_path = SECRETS / "csrf.txt"
    if not cookie_path.exists() or not csrf_path.exists():
        raise FileNotFoundError(
            f"Missing {cookie_path} or {csrf_path}. "
            "Paste your Superwall session cookie and CSRF token there."
        )
    return Auth(
        cookie=cookie_path.read_text().strip(),
        csrf=csrf_path.read_text().strip(),
    )
