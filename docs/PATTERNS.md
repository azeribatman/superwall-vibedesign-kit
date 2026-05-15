# Design Pattern Catalog

Synthesized from 5 parallel analyses across all 196 Superwall v4 templates
(see `patterns-bucket-[1-5].md` for per-bucket detail).

## TL;DR

The vast majority of "real" Superwall paywalls are single-page scrollers.
Multi-screen, quiz, drawer, and lottie/video features exist — but almost all
live in a small number of large, showcase templates. If you're rebuilding
any typical paywall, assume: one page, product list, big CTA, conditional
text based on `products.hasIntroductoryOffer`. Anything fancier is an
outlier.

## How the 196 templates break down by structure

| Archetype | Count (approx) | Examples |
|---|---|---|
| **Single-page product picker** | ~140 | Most of bucket 1-3; simplest form |
| **Single-page with custom state modals** | ~30 | `state.modalOpen` toggled in-page drawers |
| **Multi-screen w/ real navigation** | ~15 | Uses `navigation` node + `state:node.<id>.currentIndex` |
| **Multi-screen via `state.currentPage` (fake nav)** | ~5 | `24860`, `26860` (bucket 2) |
| **Tier toggle on top of product index** | ~8 | Surfshark, Flightradar24 Gold/Silver (bucket 5) |
| **Quiz flow (real)** | 2 | `184765` Blinkist, `192827` Flows |
| **Quiz flow (faked with stacks)** | 1 | `144797` (5 questions via `state.question1..5`) |
| **Exit survey router** | 2 | `178252`/`193141` route via `state:self.value` |
| **FAQ accordion** | 5 | All reuse scalar `state:params.answerOpened` |
| **Timeline-as-hero** | 2 | `25300` Roi, `68527` Timeline & Benefits |
| **Video hero carousel** | 2 | `20864` Mojo (5 videos), `25618` Mojo variant |
| **Credit-store** | 1 | `43056` Game On — running `creditTotal` counter |

## Native component usage (across all 196 templates)

| Component | Templates using it | Notes |
|---|---|---|
| `stack`, `text`, `img`, `icon` | 196 | Universal |
| `navigation` | ~24 | ≤13% of templates. Many wrap a single child (no real nav) |
| `video` | 9 distinct | Mojo (5 reel), Ladder, Scape, Wallpaper Maker, Arch (x2), Aesthetic, ReciMe, Calorie Tracking, Recipe Keeper |
| `drawer` (native) | 2 | Strava (171424), Ladder (184505 — 2 drawers) |
| `multiple-choice` + `choice-item` | 2 | Blinkist (184765), Flows (192827) |
| `lottie` | 2 templates | Calorie Tracking (47309), one other |
| `indicator` / `indicator-item` | 3 | Blinkist, Flows, Flat |

**Key insight:** designers overwhelmingly **fake native components**. "Drawers"
are almost always a plain stack toggled by `state.modalOpen`. Quiz questions
are stacks toggled by `state.question*` bools. Steppers are hand-built with
stacks and conditional opacity.

## Recurring custom state patterns

These are states designers invent themselves (not provided by the platform):

| State key | Used in | What it does |
|---|---|---|
| `state:state.enableFreeTrial` | ~10 templates | Custom trial toggle switch — swaps selected plan AND CTA copy |
| `state:state.modalOpen` | ~15 | Hand-rolled modal overlays |
| `state:state.showMore` | ~5 | Expand/collapse sections |
| `state:state.activeTab` | ~3 | In-page tab paywalls (Inkitt, Rapchat) |
| `state:state.planSelected` | ~2 | Alternative to `products.selectedIndex` (Captions) |
| `state:state.currentPage` / `screenNum` / `nextScreen` | ~5 | Fake multi-screen without navigation node |
| `state:state.question1..N` | ~4 | Quiz flow |
| `state:params.answerOpened` | 5 (FAQ cluster) | **Single scalar** shared across FAQ rows — opening one auto-closes previous |
| `state:state.segmentedControlIndex` | 2 | Monthly/Yearly pricing tabs |
| `state:state.endDate` | 1 | Countdown timer (73182) |
| `state:self.value` | 2 | Exit survey multi-select routing |
| `state:node.<id>.currentIndex` | ~15 | Navigation node's active page |
| `state:node.<id>.childPageIndex` | 2 | Carousel positioning (Prequel 168637) |

## Nav navigation idioms

Three distinct ways templates advance between "screens":

1. **`navigation` node + `set-state` on `currentIndex`** — the standard.
   Continue button has `clickBehavior` = `set-state action` setting
   `state:node.<navId>.currentIndex = currentIndex + 1`. Jump to a specific
   screen by setting the index to a literal.

