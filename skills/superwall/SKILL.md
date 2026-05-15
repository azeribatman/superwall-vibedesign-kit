---
name: superwall
description: Activates whenever the user mentions Superwall, paywalls, or asks to create, build, design, edit, change colors/text, copy a screenshot, generate images with AI, rebuild, duplicate, pull, push, or modify any Superwall paywall. Triggers on phrases like "build a paywall", "make it look like this screenshot", "change my paywall", "create a new paywall in app <ID>", "duplicate this template", "edit Superwall", "make CTA purple", "generate a hero image", "upload image to superwall", or anything referencing `superwall.com`, `paywall id`, or `application id`.
version: 0.5.0
license: MIT
---

# Superwall in Your Pocket

You can read, mutate, **build paywalls from scratch**, generate AI images,
upload assets, and ship live edits in any Superwall account using the
toolkit in this repo. This is everything we've reverse-engineered about
Superwall's internal tRPC API. The public Superwall MCP only manages
metadata — it can't touch design, layout, or content.

## When this skill activates

- "Build/create a paywall in app X" → from-scratch via `Scratch`
- "Make my paywall look like this [screenshot]" → from-scratch matching the image
- "Change my paywall's color/text/products" → mutate via `PaywallBuilder`
- "Generate an image for the hero" → `c.generate_and_upload_image(...)`
- "Upload my image to superwall" → `c.upload_image_bytes(...)`
- "Make it swipable / multi-page / Citizen-style" → see "Swipable / multi-page paywall" section
- Anything else touching paywall design, layout, or assets

---

## Step 1 — Authentication (always first)

```bash
test -f .secrets/cookie.txt
```

If missing, walk the user through the **20-second login**:

> 1. Open **superwall.com** in Chrome and log in.
> 2. Open DevTools (Cmd+Opt+I) → **Console**.
> 3. Paste:
>
> ```js
> copy(`accounts_superwall_token=${document.cookie.match(/accounts_superwall_token=([^;]+)/)[1]}\npaywall_sAntiCsrfToken=${document.cookie.match(/paywall_sAntiCsrfToken=([^;]+)/)[1]}`)
> ```
>
> 4. Paste the two lines back here.

Save:
```bash
mkdir -p .secrets
cat > .secrets/cookie.txt << 'COOKIE'
accounts_superwall_token=<TOKEN>; paywall_sAntiCsrfToken=<CSRF>
COOKIE
chmod 600 .secrets/cookie.txt
```

Smoke test: `c.query("user.getSelf", {})` returns a `user.id`.

**Fallback**: a Copy-as-cURL also works — `scripts/login.py` parses both.
**403 on later push** = wrong workspace. Re-auth.

---

## Step 2 — Identify the target

URL pattern: `https://superwall.com/applications/<APP_ID>/paywalls/<PAYWALL_ID>`

For a brand new paywall: only `application_id` is needed; `paywall_id`
will be returned from `c.create_paywall()`.

---

## Step 3 — The complete client API

```python
import sys; sys.path.insert(0, "src")
from superwall_kit import (
    SuperwallClient, validate_snapshot, summarize,
    PaywallBuilder, Grammar,
)
from superwall_kit.scratch import Scratch, ref_token, lit, text_liquid
c = SuperwallClient()
```

### Paywall management
| Method | Purpose |
|---|---|
| `c.create_paywall(application_id)` | Create a new empty v4 paywall. Returns `{paywall: {id}, redirectURL, versions}`. |
| `c.get_snapshot(paywall_id)` | Pull a paywall's current snapshot. Inner snapshot at `result["snapshot"]`. |
| `c.push_snapshot(paywall_id, application_id, snapshot)` | Prepare + promote in one call. Returns new version int. |
| `c.list_paywalls(application_id, take, skip)` | List paywalls in an app. |

### Assets (images, videos)
| Method | Purpose |
|---|---|
| `c.list_assets(application_id, type="image", limit=100)` | Browse already-uploaded assets. |
| `c.upload_image_bytes(bytes, application_id, name, mime)` | Upload raw bytes. Returns final user-content URL. |
| `c.upload_data_url(data_url, application_id, name)` | Upload a `data:image/...;base64,...` URL. |

### AI
| Method | Purpose |
|---|---|
| `c.generate_image(prompt, style, sub_style)` | Generate via Recraft. Returns base64 dataUrl. |
| `c.remove_background(image_url)` | AI cutout. Returns dataUrl. |
| `c.generate_and_upload_image(prompt, application_id, style, sub_style, remove_bg)` | End-to-end: generate → upload → register → return URL. |

### Validation
| Method | Purpose |
|---|---|
| `validate_snapshot({"snapshot": snap})` | Pre-push structural check. Returns `[(level, code, msg), ...]`. |
| `summarize(issues)` | Pretty-print validation results. |

---

## Step 4 — Authoring strategies

### Strategy A — From scratch (`Scratch`)
Use for: "build a new paywall like this screenshot", "create from scratch in app X". Every record generated; nothing cloned. Push to a paywall created via `c.create_paywall()`.

### Strategy B — Mutate (`PaywallBuilder`)
Use for: "change my paywall's color/text/products", small edits. Clones a donor template or pulled paywall, applies mutations.

```python
b = PaywallBuilder.from_donor("template_id_or_path")
b.set_text("Continue", "Get Started")
b.set_theme("state:style.interface.primary", "#22c55e")
b.set_image("Hero", "https://...")
issues = b.validate()
ver = c.push_snapshot(paywall_id=PID, application_id=APP, snapshot=b.snapshot())
```

---

## Step 5 — From-scratch composition recipe

Tested end-to-end on the Citizen / Offender Premium paywall.

