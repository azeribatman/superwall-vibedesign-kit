# Bucket 2 — Small-Medium Templates (205-243 nodes)

Bucket identified by nodeCount range 205-243 (39 templates) — matches the size
band advertised for bucket_2.txt. Exact IDs listed below. The bucket file at
`/tmp/sw/bucket_2.txt` was outside the sandboxed read area, so membership was
recovered by filtering `data/catalog/templates_index.json` by the stated range
and the resulting set has exactly 39 entries.

## Design archetypes found

- **Single-page scroller with fixed footer CTA** (majority, ~28/39) — one
  vertically-scrolling page: hero / features / products / CTA, with a
  navbar stack + "Fixed Footer" stack pinned below. No real page transitions.
  - example: `174319` Gymverse — logo, accolades, header, bullet features list,
    two horizontal products, single purchase CTA, footer links
  - example: `171422` My Fitness Pal — hero image, title, 3 bullet lines,
    horizontal product cards, fixed footer button
  - example: `180058` 1Password — hero, "Save x%" label, two products, CTA
  - example: `187477` Fitbit — icon bullet stack, First Product/Second Product
    selectors, fixed footer
  - example: `33694` Hulu — icon bullet list, two pricing rows, feature grid
    (Top/Bottom columns)
  - example: `32970` MouseWait — Left Col / Right Col checklist, two product
    selector
  - example: `195702` Deezer — "Timeline" pattern (3 Timeline Items) + single
    product, next button
  - example: `23409` DocuSnap — Timeline item section + Picker with Product 2
  - example: `72708` Grok — icon bullets, Product 1 / Product 2, heading
  - example: `89173` Recorder Pro — icon bullet items, Primary / Product Group

- **Single-page + fake modal "drawer"** (~11/39) — uses a stack named
  "Drawer" / "Modal Drawer" / "Fixed Drawer" that is shown/hidden by a custom
  boolean state (no `drawer` node type). The stack holds supplemental
  product picker, feature bullets, or "View all plans" content.
  - example: `25718` Mimo — `state.modalOpen` toggles
    "Drawer with View All Plans button"
  - example: `25763`/`25764` Zest (two variants) — `state.modalOpen` on a
    Drawer stack holding secondary product + Middle/Right buttons
  - example: `36592` Yuno — `state.modalOpen` on "Modal Drawer" with
    "No payment" items
  - example: `65758` Flibbo — `state.showingOptions` toggles a Drawer with
    product options; has a dedicated "Hide Options Button"
  - example: `51128` Mindmod — "Fixed Drawer" housing all three product cards
  - example: `38393` Aesthetic — Drawer + `state.showMore` + `enableFreeTrial`
  - example: `26860` Planner 5D — two-Drawer/two-Navbar layout driven by
    `state.nextScreen` (swapping between "pages" without a real nav node)
  - example: `89173` / `27899` / `50216` / `59274` / `72708` — all contain a
    "Drawer" stack grouping the product picker or upsell content

- **Stepper/quiz-style multi-screen (single-page, state-driven)** (1/39) —
  no `navigation` node; instead uses a custom `state.currentPage` as the
  screen cursor and gates 14 conditional bindings by it.
  - example: `24860` Multi Page — explicit "Page 1" / "Page 2" / "Page 3" named
    stacks, Timeline Items, Left/Right buttons; all visibility conditionals
    read `state.currentPage`

- **Pricing-tabs / segmented control** (2/39) — a segmented-control row
  switches the visible plan without changing selectedIndex UI, via a custom
  index state.
  - example: `21386` Pixite — `state.segmentedControlIndex`
  - example: `29608` Pigment — `state.segmentedControlIndex`

- **Trial-toggle switch on single page** (5/39) — a "Free Trial Toggle" row
  drives `state.enableFreeTrial` and swaps pricing between trial / non-trial.
  - example: `23142` Planner5D
  - example: `168609` Picture This — toggle + `state.isChecked`
  - example: `168642` CamScanner — toggle + `state.isChecked`
  - example: `49392` StudyAI
  - example: `26860` Planner 5D (also stepper-like, double role)

- **Transaction-abandon / countdown offer** (2/39) — minimal single-page
  recovery template with heading, badge, countdown.
  - example: `73182` Transaction Abandon One-time Offer — uses
    `state.endDate` for a Countdown stack; only one product
  - example: `205050` Transaction Abandon | Extended Week — single product,
    badge + caption + heading + container, toggles `state.showLogo`

- **Review-carousel hero** (2/39) — horizontally paginated reviews using
  `state:node.<id>.childPageIndex` (the built-in scroll index of a stack
  with `snapPosition`), plus a row of "Indicator" dot stacks.
  - example: `168637` Prequel — 4 Review Containers, 4 Indicator dots,
    scroll state `node.761lLXeRfg3X-L1vvhPGl.childPageIndex`
  - example: `26698` Citizen — "Image Carousel" with 4 "Page Indicator" stacks
    (no explicit childPageIndex field in conditionals, so indicator is visual
    only or read via another mechanism)