2. **`navigate-page` action** — newer templates use a dedicated action type.
   `192827`, `186653`, `178252`, `193141`.

3. **Fake navigation with custom state** — no `navigation` node; a stack tree
   where each "page" has `css:display: conditional` on `state.currentPage`.
   Used by `24860`, `26860`, and a few bucket-5 templates.

**Blitz shortcut for rebuilding Alavai's "skip to screen 3":** use idiom 1
(set `currentIndex` to 2 from a click action) instead of wrapping pages in
conditional `css:display`.

## Product layout archetypes

| Pattern | Typical use |
|---|---|
| **Two cards side-by-side (Monthly \| Yearly)** | Dominant. ~70% of paywalls |
| **Stacked list** (radio-style rows) | Common for 3+ plans |
| **Single product** (no selection) | Minimalist ones in bucket 1 |
| **Pricing tabs** (`state.segmentedControlIndex`) | ~3 templates |
| **Tier × period matrix** (2D: Gold/Silver × annual/monthly) | Surfshark, Flightradar24, Home Planner, LUDEX, Grindr |
| **Toggle switch flips selected product** | Free-trial-slider pattern (`state.enableFreeTrial`) |
| **Discount upsell as a separate screen** | Bucket 5 cluster; presented after main paywall |

## Feature presentation patterns

| Pattern | Count | Notes |
|---|---|---|
| **Icon bullets list** (3-5 rows) | Majority | Icon container + text label |
| **Comparison table** (Free vs Pro) | ~15 | 2-column grid of features |
| **Carousel / slider reviews** | ~5 | Use `childPageIndex` or CSS transitions |
| **Timeline (Day 0 → Day N)** | ~5 | Roi, Timeline & Benefits, many free-trial templates |
| **Stacked testimonials** | ~10 | Static testimonial cards |
| **FAQ accordion** | 5 | Shared `answerOpened` scalar |
| **Video reel** (multiple videos stacked) | 2 | Mojo variants |

## Clever tricks worth stealing

1. **Single-scalar FAQ** (`state:params.answerOpened`) — instead of N
   booleans for N rows, store which row is open. Opening a row
   auto-closes all others. Elegant.

2. **Tier × period matrix** — split a 4-product grid into two independent
   state toggles instead of exposing all 4 as `products.selectedIndex`.
   Much cleaner UX, still maps to real products via conditional derivation.

3. **Exit-offer intercept** (`50710`) — uses `state.modalOpen` to
   intercept the dismiss gesture, showing a discount offer over the
   existing paywall. No new screen needed.

4. **Free-trial-slider toggle** (canonical: `23367`) — a single switch that
   both (a) changes `state.enableFreeTrial`, (b) flips selected product, and
   (c) rewrites the CTA copy via conditional text.

5. **Running counter credit store** (`43056` Game On) — tracks
   `state.creditTotal` across interactions, essentially turning the
   paywall into a tiny app.

6. **Conditional `css:display`** — the "hide this screen when no trial"
   trick we used for Alavai. Used ~12 places across templates (mostly for
   trial-conditional secondary screens).

7. **`css:transition` + state toggle** = free animations. Designers
   animate modals and accordion content just by toggling `max-height` in a
   conditional with a transition property.

## What's missing / not used

- **No templates use haptic feedback props** (there don't appear to be any)
- **Zero templates call `ai.generateImage`** at paywall time — AI endpoints
  are editor-only helpers, not runtime
- **Video node is underused** — only 9/196 templates
- **Real `drawer` node is almost unused** — people prefer hand-rolled modals
- **Only 2 templates use the native quiz components** — the rest fake it

## Takeaways for rebuilding any paywall

1. **Start from a real template that matches the archetype** — duplicating
   an existing snapshot via `duplicatePaywall` is cheaper than building
   from scratch.
2. **Use platform theme tokens religiously** — `state:style.interface.*`
   variables. Setting hard hex values breaks dark mode and defeats the
   theme system.
3. **For CTA-on-primary contrast**, use `state:style.interface.ctaText` if
   present, else set the button text to an explicit literal white.
4. **For multi-screen, prefer `navigation` + `set-state`** over fake
   `state.currentPage`. The navigation node has built-in transitions.
5. **For conditional content**, wrap values in `{type:"conditional"}` — you
   can switch on product state, device state, or any custom state. The
   operators cover everything short of arithmetic.
6. **For quiz flows**, use real `multiple-choice` nodes when possible (only
   2 templates do, but it's the clean way).
7. **Don't over-engineer custom state** — designers routinely cram 5
   different states into one paywall; start minimal and add as needed.
