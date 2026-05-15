# Bucket 1 — Small Templates (124-204 nodes)

39 templates, the smallest in the catalog. Reconstructed from `templates_index.json`
by selecting all entries with `nodeCount` in [124, 204].

This bucket is overwhelmingly dominated by **single-page, single-screen paywalls**
with minimal state surface area. No drawers, lotties, multiple-choice, or indicators
appear anywhere in the bucket, and only one template uses real navigation.

## Design archetypes found

- **Single-page product picker** (34 of 39) — one static page: header/hero + value
  props + 1-3 product rows + CTA + footer links. Product selection is driven by
  the universal `state:products.selectedIndex` conditional (every single template
  in the bucket uses it). Trial copy swaps on `state:products.hasIntroductoryOffer`.
  Examples: `27894` SKAI Weather, `35530` CoinStats, `25513` Fitness AI,
  `26106` PocketShop Merchant, `51564` Black Friday.
- **Video-hero single-page** (4) — identical archetype to above but with one
  inline `video` node instead of a hero image. Examples: `31425` Scape,
  `50814` Wallpaper Maker, `54972` Arch iOS, `59270` Arch.
- **Multi-screen navigation** (1) — only `174299` Facetune uses a real
  `navigation` node (nav:1) with multiple pages. Everything else is flat.
- **Quiz / drawer / modal / stepper paywalls** — zero. These are exclusively in
  the larger buckets.

## Unique components seen

- `video` — 4 templates (Scape, Wallpaper Maker, Arch iOS, Arch). Used as a
  full-bleed looping hero behind the CTA stack.
- `navigation` — 1 template (Facetune).
- `icon` — common but unremarkable (dismiss X, check bullets, chevrons).
- Not seen at all in this bucket: `lottie`, `drawer`, `multiple-choice`,
  `choice-item`, `indicator`, `indicator-item`.

## Notable state / conditional patterns

- **Universal:** every one of the 39 templates uses both
  `state:products.selectedIndex` (to restyle the selected product row) and
  `state:products.hasIntroductoryOffer` (to switch CTA copy between "Start Free
  Trial" and "Continue" / "Subscribe").
- **Custom state (`state:state.*`):** almost entirely absent. No bucket member
  uses `enableFreeTrial`, `showMore`, `modalOpen`, `activeTab`, `screenNum`,
  `planSelected`, or `question*`. Designers rely purely on built-in product
  state for interactivity.
- **Navigation state (`state:node.<id>.currentIndex`):** zero usage — consistent
  with the bucket being flat single-page layouts. Facetune's navigation exists
  but the template does not gate other content on the current page index.
- **Theme tokens:** standard `style.interface.{text, primary, background,
  border, productSelectedBg}` usage; several also pull
  `style.deviceSize.{cornerRadius, padding}` for layout.
- **No `paywall_notification:TRIAL_STARTED`** records in any bucket-1 template —
  trial reminders are a feature of larger, more elaborate paywalls.

Takeaway: bucket 1 is the "minimum viable paywall" cohort. If you need a
reference for the cheapest viable layout — hero, value-prop list, 2-3 product
rows wired to `selectedIndex`, CTA, footer — pick any template from this bucket.

## Per-template one-liners

- `174299` **Facetune** — only bucket-1 template with a multi-page `navigation`
  container; otherwise a standard product picker.
- `174311` **Ultimate Guitar: Chords & Tabs** — image-heavy single page (6 imgs),
  small stack tree (25).
- `174380` **Life360** — icon-driven (no imgs) single page, 3 product rows.
- `23247` **Motivation** — minimal stack tree (20), short feature list, single CTA.
- `24741` **Visory** — img hero + 3-tier product list, no icons.
- `25341` **Fig** — img-heavy single page, text-dense (17 text nodes).
- `25513` **Fitness AI** — the smallest stack tree in the bucket (9 stacks),
  extremely flat single-page layout.
- `25762` **Zest** — balanced text + img mix (21/5), single page.
- `26106` **PocketShop Merchant** — gallery-style single page (7 imgs).
- `26986` **Fizz** — deepest stack nesting in bucket (58 stacks) despite only
  201 nodes; highly componentized single page.
- `27894` **SKAI Weather** — smallest template in bucket (124 nodes), icon-driven
  weather-themed single page.
- `27896` **Calorik** — img-led single page, 3 product rows.
- `28630` **Waking Up** — meditation-style single page, mostly imagery.
- `29609` **CoinStats** — text-heavy (20 texts) single page with 1 hero image.
- `29610` **CoinStats** (variant) — slightly larger sibling of 29609, same archetype.
- `29634` **Anime Waifu** — img-gallery single page.
- `30151` **Notability** — icon bullet-list single page (7 icons, 1 img).
- `30467` **Juiced** — img-heavy single page (7 imgs).
- `31425` **Scape** — video-hero single page with 1 inline `video`, icon chrome.
- `35530` **CoinStats** (smallest CoinStats) — 141 nodes, minimal single page.
- `37576` **Dreamy** — icon bullet-list single page, no imagery.
- `37925` **Perplexity** — icon-driven single page (8 icons, 14 texts).
- `39038` **Toonsutra** — text-dense single page (27 texts), 204 nodes.
- `39364` **New York Magazine** — editorial single page with 5 imgs, low
  unique-name count (12).
- `39779` **LazyBudget** — img-led single page.
- `43046` **Capture AI** — minimal icon single page.
- `45926` **Coin Stats - Halloween** — seasonal reskin of the CoinStats single
  page.
- `47144` **Hulah** — most text-dense in bucket (33 texts, 35 stacks), 30 unique
  names; approaches multi-section feel while staying single page.
- `47320` **AutoPaste** — img-led single page.
- `50814` **Wallpaper Maker** — video-hero single page, icon-heavy chrome
  (6 icons, 1 video).
- `51564` **Black Friday** — promotional single page, img-led.
- `54955` **LiftAI** — icon bullet-list single page (5 icons, 17 texts).
- `54972` **Arch iOS** — video-hero single page with 1 `video`, mirrors 59270.
- `59270` **Arch** — video-hero single page, sibling of 54972.
- `59402` **Voice AI** — icon-list single page (6 icons, 16 texts).
- `59582` **Soundmap** — unusual: *no* image or icon nodes, pure stack+text
  single page (20 stacks, 21 texts).
- `62186` **StepSaga** — img-heavy single page (10 imgs), deepest img count in
  bucket.
- `68528` **Discount Offer** — promotional single page with icon bullets.
- `77970` **Web2App Demo** — icon-heavy demo single page (30 stacks, 5 icons).
