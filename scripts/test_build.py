#!/usr/bin/env python3
"""End-to-end test: load the smallest template, mutate it, validate.

Usage:
    python3 scripts/test_build.py                  # dry-run, no push
    python3 scripts/test_build.py --donor 25513
    python3 scripts/test_build.py --push <PAYWALL_ID> --app <APP_ID>
"""
import sys, json, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from superwall_kit import PaywallBuilder, summarize, SuperwallClient


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--donor", default="25513", help="template id to clone")
    ap.add_argument("--push", type=int, help="push to this paywall id (live!)")
    ap.add_argument("--app", type=int, help="application id (required with --push)")
    ap.add_argument("--out", default="data/pulled/_built.json", help="where to save the built snapshot")
    args = ap.parse_args()

    print(f"loading donor template {args.donor}...")
    b = PaywallBuilder.from_donor(args.donor)

    print("mutating: rename + swap a couple of texts + tweak primary color...")
    b.set_name("Built via superwall-kit")
    b.set_identifier("kit_built_demo")
    # Try a benign text replace; templates often have these strings
    for needle, repl in [
        ("Continue", "Get Started"),
        ("Start Free Trial", "Try Free"),
        ("Unlock", "Subscribe"),
    ]:
        b.set_text(needle, repl)

    # Try theme override (skip if token missing)
    try:
        b.set_theme("state:style.interface.primary", {"type": "css-color", "value": "#22c55e"})
        print("  theme primary -> #22c55e")
    except KeyError as e:
        print(f"  (skip theme override: {e})")

    print("\nvalidating...")
    issues = b.validate()
    print(summarize(issues))

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(b.envelope(), indent=2))
    print(f"\nbuilt snapshot saved to {out_path.relative_to(ROOT)}")

    n_errors = sum(1 for lvl, *_ in issues if lvl == "error")
    if args.push:
        if not args.app:
            print("--push requires --app"); sys.exit(2)
        if n_errors:
            print(f"\nrefusing to push: {n_errors} validation errors. fix first.")
            sys.exit(1)
        print(f"\nPUSH MODE: target paywall={args.push} app={args.app}")
        confirm = input("type 'yes' to push: ").strip().lower()
        if confirm != "yes":
            print("aborted.")
            return
        c = SuperwallClient()
        ver = c.push_snapshot(paywall_id=args.push, application_id=args.app, snapshot=b.snapshot())
        print(f"pushed. new version: {ver}")
    else:
        print("\n(dry-run; pass --push <id> --app <id> to actually push)")


if __name__ == "__main__":
    main()