```python
s = Scratch(name="My Paywall", identifier="my_paywall_kit")

# 1. Theme tokens (.light + .dark records auto-generated)
s.theme(
    background="#0F0E11", text="#FFFFFF",
    primary="#C8102E",                  # brand red
    secondary="#D9261F", ctaText="#FFFFFF", ctaBg="#C8102E",
    border="#3A2D2F", borderSelected="#C8102E",
    cardBg="#0F0E11", productSelectedBg="#C8102E33",
    linkMuted="#FFFFFF8C",              # rgba(255,255,255,0.55)
)

# 2. Products — must be REAL identifiers from the app's catalog or push 409s
s.product("primary",   "com.yourapp.yearly")    # replace with the SKU from your App Store catalog
s.product("secondary", "com.yourapp.monthly")

# 3. Root with safe-area — main=space-between anchors top vs bottom groups
root = s.root_stack(
    axis="y", cross="stretch", main="space-between", gap="0px",
    bg=ref_token("background"), padding={"top": 60, "x": 20, "bottom": 40},
)
# Override with custom CSS for env() safe-area + relative positioning
s.records[root]["properties"]["prop:custom-css"] = lit({
    "type": "property-custom-css",
    "properties": [
        # max() ensures editor preview (where env=0) still has real padding
        {"type": "custom-css-property", "id": "action:sa01", "property": "paddingTop",
         "value": "max(calc(env(safe-area-inset-top, 0px) + 16px), 64px)"},
        {"type": "custom-css-property", "id": "action:sa02", "property": "paddingBottom",
         "value": "max(calc(env(safe-area-inset-bottom, 0px) + 24px), 56px)"},
        {"type": "custom-css-property", "id": "action:sa03", "property": "position", "value": "relative"},
    ],
})

# 4. Top group + bottom group split for space-between to actually distribute
top_group = s.stack(root, axis="y", cross="stretch", name="TopGroup")
bottom_group = s.stack(root, axis="y", cross="stretch", name="BottomGroup")

# 5. Build content using primitives — see "Layout primitives" below
```

---

## Layout primitives + hard-won rules

### Stacks (the only container)
- `axis`: `"y"` (column) or `"x"` (row)
- `cross`: `"start"` | `"center"` | `"end"` | `"stretch"`
- `main`: `"start"` | `"center"` | `"end"` | `"stretch"` | `"space-between"`
- `gap`: child spacing as a CSS length string ("12px")
- `padding`: dict — `{"all": N}`, `{"x": N, "y": N}`, or per-side `{"top|right|bottom|left": N}`
- `radius`: corner radius int (px)
- `border_color` + `border_width`: helper auto-emits the long combo keys + `borderStyle: solid`
- `bg`: hex string or `ref_token(name)`

### The 4 layout patterns that actually work
| Goal | How |
|---|---|
| Equal-width children (cards row) | Parent `main="stretch"`, **no** explicit child width. Don't use `width=48% + main=space-between` — that pins to the edges. |
| Full-width children (CTA) | Parent `cross="stretch"`. Children inherit width without setting `css:width`. |
| Centered small element (pill, dots) | Wrap in extra `axis="x" main="center" cross="center"` row so the inner element keeps content-width. |
| Anchor bottom to safe-area | Root `main="space-between"`, content split into `TopGroup` + `BottomGroup`. |

### Why your borders aren't rendering
Superwall ignores single-key `css:borderRadius` / `css:borderWidth`. Use the **combo keys** (the helpers do this for you):
- `css:borderTopWidth;borderRightWidth;borderBottomWidth;borderLeftWidth`
- `css:borderTopStyle;borderRightStyle;borderBottomStyle;borderLeftStyle` ← MUST be `"solid"`
- `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius`

### Why your padding isn't applying
There is **no `css:padding` shorthand**. Use combo keys (helpers do this):
- `css:paddingLeft;paddingRight` (the "x")
- `css:paddingTop;paddingBottom` (the "y")
- `css:paddingTop`, `css:paddingRight`, `css:paddingBottom`, `css:paddingLeft` (per-side)

### Length / unit shapes
- `length(N)` → `{type:"css-length", value:"N", unit:"px"}`
- `length(N, "%")`, `length(N, "vw")`, `length(N, "vh")` are valid
- `"fr"` is **not** a valid unit (will 500). Use `%` for proportional widths.

### Theme token references
Always `ref_token("primary")`, `ref_token("text")`, etc. — never hardcoded hex unless absolutely necessary. Token name resolves to `state:style.interface.<token>` which Superwall maps to `.light` / `.dark` records.

### App Store compliance — CTA text MUST match selected product

Apple guideline 3.1.2: the purchase button label must reflect what's actually being purchased. If the user selects the $1.99/month plan and the button still says "START FOR FREE", that's a rejection.

Use a conditional `prop:text` on the CTA label tied to `state:products.selectedIndex`:

```python
s.records[cta_label_id]["properties"]["prop:text"] = {
    "type": "conditional",
    "options": [
        {"query": {"combinator": "and",
                   "rules": [{"field": "state:products.selectedIndex",
                              "operator": "=", "valueSource": "value",
                              "value": {"type": "variable-number", "value": 1}}]},
         "value": lit({"type": "property-text", "value": "CONTINUE",
                       "rendering": {"type": "literal"}})},
        {"query": {"combinator": "and", "rules": []},
         "value": lit({"type": "property-text", "value": "START FOR FREE",
                       "rendering": {"type": "literal"}})},
    ],
}
```

Standard button text per offer:
- **3-day free trial** → "START FOR FREE" or "Start Free Trial"
- **Paid intro at $1.99** → "CONTINUE" or "Subscribe"
- **Yearly subscription** → "Subscribe" or "Continue"

