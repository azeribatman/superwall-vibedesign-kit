"""Thin wrapper over Superwall's internal tRPC endpoints.

All the editor does goes through /api/trpc. We call the same endpoints with
the same auth the browser uses.
"""
from __future__ import annotations
import json
import urllib.parse
import urllib.request
from typing import Any

from .auth import Auth, load_auth

BASE = "https://superwall.com/api/trpc"


class SuperwallError(RuntimeError):
    pass


class SuperwallClient:
    def __init__(self, auth: Auth | None = None):
        self.auth = auth or load_auth()

    def _request(self, method: str, path: str, body: bytes | None = None) -> Any:
        url = f"{BASE}/{path}"
        req = urllib.request.Request(url, data=body, method=method)
        for k, v in self.auth.headers().items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as e:
            raw = e.read()
            raise SuperwallError(f"HTTP {e.code} on {path}: {raw[:400].decode(errors='replace')}")
        return json.loads(raw)

    # --- tRPC query helpers ---
    def query(self, endpoint: str, payload: dict) -> Any:
        """GET a tRPC query. Payload is the JSON input; we wrap it in batch=1 shape."""
        wrapped = {"0": {"json": payload}}
        qs = urllib.parse.urlencode({"batch": 1, "input": json.dumps(wrapped)})
        data = self._request("GET", f"{endpoint}?{qs}")
        return data[0]["result"]["data"]["json"]

    def mutate(self, endpoint: str, payload: dict) -> Any:
        """POST a tRPC mutation."""
        wrapped = {"0": {"json": payload}}
        body = json.dumps(wrapped).encode()
        data = self._request("POST", f"{endpoint}?batch=1", body)
        return data[0]["result"]["data"]["json"]

    # --- High-level paywall ops ---
    def get_snapshot(self, paywall_id: int, version: str = "latest") -> dict:
        return self.query(
            "paywalls.getLatestSnapshotByVersion",
            {"paywallId": paywall_id, "version": version},
        )

    def prepare_snapshot(self, paywall_id: int, application_id: int, snapshot: dict) -> str:
        res = self.mutate(
            "paywalls.prepareSnapshotForPromotion",
            {
                "paywallId": paywall_id,
                "applicationId": application_id,
                "snapshot": snapshot,
                "title": None,
                "description": None,
            },
        )
        return res["data"]["snapshotIdentifier"]

    def promote_snapshot(self, paywall_id: int, application_id: int, snapshot_id: str) -> int:
        res = self.mutate(
            "paywalls.promoteFromSnapshot",
            {
                "paywallId": paywall_id,
                "applicationId": application_id,
                "snapshotIdentifier": snapshot_id,
                "title": None,
                "description": None,
            },
        )
        return res["version"]

    def push_snapshot(self, paywall_id: int, application_id: int, snapshot: dict) -> int:
        """prepare + promote in one shot."""
        sid = self.prepare_snapshot(paywall_id, application_id, snapshot)
        return self.promote_snapshot(paywall_id, application_id, sid)
