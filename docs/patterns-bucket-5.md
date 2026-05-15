# Bucket 5 — Large Templates (360–747 nodes by raw record count)

Scope: 40 templates from `/tmp/sw/bucket_5.txt`. Node counts below are
**only `typeName:node` records** (the index's node count also includes
state/style records, which is why e.g. Tiimo is 521 nodes here vs 747 in
the index).

## Design archetypes found

- **Conditional-tier selector (single page, state-driven toggles)** (~12)
  — One visual page whose content flips between product tiers using a
  custom boolean/enum state plus `state:products.selectedIndex`. No real
  navigation node is used (or it has 1 child). Users tap plan cards that
  fire `set-product-index` + `set-state` in the same click.
  - `174303` **Peloton** — `state.isMonthlySelected` drives a monthly/
    annual swap, 14 set-product-index clicks.
  - `178078` **LUDEX Sports Card Scanner** — `state.planSelected` drives
    25 conditionals across plan cards.
  - `187470` **Surfshark VPN** — `state.selectedPlanType` (Starter vs.
    One) flips 6 products between two tiers, period picker stays.
  - `201529` **Home Planner** — 9 products arranged as
    Personal/Plus/Pro × weekly/monthly/6-month, driven by
    `state.isPersonalSelected` + `state.isProSelected` plus
    `selectedIndex` (68 selectedIndex conds — biggest in the bucket).
  - `47317` **Club Pillar** — `state.activeTab` tab switcher over 6
    products.
  - `181568` **Grindr** — `state.isXtraSelected` tier flip, 6 products,
    no drawer.

- **Multi-page nav with explicit `currentIndex` paging** (~10) — real
  `navigation` node; pages gated by
  `state:node.<navId>.currentIndex` conditionals; CTAs fire
  `set-state` on that same stateId to advance. This is the Superwall-
  canonical multi-page pattern (the `ReCuE6cnEcUf-aU8BkDcZ` nav id is
  literally copy-pasted across the "Multi-Page | …" series).
  - `118403` **Multi-Page | Two Plans** — 3 pages, 16 currentIndex
    conds.
  - `119147` **Multi-Page | Single Plan + Exit Offer** — video + lottie
    + drawer + 17 currentIndex conds.
  - `134481` **Design Your Trial | Multi-Page** — trial-first flow, 17
    currentIndex conds, hasIntroductoryOffer gating throughout.
  - `138070` **Design Your Trial | Single Page** — same family but one
    page; currentIndex still used for a mini sub-flow.
  - `119152` / `119153` — single-page variants of the same family.

- **Onboarding quiz flow** (4) — multi-screen questionnaire whose
  answers persist as `state.question1..N` then funnel into a paywall
  page.
  - `144797` **Onboarding Questionnaire v2** — 8 pages (Page 1–7 +
    Paywall), 5 question states (`state.question1..5`), 46 set-state
    click actions, progress bar named "Bar (Edit my width)".
  - `192827` **Getting Started with Flows** — 11 pages including
    branched **Page 4A / Page 4B**, the only template in the bucket
    using real `multiple-choice` + `choice-item` + `indicator` nodes and
    `navigate-page` click actions. Also the only bucket member using
    `state:self.isSelected` (choice-item self ref).

- **Exit / cancellation survey → offer router** (2) — identical
  structure, different branding.
  - `178252` **Transaction Abandon Survey** / `193141` **Cancellation
    Recovery Template** — one `multiple-choice` with 6 branch pages
    (Page 1A…1F), each surfacing a different product (`exitOffer`,
    `extendedTrial`, `trialOffer`, or `primary`). Uses `state:self.value`
    on the choice-item to route, plus `set-attribute` (only seen in
    193141) to tag the user.

- **FAQ-accordion paywall** (5) — long scroll page where each FAQ row
  toggles open via `state:params.answerOpened`; usually paired with
  `state.showMore` for a features expander.
  - `34618` **Skill Yoga** (30× answerOpened), `36752` **Impact** (21),
    `26115` **Superwall** (39), `25640` **SuperApp** (72 — the biggest),
    `54098` **Mr. Arthur** (15). These are the `set-state`-heavy
    templates (30–81 set-state actions).

