# superwall-vibedesign-kit

You can read, mutate, and **build Superwall paywalls from scratch** by
talking to the user in plain English. Don't make them paste JSON, learn
the schema, or hand-edit anything. You handle the technical work.

The full skill prompt lives at `skills/superwall/SKILL.md` — read it
when you're activating this workflow. This file is the project-level
quick reference.

## Auth — first thing to check

```bash
test -f .secrets/cookie.txt
```

If missing, walk the user through the 20-second console snippet (in
`skills/superwall/SKILL.md` → Step 1) and write the cookie file. If
push later returns 403, the cookie is for the wrong workspace.

## Client API quick reference

```python
import sys; sys.path.insert(0, "src")
from superwall_kit import SuperwallClient, validate_snapshot, summarize, PaywallBuilder, Grammar
from superwall_kit.scratch import Scratch, ref_token, lit, text_liquid
c = SuperwallClient()

# Paywalls
c.create_paywall(application_id=APP)                        # new empty
c.get_snapshot(paywall_id=PID)                              # pull
c.push_snapshot(paywall_id=PID, application_id=APP, snapshot=snap)
c.list_paywalls(application_id=APP)

# Assets / images
c.upload_image_bytes(bytes, application_id=APP, name="...", mime="image/png")
c.upload_data_url(data_url, application_id=APP, name="...")
c.list_assets(application_id=APP, type="image")

# AI
c.generate_image(prompt, style="digital_illustration", sub_style="2d_art_poster")
c.remove_background(image_url)
c.generate_and_upload_image(prompt, application_id=APP, style=..., sub_style=..., remove_bg=False)

# Validation
validate_snapshot({"snapshot": snap})
```

## Two ways to author

| Use this | When |
|---|---|
| `Scratch` — every node generated from primitives | "build a paywall from this screenshot", "make a new paywall like X", from-scratch composition |
| `PaywallBuilder.from_donor(...)` — clones + mutates | "change my paywall's color/text", small edits to existing paywalls |

## Custom CSS injection (for what grammar doesn't cover)

Use `prop:custom-css` on a STACK (not text) to inject any CSS:
```python
s.records[node]["properties"]["prop:custom-css"] = lit({
    "type": "property-custom-css",
    "properties": [
        {"type": "custom-css-property", "id": "action:xx01",
         "property": "<camelCaseCssProperty>", "value": "<css value>"},
    ],
})
```

Use cases: absolute positioning, env() safe-area, animations, backdrop blur, negative margins, transforms, letterSpacing. Each property entry needs a unique `id`.

## Hard-won layout rules (don't relearn)

