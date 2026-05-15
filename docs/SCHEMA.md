# Paywall Snapshot Schema

Reverse-engineered from 196 v4 templates. See `data/catalog/` for raw data.

## Top-level shape

```
snapshot = {
  "store": { <recordId>: <record>, ... },   # ~300-400 records per paywall
  "schema": { ... }
}
```

Each record's id is namespaced: `paywall:paywall`, `page:page`,
`node:<hash>`, `state:<path>`, etc. The type is in `typeName`.

## Record types (`typeName`)

| typeName | Purpose |
|---|---|
| `paywall` | Top-level paywall config (name, identifier, presentation style) |
| `document` | Editor document metadata (gridSize, etc.) |
| `page` | A page in the paywall (usually just one; multi-screen uses navigation children) |
| `node` | Visual elements — stacks, texts, images, icons, etc. |
| `state` | State variables (products.*, device.*, style.interface.*, custom state) |
| `style_variable_group` | Theme groups (interface tokens, device size tokens, theme modes) |
| `paywall_product` | Product references attached to the paywall |
| `paywall_notification` | Trial reminders and similar push notifications |

## Node types (from 196 templates)

| type | Count | Notes |
|---|---|---|
| `stack` | 10,524 | Flex container — the building block of every layout |
| `text` | 6,028 | Text element with `prop:text` + css font/color |
| `img` | 1,520 | Static image (`prop:image`) |
| `icon` | 998 | Icon (`prop:icon`) — separate type from img |
| `navigation` | 40 | Multi-screen container. Children = pages. |
| `video` | 32 | Inline video (`prop:video`) |
| `drawer` | 10 | Slide-up drawer (`prop:drawer`) |
| `multiple-choice` | 8 | Quiz/survey container (`prop:multiple-choice`) |
| `choice-item` | 8 | One answer in multiple-choice |
| `lottie` | 6 | Lottie animation (`prop:lottie`) |
| `indicator` | 3 | Stepper/pagination indicator |
| `indicator-item` | 3 | One dot in an indicator |

## Node common fields

```
{
  "id": "node:<hash>",
  "typeName": "node",
  "type": "stack|text|img|icon|...",
  "name": "Purchase Selected",    # semantic name from designer
  "parentId": "node:<hash>",       # tree structure via parent pointers
  "index": "a2",                   # fractional index for ordering among siblings
  "x": 0, "y": 0,
  "rotation": 0,
  "opacity": 1,
  "isLocked": false,
  "properties": { ... },           # declared overrides
  "defaultProperties": { ... },    # inherited / default values
  "clickBehavior": {"type": "do-nothing"},
  "meta": {},
  "props": {},
  "requiredRecordIds": []
}
```

**Critical:** always check BOTH `properties` and `defaultProperties` when
reading; either may hold the real value. A `{"type": "tombstone"}` in
`properties` means "use the default".

## Property keys (65 distinct)

### CSS properties (map ~1:1 to web CSS)

Layout: `css:width`, `css:height`, `css:minHeight`, `css:minWidth`,
`css:maxHeight`, `css:maxWidth`, `css:position`, `css:top`, `css:right`,
`css:bottom`, `css:left`, `css:display`, `css:overflow`, `css:zIndex`

Box model:
- `css:paddingTop`, `css:paddingBottom`, `css:paddingLeft`, `css:paddingRight`
- `css:paddingTop;paddingBottom`, `css:paddingLeft;paddingRight` (paired)
- `css:marginTop`, `css:marginBottom`, `css:marginLeft`, `css:marginRight`
- `css:marginTop;marginBottom`, `css:marginLeft;marginRight` (paired)
- `css:borderTopWidth;borderRightWidth;borderBottomWidth;borderLeftWidth`
- `css:borderTopStyle;borderRightStyle;borderBottomStyle;borderLeftStyle`
- `css:borderColor`
- `css:borderTopLeftRadius`, `css:borderTopRightRadius`,
  `css:borderBottomLeftRadius`, `css:borderBottomRightRadius`
- `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` (shorthand)

