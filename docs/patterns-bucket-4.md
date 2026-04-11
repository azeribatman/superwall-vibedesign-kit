# Bucket 4 — Medium-Large Templates (282-359 nodes)

Source: 39 templates with `nodeCount` between 282 and 359 inclusive, taken
from `data/catalog/templates_index.json`. Per-file signal extraction was
limited by the single-line JSON format (no practical tree walks), so
archetype assignment relies on:

- nodeTypes mix in the catalog (presence of `navigation`, `drawer`,
  `video`, `lottie`, `multiple-choice`, `choice-item`, `indicator`);
- occurrence greps for `"type": "navigation|drawer|multiple-choice|video|
  lottie|indicator"` across each JSON;
- state-key greps: `currentIndex`, `state:state.enableFreeTrial`,
  `state:state.modalOpen`, `state:state.showMore`, `state:state.activeTab`,
  `state:state.planSelected`, `state:state.screenNum`, quiz keys;
- the human template name from the catalog.

Counts: 9 templates have a `navigation` node, 2 have `drawer`, 2 have
`lottie`, 7 have `video`, 1 has `multiple-choice`/`choice-item`, 1 has
`indicator`. The remaining 27 are single-page at this node count — i.e.
the bigger page budget is spent on denser content, not additional screens.

## Design archetypes found

- **Single-page content-heavy paywall (~24/39)** — one page, no
  navigation/drawer, but 30-50 text nodes and rich imagery build out
  several "sections" in a single scroll: hero, feature bullets, testimonial
  strip, comparison/timeline, pricing cards, CTA, footer links.
  - `168635` Cleaner Guru — 284 nodes, stack+text+img only, uses
    `state.enableFreeTrial` trial toggle.
  - `171426` Onhunt — 283 nodes, single page, custom state drives small
    reveals.
  - `171431` Hily Dating — 311 nodes, image-heavy (icons+imgs), no
    navigation.
  - `178080` Captions — 292 nodes, custom `state.planSelected` acts as an
    in-page pricing toggle (two plan chips, no page switch).
  - `201521` FaxFree — 327 nodes.
  - `201530` Freeletics — 288 nodes.
  - `22812` Sharpen — 285 nodes, icon-rich feature grid.
  - `23125` Mimo — 294 nodes, has `state.showMore` (expand/collapse) and
    `state.enableFreeTrial`.
  - `23443` Outside — 314 nodes, large image gallery, trial toggle +
    modalOpen.
  - `24606` TikMaker — 321 nodes, in-page modal via `state.modalOpen`.
  - `24939` Yubo — 310, mostly stacks+img+text.
  - `24940` Yubo — 315, image-heavy variant.
  - `26697` Citizen — 346 nodes, 108 stacks (deepest nesting in bucket),
    no extra types.
  - `29641` Flat — 315 nodes, icon+img+text feature matrix.
  - `33698` Lens Buddy — 305 nodes, trial toggle + modalOpen.
  - `34775` Exit Popup — 285, uses modalOpen (a self-modal / exit offer
    inside a single page).
  - `35716` Fig — 301, modalOpen.
  - `38697` Fizz — 292, img-heavy (24 imgs), stack+text only.
  - `45273` Inkitt — 334 nodes, uses `state.activeTab` → in-page tabs
    (see "Tabs" pattern below).
  - `50100` Black Friday — 300, promo layout.
  - `50211` Mobile Security — 353, trial toggle, 42 imgs (icon/badge
    grid).
  - `50855` Luxe Wallpapers — 287, image grid.
  - `54171` Rapchat — 343, uses `state.activeTab` → tabs.
  - `54964` Hulah — 330 nodes, icon+text feature list.
  - `65472` Earth.fm — 315 nodes.

- **Multi-screen navigation paywall (6/39)** — a `navigation` node plus
  active use of `state:node.<nav>.currentIndex` for per-screen gating /
  next-page CTAs.
  - `108850` Snapchat — 305 nodes, navigation + currentIndex; Snapchat-
    style 2-3 intro screens then plans.
  - `112279` Onboarding Questionnaire — 358 nodes, navigation + inline
    `video` hero + custom state keys matching question/screen patterns
    (quiz-lite flow: questions gate the final plan screen).
  - `119449` Sports Betting — 355 nodes, navigation + `lottie` hero,
    currentIndex gating.
  - `184505` Ladder Onboarding Template — 316 nodes, navigation + inline
    `video` + **two `drawer` nodes** (terms + confirm drawer) + icon-
    heavy content. The most structurally rich template in the bucket.
  - `184765` Blinkist Onboarding Template — 330 nodes, navigation +
    **`multiple-choice`×3 / `choice-item`×3 / `indicator`** stepper — the
    only true quiz-flow paywall in bucket 4. Uses custom `state.state.*`
    question keys and `currentIndex` to advance.
  - `77260` Duolingo — 309 nodes, navigation + `lottie` hero icon;
    multi-screen with currentIndex gating.

