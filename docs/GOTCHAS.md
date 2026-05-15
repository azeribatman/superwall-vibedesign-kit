# Gotchas & Field Notes

Things we learned the hard way, captured so you don't have to relearn them.
Read this *before* writing a builder script that touches a real paywall.

## API surface

### What works

- `paywalls.getLatestSnapshotByVersion` — pull (`{paywallId, version}`)
- `paywalls.prepareSnapshotForPromotion` — stage (`{paywallId, applicationId, snapshot, title, description}`)
- `paywalls.promoteFromSnapshot` — go-live (`{paywallId, applicationId, snapshotIdentifier, title, description}`)
- `applications.getApplication` — basic app metadata (`{applicationId}`)

### What doesn't (404 NOT_FOUND on every variation we tried)

These look obvious in `docs/METHOD.md` but the public tRPC surface rejects them:

- `paywalls.getPaywalls`, `paywalls.getPaywallsForApplication`, `paywalls.list`,
  `paywalls.getAll`, `paywalls.getMany`, `paywalls.get` — no working "list paywalls" endpoint
- `paywalls.createPaywall`, `paywalls.duplicatePaywall`, `paywall.create`,
  `paywalls.duplicate` — no working "create new paywall" endpoint
- `campaigns.getCampaignsForApplication`, `rules.getRulesForApplication`,
  `triggers.getTriggersForApplication` — no working campaign listing

**Practical implication:** to build a brand-new paywall, the user must
create the empty paywall record via the dashboard UI first (one click in
the sidebar), then we push the full snapshot via the API. There is no
fully automated "create from scratch" path.

### Required fields that error if missing/null

`prepareSnapshotForPromotion` will reject with:

- `HTTP 400 — title: Expected string, received null` → both `title` and `description` must be non-null strings on both `prepare` and `promote` calls.
- `HTTP 500 — At paywall(id = paywall:paywall).localizationProvider: Expected object, got null` → `paywall:paywall.localizationProvider` must be a full object. For workspace 7587 it's:
  ```python
  {
      'id': 'localization_provider:superwall:7587:default',
      'projectDisplayName': 'Default',
      'internalLocalizationProviderId': 7531,
  }
  ```
  (the `internalLocalizationProviderId` is workspace-specific — pull a
  known-good paywall and copy from there)
- `HTTP 409 — Some products are missing values` → every `paywall_product:*` record's `identifier` must be a real ASC product ID. The literal string `"missing"` (which is what fresh template paywalls have) is rejected. If you only need one product on the paywall, set the unused secondary/tertiary slots to the same valid ID as primary — they don't have to be visually rendered, they just have to exist.

## Schema quirks (v4)

### Valid action types (enum)

```
set-state, open-url, close, restore, purchase,
custom-in-app, custom-placement, request-store-review,
set-attribute, set-product-i…
```

`dismiss` is **NOT** a valid action type, even though we have a
`click_dismiss()` helper named that way. The actual close action is
`{type: 'close'}`. Schema error spells out the full list.

### Icon names are PascalCase

The icon set inside `prop:icon.name` is case-sensitive. Valid examples
seen in real templates:

```
X, Check, ChevronDown, ChevronLeft, ChevronRight, ChevronUp,
Plus, Minus, Star, Heart, Lock, …
```

Lowercase (`x`, `check`) is silently accepted at write time but **the
editor crashes with "Something's gone wrong"** when rendering them.
Always capitalize.

### Properties that crash the v4 editor

- `css:webkitLineClamp` — not in the v4 schema. The API accepts it but
  the editor's renderer throws on it. Use `lineSpacing` and let text
  flow naturally instead.

### Click behaviors live in `properties`, not the top-level field

Every node has a top-level `clickBehavior` field that defaults to
`{type: 'do-nothing'}`. **Setting it there does nothing.** The actual
behavior must go in `properties['prop:click-behavior']`. Pattern:

```python
node['properties']['prop:click-behavior'] = lit({
    'type': 'property-click-behavior',
    'clickActions': [{
        'type': 'action-execution',
        'action': {'type': 'close'},  # or set-state, purchase, …
        'id': action_id(),            # id on the wrapper, not the action
    }],
    'animation': 'none',  # or 'scale-in-out'
})
```

Action shape gotchas:

- `set-state` needs `operation: {type: 'set'}` and `value: {type: 'variable-number'|'variable-string'|…, value: …}`
- `purchase` needs `reference: {type: 'by-selected'}` (or `{type: 'by-product-id', productId: …}`)
- `open-url` needs `urlType: 'in-app-browser'` or `'external-browser'`

### Stack property values

- `axis`: `'x'` or `'y'` (NOT `'HORIZONTAL'` / `'VERTICAL'`)
- `wrap`: `'nowrap'` (string, not boolean)
- `scroll`: `'none'` or `'normal'` (string, not boolean)
- `gap`: `'<n>px'` string, not int
- `css-percentage` value needs `unit: '%'`
- `css-length` supports `vh`, `vw`, `px`, plus `'auto'` with `unit: 'none'`