Typography: `css:color`, `css:font`, `css:fontSize`, `css:lineHeight`,
`css:letterSpacing`, `css:textAlign`, `css:textDecoration`,
`css:textTransform`, `css:textShadow`

Visual: `css:backgroundColor`, `css:backgroundImage`, `css:backdropFilter`,
`css:opacity`, `css:boxShadow`, `css:filter`, `css:transition`

Transforms: `css:transform[translate]`, `css:transform[scale]`,
`css:transform[rotate]`

### `prop:` properties (type-specific)

| Prop | On type | Shape |
|---|---|---|
| `prop:stack` | stack | `{axis, reverse, crossAxisAlignment, mainAxisDistribution, wrap, gap, scroll, snapPosition}` |
| `prop:text` | text | `{value, rendering, localizationMeta}` |
| `prop:image` | img | `{value, rendering}` |
| `prop:icon` | icon | Icon reference + tint |
| `prop:navigation` | navigation | `{transition}` (none/push/slide) |
| `prop:video` | video | Video source config |
| `prop:lottie` | lottie | Lottie source config |
| `prop:drawer` | drawer | Drawer behavior config |
| `prop:multiple-choice` | multiple-choice | Quiz config |
| `prop:indicator` | indicator | Pagination config |
| `prop:click-behavior` | any | Click action (set-state, navigate, purchase, etc.) |
| `prop:custom-css` | any | Raw CSS escape hatch |

## Value wrapper system

Every property value is one of:

### `literal`
```json
{"type": "literal", "value": {"type": "css-color", "value": "#8C59D9ff"}}
```
Static value. Inner types include:
- `css-color`, `css-length`, `css-percentage`, `css-string`, `css-keyword`
- `css-font`, `css-box-shadow`, `css-background-image`, `css-transform-*`
- `property-text`, `property-image`, `property-stack`, `property-navigation`,
  `property-click-behavior`, etc.

### `conditional`
```json
{
  "type": "conditional",
  "options": [
    {
      "query": {"combinator": "and|or", "rules": [...], "id": "<uuid>"},
      "value": <value_wrapper>
    },
    {
      "query": {"combinator": "and", "rules": [], "id": "<uuid>"},  // default
      "value": <fallback_value>
    }
  ]
}
```

Rules look like:
```json
{
  "id": "<uuid>",
  "field": "state:products.hasIntroductoryOffer",
  "operator": "=",
  "valueSource": "value",
  "value": {"type": "variable-boolean", "value": true}
}
```

Operators seen: `=`, `!=`, `<`, `<=`, `>`, `>=`, `contains`, `?`.

**Every option's query needs an `id` (uuid).** The default option has empty
`rules` and still needs an id. First match wins.

### `referential`
```json
{"type": "referential", "stateId": "state:style.interface.primary"}
```
Pulls value from a state variable. Use this to reference theme tokens or
dynamic product data.

### `tombstone`
```json
{"type": "tombstone"}
```
"Use default value." Presence in `properties` cancels an override.

## State variables (141 unique seen)

### Theme tokens (`state:style.interface.*`)
Universal — present in almost every template:

| Token | Usage | Notes |
|---|---|---|
| `.text` | 196 templates | Primary text color |
| `.primary` | 191 | Brand/accent color |
| `.background` | 164 | Page background |
| `.border` | 101 | Default border |
| `.productSelectedBg` | 52 | **Selected product button bg (often differs from .primary)** |
| `.secondary` | 52 | Secondary accent |
| `.elementBackground` | 52 | Card/chip background |
| `.productBg` | 22 | Unselected product bg |
| `.text2`, `.textSecondary`, `.textLight` | 15/12/7 | Secondary text shades |
| `.cardBg` | 10 | Card backgrounds |
| `.borderSelected` | 7 | Selected product border |
| `.ctaText` | 6 | **Dedicated CTA text color — use for buttons on primary bg** |
| `.text50` | 6 | 50% opacity text variant |

Each token is defined once per theme mode (usually `.light` and `.dark`):

```
state:style.interface.primary.light    → #8C59D9ff (css-color)
state:style.interface.primary.dark     → #8C59D9ff
```