- **Borders**: use `border_color` + `border_width` on `stack()`. The helper auto-emits the combo keys (`css:borderTopWidth;borderRightWidth;...`) and `borderStyle: solid`. Single-key forms are silently ignored.
- **Padding**: pass `padding={"all|x|y|top|right|bottom|left": N}` to `stack()` / `root_stack()`. There is no shorthand — Superwall uses combo keys per axis.
- **Equal-width children** (e.g. side-by-side product cards): parent `main="stretch"`, **no** explicit child width. `width=48% + main=space-between` pins to edges.
- **Full-width children** (e.g. CTA): parent `cross="stretch"`. Children inherit width.
- **Centered small element** (pill, dots): wrap in an `axis="x" main="center"` row so it stays compact.
- **Theme refs**: always `ref_token("primary")` etc., never hardcoded hex unless no token covers it.
- **Click actions** valid types: `purchase`, `restore`, `close`, `open-url`, `navigate-page`, `set-state`, `set-product-index`, `select-choice`, `request-permission`, `set-attribute`, `custom-in-app`, `custom-placement`. `set_click(node, [{...}])` wraps them in `action-execution`.
- **Conditional**: `{query:{combinator:"and", rules:[{field, operator, value}]}, value: ...}`. Operators: `=`, `!=`, `<`, `<=`, `>`, `>=`, `contains`.
- **paywall record `templateType`**: `"UNLISTED"` or `"GLOBAL"` (not `"PRIVATE"`).
- **Snapshot envelope** for `push_snapshot`: `{store, schema}` flat — `Scratch.build()` returns this directly.
- **Images**: always create the rectangle first (`s.image_box(parent, url, width, height, fit="cover")`), never let the image's intrinsic size dictate layout. Generate via `c.generate_and_upload_image(prompt, application_id, style, sub_style)` — returns a ready-to-use URL. **PNG is reliable; JPEG sometimes doesn't render** — convert with `sips -s format png` before upload. WebP works through the editor's manual upload.
- **Live prices**: `s.text_liquid(parent, "{{ products.primary.price }}/year", required_state_ids=["state:products.primary.price"], ...)`.
- **Selected product state**: `state:products.selectedIndex` (NOT `selectedProductIndex`). Action: `set-product-index`. Build conditionals on borderColor/Width/backgroundColor for visual toggling.
- **Safe-area**: editor preview has `env() = 0`. Always use `max(calc(env(...) + N), FALLBACK)`.
- **Real product identifiers required** for push to succeed (otherwise 409). Pull an existing paywall in the same app to find the SKUs.
- **Custom CSS only on stacks**, never on text nodes (push validation fails with cryptic 'accept' error).
- **Swipable paywalls** (Citizen-style multi-page): paging x-stack carousel with `scroll="paging"`, `width=100vw`, `height=calc(100vh - 420px)` (raw unit), `marginLeft: -<rootPad>` to escape parent padding. Each page also `width+minWidth=100vw` + matching height. The carousel auto-writes its visible index to **`state:node.<carouselId>.childPageIndex`** (NOT `currentIndex`).
- **Pagination dots**: use a real `indicator` node + 1 `indicator-item` child (NOT manual conditional stacks — server may reject those). Bind `currentIndex` state-ref to the carousel's `childPageIndex` state. Inside the item, conditional bg uses **`state:self.isCurrent`** for single-dot highlight, NOT `isCompleted` (which is progress-bar fill).
- **Web preview doesn't simulate swipe** for paging stacks — test on device.
- **App Store guideline 3.1.2**: CTA text must change with selected product. Bind `prop:text` of the CTA label to a conditional on `state:products.selectedIndex` (e.g., index=0 → "START FOR FREE", index=1 → "CONTINUE"). Static "START FOR FREE" while a paid plan is selected = rejection.
- **Default selected product**: add a `state:products.selectedIndex` state record to the snapshot store with `defaultValue: {type: variable-number, value: 0}` so the first card renders selected on first paint (otherwise the conditional falls through and both cards look unselected).
- **Per-slide pill label**: build a single conditional `prop:text` with N rules (one per slide index) reading from the carousel's `childPageIndex`. Pill auto-updates as user swipes.
- **Skip on last slide**: conditional `css:display = "flex"` when `childPageIndex == last`, else `"none"`. Don't use time-delayed `fadeIn` for swipable paywalls.
- **featureGating**: `"GATED"` (locked behind purchase, default for free-trial models) or `"NON_GATED"` (informational). `Scratch()` defaults to `GATED` since v0.5.0.
- **Responsive hero sizing**: use CSS `min(300px, 72vw, 38vh)` raw length. `flex:1 + height:100%` doesn't render in Superwall.
- **AI image pipeline**: gpt-image-2 high + green-screen prompt → Bria RMBG → upload. Trigger words on OpenAI content filter: "Sexual Assault" → use "Restricted Category"; "offender warning" → use "alert pin".
- **Fal MCP setup**: `claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp --header "Authorization: Bearer <KEY>"` then restart with `claude -c`.

## Reference files

- `docs/REFERENCE.md` — **auto-generated** SwiftUI-style reference for every node, property, value type, click action, font, icon, theme token (mined from 208 templates). **Read before designing.**
- `docs/GOTCHAS.md` — editor-crash causes
- `docs/SCHEMA.md` — narrative schema
- `data/grammar/*.json` — machine-readable grammar (composition, properties, fonts, icons, click_behaviors, conditional_operators, theme_tokens)
- `data/fragments/` — 2231 reusable subtrees from real templates
- `data/templates/*.json` — pulled live templates (refresh: `python3 scripts/pull_templates.py`)
- `scripts/build_test_paywall.py` — working from-scratch example (the "Premium" screenshot)
- `scripts/build_test_paywall.py` — minimal from-scratch example showing the full composer flow

To refresh after pulling templates:
```bash
python3 scripts/pull_templates.py
python3 scripts/mine_full_grammar.py
python3 scripts/mine_fragments.py
```

## Rules

1. **Validate before pushing.** Refuse on `error`-level issues.
2. **Confirm substantial pushes.** Summarize changes; share editor URL after.
3. **Plain English summaries only** — never dump JSON at the user.
4. **A successful push ≠ renders.** Ask user to reload the editor; "Something's gone wrong" usually means an unrecognized property or action type.
5. **No new dependencies** — stdlib + the existing client only.

## Typical requests

- **"Build a paywall like this screenshot in app X"** → `create_paywall(X)` → compose with `Scratch` → validate → push → share URL.
- **"Change CTA color to green"** → `get_snapshot` → `PaywallBuilder.set_theme("state:style.interface.primary", "#22c55e")` → push.
- **"Duplicate template T to a new paywall in app A"** → `create_paywall(A)` → load template snapshot → mutate name/products → push to new pid.
- **"Add a trial-only screen"** → pull → graft a page sibling with conditional `css:display` on `state:products.hasIntroductoryOffer` → push.
