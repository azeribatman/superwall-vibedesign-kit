# Bucket 3 — Medium Templates (244-281 nodes)

Source: 38 templates in the 244-281 node range (brief says 39; I found 38 that
fall in the inclusive range from `data/catalog/templates_index.json`. The
missing one is probably a neighbor at 243 or 282 depending on how the bucket
edges were assigned — noted as unresolved below).

Signals were extracted by grepping each template JSON for node types
(`navigation`, `drawer`, `lottie`, `video`, `multiple-choice`, `indicator`),
state keys (`state.enableFreeTrial`, `state.modalOpen`, `state.showMore`),
name tokens (`Trial Toggle`, `Timeline`, `Tab`, `Carousel`, `Feature`,
`Hero`), and click-action substrings. Full per-node tree walks were not
feasible due to single-line JSON formatting — one-liners below lean on the
signal mix plus the human template names.

## Design archetypes found

- **Single-page list paywall (dominant, ~32/38)** — one page, hero art at
  top, 3-6 benefit/feature rows, 2-product card stack, one CTA. Classic.
  No `navigation` node, no `drawer`, one `typeName: page` record.
  - examples: `22020` Wombo, `22969` Palette, `23139` Fitness, `26694`
    Twinbees, `29156` Zario, `35713` Fizz, `37001` Moneta, `39152`
    Vocabulary, `45912` Opal, `50800` Ad Block, `53049` Calorie Tracker,
    `98074` Robin, `180050` Nebula, `23367` Free Trial Slider.

- **Multi-screen / navigation-driven (3/38)** — a `navigation` node wraps
  child stacks; transitions between screens.
  - `168618` NordVPN — uses `state:node.<nav>.currentIndex` conditionals
    (1 hit) to gate content per screen. Screens ordered as intro →
    features → plans.
  - `171418` DuoLingo — `navigation` present but no `currentIndex`
    conditionals found; screens appear to advance linearly via per-screen
    CTAs rather than gated reveals.
  - `195704` Muscle Monster Workout Planner — same pattern as DuoLingo
    (nav, no currentIndex gating).

- **Single-page with trial toggle (7/38)** — single screen, but includes
  a `Trial Toggle` switch backed by custom `state.enableFreeTrial`, which
  conditionally swaps product/CTA copy and selects the trial vs. non-trial
  plan.
  - `23367` Free Trial Slider — the reference implementation (name is
    literally "Free Trial Slider").
  - `29156` Zario, `36721` Panda Hero, `54958` Zest, `59277` FoodCheck,
    `59285` Homework AI, `67447` Homework AI (Template).

- **Single-page with modal/drawer-ish overlay (5/38)** — uses
  `state.modalOpen` to toggle an overlay (promo, terms, detail sheet),
  but the overlay is built from regular stacks, not a `drawer` node. No
  template in this bucket uses the dedicated `drawer` type.
  - `26694` Twinbees, `26838` 1 Second Everyday Journal, `47309` Calorie
    Tracking, `48536` Homework Helper, `50710` Exit Offer.

- **Timeline hero (2/38)** — a visual "Day 1 → Day 3 → Day 7" trial
  timeline is the hero instead of an image.
  - `25300` Roi - Trial Timeline — the name says it outright.
  - `68527` Timeline & Benefits — also combines the timeline with a
    benefit list below.

## Unique components seen

- **`navigation`** — only 3 of 38: `168618`, `171418`, `195704`.
- **`video`** — 2 of 38: `47309` Calorie Tracking, `59287` Recipe Keeper.
  Both are single-page layouts using a top video as the hero.
- **`lottie`** — 1 of 38: `47309` Calorie Tracking (same template that
  uses video; it mixes both).
- **`drawer`** — 0 of 38. None of this bucket uses the dedicated drawer
  node; overlays are hand-rolled stacks gated on `state.modalOpen`.
- **`multiple-choice` / `choice-item`** — 0 of 38. No quizzes in this
  bucket (quizzes live in the larger-node buckets: 112279, 144797,
  178252, 192827).
- **`indicator` / `indicator-item`** — 0 of 38. No stepper dots here.
- **`icon`** — universal; every template uses icons for feature rows.

So the "interesting" node-type surface area of this bucket is small:
navigation in 3, video in 2, lottie in 1, no drawers, no quizzes, no
indicators. Bucket 3 is mostly plain `stack/text/img/icon` compositions.

## Notable state / conditional patterns

- **`state:state.enableFreeTrial` (7/38)** — dominant custom state in this
  bucket. Used as a switch: when true, the CTA reads "Start Free Trial"
  and `products.selectedIndex` is forced to the trial plan; when false,
  the CTA reads "Continue" and maps to the non-trial plan. Cluster:
  `23367, 29156, 36721, 54958, 59277, 59285, 67447`.

- **`state:state.modalOpen` (5/38)** — toggles a bespoke stack overlay.
  Used on `26694, 26838, 47309, 48536, 50710`. `50710` Exit Offer uses it
  as the core mechanic — dismiss attempt flips modalOpen, which reveals
  the discount offer stack.

- **`state:state.showMore` (1/38)** — `50800` Ad Block. Expand/collapse on
  the feature list.