- **Navigation node present but not programmatically switched (3/39)** —
  `navigation` exists in nodeTypes, but no `currentIndex` set-state
  actions were found, suggesting a single visible page or purely
  visual/transition use.
  - `171424` Strava — navigation + `drawer` (info / upsell drawer). The
    drawer, not page switching, is the dynamic bit.
  - `180053` Scenic Motorcycle Navigation — navigation wrapper, custom
    state drives reveals rather than currentIndex.
  - `195720` Surfline — navigation wrapper, 96 stacks (deep content),
    currentIndex not hit.

- **In-page tab paywall (2/39)** — single page, but with a `state.activeTab`
  custom state used to swap what pricing / feature block is visible
  (equivalent to a tab bar).
  - `45273` Inkitt
  - `54171` Rapchat

- **Quiz-flow paywall (1/39)** — multiple-choice + choice-item + indicator
  + navigation + question state.
  - `184765` Blinkist Onboarding Template (already listed above) — 3
    question screens with pip indicator, then pricing.

- **Video-hero paywall (7/39, overlapping other archetypes)** — at least
  one inline `video` node used as hero/background:
  - `25618` Mojo — 302 nodes, **5 video nodes** (video carousel / rotating
    feature showcase — very unusual count).
  - `24932` PiCal — 316 nodes, 1 video.
  - `26128` EduAI — 282 nodes, 1 video, 21 imgs.
  - `36754` Harmony Calories — 319 nodes, 1 video.
  - `36761` Unscripted — 292 nodes, 1 video.
  - `112279` Onboarding Questionnaire — inline video inside quiz-lite.
  - `184505` Ladder — hero/section video.

## Unique components seen

- `navigation` — 9/39 templates. Actively switched via `currentIndex`
  set-state in only 6 of them; the other 3 (`171424` Strava, `180053`
  Scenic Moto, `195720` Surfline) appear to use the navigation wrapper
  as a container/transition shell, not a driven flow.
- `drawer` — 2/39: `171424` Strava (one drawer), `184505` Ladder (two
  drawers). In both cases the drawer hosts an exit-offer / terms /
  details sheet triggered from a button in the main flow.
- `multiple-choice` + `choice-item` — 1/39: `184765` Blinkist
  Onboarding. Three question/answer groups in a quiz flow.
- `indicator` + `indicator-item` — 1/39: `184765` Blinkist Onboarding
  (stepper dots for the quiz progress).
- `lottie` — 2/39: `119449` Sports Betting (hero lottie), `77260`
  Duolingo (icon/lottie accent).