- **Video / hero-first pitch** (6) — hero is a `video` or `lottie`, CTA
  and plans below, few conditionals.
  - `24318` **Vixer** (1 video), `24852` **Video Background** (1 video),
    `20864` **Mojo (v1)** (**5 videos** stacked — probably a reel
    carousel), `85935` **Multi-page with video** (video + drawer +
    navigation).

- **Hybrid "showcase then plans" single page** (5) — no navigation but
  large node count driven by custom imagery/testimonials; just
  `selectedIndex` + maybe a `modalOpen` drawer.
  - `29642` **Flat**, `27665` **CoinStats** (biggest showcase at 257
    nodes, `state.showFeatures` toggle), `46406` **Rink**,
    `29339` **Mojo (v2)**, `178533` **Game Changer** (380 nodes, zero
    set-state — pure static marketing + selectedIndex).

- **Credit / consumable store** (1 — unique in bucket)
  - `43056` **Game On** — 5 credit products and a `state.creditTotal`
    counter used in 8 conditionals. Taps add to a running credit total
    before purchase; no subscriptions.

## Unique components seen

- `navigation` node with real multi-page children: 17 templates. Most
  common child count is 1–3; outliers: **144797** (8 pages),
  **192827** (11 pages, branched 4A/4B), **178252/193141** (7 pages,
  1 root + 6 survey branches).
- `drawer` nodes: 7 (174303, 85935, 65504, 119153, 119147, 187470,
  195712). Always toggled via
  `set-state:node.<drawerId>.isOpen`. Used for T&C / restore /
  "see all plans" overlays.
- `video` hero: 7 (24318, 24852, 20864, 85935, 118403, 119147, 134481,
  144797, 195712). **20864 Mojo** is the only one with 5 videos — a
  vertical reel/carousel.
- `lottie`: 3 (118403, 119147, 134481) — all in the "Design Your Trial
  / Multi-Page | Two Plans" family, used as a trial-countdown
  illustration.
- `multiple-choice` + `choice-item`: only `192827` (3 each — true quiz
  nodes) and `178252`/`193141` (1 each — exit survey). Everywhere else
  "quizzes" are faked with stacks + set-state.
- `indicator` + `indicator-item`: only `192827` (flows) and `186653`
  (PictureThis onboarding). These are the canonical pagination dots.
- `set-attribute` click action: only `193141` — tags user with the
  survey answer.
- `request-permission` click action: only `186653` PictureThis (push
  permission).
- `navigate-page` click action (vs. the commoner
  `set-state:…currentIndex` hack): only `192827`, `186653`, `178252`,
  `193141`. So the bucket splits cleanly into "modern navigate-page"
  users and "legacy currentIndex" users.
- `state:self.*`: only `192827` (`self.isSelected`) and `178252/193141`
  (`self.value`) — component-scoped state on choice items. Nice pattern
  for reusable selection UI.

## Notable state / conditional patterns

- **Custom enum toggles for plan tier** are everywhere instead of a
  single index: `state.isMonthlySelected` (174303), `state.planSelected`
  (178078), `state.selectedPlanType` (187470), `state.isXtraSelected`
  (181568), `state.isAnnualSelected` (178084), `state.isPersonalSelected`
  + `state.isProSelected` (201529, used together to pick one of 3
  tiers), `state.activeTab` (47317). These sit *alongside*
  `products.selectedIndex` rather than replacing it — the custom state
  decides which **tier** is visible and `selectedIndex` decides which
  **period** within the tier. Clever factoring: a 3×3 product matrix
  stays flat but reads as two independent selects.
- **`childPageIndex` (not `currentIndex`)** appears in 178079, 181568,
  178084, 195712 — seems to be a newer nav-index variable used by the
  editor's navigate-page action (vs. the legacy `currentIndex` set-state
  hack). Both coexist and both encode "which page is active."
- **`state:params.answerOpened`** is the canonical FAQ accordion key,
  always mirrored in the `set-state` handler on the row. 34618 Skill
  Yoga has 30 of these, 25640 SuperApp has 72.
- **`hasIntroductoryOffer` × `currentIndex` combo**: the Design Your
  Trial family (134481, 138070, 118403, 119147, 119153, 119152) gates
  ~15–22 conditionals on `hasIntroductoryOffer` *and* another ~4–17 on
  `currentIndex`, so a single template serves the "trial available" and
  "no trial" branches and also the multi-step flow. One template, four
  rendered states.