### Layout tokens (`state:style.deviceSize.*`)

| Token | Use |
|---|---|
| `state:style.deviceSize.cornerRadius` | Universal corner radius (e.g. 16px) |
| `state:style.deviceSize.padding` | Universal padding (e.g. 16px) |

Scoped by breakpoint: `.sm`, `.md`, etc.

### Product state (`state:products.*`)

| Variable | Use |
|---|---|
| `products.selectedIndex` | Which product the user picked (integer) |
| `products.hasIntroductoryOffer` | Any product has a trial (boolean) |
| `products.selected.trialPeriodDays` | Days in selected product's trial |
| `products.selected.trialPeriodText` | Localized trial text |
| `products.selected.trialPeriodEndDate` | Date when trial ends |
| `products.selected.price` | Display price |
| `products.selected.period` | "week", "month", "year" |
| `products.<key>.price`, `.rawPrice`, `.monthlyPrice` | Per-product values |

`<key>` is the paywall_product's `id` suffix (e.g. `annual`, `monthly`).

### Device state (`state:device.*`)

| Variable | Use |
|---|---|
| `device.interfaceStyle` | `"light"` or `"dark"` — drives theme mode |
| `device.viewPortHeight` | Adaptive layouts |
| `device.viewPortWidth` | Adaptive layouts |
| `device.viewPortBreakpoint` | `"sm"`, `"md"`, etc. |

### Navigation state

`state:node.<navNodeId>.currentIndex` — **the current page index of a
navigation node**. Query this in conditionals to show/hide content based
on which screen is active. Also how you implement "jump to screen 3".

### Custom state (user-defined)

Designers declare their own states for things like:
`state:state.enableFreeTrial`, `state:state.showMore`, `state:state.activeTab`,
`state:state.modalOpen`, `state:state.planSelected`, `state:state.question1..N`
(for quizzes), `state:state.screenNum`.

## Click behaviors

Found as `prop:click-behavior` on stacks/buttons. Wrapper:
```json
{
  "type": "literal",
  "value": {
    "type": "property-click-behavior",
    "clickActions": [
      {"type": "action-execution", "action": {...}},
      ...
    ]
  }
}
```

Action types observed:
- `set-state` — mutate a state variable (navigate pages, toggle modal, etc.)
- `purchase` — trigger purchase of a product
- `restore` — restore purchases
- `open-url` — open external link
- `dismiss` — close paywall
- `custom` — custom action handler

## Conditional query fields (top usage)

| Field | Count | Purpose |
|---|---|---|
| `state:products.selectedIndex` | 1547 | Highlight selected product |
| `state:products.hasIntroductoryOffer` | 372 | Show trial-specific UI |
| `state:state.enableFreeTrial` | 229 | Custom trial toggle switch |
| `state:params.answerOpened` | 207 | Quiz UI |
| `state:state.showMore` | 117 | Expand/collapse |
| `state:device.viewPortHeight` | 115 | Responsive layout |
| `state:products.selected.trialPeriodDays` | 109 | Trial days gating |
| `state:state.modalOpen` | 80 | Modal state |
| `state:device.interfaceStyle` | 71 | Light/dark mode branching |
| `state:node.<id>.currentIndex` | 62+ | **Active screen for navigation** |

## Products

```json
"paywall_product:annual": {
  "id": "paywall_product:annual",
  "typeName": "paywall_product",
  "store": "app-store",
  "identifier": "com.your.annual.id",   // must exist in Products catalog
  "productVariables": {"source": "sdk"},
  "index": "a0"
}
```

## Paywall_notification

```json
"paywall_notification:TRIAL_STARTED": {
  "id": "paywall_notification:TRIAL_STARTED",
  "typeName": "paywall_notification",
  "title": <property-text wrapper>,
  "subtitle": <property-text wrapper>,
  "body": <property-text wrapper>,
  "delay": <number wrapper>,
  "before_trial_end": <variable-number wrapper> // ms before trial end
}
```

Only type observed: `TRIAL_STARTED` (the "your trial ends soon" reminder).