- `video` — 7/39, max 5 videos in a single template (`25618` Mojo — the
  5-video feature carousel is the bucket's most unusual use).

## Notable state/conditional patterns

- `state:node.<navId>.currentIndex` — 6 bucket-4 templates drive multi-
  screen flows with conditional set-state actions on next/back buttons:
  `108850`, `112279`, `119449`, `184505`, `184765`, `77260`.

- `state:state.enableFreeTrial` — trial toggle switch on single-page
  templates: `168635` Cleaner Guru, `33698` Lens Buddy, `23443` Outside,
  `23125` Mimo, `50211` Mobile Security (5/39).

- `state:state.modalOpen` — in-page modal/popover without using a
  `drawer` node (overlay done with conditional visibility on a stack):
  `24606` TikMaker, `36754` Harmony Calories, `35716` Fig, `34775` Exit
  Popup, `33698` Lens Buddy, `26128` EduAI, `25618` Mojo, `24932` PiCal,
  `23443` Outside (9/39). This is the dominant "fake drawer" technique
  at this size — much more common than the real `drawer` node.

- `state:state.activeTab` — in-page tab switcher: `45273` Inkitt,
  `54171` Rapchat.

- `state:state.showMore` — expand/collapse reveal: `23125` Mimo.

- `state:state.planSelected` — custom two-plan selector (parallel to
  `products.selectedIndex`, used when the designer wanted the data bound
  to a named state): `178080` Captions.

- Quiz / multi-step state — `state:state.*` question/screen keys:
  `112279` Onboarding Questionnaire (custom per-question state, even
  though it lacks `multiple-choice` node type — implemented with plain
  stacks + set-state), and `184765` Blinkist (uses real multiple-choice
  nodes plus custom state).

- Trial toggle + modalOpen combo — `33698` Lens Buddy and `23443`
  Outside both layer a trial toggle with an in-page "how the trial
  works" modal.

## Per-template one-liners

- `108850` **Snapchat** — 305n, nav + currentIndex, multi-screen Snapchat-
  styled intro → plans flow.
- `112279` **Onboarding Questionnaire** — 358n, nav + inline video +
  custom question state, quiz-lite onboarding with a video hero.
- `119449` **Sports Betting** — 355n, nav + lottie hero + currentIndex,
  themed multi-screen betting pitch.
- `168635` **Cleaner Guru: Clean Up Storage** — 284n, single page w/
  trial-toggle (`enableFreeTrial`), no navigation despite size.
- `171424` **Strava** — 321n, nav (container-only) + drawer sheet for
  upsell/terms + custom state.
- `171426` **Onhunt** — 283n, single page, small custom state reveals,
  icon-bullet features.
- `171431` **Hily Dating** — 311n, dense single-page with icon rows and
  photo blocks.
- `178080` **Captions: AI Short-Form Video** — 292n, single page w/ a
  named `state.planSelected` two-plan toggle instead of `selectedIndex`.
- `180053` **Scenic Motorcycle Navigation** — 359n, navigation wrapper
  + custom state (no currentIndex gates).
- `184505` **Ladder Onboarding Template** — 316n, nav + inline video +
  **two drawers**, the most structurally rich template in the bucket.
- `184765` **Blinkist Onboarding Template** — 330n, the **only true
  quiz-flow paywall**: nav + 3× multiple-choice + choice-item + indicator
  stepper + question state.
- `195720` **Surfline: Wave & Surf Reports** — 324n, nav (container
  only), 96 stacks of layered content and icon lists.
- `201521` **FaxFree: Send Fax From iPhone** — 327n, single-page dense
  content paywall.
- `201530` **Freeletics: Workouts & Fitness** — 288n, text-heavy single
  page with custom state.
- `22812` **Sharpen** — 285n, single-page with large icon-bullet feature
  grid (7 icons).
- `23125` **Mimo** — 294n, single page with `showMore` expand section and
  `enableFreeTrial` toggle.
- `23443` **Outside** — 314n, image gallery + trial toggle + modalOpen
  in-page info modal.
- `24606` **TikMaker** — 321n, single page w/ `modalOpen`-driven popover.
- `24932` **PiCal** — 316n, single page with inline video + modal.
- `24939` **Yubo** — 310n, stack+img+text only.
- `24940` **Yubo** — 315n, image-heavy variant (19 imgs).
- `25618` **Mojo** — 302n, **5 videos** (rotating feature carousel),
  modalOpen for info popover — unique in bucket 4.
- `26128` **EduAI** — 282n, video hero + modalOpen.
- `26697` **Citizen** — 346n, 108 stacks, deepest nested content layout
  in the bucket, no nav/drawer/video.
- `29641` **Flat** — 315n, icon + image feature matrix single page.
- `33698` **Lens Buddy** — 305n, trial toggle + modalOpen "how it works"
  popover.
- `34775` **Exit Popup** — 285n, single page whose `modalOpen` state
  drives an in-page exit-offer overlay.
- `35716` **Fig** — 301n, single page w/ modalOpen popover.
- `36754` **Harmony Calories** — 319n, single page w/ inline video and
  modalOpen.
- `36761` **Unscripted** — 292n, video-hero single page.
- `38697` **Fizz** — 292n, 24 imgs, stack+text+img single page.
- `45273` **Inkitt** — 334n, **tab paywall** via `state.activeTab`.
- `50100` **Black Friday** — 300n, promo layout single page.
- `50211` **Mobile Security** — 353n, 42 imgs (badge/shield grid), trial
  toggle.
- `50855` **Luxe Wallpapers** — 287n, wallpaper grid single page.
- `54171` **Rapchat** — 343n, **tab paywall** via `state.activeTab`.
- `54964` **Hulah** — 330n, icon-rich feature list single page.
- `65472` **Earth.fm** — 315n, single page, custom state accents.
- `77260` **Duolingo** — 309n, nav + lottie + currentIndex multi-screen.

## Caveats

- "Multi-screen" vs "navigation container only" is inferred from the
  presence of `set-state` actions targeting `state:node.<id>.currentIndex`.
  A template could in principle use other mechanisms (e.g. scroll
  snapping inside the navigation) without that signal — I've flagged
  those as "container-only" but they may still be multi-screen visually.
- Exact page counts inside a navigation node were not extractable
  because each template JSON is one line and too large for Read to slice.
- Pricing layout (cards vs stacked vs single) could not be determined
  from node-type counts alone; the per-template one-liners describe
  hero/state traits rather than pricing UI.