### Liquid templates need the right rendering type

A text value that contains `{{ products.primary.price }}` must declare
`rendering: {type: 'liquid', requiredStateIds: [...]}` and list every
`state:<dotted path>` referenced. Plain strings use
`rendering: {type: 'literal'}`. Mixing them up means the placeholder
renders literally as `{{ ... }}` instead of the value.

### Conditional values

Wrap in a `'conditional'` object with options. **Each option's `value`
must itself be a literal wrapper** (`lit({...})`), not a raw value.
Catch-all option uses an empty `rules` list.

```python
{
    'type': 'conditional',
    'options': [
        {'query': {'combinator': 'and', 'rules': [rule_eq(...)], 'id': hash_id('q')[5:]},
         'value': lit({'type': 'css-color', 'value': '#ff0000ff'})},
        {'query': {'combinator': 'and', 'rules': [], 'id': hash_id('q')[5:]},
         'value': lit({'type': 'css-color', 'value': '#888888ff'})},
    ],
}
```

### Navigation state key

The state ID for the current navigation index is
`state:node.<navIdWithoutPrefix>.currentIndex`. The nav node's id is
`node:abc…` — strip the `node:` prefix when building the state ID:

```python
nav_short = nav_id.removeprefix('node:')
nav_index_state = f'state:node.{nav_short}.currentIndex'
```

Doubling the prefix (`state:node.node:abc.currentIndex`) silently fails.

## Layout traps

- **Side-by-side cards in a flex row:** `width=49%` + `gap=10px` +
  `mainAxisDistribution='space-between'` overflows the row by 4–6px,
  and centered text inside a card can spill past its border. Either
  drop to `width=48%` *or* stack vertically.
- **Safe-area top on iPhone:** put fixed top-bar buttons at
  `top: 58px` (not `14px`) to clear the notch / Dynamic Island. Then
  give the page content `paddingTop: 80` so the headline isn't hidden
  behind the bar.
- **Fixed footer pattern:** `position: fixed; bottom: 0; left: 0;
  right: 0; zIndex: 100`, with the page content `paddingBottom: ~220`
  so scrollable content doesn't hide behind the footer.
- **Horizontal padding via device-size token:** use a conditional
  whose default branch is
  `referential('state:style.deviceSize.padding')` rather than a fixed
  px value, so the paywall adapts across iPhone widths.

## Workflow: building a brand-new paywall

Because the create-paywall endpoint isn't reachable, the workflow is:

1. **Dashboard step (user)** — create an empty paywall (or duplicate
   any existing one) in the Superwall web UI, name it. Copy the
   numeric paywall ID from the URL.
2. **Script step (you)** — pull that paywall's snapshot, reset
   `paywall:paywall.name`, `featureGating`, `localizationProvider`, and
   the `paywall_product:*` identifiers, then build a fresh node tree
   (drop existing `node:*` records and add the new ones), and push
   with `prepare` + `promote`.

When writing the build script, mutate existing structures rather than
constructing records from scratch where possible — the gotchas above
(icon casing, action enum, click-behavior shape, conditional
wrapping) are easy to forget and the API will accept invalid inputs
that crash the editor on read.

## iOS SDK app review (effective 2026-04-28)

For consumers of `superwall-kit` who also ship an iOS app: Apple now
rejects every App Store upload that wasn't built with **Xcode 26 / iOS
26 SDK**. The deployment target (minimum iOS the user runs) is
independent and can stay at iOS 17 or 18. But the *build machine* must
have Xcode 26+. There is no flag, no waiver, no per-region exception.
This bites teams who use a dedicated build/CI machine with an older
Xcode.

## Subscription decline-chain pattern (iOS SDK 4.x)

If the consumer wants "user dismisses → next paywall opens
automatically" behavior, the SDK signals to listen for are:

- **`PaywallResult.declined`** in `PaywallPresentationHandler.onDismiss` —
  fires only when the user **manually closes the paywall** (taps the X
  button or drags-to-dismiss). Paywalls without a close button never
  fire this.
- **`SuperwallEvent.transactionAbandon`** in `SuperwallDelegate.handleSuperwallEvent` —
  fires when the user cancels the StoreKit purchase popup. The paywall
  stays on screen, so the chain handler must call
  `Superwall.shared.dismiss()` first, then re-register.
- **`PaywallInfo.closeReason == .forNextPaywall`** — Superwall is
  already auto-chaining (e.g., via editor-configured trigger-another-
  paywall action). Skip the manual re-trigger to avoid double
  presentation.

Cap the chain at ~4 re-presentations so a Winback paywall that
matches `decline_count >= 1` doesn't loop forever.

For single-shot paywalls used as fallbacks, match the paywall's
`name` (case-insensitive) against a token list and skip the
re-trigger when hit, so closing the fallback doesn't open another
paywall.