- **Navigation node wrapping a single page** (several, e.g.
  `120295`, `168609`, `168642`, `171422`, `174319`, `180058`, `187477`,
  `187486`) — there *is* a `navigation:1` node but it has exactly one child
  stack named "Page 1" / "Page 0". The nav is a structural wrapper, not
  used for screen transitions. These are architecturally identical to the
  single-page scroller group; only the root node differs.

## Unique components seen

- **`video` node** — only 2 bucket members, both as a looping hero/background:
  - `38393` Aesthetic — "Video" named twice inside Background/Container stacks
  - `43227` ReciMe — a single video, likely an inline demo clip
- **`drawer` node (native)** — **zero** in bucket 2. All "Drawer"-named
  elements are plain `stack` nodes toggled by custom state.
- **`lottie`, `multiple-choice`, `choice-item`, `indicator`, `indicator-item`** —
  **zero** in bucket 2. Indicators are composed from small dot stacks.
- **`navigation` node** — present in the templates noted above but almost
  always wrapping exactly one page; bucket 2 does not contain any template
  with multiple navigation children (no real multi-screen routing).

## Notable state / conditional patterns

- **`state:state.modalOpen`** — the dominant custom state in the bucket.
  Used by `25718`, `25763`, `25764`, `36592` to show/hide the fake drawer.
  Read via `?` / `=` operators in conditionals that flip
  `css:display` or `css:opacity` on the Drawer stack.
- **`state:state.enableFreeTrial`** — free-trial toggle switch. Seen in
  `23142`, `38393`, `49392`, `168609` (paired with `state.isChecked`),
  `168642` (same pattern). Drives alternate pricing copy and
  sometimes which product is selected.
- **`state:state.showMore`** — expand/collapse longer feature list.
  `25313` Fizz, `38393` Aesthetic. Fizz also reads
  `state:params.answerOpened` (the only bucket template that touches
  the params namespace, suggesting a FAQ accordion).
- **`state:state.currentPage`** — pure state-driven multi-screen
  (`24860` Multi Page). No navigation node, 14 conditionals gate content
  blocks by integer equality.
- **`state:state.nextScreen`** — `26860` Planner 5D uses this + two Navbar
  stacks to fake screen-to-screen transitions.
- **`state:state.segmentedControlIndex`** — pricing tab selector in
  `21386` Pixite and `29608` Pigment.
- **`state:state.showingOptions`** — `65758` Flibbo, shows/hides product
  options with a dedicated Hide Options Button.
- **`state:state.isChecked`** — companion boolean for trial toggles,
  paired with `enableFreeTrial` in `168609`, `168642`.
- **`state:state.showLogo`** — `205050` toggles logo visibility
  (likely responsive trick on small screens).
- **`state:state.endDate`** — `73182` only; drives a Countdown stack.
- **`state:node.<id>.childPageIndex`** — built-in scroll index used by
  `168637` Prequel to pick the current review in a horizontal
  snap-scrolling stack. Only such reference in the bucket.
- **`state:device.viewPortHeight`** — read by `168609`, `168637`,
  `168642`, `171422`, `180058`, `187486`, `205050` for responsive
  tweaks (typically tightening spacing on short phones).
- **Product count distribution** — 2 products: 26 templates;
  3 products: 9 templates (`120295`, `187486`, `21386`, `23142`, `29608`,
  `27899`, `42871`, `51128`, `59274`); 1 product: 4 templates (`195702`,
  `205050`, `24860`, `73182`). The single-product templates are the
  countdown/abandonment and simple upsell variants.
- **Templates with zero custom state and zero conditional fields** —
  `29794` Green Noise, `33694` Hulu, `42871` Remote Control. These are
  fully static single-page layouts. Remarkable given the ~210-230 node
  sizes — the bulk is visual decoration, not interactivity.

## CTA / Navigation logic patterns

- **Single big "Fixed Footer" CTA** is universal. Almost every template
  ends with a node named "Fixed Footer" / "Footer" containing one
  purchase button. `click-behavior` is `purchase` on `products.selected`.
- **Per-product selector stacks** (`First Product`, `Second Product`,
  `Primary Selector`, `Secondary Selector`, `Tertiary Selector`) with
  `set-state` on `state:products.selectedIndex` are the norm.
- **Explicit dismiss button** — most have a "Left Button" / "Left Buttons"
  stack with a close/dismiss click action. Where a trial toggle exists,
  `set-state` flips `state.enableFreeTrial`.
- **No `open-url` observed at scan depth** in bucket 2, except likely in
  footer link stacks (`Footer Links`) that were not individually
  disassembled here.

## Per-template one-liners

- `120295` **GOSPEL** — single page in nav wrapper, 3-product stacked
  selector, trial-aware copy, no custom state.
- `168609` **Picture This - Plant Identifier** — nav+1 page, 2 products,
  trial toggle driven by `enableFreeTrial`/`isChecked`, bullets-with-tick
  feature list.
