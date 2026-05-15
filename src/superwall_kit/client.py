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
                "title": "",
                "description": "",
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
                "title": "",
                "description": "",
            },
        )
        return res["version"]

    def push_snapshot(self, paywall_id: int, application_id: int, snapshot: dict) -> int:
        """prepare + promote in one shot."""
        sid = self.prepare_snapshot(paywall_id, application_id, snapshot)
        return self.promote_snapshot(paywall_id, application_id, sid)

    def create_paywall(self, application_id: int) -> dict:
        """Create a brand-new empty v4 paywall in the application.
        Returns the API response; access `result['paywall']['id']` for the new paywall id.
        """
        return self.mutate(
            "blitzMigration.paywalls.createPaywallV4",
            {"applicationId": application_id},
        )

    def list_paywalls(self, application_id: int, take: int = 50, skip: int = 0) -> dict:
        return self.query(
            "blitzMigration.paywalls.getPaywalls",
            {"applicationId": application_id, "take": take, "skip": skip},
        )

    def list_assets(self, application_id: int, *, type: str = "image", limit: int = 100) -> dict:
        """List previously-uploaded assets in an application (images, videos, lottie)."""
        return self.query("assets.list",
                          {"applicationId": application_id, "type": type, "limit": limit})

    # --- AI image generation + asset upload ---
    def generate_image(self, prompt: str, *, style: str = "digital_illustration",
                       sub_style: str = "2d_art_poster") -> str:
        """Run Superwall's AI image generator. Returns a base64 data URL.

        Common styles: 'realistic_image', 'digital_illustration', 'vector_illustration', 'icon'.
        Common sub_styles for digital_illustration: '2d_art_poster', '2d_art_poster_2',
        'engraving_color', 'grain', 'hand_drawn', 'multicolor', 'pixel_art',
        'pop_art', 'street_art', 'urban_glow', 'noir', 'pastel_gradient', etc.
        """
        r = self.mutate("ai.generateImage",
                        {"prompt": prompt, "style": style, "subStyle": sub_style})
        return r["dataUrl"]

    def remove_background(self, image_url: str) -> str:
        """Run AI background removal. Returns a base64 data URL of the cutout."""
        r = self.mutate("ai.removeBackground", {"imageUrl": image_url})
        # may return {dataUrl} or {imageUrl} — handle both
        return r.get("dataUrl") or r.get("imageUrl") or r.get("url")

    def upload_image_bytes(self, image_bytes: bytes, *, application_id: int,
                            name: str | None = None, mime: str = "image/png") -> str:
        """Upload a raw image (bytes) and register it as an asset. Returns the
        final user-content URL ready to drop into a paywall."""
        import base64, hashlib, time
        ext = mime.split("/")[-1] if "/" in mime else "png"
        if not name:
            name = f"generated-{int(time.time())}"
        filename = f"{name}.{ext}"

        checksum = base64.b64encode(hashlib.md5(image_bytes).digest()).decode()
        r = self.mutate("assets.generateUploadInstructions", {
            "filename": filename,
            "byteSize": len(image_bytes),
            "checksum": checksum,
            "contentType": mime,
            "metadata": {"lastModified": int(time.time() * 1000)},
            "applicationId": application_id,
        })
        ins, res = r["instructions"], r["result"]

        # PUT to the presigned URL
        req = urllib.request.Request(ins["url"], data=image_bytes, method=ins["method"])
        for h, v in (ins.get("headers") or {}).items():
            req.add_header(h, v)
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()

        # Register
        public_url = res["url"]
        key = public_url.rsplit("/", 1)[-1]
        self.mutate("assets.create", {
            "applicationId": application_id,
            "key": key,
            "name": name,
            "url": public_url,
            "type": "image",
            "mimeType": mime,
            "fileSize": len(image_bytes),
        })
        return public_url

    def upload_data_url(self, data_url: str, *, application_id: int,
                        name: str | None = None) -> str:
        """Convert a base64 data URL (e.g. from `generate_image`) to bytes and upload."""
        import base64, re
        m = re.match(r"data:([^;]+);base64,(.+)", data_url)
        if not m:
            raise ValueError("not a base64 data URL")
        mime, b64 = m.group(1), m.group(2)
        return self.upload_image_bytes(base64.b64decode(b64),
                                       application_id=application_id,
                                       name=name, mime=mime)

    def generate_and_upload_image(self, prompt: str, *, application_id: int,
                                   style: str = "digital_illustration",
                                   sub_style: str = "2d_art_poster",
                                   remove_bg: bool = False,
                                   name: str | None = None) -> str:
        """End-to-end: generate via AI, optionally remove background, upload, register.
        Returns the final user-content URL."""
        data_url = self.generate_image(prompt, style=style, sub_style=sub_style)
        public_url = self.upload_data_url(data_url, application_id=application_id, name=name)
        if remove_bg:
            cutout = self.remove_background(public_url)
            if cutout and cutout.startswith("data:"):
                public_url = self.upload_data_url(
                    cutout, application_id=application_id,
                    name=(name or "generated") + "-no-bg")
            elif cutout:
                public_url = cutout
        return public_url
