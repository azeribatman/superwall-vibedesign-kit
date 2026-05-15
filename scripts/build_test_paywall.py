#!/usr/bin/env python3
"""End-to-end demo: compose a single-page paywall from scratch, validate it,
optionally create a brand-new paywall in your Superwall app and push it live.

Usage:
    APP_ID=12345 python3 scripts/build_test_paywall.py
    APP_ID=12345 python3 scripts/build_test_paywall.py --push
"""
import sys, os, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from superwall_kit import SuperwallClient, validate_snapshot, summarize
from superwall_kit.scratch import (
    Scratch, length, color, font, text_value, icon_value, stack_property,
    click_behavior, ref_token, lit,
)

# Set via `APP_ID=12345 python3 scripts/build_test_paywall.py`
APP_ID = int(os.environ.get("APP_ID", "0"))


def compose():
    s = Scratch(name="test", identifier="test_paywall_kit")
    # Theme
    s.theme(
        background="#000000",
        text="#ffffff",
        primary="#3b82f6",          # blue used for accents/checks/border
        secondary="#9ca3af",        # muted
        ctaText="#0b1220",          # dark text on CTA
        ctaBg="#a8c3e6",            # light blue CTA background
        border="#1f2937",           # subtle border
        borderSelected="#3b82f6",
        cardBg="#000000",
        elementBackground="#0a0a0a",
        productSelectedBg="#000000",
    )

    # Skip product records for now — push will set them via the paywall UI.
    # The CTA still emits set-product-index actions; renderer falls back gracefully.

    # Root: stretch all children to full width; add horizontal padding so everything insets nicely
    root = s.root_stack(
        axis="y", cross="stretch", main="start", gap="0px",
        bg=ref_token("background"), name="Main",
        padding={"top": 60, "x": 20, "bottom": 24},
    )

    pill_wrap = s.stack(root, axis="x", main="center", cross="center", name="PillWrap")
    pill = s.stack(pill_wrap, axis="x", main="center", cross="center",
                   padding={"y": 8, "x": 22},
                   border_color=ref_token("primary"), border_width=1.5, radius=999,
                   name="PremiumPill")
    s.text(pill, "Premium", size=14, weight="700",
           color_=ref_token("primary"), align="center")

    # Title
    s.stack(root, height=18, name="Sp1")
    s.text(root, "Get the full picture with Premium",
           size=30, weight="600", color_=ref_token("text"), align="center", line_height="36px",
           name="Title")

    s.stack(root, height=80, name="Sp2")

    # Checklist (left-aligned rows; inset slightly)
    checklist = s.stack(root, axis="y", gap="18px",
                        padding={"x": 12},
                        cross="start", name="Checklist")

    def add_check_row(prefix, bold_part="", suffix=""):
        row = s.stack(checklist, axis="x", cross="center", gap="14px", name="Row")
        s.icon(row, "Check", color_=ref_token("primary"), size=18, node_name="Check")
        if bold_part:
            line = s.stack(row, axis="x", cross="center", gap="6px", name="Line")
            s.text(line, prefix, size=18, weight="400", color_=ref_token("text"), align="start")
            s.text(line, bold_part, size=18, weight="700", color_=ref_token("text"), align="start")
            if suffix:
                s.text(line, suffix, size=18, weight="400", color_=ref_token("text"), align="start")
        else:
            s.text(row, prefix, size=18, weight="400", color_=ref_token("text"), align="start")

    add_check_row("Everything in", "Free")
    for line in [
        "Unlock advanced features",
        "Faster search and filters",
        "Priority support",
        "Customize the experience",
        "Sync across your devices",
    ]:
        add_check_row(line)

    s.stack(root, height=60, name="Sp3")

    # Indicator dots (center-aligned, small)
    dots_wrap = s.stack(root, axis="x", main="center", cross="center", name="DotsWrap")
    dots = s.stack(dots_wrap, axis="x", gap="8px", main="center", cross="center", name="Dots")
    for i in range(5):
        c = "#ffffff" if i == 0 else "#3a3a3a"
        s.stack(dots, width=8, height=8, radius=999, bg=c, name=f"Dot{i}")

    s.stack(root, height=24, name="Sp4")

    # Subtitle
    s.text(root, "Claim your offer, and then $19.99/mo.",
           size=14, weight="400", color_=ref_token("text"), align="center", name="Sub1")
    s.text(root, "Swipe \U0001F449 to decline.",
           size=14, weight="400", color_=ref_token("text"), align="center", name="Sub2")

    s.stack(root, height=18, name="Sp5")

    # Product cards row — flex-stretch distribution (template-style)
    cards = s.stack(root, axis="x", gap="10px", main="stretch", cross="stretch",
                    name="Cards")

    def product_card(card_title, card_value, selected, action_index):
        # No explicit width — main=stretch on parent makes children share space equally
        c = s.stack(cards, axis="y", main="center", cross="center", gap="8px",
                    padding={"y": 20, "x": 8},
                    border_color=ref_token("borderSelected") if selected else ref_token("border"),
                    border_width=2 if selected else 1, radius=14,
                    bg=ref_token("cardBg"), name=f"Card-{card_title}")
        s.text(c, card_title, size=12, weight="700",
               color_=ref_token("text"), align="center")
        s.text(c, card_value, size=15, weight="400",
               color_=ref_token("secondary"), align="center")
        s.set_click(c, [{"type": "set-product-index", "index": action_index}])
        return c

    product_card("TRY FOR 7 DAYS", "Free", selected=True, action_index=0)
    product_card("TRY FOR 30 DAYS", "$1.99", selected=False, action_index=1)

    s.stack(root, height=18, name="Sp6")

    # Terms
    s.text(root, "By tapping above, you agree to the Supplemental Terms, Terms of Use, and Privacy Policy",
           size=12, weight="400", color_=ref_token("secondary"), align="center", name="Terms")

    s.stack(root, height=14, name="Sp7")

    # CTA button — direct child of root (root cross=stretch), so it fills width
    cta = s.stack(root, axis="x", main="center", cross="center",
                  padding={"y": 20},
                  radius=999, bg=ref_token("ctaBg"),
                  name="CTA")
    s.text(cta, "START FOR FREE", size=16, weight="700",
           color_=ref_token("ctaText"), align="center")
    s.set_click(cta, [{"type": "purchase", "reference": {"type": "by-selected"}}])

    s.stack(root, height=24, name="BottomSpacer")

    return s.build()