- **`state:device.viewPortHeight` responsive gating** is heavy in
  201529 (28 conds) and 186653 (8) — adaptive layout for short phones.
- **`state:device.interfaceStyle`** is heavily queried by 29339 Mojo
  (18 conds) even though theme tokens already handle light/dark — used
  to swap raster hero images per mode.
- **Tiimo (61133)** — the biggest (521 node-records) is surprisingly
  *stateless*: only 7 `state.showingFeatures` conds, 4 `showingAllPlans`
  conds and 6 `selectedIndex`. It's huge because it's a literal
  16-bullet feature list + per-plan "what's included" card stacks, not
  because of logic.

## Clever designer tricks

- **"One nav id to rule them all"**: 118403 / 119147 / 119152 / 119153 /
  134481 / 138070 all reference the *same* nav node id
  `ReCuE6cnEcUf-aU8BkDcZ` in their conditionals — Superwall's template
  family was clearly forked from a single source, and the currentIndex
  routing id was preserved across all of them. Anyone copy-pasting
  between them will collide if they're merged.
- **Branched quiz page naming** (`Page 4A` / `Page 4B` in 192827, and
  `Page 1A…1F` in 178252/193141) — a designer convention to show that
  two children of a nav are alternate paths, not sequential. The editor
  still orders by fractional index, but names encode the branch.
- **Two-axis product matrix via two booleans**: 201529 Home Planner
  uses `isPersonalSelected` + `isProSelected` to encode three tiers (if
  both false → "Plus"). With `selectedIndex` picking the period,
  9 products become a 3×3 grid driven by 3 state variables.
- **Surfshark's pricebook** (187470): six products split into "Starter"
  and "One" via `state.selectedPlanType`. The pattern keeps the period
  selector (`selectedIndex`) visually identical while swapping the
  underlying price text — a single layout renders two separate pricing
  tables.
- **Credit-store reuse of a subscription layout** (43056 Game On):
  reskins the standard "plan cards" layout but swaps in consumable
  IAPs; `state.creditTotal` increments across taps so the same button
  doubles as "add credits" and "buy" depending on the count.
- **FAQ accordions with shared key** (25640 SuperApp, 34618 Skill Yoga,
  54098 Mr. Arthur): every row mutates the same
  `state:params.answerOpened` — because it's scalar, opening any row
  auto-closes the previous. A one-line accordion controller.
- **Tier-detail drawer via `node.<id>.isOpen`** (65504, 174303, 85935,
  187470, 195712, 119153, 119147): not `state.*`, not `state.modalOpen`
  — a node-scoped `isOpen` variable lives on the drawer node itself, so
  multiple drawers in one page don't collide.
- **Hero "reel" with 5 videos** (20864 Mojo v1): 5 separate `video`
  nodes stacked inside a scroll stack as a vertical looping showcase —
  only template in the bucket with more than one video.
- **`state:self.value` on a choice-item** (178252/193141): rules read
  the component's own current value, so the same survey card template
  can light up differently depending on which answer it represents —
  the node is truly reusable instead of one-per-answer.
- **193141 is 178252 + one extra `set-attribute` action** — same 215
  nodes, same names. Designers cloned the survey and bolted on attribute
  tagging without touching the layout.

## Per-template one-liners

