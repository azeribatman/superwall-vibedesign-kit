#!/usr/bin/env python3
"""Bulk-pull all v4 Superwall templates into data/templates/<id>.json.

Each file contains:
  {
    "meta": {...}, # name, categories, id, previews, etc.
    "snapshot": {...} # the full design JSON
  }
"""
import sys, json, os, time, concurrent.futures
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from superwall_kit import SuperwallClient

OUT_DIR = ROOT / "data" / "templates"
OUT_DIR.mkdir(parents=True, exist_ok=True)

APP_ID = 37837  # any logged-in app works for listing GLOBAL templates


def list_all(client):
    out = []
    skip = 0
    while True:
        r = client.query(
            "blitzMigration.paywalls.getPaywallTemplates",
            {"take": 250, "skip": skip, "applicationId": APP_ID, "v4Only": True},
        )
        batch = r["paywallTemplates"]
        out.extend(batch)
        if not r.get("hasMore"):
            break
        skip += len(batch)
    return out


def pull_one(meta):
    tid = meta["id"]
    out_path = OUT_DIR / f"{tid}.json"
    if out_path.exists():
        return tid, "cached"
    client = SuperwallClient()
    try:
        snap = client.get_snapshot(tid)
    except Exception as e:
        return tid, f"ERROR {e}"
    record = {
        "meta": {
            "id": meta["id"],
            "name": meta["name"],
            "templateType": meta.get("templateType"),
            "templateCategories": meta.get("templateCategories"),
            "applicationId": meta.get("applicationId"),
            "updatedAt": str(meta.get("updatedAt")),
            "createdAt": str(meta.get("createdAt")),
            "v4": meta.get("v4"),
            "previews": meta.get("previews"),
        },
        "snapshot": snap,
    }
    out_path.write_text(json.dumps(record))
    return tid, f"OK {len(json.dumps(snap))//1024}KB"


def main():
    t0 = time.time()
    client = SuperwallClient()
    print(f"listing templates...")
    all_meta = list_all(client)
    print(f"{len(all_meta)} v4 templates")

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        done = 0
        for tid, status in ex.map(pull_one, all_meta):
            done += 1
            if done % 20 == 0 or "ERROR" in status:
                print(f"[{done}/{len(all_meta)}] {tid}: {status}")

    total = sum(f.stat().st_size for f in OUT_DIR.glob("*.json"))
    print(f"\ndone in {time.time()-t0:.1f}s | {len(list(OUT_DIR.glob('*.json')))} files | {total/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