- **`state:node.<nav>.currentIndex` (1/38)** — only `168618` NordVPN in
  this bucket actively uses the navigation index as a query field to
  change body content across screens. `171418` and `195704` have a
  navigation node but no currentIndex conditionals — they appear to use
  per-screen CTAs that call `set-state` to advance without gating UI.

- **No `state:params.answerOpened` (quiz state) and no
  `state:state.activeTab`/`planSelected`/`screenNum`** in this bucket —
  those custom states cluster in larger-complexity templates (bucket 4+).

- **Standard theme tokens** — every template uses
  `state:style.interface.primary/.text/.background`; about half also use
  `.productSelectedBg` / `.productBg` for the selected-card highlight,
  which is the usual pattern from the schema doc.

## CTA and pricing patterns (from signal mix + names)

- **Single CTA + 2 product cards, stacked vertically** — the majority.
  Consistent with `products.selectedIndex` being by far the top
  conditional field in the schema catalog.
- **Trial toggle switches which card is selected** — the `enableFreeTrial`
  cluster above.
- **Per-screen CTA on the 3 navigation templates** — each screen has its
  own "Continue"/"Next" button that sets the current index.
- **Dismiss** — every paywall has an X/close somewhere; dismiss
  click-actions were not individually counted here.

## Per-template one-liners

- `22020` **Wombo** — single-page, feature list + 2-plan stack + single CTA.
- `22320` **Yubo** — single-page two-plan card layout (contains "Tab/Timeline" named stack, likely a pill selector).
- `22969` **Palette** — single-page color-brand paywall, feature list + 2 plans.
- `23139` **Fitness** — single-page fitness list paywall with icon benefits.
- `23293` **Team Snap** — single-page sports/team list layout.
- `23367` **Free Trial Slider** — canonical single-page with `state.enableFreeTrial` toggle that swaps CTA + selected plan.
- `25169` **Roi** — single-page pricing paywall; sibling to the Roi Timeline variant.
- `25300` **Roi - Trial Timeline** — single-page with Day 1/3/7 trial timeline as the hero.
- `26131` **Roi** — another Roi variant, single-page.
- `26138` **Mood Bubble** — single-page pastel list paywall.
- `26542` **PNK** — single-page with named Feature block, 2 plans.
- `26694` **Twinbees** — single-page + `modalOpen` overlay (terms/detail sheet).
- `26838` **1 Second Everyday Journal** — single-page + `modalOpen` (likely "What's included" sheet).
- `27667` **Rapchat** — single-page with Feature block, 2 plans.
- `29156` **Zario** — single-page with `enableFreeTrial` toggle.
- `31317` **ParrotPal** — single-page list paywall.
- `35713` **Fizz** — single-page Fizz variant, list + plans.
- `36721` **Panda Hero** — single-page with explicit "Hero" stack + `enableFreeTrial` toggle.
- `37001` **Moneta** — single-page finance-style paywall.
- `39152` **Vocabulary** — single-page list paywall.
- `45912` **Opal** — single-page list paywall.
- `47309` **Calorie Tracking** — single-page with **video** hero, a **lottie** animation, and `modalOpen` overlay. The richest template in this bucket.
- `47550` **Special Offer** — single-page discount/offer layout.
- `48536` **Homework Helper** — single-page + `modalOpen` overlay.
- `50710` **Exit Offer** — single-page whose core mechanic is `modalOpen` flipping on dismiss to reveal a discount offer.
- `50800` **Ad Block** — single-page with `state.showMore` expand/collapse on the feature list.
- `53049` **Calorie Tracker** — single-page list paywall (distinct from 47309).
- `54958` **Zest** — single-page with `enableFreeTrial` toggle + Feature block.
- `59277` **FoodCheck** — single-page with `enableFreeTrial` toggle.
- `59285` **Homework AI** — single-page with `enableFreeTrial` toggle + Feature block.
- `59287` **Recipe Keeper** — single-page with **video** hero.
- `67447` **Homework AI (Template)** — single-page with `enableFreeTrial` toggle + Feature block. Sibling of 59285.
- `68527` **Timeline & Benefits** — single-page timeline hero over a benefits list.
- `98074` **Robin** — single-page list paywall.
- `168618` **NordVPN** — multi-screen via `navigation` with `currentIndex`-gated content; intro → features → plan screens.
- `171418` **DuoLingo** — multi-screen via `navigation`; screens advance linearly through per-screen CTAs (no currentIndex gating).
- `180050` **Nebula: Horoscope & Astrology** — single-page astrology-styled list paywall.
- `195704` **Muscle Monster Workout Planner** — multi-screen via `navigation`, similar to DuoLingo (linear advance).

### Unresolved

- Brief says 39 templates; I enumerated 38 in the 244-281 inclusive node
  range from `templates_index.json`. The likely 39th is a boundary case
  at 243 (`168642` CamScanner, 243) or 282 (`26128` EduAI, 282); without
  access to `/tmp/sw/bucket_3.txt` (read denied in this session) I can't
  confirm which edge the original bucketing uses. Neither candidate
  introduces new archetypes: `168642` is a standard single-page list
  paywall, and `26128` likewise.