- `24318` **Vixer** — 45-node video-hero single plan, modalOpen T&C drawer, 2 products.
- `174303` **Peloton** — 140-node monthly/annual toggle via `isMonthlySelected`, drawer, 4 products.
- `29642` **Flat** — 163-node static marketing page, 3 products, modalOpen only.
- `23448` **Speak** — 151 nodes, dual "more info" expanders (`showMoreInfo`, `showMoreInfo2`), 3 products.
- `138070` **Design Your Trial | Single Page** — 119 nodes, 15 `hasIntroductoryOffer` conds gate trial vs. non-trial copy, shared nav id.
- `85935` **Multi-page with video** — 142 nodes, nav + drawer + video + `enableFreeTrial` switch, 4 products.
- `180048` **Essential - Healthy Lifestyle** — 81 nodes, 49 `selectedIndex` conds (very product-heavy for its size), 6 products.
- `34375` **Yuno** — 180 nodes, `state.changeToScreen` custom screen-router (scrolls instead of navigates).
- `118403` **Multi-Page | Two Plans** — 97 nodes, 3-page nav, video + lottie, shared `ReCuE6cnEcUf…` id.
- `119152` **Single-Page | Two Plans** — 97-node single-page sibling, same shared nav id.
- `144797` **Onboarding Questionnaire v2** — 174 nodes, **5-question quiz → paywall**, 46 set-state actions, progress bar.
- `65504` **Multi-page with offer** — 148 nodes, nav + drawer + video, `isChecked` + `enableFreeTrial`.
- `47317` **Club Pillar** — 93 nodes, `state.activeTab` tab switcher over 6 products.
- `46406` **Rink** — 156 nodes, `state.enableFreeTrial` toggle gates 12 conds, 4 products.
- `119153` **Single-Page | Single Plan + Exit Offer** — 112 nodes, drawer-based exit offer.
- `178078` **LUDEX Sports Card Scanner** — 107 nodes, `state.planSelected` gates 25 conds across 6 products.
- `24852` **Video Background** — 54-node sibling of Vixer, same modalOpen drawer.
- `34618` **Skill Yoga** — 248 nodes, 30-row FAQ accordion via `params.answerOpened`, `state.showMore`.
- `20864` **Mojo** — 88 nodes with **5 videos** — vertical reel + 2-plan picker.
- `119147` **Multi-Page | Single Plan + Exit Offer** — 126 nodes, video + lottie + drawer, 17 currentIndex conds.
- `27665` **CoinStats** — 257 nodes, `state.showFeatures` expander, huge static showcase.
- `178079` **DreamApp** — 201 nodes, `state.isChecked` + `enableFreeTrial`, uses `childPageIndex` (newer nav variable).
- `36752` **Impact** — 238 nodes, 21-row FAQ accordion.
- `43056` **Game On** — 85 nodes, **credit store** — 5 consumable IAPs with `state.creditTotal` counter.
- `192827` **Getting Started with Flows** — 268 nodes, **only real multiple-choice/choice-item/indicator template**, 11 nav pages with branched 4A/4B.
- `134481` **Design Your Trial | Multi-Page** — 138 nodes, the canonical "Design Your Trial" multi-page template.
- `26115` **Superwall** — 269 nodes, huge FAQ (39 answerOpened + 21 showMore), self-promo paywall.
- `186653` **PictureThis Onboarding Template** — 299 nodes, uses `navigate-page` + `request-permission` + `params.purchaseCompleted` — most modern click-action vocabulary in the bucket.
- `201529` **Home Planner - AI Room Design** — 137 nodes driving **9 products as a 3×3 tier×period matrix**, viewPortHeight responsive.
- `181568` **Grindr** — 244 nodes, `state.isXtraSelected` tier flip, uses `childPageIndex`.
- `178252` **Transaction Abandon Survey** — 215 nodes, **exit survey with 6 branch pages** routing to 4 different offer products via `self.value`.
- `193141` **Cancellation Recovery Template** — identical to 178252 + one `set-attribute` action to tag the user.
- `54098` **Mr. Arthur** — 306 nodes, 3 custom states, FAQ + feature expander + modal, 40 set-state actions.
- `29339` **Mojo (v2)** — 166 nodes, 18 `interfaceStyle` conds for light/dark raster hero swap.
- `25640` **SuperApp** — 374 nodes, **72-row FAQ accordion** (biggest in bucket), 81 set-state actions.
- `178533` **Game Changer** — 380 nodes but essentially **logic-less** (0 custom states, 0 set-state); pure marketing.
- `187470` **Surfshark VPN** — 295 nodes, `state.selectedPlanType` (Starter vs One) + drawer, 6 products in two tiers.
- `178084` **Flightradar24** — 383 nodes, Gold/Silver × yearly/monthly 2×2 matrix via `state.isAnnualSelected` + `childPageIndex`.
- `195712` **Fastic AI Food Calorie Scanner** — 379 nodes, nav + drawer + `childPageIndex`, nearly logicless layout-heavy.
- `61133` **Tiimo** — 521 nodes (the biggest) yet simple: `showingFeatures` / `showingAllPlans`, massive bullet / feature list.