### Default selected product on first paint

The conditional cards reference `state:products.selectedIndex`. If that state isn't in the snapshot store, the SDK seeds it lazily — but conditionals evaluate **before** the seed, so on first paint both cards render unselected ("default" branch). Fix: add the state record explicitly:

```python
s.records["state:products.selectedIndex"] = {
    "locked": False, "derivation": None,
    "id": "state:products.selectedIndex",
    "defaultValue": {"type": "variable-number", "value": 0},
    "nonRemovable": True, "typeName": "state",
}
```

`defaultValue.value = 0` makes the first product (`paywall_product:primary`) render selected on appear. Use `1` for secondary, etc.

### featureGating — GATED vs NON_GATED

`paywall:paywall.featureGating`:
- **`"GATED"`**: feature is locked behind purchase. After paywall closes/dismisses, the feature is **not** accessible unless the user has an active subscription. The iOS SDK gates on this via `Superwall.shared.register(...)` callbacks.
- **`"NON_GATED"`**: feature is accessible whether or not the user purchases. Paywall is informational/promotional.

For free-trial-or-paid models you almost always want `"GATED"` so dismissing the paywall doesn't unlock the feature.

`Scratch(...)` defaults to `"GATED"` since v0.5.0. Override via the paywall record if needed:
```python
s.records["paywall:paywall"]["featureGating"] = "NON_GATED"
```

### Selection state (toggling cards visually)
- State id: `state:products.selectedIndex` (NOT `selectedProductIndex`)
- Action: `{"type": "set-product-index", "index": N}` wrapped in `action-execution`
- Visual: build conditionals on `css:borderColor`, `css:borderTopWidth;...`, `css:backgroundColor` that compare `state:products.selectedIndex` `=` `{type:"variable-number", value:N}`

### Live prices via Liquid
```python
s.text_liquid(parent, "{{ products.primary.price }}/year",
              required_state_ids=["state:products.primary.price"], ...)
```

The text node's `prop:text` becomes `{type:"property-text", value:"...", rendering:{type:"liquid", requiredStateIds:[...]}}`.

### Conditional values (state-driven props)
```python
{
  "type": "conditional",
  "options": [
    {"query": {"combinator": "and",
               "rules": [{"field": "state:X", "operator": "=", "valueSource": "value",
                          "value": {"type": "variable-number|variable-string|variable-boolean", "value": V}}]},
     "value": <wrapped-value>},
    {"query": {"combinator": "and", "rules": []}, "value": <default-wrapped-value>},
  ],
}
```
Operators: `=`, `!=`, `<`, `<=`, `>`, `>=`, `contains`.

---

## Swipable / multi-page paywall (Citizen-style)

When the user wants a swipable carousel — different title/description/hero
per page, sticky pill on top, sticky cards/CTA on bottom — there's an
exact recipe. Every detail below is mined from real working templates and
verified on device.

### Layout shape

```
root (axis=y, main=space-between, padding for safe area)
├── top_group (axis=y)
│   ├── header_row (centered pill + absolute-right Skip)
│   ├── carousel  ←  the swipable bit (paging stack)
│   │   ├── page 1  (title + description + hero)
│   │   ├── page 2
│   │   └── ...
│   └── dots wrap (indicator + 1 indicator-item template)
└── bottom_group (axis=y)
    ├── product cards (with conditional borders + BEST VALUE chip)
    ├── CTA button
    └── footer links
```

### Carousel — paging x-stack

```python
carousel = s.stack(top_group, axis="x", main="start", cross="center", gap="0px",
                   scroll="paging", snap="center",
                   width=lit({"type": "css-length", "value": "100", "unit": "vw"}),
                   height=lit({"type": "css-length", "unit": "raw",
                                "value": "calc(100vh - 420px)"}),
                   name="Carousel")
s.records[carousel]["properties"]["css:position"] = lit({"type": "css-string", "value": "relative"})
# Shift left by parent's horizontal padding so the 100vw carousel reaches viewport x=0
s.records[carousel]["properties"]["prop:custom-css"] = lit({
    "type": "property-custom-css",
    "properties": [{"type": "custom-css-property", "id": "action:cm01",
                    "property": "marginLeft", "value": "-20px"}],
})
```

**Hard rules** (every one is a real bug we hit while building this):
- `scroll` enum is `none | normal | paging | infinite`. NOT `"x"`/`"y"`.
- The carousel **must** have an explicit `height` — use `calc(100vh - <reserve>px)` with `unit: "raw"`. Without it, `paging` has no viewport to snap inside and nothing scrolls.
- `width: 100vw` makes the carousel ignore parent padding. To start at viewport x=0 (no left-edge gap), add a `marginLeft: -<rootHorizontalPadding>` via `prop:custom-css`.
- The web editor preview does **not** simulate touch swipe for paging stacks. Test on device or via "Preview → Open on device". Working on device ≠ working in web preview.

### Pages — each one a 100vw slide

```python
for i, page in enumerate(PAGES):
    page_stack = s.stack(carousel, axis="y", cross="stretch", main="center", gap="0px",
                         padding={"x": 20},
                         width=lit({"type": "css-length", "value": "100", "unit": "vw"}),
                         height=lit({"type": "css-length", "unit": "raw",
                                      "value": "calc(100vh - 420px)"}),
                         name=f"Page{i+1}")
    # minWidth keeps flex from shrinking the page
    s.records[page_stack]["properties"]["css:minWidth"] = lit({
        "type": "css-length", "value": "100", "unit": "vw"
    })
    s.text(page_stack, page["title"], size=28, weight="500",
           color_=ref_token("primary"), align="center", line_height=34)
    s.stack(page_stack, height=12)
    s.text(page_stack, page["desc"], size=15, weight="400",
           color_=ref_token("text"), align="center", line_height=22)
    s.stack(page_stack, height=20)
    hero_wrap = s.stack(page_stack, axis="x", main="center", cross="center")
    s.image_box(hero_wrap, hero_url, width=220, height=220, fit="cover", radius=20)
```