def create_blank_paywall(c):
    """Real from-scratch paywall creation via createPaywallV4."""
    r = c.mutate("blitzMigration.paywalls.createPaywallV4",
                 {"applicationId": APP_ID})
    return "blitzMigration.paywalls.createPaywallV4", r


def main():
    if not APP_ID:
        print("Set APP_ID env var to one of your Superwall app IDs.")
        print("  e.g.   APP_ID=12345 python3 scripts/build_test_paywall.py --push")
        return 2
    print(f"composing snapshot from scratch (app {APP_ID})...")
    snap = compose()
    print(f"  records: {len(snap['store'])}")

    print("\nvalidating...")
    issues = validate_snapshot(snap)
    print(summarize(issues))
    n_err = sum(1 for lvl, *_ in issues if lvl == "error")

    out = ROOT / "data" / "pulled" / "_test_built.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, indent=2))
    print(f"\nsaved to {out.relative_to(ROOT)}")

    if n_err:
        print(f"\nrefusing to push: {n_err} validation errors.")
        return 1

    if "--push" not in sys.argv:
        print("\n(dry-run; pass --push to create paywall + push)")
        return 0

    c = SuperwallClient()
    print("\ncreating empty paywall (via duplicate; design will be overwritten)...")
    proc, result = create_blank_paywall(c)
    if not proc:
        print("ERROR: could not create paywall. Aborting.")
        return 2

    print(f"  via {proc}")
    print(f"  result keys: {list((result or {}).keys()) if isinstance(result, dict) else type(result).__name__}")
    if isinstance(result, dict):
        pid = result.get("id") or (result.get("paywall") or {}).get("id") or result.get("paywallId") or result.get("databaseId")
    else:
        pid = result
    if not pid:
        print("ERROR: couldn't extract paywall id from response.")
        print(json.dumps(result, indent=2)[:800])
        return 2

    print(f"\npushing snapshot to paywall {pid}...")
    ver = c.push_snapshot(paywall_id=int(pid), application_id=APP_ID, snapshot=snap)
    print(f"PUSHED. version: {ver}")
    print(f"\nopen: https://superwall.com/applications/{APP_ID}/paywalls/{pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