- `168637` **Prequel: Photo & Video Editor** — no nav node; horizontally
  paginated Review carousel + dot indicator using
  `node.<id>.childPageIndex`, 2 products.
- `168642` **CamScanner - PDF Scanner App** — nav+1 page, trial toggle
  (`enableFreeTrial`/`isChecked`), accolades row, icon bullets, 2 products.
- `171422` **My Fitness Pal** — nav+1 page, hero image, 3-line bullet
  block, horizontal 2-product selector, fixed footer.
- `174319` **Gymverse** — no nav node, logo + accolades + bullet features +
  2 horizontal products + footer links.
- `180058` **1Password** — nav+1 "Page 0", "Save x% label" badge, 2
  products, full toolbar/navbar/simple-navbar structure.
- `187477` **Fitbit** — nav+1 page, icon check list, First/Second Product
  cards, very simple single-page.
- `187486` **Yoga-Go** — nav+1 page, 3 products (monthly/yearly/quarter),
  horizontal products, trial copy.
- `195702` **Deezer** — no nav node, single-product upsell using 3
  "Timeline Item" steps, hasIntroductoryOffer gating.
- `205050` **Transaction Abandon | Extended Week** — single product, hero
  badge + caption + heading, `state.showLogo` toggle, trial reminder.
- `21386` **Pixite** — no nav, 3 products swapped via
  `state.segmentedControlIndex`, single Card layout.
- `23142` **Planner5D** — no nav, `enableFreeTrial` toggle row controls
  3 Selector stacks and purchase button.
- `23409` **DocuSnap** — no nav, Timeline Items list, Picker section with
  Product 2, minimal custom state.
- `24860` **Multi Page** — no nav node; pure state-machine multi-screen
  using `state.currentPage` integer over 3 Page stacks, 14 conditionals.
- `25313` **Fizz** — no nav, `state.showMore` + `params.answerOpened`
  (FAQ/expanding items), 5 content blocks, 2 products, Drawer stack.
- `25718` **Mimo** — no nav, `state.modalOpen` drives fake Drawer with
  "View All Plans" button, 2 products.
- `25763` **Zest** (variant A) — `state.modalOpen`, Timeline section,
  Middle/Right Button row, Drawer with View All Plans.
- `25764` **Zest** (variant B) — leaner Zest twin; same modalOpen Drawer
  pattern, fewer decorations.
- `26698` **Citizen** — no custom state, image carousel hero with 4
  "Page Indicator" dots, 2 products, Drawer stack.
- `26860` **Planner 5D** — `state.enableFreeTrial` + `state.nextScreen`;
  two Navbars + two Drawers simulate a 2-screen flow without nav node.
- `27899` **Scanner App** — no custom state, 3 products, Product Selector
  stack + Drawer, trial-days conditionals per product.
- `29608` **Pigment** — `state.segmentedControlIndex` pricing tabs,
  3 products, single Card layout (twin of Pixite).
- `29794` **Green Noise** — fully static, 2 products, bullet items list,
  Drawer stack, zero conditionals.
- `32970` **MouseWait** — no custom state, Left Col / Right Col checklist
  (7 Check Items), 2 product Selector stacks, Drawer.
- `33694` **Hulu** — fully static, 8 feature Items in two Top/Bottom rows,
  2 products, no custom state.
- `36592` **Yuno** — `state.modalOpen` fake Drawer, "No payment" items,
  image-heavy (15 imgs), 2 products.
- `38393` **Aesthetic** — has `video` node; `state.showMore` +
  `state.enableFreeTrial`, 4-col layout, Drawer/Overlay stacks.
- `42871` **Remote Control for All TV Plus** — fully static, 3 products,
  bullet list + Gradient + Drawer, no custom state.
- `43227` **ReciMe** — has `video`, Imports Section, icon bullets,
  2 pricing rows, Drawer, Mask element.
- `49392` **StudyAI** — `state.enableFreeTrial` toggle, 4 Items feature
  list, 2 products, Drawer.
- `50216` **IQ Masters** — 7 icons, 3 Items, 2 products, Drawer, standard
  trial conditionals, no custom state.
- `51128` **Mindmod** — 3 products inside a "Fixed Drawer" stack, Left/Right
  bullets, no custom state.
- `55035` **Coursology** — heavy on imgs (19), static 2-product layout with
  stars/reviews, Check 1..4 items, no custom state.
- `59274` **Billio** — 3 products in Feature/Divider rows, Drawer, trial
  conditionals per product.
- `65758` **Flibbo** — `state.showingOptions` drives a full-page options
  Drawer with explicit Hide Options Button; 2 products.
- `72708` **Grok** — 9 icons, Product 1 / Product 2 in a Picker Container,
  Fixed Footer, standard trial conditionals.
- `73182` **Transaction Abandon One-time Offer** — countdown template,
  `state.endDate`, 1 product, Offer badge, Close Button.
- `89173` **Recorder Pro (Web Checkout Link)** — 11 icons, 3 Item bullets,
  Primary / Product Group in a Drawer, no custom state.