- Each page must have **width AND minWidth set to 100vw** so flex keeps them at full viewport width — without `minWidth`, flex shrinks them and you get a single-page that doesn't scroll.
- Page height matches the carousel's height (use the same `calc(...)`).
- `main="center"` vertically centers title/description/hero inside the slide.

**Sizing the reserve**: `calc(100vh - <reserve>px)` — the reserve is everything the carousel ISN'T (top safe-area + pill + dots + cards + CTA + links + bottom safe-area). For most layouts, **`calc(100vh - 420px)`** works on iPhone 14/15. iPhone SE may overflow — reduce hero size if so.

### Pagination dots — `indicator` node bound to `childPageIndex`

The paging stack auto-tracks its visible page index in
**`state:node.<carouselId>.childPageIndex`** — NOT `currentIndex`. The
SDK writes this state on every swipe.

Use a real `indicator` node (not manual conditional dots — the renderer
sometimes rejects manual dots with "Failed to get store url"). The
indicator needs **one** `indicator-item` child as a template; the SDK
iterates it `totalItems` times and exposes per-item `state:self.*`
booleans.

```python
indicator_id = s._new_node_id()
carousel_short = carousel.split(":", 1)[1]
indicator_state = f"state:node.{carousel_short}.childPageIndex"

# state record must exist in the store for the state-ref to validate
s.records[indicator_state] = {
    "locked": False, "derivation": None, "id": indicator_state,
    "defaultValue": {"type": "variable-number", "value": 0},
    "nonRemovable": True, "typeName": "state",
}

indicator_props = {
    "prop:indicator": lit({
        "type": "property-indicator",
        "currentIndex": {"type": "state-ref", "stateId": indicator_state},
        "totalItems": {"type": "literal", "value": len(PAGES)},
    }),
    "prop:stack": stack_property(axis="x", main="center", cross="center", gap="8px"),
}
s.records[indicator_id] = {
    "x": 0, "y": 0, "rotation": 0, "isLocked": False, "opacity": 1,
    "defaultProperties": indicator_props,    # MUST have both default + properties
    "properties": indicator_props,
    "meta": {}, "requiredRecordIds": [],
    "clickBehavior": {"type": "do-nothing"},
    "name": "Indicator", "type": "indicator",
    "index": s._next_index(dots_wrap),
    "parentId": dots_wrap, "props": {},
    "id": indicator_id, "typeName": "node",
}

# One indicator-item child — the dot template
item_id = s._new_node_id()
item_defaults = {
    "prop:stack": stack_property(axis="x", main="start", cross="center", gap="8px"),
    "css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius": length(999),
    "css:width": length(7),
    "css:height": length(7),
    "css:backgroundColor": {
        "type": "conditional",
        "options": [
            # state:self.isCurrent → true only on the active item.
            # DO NOT use state:self.isCompleted — that's progress-bar behavior
            # (cumulative fill up to currentIndex), not pagination dots.
            {"query": {"combinator": "and",
                       "rules": [{
                           "id": "indicator-current-rule",
                           "field": "state:self.isCurrent",
                           "operator": "=",
                           "valueSource": "value",
                           "value": {"type": "variable-boolean", "value": True},
                       }],
                       "id": "indicator-current-query"},
             "value": lit({"type": "css-color", "value": "#FFFFFF"})},
            {"query": {"combinator": "and", "rules": []},
             "value": lit({"type": "css-color", "value": "#FFFFFF40"})},
        ],
    },
}
s.records[item_id] = {
    "x": 0, "y": 0, "rotation": 0, "isLocked": False, "opacity": 1,
    "defaultProperties": item_defaults,
    "properties": {},
    "meta": {}, "requiredRecordIds": [],
    "clickBehavior": {"type": "do-nothing"},
    "name": "Indicator Item", "type": "indicator-item",
    "parentId": indicator_id, "index": "a0",
    "props": {}, "id": item_id, "typeName": "node",
}
```

### Indicator self-state cheat sheet

| `state:self.<name>` | When true | Use for |
|---|---|---|
| `isCurrent` | **only** on the active item | pagination dots (single highlight) |
| `isCompleted` | items whose index ≤ currentIndex | progress bar (cumulative fill) |
| `isFirst` | the first item | asymmetric corner radius (left side) |
| `isLast` | the last item | asymmetric corner radius (right side) |
| `isSelected` | items selected in multi-choice | quiz / survey UIs |
| `index`, `label`, `value` | item's numeric index / label / value | text bindings, computed conditions |

### Auto-state suffixes (mined from templates)

| Suffix | Owned by | Meaning |
|---|---|---|
| `childPageIndex` | paging x-stack | currently visible page (auto-written on swipe) |
| `currentIndex` | `navigation`, `indicator` | sequential nav step / indicator-controlled progress |
| `flowPosition` | `navigation` (some) | broader flow tracking |
| `canIncrementIndex` | indicator flow | next-button guard |
| `hasSelection`, `selectedValue`, `selectedValues` | `multiple-choice` | quiz answer state |
| `isOpen` | `drawer` | drawer open/closed |
| `value` | generic | custom state |

### Per-slide pill label (conditional on `childPageIndex`)

Citizen-style paywalls change the pill label per slide ("Family Safety" → "Offender Locator" → ...). Build it as a single conditional `prop:text` on the pill's text node, with one rule per page index:

```python
PILL_LABELS = ["Offender Premium", "Family Safety", "Offender Locator", ...]
options = []
for idx, label in enumerate(PILL_LABELS):
    options.append({
        "query": {"combinator": "and",
                  "rules": [{"id": f"pill-{idx}-rule",
                             "field": CAROUSEL_INDEX_STATE,   # state:node.<carouselId>.childPageIndex
                             "operator": "=", "valueSource": "value",
                             "value": {"type": "variable-number", "value": idx}}],
                  "id": f"pill-{idx}-query"},
        "value": lit({"type": "property-text", "value": label,
                      "rendering": {"type": "literal"}}),
    })
options.append({"query": {"combinator": "and", "rules": []},
                "value": lit({"type": "property-text", "value": "Default",
                              "rendering": {"type": "literal"}})})
s.records[pill_label_id]["properties"]["prop:text"] = {"type": "conditional", "options": options}
```

The pill auto-updates as the user swipes.

### Skip button visible only on the last slide

Conditional `css:display`:

```python
last = len(PAGES) - 1
s.records[skip_id]["properties"]["css:display"] = {
    "type": "conditional",
    "options": [
        {"query": {"combinator": "and",
                   "rules": [{"field": CAROUSEL_INDEX_STATE, "operator": "=",
                              "valueSource": "value",
                              "value": {"type": "variable-number", "value": last}}]},
         "value": lit({"type": "css-string", "value": "flex"})},
        {"query": {"combinator": "and", "rules": []},
         "value": lit({"type": "css-string", "value": "none"})},
    ],
}
```

DON'T use `animation: fadeIn 5s` for delayed Skip on swipable paywalls — the user might not have reached the value-prop pages yet. Last-slide-only is App-Store-compliant (Skip is reachable in seconds via swipe) and pushes through the funnel first.

### Don't use `navigation` for in-paywall swipe

`navigation` is for full-screen multi-step flows (intro → paywall →
upsell). Embedding it inside a paywall doesn't give you sticky top/bottom
unless you duplicate them on every page. Use a paging x-stack carousel
for swipable content within a single paywall.

### Reference layout

The full Citizen-style recipe is documented above. For composing the
whole swipable from scratch, follow this skeleton:

```python
s = Scratch(name="my_swipable_paywall", identifier="my_swipable_kit")
s.theme(background="#000", text="#FFF", primary="#YOURBRAND", ...)
s.product("primary",   "com.yourapp.trial_3day")
s.product("secondary", "com.yourapp.monthly_intro")

# state for default-selected card (must be in store, see App Store compliance)
s.records["state:products.selectedIndex"] = {
    "locked": False, "derivation": None, "id": "state:products.selectedIndex",
    "defaultValue": {"type": "variable-number", "value": 0},
    "nonRemovable": True, "typeName": "state",
}

root = s.root_stack(axis="y", cross="stretch", main="space-between",
                    padding={"top": 60, "x": 20, "bottom": 16}, ...)
top_group = s.stack(root, axis="y", cross="stretch", name="TopGroup")
bottom_group = s.stack(root, axis="y", cross="stretch", name="BottomGroup")

# header (pill + skip), carousel (paging), per-slide title/desc/hero,
# indicator (childPageIndex bound), bottom group (subtitle, cards, CTA, links)
# — see the patterns above.

snapshot = s.build()
ver = c.push_snapshot(paywall_id=PID, application_id=APP, snapshot=snapshot)
```

---

## Images

### Responsive hero sizing (works on iPhone SE → Pro Max)

`flex: 1 + height: 100%` doesn't render reliably in Superwall — `height: 100%` inside a flex parent often computes to 0. For responsive heroes, use **CSS `min()`** to clamp on multiple axes:

```python
s.image_box(hero_wrap, hero_url,
            width=lit({"type":"css-length", "unit":"raw",
                        "value":"min(300px, 72vw, 38vh)"}),
            height=lit({"type":"css-length", "unit":"raw",
                         "value":"min(300px, 72vw, 38vh)"}),
            fit="contain", radius=0)
```

The hero takes the smallest of:
- **300px** — max size on big phones
- **72vw** — caps on narrow screens (no horizontal overflow)
- **38vh** — caps on short screens (won't overflow vertical layout)

Adjust the vh number based on how much of the slide your hero should claim (35–45vh works for most layouts).

### Slide reserve math (for `calc(100vh - reserve)`)

Carousel height = `calc(100vh - <reserve>px)`. Underestimating the reserve = bottom of every hero clips behind the bottom drawer.

Reserve = **top safe-area + header row + spacing + bottom drawer total height**:
- Top: ~64px (safe-area-top + 16) + ~40px (pill row) = ~104
- Spacing pill→carousel: 20
- Bottom drawer (subtitle + cards + CTA + links + paddings): **~280-300px** in a Citizen-style layout
- Bottom safe-area: ~36

That puts reserve around **440px** for a Citizen-style layout. If the heroes are clipping, add 40-60 more to the reserve and reduce hero size — the slide is genuinely too short.

### Pattern: rectangle first, then fill
**Never** create an `<img>` and let its dimensions set the layout. Create
a fixed-size **stack**, fill its background with the image:

```python
hero_url = c.generate_and_upload_image(prompt, application_id=APP, ...)
hero_wrap = s.stack(root, axis="x", main="center", cross="center")
s.image_box(hero_wrap, hero_url, width=320, height=320, fit="cover", radius=12)
```

`fit="cover"` = aspect fill (crop overflow). `fit="contain"` = aspect fit (letterbox).

### Full-bleed image (escape root padding)
The root has horizontal padding. To go edge-to-edge or partial-bleed,
add negative margins on the wrap via `prop:custom-css`:

```python
s.records[hero_wrap]["properties"]["prop:custom-css"] = lit({
    "type": "property-custom-css",
    "properties": [
        {"type": "custom-css-property", "id": "action:hw01", "property": "marginLeft", "value": "-10px"},
        {"type": "custom-css-property", "id": "action:hw02", "property": "marginRight", "value": "-10px"},
        {"type": "custom-css-property", "id": "action:hw03", "property": "marginBottom", "value": "32px"},
    ],
})
```

### Image format gotcha
- **PNG** is reliable end-to-end (upload → render).
- **JPEG** uploaded successfully but the renderer wouldn't draw it. Convert with `sips -s format png input.jpg --out output.png`.
- **WebP** appears to work via the editor's manual upload path; safer to use PNG via API.

### Asset upload pipeline (what `upload_image_bytes` does internally)
1. **`assets.generateUploadInstructions`** with `{filename, byteSize, checksum (md5 base64), contentType, metadata: {lastModified: ms}, applicationId}` → returns `{instructions: {url, method, headers}, result: {url, contentType}}`. The `instructions.url` is a presigned S3 PUT URL valid for 5 min.
2. **PUT** the bytes to `instructions.url` with `Content-Type: <mime>`.
3. **`assets.create`** with `{applicationId, key, name, url (the public one from step 1), type:"image", mimeType, fileSize}`. The `key` is the filename portion of the public URL.

Final URL pattern: `https://user-content.superwalleditor.com/user-content/<key>[.ext]`.

### AI image generation — two paths

**The simple path** (no extra setup, recommended default):
1. Ask the user to drop an image into the chat (drag-and-drop a PNG/JPG into Claude Code, or paste a URL).
2. Upload to Superwall: `c.upload_image_bytes(bytes_or_path, application_id=APP, mime="image/png")` → returns a public CDN URL.
3. Drop the URL into `s.image_box(parent, url, width=..., height=..., fit="contain")`.

This is the path most users will take. They generate their own image in ChatGPT / Midjourney / Photoshop and pass it in.

**The Fal path** (optional, for when Claude itself should generate hero images):

Install once:
```bash
claude mcp add --transport http fal-ai \
  https://mcp.fal.ai/mcp \
  --header "Authorization: Bearer YOUR_FAL_KEY"
```
Restart Claude (`claude -c`) after install for the MCP tools to load.

**Three models that matter:**

| Model | Use for |
|---|---|
| `openai/gpt-image-2` (text-to-image) | Highest quality. Set `quality: "high"` (or `medium` for speed). 1024×1024. |
| `openai/gpt-image-2/edit` (image-to-image) | Same quality, takes a reference image (`image_urls`) so the new generation matches the reference's style. |
| `fal-ai/ideogram/v3/generate-transparent` | Native transparent PNG. Lower fidelity than gpt-image-2 — use only when you can't post-process. |
| `fal-ai/bria/background/remove` | Best background remover for premium 3D illustrations (cleaner than Superwall's `ai.removeBackground` or `fal-ai/imageutils/rembg`). |

**Recommended pipeline for paywall heroes:**

1. Generate via `openai/gpt-image-2` at `quality: "high"`. Add **green-screen instruction** to the prompt: "...on a SOLID PURE GREEN CHROMA KEY BACKGROUND (#00B140, uniform, for compositing). Subject CLEANLY SEPARATED from green bg, no green tint on the illustration."
2. Pass the result through `fal-ai/bria/background/remove` to subtract the green.
3. Upload the cutout to Superwall via `c.upload_image_bytes(...)`.
4. Use in `s.image_box(...)` with `fit: "contain", radius: 0` (transparent — no rect to round).

This is faster + sharper than asking Ideogram for "transparent background" directly, because gpt-image-2 produces better illustrations and Bria does great matting.

**OpenAI content-filter trigger words** (will return `"Downstream service error"`):
- "Sexual Assault" → use "Restricted Category"
- "offender warning" → use "alert" / "alert pin"
- Don't write actual victim/crime descriptions — keep prompts UI-mockup-style

If a job's status returns `COMPLETED` but the result endpoint 500s with `"Downstream service error"`, the prompt was content-filtered. Soften and resubmit.

**Submitting in parallel** (faster than sync `run_model`):
```python
mcp__fal-ai__submit_job(...)   # returns request_id
mcp__fal-ai__check_job(...)    # poll status, then action="result"
```
Submit all N jobs first, then poll. 5 high-quality jobs take ~60-90s in parallel.

**Image-to-image (style transfer)** — use the `edit` endpoint with a reference image as `image_urls: [<ref-url>]`. Prompt: "Reuse the SAME visual style as the reference image (...), but change the SCENE entirely. New scene: ..." Great for consistency across multiple slides.

### AI image generation — built into the toolkit
```python
url = c.generate_and_upload_image(
    "your prompt",
    application_id=APP,
    style="digital_illustration",   # or realistic_image, vector_illustration, icon
    sub_style="2d_art_poster",       # see full list below
    remove_bg=False,
    name="my-asset",
)
```

**Style × sub_style constraint**: `realistic_image` does NOT pair with `2d_art_poster`. If you get a 500 with "Style X and substyle Y can't be used together", switch sub_style or use `digital_illustration`.

**Sub-styles for `digital_illustration`** (mined from the AI Tools dropdown):
`2d_art_poster`, `2d_art_poster_2`, `engraving_color`, `grain`, `hand_drawn`, `hand_drawn_outline`, `handmade_3d`, `infantile_sketch`, `pixel_art`, `antiquarian`, `bold_fantasy`, `child_book`, `child_books`, `cover`, `crosshatch`, `digital_engraving`, `expressionism`, `freehand_details`, `grain_20`, `graphic_intensity`, `hard_comics`, `long_shadow`, `modern_folk`, `multicolor`, `neon_calm`, `noir`, `nostalgic_pastel`, `outline_details`, `pastel_gradient`, `pastel_sketch`, `pop_art`, `pop_renaissance`, `street_art`, `tablet_sketch`, `urban_glow`, `urban_sketching`, `vanilla_dreams`, `young_adult_book`, `young_adult_book_2`.

Naming convention: lowercase, spaces → underscores, `2D` → `2d`, "X 2" → `x_2`.

---

## Custom CSS (`prop:custom-css`)

For anything the grammar doesn't expose: absolute positioning, animations,
backdrop filters, env() safe-area, transforms, etc.

```python
s.records[node_id]["properties"]["prop:custom-css"] = lit({
    "type": "property-custom-css",
    "properties": [
        {"type": "custom-css-property", "id": "action:abc01",
         "property": "<camelCaseCssProperty>", "value": "<css value string>"},
        ...
    ],
})
```

Each property needs a unique `id` like `action:<short>` (id collisions across the snapshot are bad).

### Patterns we've shipped successfully
- **Safe-area padding**: `paddingTop = "max(calc(env(safe-area-inset-top, 0px) + 16px), 64px)"` — fallback ensures editor preview (where `env=0`) still has real padding.
- **Absolute positioning** for chips / buttons: parent gets `position: relative`, child gets `position: absolute` + `top/right/left/bottom` + optional `transform: translateX(-50%)` for centering.
- **BEST VALUE chip** floating over a card top edge: `position: absolute; top: -12px; left: 50%; transform: translateX(-50%); white-space: nowrap; width: max-content;`
- **Backdrop blur**: `backdropFilter: "blur(8px)"` + `webkitBackdropFilter: "blur(8px)"` (always set both for Safari).
- **Delayed fade-in (Skip button)**: `opacity: 0; animation: fadeIn 0.4s ease-out 5s forwards;` — relies on a `fadeIn` keyframe being defined globally by Superwall's runtime. Verified working.
- **CTA pulse**: `animation: pulse 2.4s ease-in-out infinite;` — `pulse` keyframe likely available.
- **Negative margins** to escape root padding (full-bleed images, sticky bottom): `marginLeft / marginRight: "-10px"` etc.
- **Letter spacing** for chip caps: `letterSpacing: "0.08em"`.

### Don't apply `prop:custom-css` to text nodes
Text nodes have a different schema for the property and the snapshot
push-test rejects it ("Cannot read properties of null reading 'accept'").
Apply it to a wrapping stack instead.

---

## Click actions

All wrapped in `{"type": "action-execution", "id": "action:<short>", "action": {<below>}}` and put inside `prop:click-behavior`'s `clickActions` list.

| Action | Shape |
|---|---|
| Purchase the selected product | `{"type": "purchase", "reference": {"type": "by-selected"}}` |
| Restore | `{"type": "restore"}` |
| Close / dismiss | `{"type": "close"}` |
| Open URL | `{"type": "open-url", "url": "https://...", "urlType": "in-app-browser"}` |
| Set selected product | `{"type": "set-product-index", "index": N}` |
| Set state var | `{"type": "set-state", "stateId": "state:...", "operation": {"type": "set"}, "value": {"type": "variable-...", "value": V}}` |
| Navigate page | `{"type": "navigate-page", ...}` |
| Custom in-app | `{"type": "custom-in-app", "data": "<key>"}` |
| Request permission | `{"type": "request-permission", ...}` |

`s.set_click(node, [...])` wraps the actions properly.

---

## Hard-coded knowledge (don't relearn)

### Endpoints
- **Create paywall**: `blitzMigration.paywalls.createPaywallV4` `{applicationId}` → `{paywall:{id}, redirectURL, versions}`
- **List paywalls**: `blitzMigration.paywalls.getPaywalls` `{applicationId, take, skip}` → `{paywalls, count, hasMore, nextPage}`
- **Get snapshot**: `paywalls.getLatestSnapshotByVersion` `{paywallId, version:"latest"}`
- **Prepare push**: `paywalls.prepareSnapshotForPromotion` `{paywallId, applicationId, snapshot, title:"", description:""}`
- **Promote push**: `paywalls.promoteFromSnapshot` `{paywallId, applicationId, snapshotIdentifier, title:"", description:""}`
- **List apps**: `blitzMigration.applications.getApplications` `{}`
- **AI image gen**: `ai.generateImage` `{prompt, style, subStyle}` → `{dataUrl}`
- **AI remove bg**: `ai.removeBackground` `{imageUrl}` → `{dataUrl|imageUrl|url}`
- **Asset upload step 1**: `assets.generateUploadInstructions` `{filename, byteSize, checksum, contentType, metadata, applicationId}`
- **Asset upload step 2**: PUT to `instructions.url` with the bytes
- **Asset upload step 3**: `assets.create` `{applicationId, key, name, url, type, mimeType, fileSize}`
- **List assets**: `assets.list` `{applicationId, type, limit}`

### Snapshot envelope shape
`push_snapshot()` expects `{store, schema}` flat — NOT wrapped in another `snapshot:` key. `Scratch.build()` returns the right shape.

### paywall record gotchas
- `templateType` must be `"GLOBAL"` or `"UNLISTED"` — `"PRIVATE"` is rejected.
- Each text node's `props.text` must exist (handled by `Scratch._put_node`).
- `css-font` value needs both `variant` AND `weight` set to the same string (handled by `font()`).
- `css:textAlign` value must be wrapped as `{type:"css-string", value:"left|center|right"}`.

### State name conventions
- Theme tokens: referenced as `state:style.interface.<name>` (without suffix); records exist with `.light` and `.dark` suffixes.
- Selected product: `state:products.selectedIndex`.
- Product price: `state:products.<key>.price` (where key = primary, secondary, tertiary).
- Product has intro: `state:products.hasIntroductoryOffer`.
- Device: `state:device.<field>` — locale, appVersion, daysSinceInstall, etc.

### Products
Must be REAL App Store / Play identifiers. `paywall_product:*` records require:
- `id`: `paywall_product:<key>` (key = primary, secondary, tertiary, or custom slug)
- `identifier`: actual SKU (e.g. `com.example.yearly`)
- `productVariables`: `{"source": "sdk"}`
- `store`: `"app-store"` or `"play-store"`
- Skipping product records works for design-only push, but the CTA's `purchase` action will no-op.

### Editor preview vs real device
- Editor preview always renders with `env(safe-area-inset-*) = 0`.
- Use `max(calc(env(...) + N), STATIC_FALLBACK)` to ensure both work.
- Some CSS animations may not play in the editor preview but do on device.

---

## Reference material on disk

- `docs/REFERENCE.md` — auto-generated SwiftUI/HTML-style reference, mined from 208 templates. Every node, property, value type, click action, font, icon, theme token. **Read first when designing.**
- `docs/SCHEMA.md` — narrative schema description.
- `docs/GOTCHAS.md` — running list of editor-crash causes.
- `data/grammar/*.json` — machine-readable grammar (composition, properties, fonts, icons, click_behaviors, conditional_operators, theme_tokens, layout_recipes).
- `data/fragments/` — 2231 reusable subtrees from real templates by purpose.
- `data/templates/*.json` — pulled live templates (`python3 scripts/pull_templates.py` to refresh).
- `scripts/build_test_paywall.py` — working from-scratch reference (the "Premium" screenshot).
- `scripts/build_test_paywall.py` — minimal from-scratch example (single-page paywall composed with primitives, validates, optionally pushes).

Refresh after pulling templates:
```bash
python3 scripts/mine_full_grammar.py && python3 scripts/mine_fragments.py
```

---

## Workflows

### "Build a paywall like this screenshot"
1. Look at the screenshot. Describe its sections.
2. `c.create_paywall(application_id=APP)` → get `pid`.
3. Compose with `Scratch` per Strategy A. Use `ref_token()` for every themable color so the user can re-theme later.
4. For images: generate with `c.generate_and_upload_image` OR ask the user to upload via the Superwall editor (the API upload occasionally has issues with the renderer; the editor's upload path always works).
5. `validate_snapshot()` — fix errors.
6. `c.push_snapshot()`. Share the editor URL.
7. Iterate based on user feedback. Always push to the same `pid` to keep version history.

### "Make my paywall match my iOS app's brand"
1. Find the user's iOS project (often at `../<appname>-iOS/` or similar).
2. Read `Theme.swift` / `OnboardingTheme.swift` / `Assets.xcassets/AccentColor.colorset` for accent + neutrals.
3. Pull or compose the paywall with those tokens via `s.theme(...)`.

### "Use my real products"
1. Pull an existing paywall in the same app: `c.get_snapshot(some_paywall_id)`.
2. Read the `paywall_product:*` records' `identifier` fields.
3. Plug into `s.product("primary", "<identifier>")`.

### "Wire restore + privacy + terms"
1. Pull any existing paywall: it'll have privacy/terms URLs in click actions.
2. Reuse those URLs with `{"type": "open-url", "url": "...", "urlType": "in-app-browser"}`.
3. Restore link uses `{"type": "restore"}`.

### "Add a delayed Skip button"
1. Place inside the same row as your top pill (or absolute on root).
2. Click action: `{"type": "close"}`.
3. CSS: `opacity: 0; animation: fadeIn 0.4s ease-out 5s forwards;` — the `fadeIn` keyframe is provided by Superwall's runtime.

### "Add live prices to product cards"
1. `s.text_liquid(card, "{{ products.primary.price }}/year", required_state_ids=["state:products.primary.price"], ...)`

### "Make the selected card visually toggle"
1. Build conditionals on the card's `css:borderColor`, `css:borderTopWidth;...`, `css:backgroundColor` that compare `state:products.selectedIndex` `=` `{type:"variable-number", value:N}`.
2. Set click action `{"type": "set-product-index", "index": N}`.

---

## Safety rules

1. **Always validate before push.** Refuse on `error`-level issues.
2. **Confirm substantial pushes.** Summarize changes; share editor URL; ask user to reload.
3. **Plain English summaries only** — never dump JSON at the user.
4. **A successful push doesn't mean it renders.** "Something's gone wrong" in the editor signals an unrecognized property or asset issue.
5. **403 on push** = wrong workspace. Re-auth.
6. **Don't touch existing paywalls the user said not to.** Always create new via `create_paywall`, or update only the specific `paywall_id` they named.

---

## Known limitations & open issues

- API image upload sometimes results in the renderer not displaying the asset on first push. Workaround: re-upload via the Superwall editor's image picker (manual) — this always works. The `assets.generateUploadInstructions` + S3 PUT + `assets.create` chain itself succeeds; the issue may be CDN propagation or asset-format quirks. PNG is most reliable.
- The `realistic_image` style only accepts a subset of sub-styles (not `2d_art_poster`).
- `prop:custom-css` on text nodes breaks push validation. Apply to wrapping stacks instead.
- The editor's preview doesn't simulate `env(safe-area-inset-*)` — always use `max(calc(env(...) + N), FALLBACK)`.
