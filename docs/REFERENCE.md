# Superwall Paywall Reference (auto-generated)

Mined from 208 templates. Source: `data/grammar/*.json`.

This is the complete grammar of what's authorable. If a property, value, icon, font, click behavior, or state is not listed here, it has not been seen in any real Superwall template — assume it is invalid until verified.


## Node types

| type | instances | templates |
|---|---|---|
| `stack` | 11368 | — |
| `text` | 6464 | — |
| `img` | 1573 | — |
| `icon` | 1079 | — |
| `navigation` | 40 | — |
| `video` | 32 | — |
| `drawer` | 12 | — |
| `multiple-choice` | 8 | — |
| `choice-item` | 8 | — |
| `lottie` | 6 | — |
| `svg` | 5 | — |
| `indicator` | 3 | — |
| `indicator-item` | 3 | — |

## Layout system

Everything visual is a `stack` (a flexbox container) or sits inside one. `stack` composes via:

- `css:flexDirection` — column/row
- `css:alignItems`, `css:justifyContent` — cross/main axis alignment
- `css:gap` — child spacing (css-length)
- `css:padding` — inner padding (css-length, often per-side via object)
- `css:width`, `css:height` — sizing (css-length, css-percentage, or `auto`)

All lengths use the `css-length` value type — see the **Value types** section.


### Common stack recipes (top patterns)

- ×901 — `css:width=100%`
- ×277 — `css:height=8px`, `css:width=8px`
- ×266 — `css:width=100vw`
- ×164 — `css:height=50px`, `css:width=30vw`
- ×137 — `css:height=100%`, `css:width=100%`
- ×112 — `css:height=100%`
- ×110 — `css:height=24px`, `css:width=24px`
- ×109 — `css:height=100vh`, `css:width=100vw`
- ×86 — `css:height=6px`, `css:width=6px`
- ×86 — `css:height=1px`, `css:width=100%`
- ×85 — `css:height=60px`
- ×83 — `css:height=50px`, `css:width=40vw`
- ×62 — `css:height=0.5px`
- ×62 — `css:height=34px`, `css:width=34px`
- ×62 — `css:height=12px`, `css:width=12px`

## Properties by node type


### `stack` (11368 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `prop:stack` | 67.1% | `property-stack`, `conditional` | `wrap=nowrap`, `wrap=wrap` | `{"type": "property-stack", "axis": "y", "reverse": false, "c…` |
| `css:backgroundColor` | 43.2% | `referential`, `conditional`, `css-color` | — | `{"type": "css-color", "value": "#000000ff"}` |
| `css:width` | 34.8% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "30", "unit": "vw"}` |
| `css:height` | 32.5% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "100", "unit": "%"}` |
| `css:paddingLeft;paddingRight` | 25.5% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "16", "unit": "px"}` |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 19.3% | `css-length`, `conditional`, `referential` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:paddingTop;paddingBottom` | 17.3% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "1", "unit": "px"}` |
| `css:borderColor` | 16.3% | `referential`, `conditional`, `css-color` | — | `{"type": "css-color", "value": "#f2d999ff"}` |
| `prop:click-behavior` | 12.6% | `property-click-behavior`, `tombstone`, `conditional` | — | `{"type": "property-click-behavior", "clickActions": [{"type"…` |
| `css:position` | 12.5% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "absolute"}` |
| `css:paddingBottom` | 10.3% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "22", "unit": "px"}` |
| `css:paddingTop` | 9.2% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "70", "unit": "px"}` |
| `css:borderTopWidth;borderRightWidth;borderBottomWidth;borderLeftWidth` | 7.9% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "1", "unit": "px"}` |
| `css:left` | 7.3% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "50", "unit": "%"}` |
| `css:zIndex` | 7.2% | `css-string`, `tombstone`, `conditional` | — | `{"type": "css-string", "value": "20"}` |
| `css:display` | 7.0% | `css-string`, `conditional`, `tombstone` | — | `{"type": "css-string", "value": "none"}` |
| `css:top` | 6.1% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `prop:custom-css` | 6.0% | `property-custom-css`, `tombstone`, `conditional` | — | `{"type": "property-custom-css", "properties": []}` |
| `css:opacity` | 5.6% | `css-percentage`, `tombstone`, `conditional` | — | `{"type": "css-percentage", "value": "0", "unit": "%"}` |
| `css:right` | 5.5% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:marginBottom` | 5.0% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "36", "unit": "px"}` |
| `css:marginTop` | 5.0% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "16", "unit": "px"}` |
| `css:bottom` | 4.1% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:transition` | 3.4% | `css-transition`, `tombstone`, `conditional` | — | `{"type": "css-transition", "property": "all", "timingFunctio…` |
| `css:borderTopStyle;borderRightStyle;borderBottomStyle;borderLeftStyle` | 3.4% | `css-string`, `tombstone`, `conditional` | — | `{"type": "css-string", "value": "solid"}` |
| `css:backgroundImage` | 3.3% | `css-background-image`, `tombstone`, `conditional` | — | `{"type": "css-background-image", "functions": [{"type": "lin…` |
| `css:minHeight` | 3.2% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "164", "unit": "px"}` |
| `css:boxShadow` | 2.9% | `tombstone`, `css-box-shadow`, `conditional` | — | `{"type": "css-box-shadow", "xOffset": {"type": "css-number-u…` |
| `css:transform[translate]` | 2.8% | `css-transform-translate`, `tombstone`, `conditional` | — | `{"type": "css-transform-translate", "x": {"type": "css-lengt…` |
| `css:paddingRight` | 2.3% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "6", "unit": "px"}` |
| `css:maxWidth` | 2.2% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "30", "unit": "vw"}` |
| `css:borderTopLeftRadius` | 2.1% | `tombstone`, `css-length`, `conditional` | — | `{"type": "css-length", "value": "12", "unit": "px"}` |
| `css:borderTopRightRadius` | 2.0% | `tombstone`, `css-length`, `conditional` | — | `{"type": "css-length", "value": "12", "unit": "px"}` |
| `css:backdropFilter` | 1.8% | `tombstone`, `css-backdrop-filter`, `conditional` | — | `{"type": "css-backdrop-filter", "filters": [{"type": "blur",…` |
| `css:paddingLeft` | 1.7% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "16", "unit": "px"}` |
| `css:overflow` | 1.6% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "scroll"}` |
| `css:marginLeft` | 0.9% | `tombstone`, `css-length` | — | `{"type": "css-length", "unit": "px", "value": "2"}` |
| `css:borderBottomLeftRadius` | 0.5% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:transform[scale]` | 0.5% | `css-transform-scale`, `tombstone`, `conditional` | — | `{"type": "css-transform-scale", "value": {"type": "css-numbe…` |
| `css:borderBottomRightRadius` | 0.5% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:maxHeight` | 0.5% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "420", "unit": "px"}` |
| `css:marginRight` | 0.3% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "24", "unit": "px"}` |
| `css:minWidth` | 0.2% | `css-length`, `tombstone` | — | `{"type": "css-length", "unit": "px", "value": "310"}` |
| `css:marginLeft;marginRight` | 0.2% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:marginTop;marginBottom` | 0.1% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "30", "unit": "px"}` |
| `css:filter` | 0.1% | `tombstone`, `css-filter`, `conditional` | — | `{"type": "css-filter", "filters": [{"type": "blur", "value":…` |
| `css:transform[rotate]` | 0.0% | `css-transform-rotate` | — | `{"type": "css-transform-rotate", "value": {"type": "css-numb…` |

### `text` (6464 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `prop:text` | 108.0% | `property-text`, `conditional`, `tombstone` | — | `{"type": "property-text", "value": "Snapchat+", "rendering":…` |
| `css:fontSize` | 77.2% | `css-length`, `conditional`, `tombstone` | — | `{"type": "css-length", "unit": "px", "value": "28"}` |
| `css:font` | 71.8% | `css-font`, `tombstone`, `conditional` | `style=normal`, `kind=custom`, `weight=500` | `{"type": "css-font", "value": "SF Pro Text", "style": "norma…` |
| `css:color` | 71.2% | `css-color`, `referential`, `conditional` | — | `{"type": "css-color", "value": "#ffffffff"}` |
| `css:lineHeight` | 32.5% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "140", "unit": "%"}` |
| `css:textAlign` | 23.8% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "center"}` |
| `css:opacity` | 12.5% | `css-percentage`, `tombstone`, `conditional` | — | `{"type": "css-percentage", "value": "75", "unit": "%"}` |
| `css:letterSpacing` | 9.4% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "-0.2", "unit": "px"}` |
| `css:paddingLeft;paddingRight` | 8.4% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:paddingTop;paddingBottom` | 8.2% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "2", "unit": "px"}` |
| `css:textTransform` | 7.6% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "capitalize"}` |
| `prop:click-behavior` | 6.7% | `property-click-behavior`, `tombstone`, `conditional` | — | `{"type": "property-click-behavior", "clickActions": [{"type"…` |
| `css:backgroundColor` | 5.7% | `css-color`, `conditional`, `referential` | — | `{"type": "css-color", "value": "#00fe99ff"}` |
| `css:textDecoration` | 4.3% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "line-through"}` |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 3.6% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "999", "unit": "px"}` |
| `css:width` | 3.2% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "28", "unit": "px"}` |
| `css:marginTop` | 2.6% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:display` | 2.3% | `css-string`, `conditional`, `tombstone` | — | `{"type": "css-string", "value": "none"}` |
| `prop:custom-css` | 1.7% | `property-custom-css`, `tombstone`, `conditional` | — | `{"type": "property-custom-css", "properties": [{"type": "cus…` |
| `css:marginBottom` | 1.7% | `css-length`, `tombstone` | — | `{"type": "css-length", "unit": "px", "value": "10"}` |
| `css:position` | 1.5% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "relative"}` |
| `css:paddingTop` | 1.2% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:right` | 1.2% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "12", "unit": "px"}` |
| `css:paddingBottom` | 1.1% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:height` | 0.9% | `tombstone`, `css-length` | — | `{"type": "css-length", "unit": "px", "value": "15"}` |
| `css:transition` | 0.9% | `css-transition`, `tombstone` | — | `{"type": "css-transition", "property": "all", "timingFunctio…` |
| `css:backgroundImage` | 0.9% | `css-background-image`, `tombstone`, `conditional` | — | `{"type": "css-background-image", "functions": [{"type": "lin…` |
| `css:zIndex` | 0.8% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "1"}` |
| `css:top` | 0.7% | `css-length`, `tombstone` | — | `{"type": "css-length", "unit": "px", "value": "-14"}` |
| `css:paddingLeft` | 0.4% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:borderTopRightRadius` | 0.4% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:borderTopLeftRadius` | 0.4% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:paddingRight` | 0.3% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "", "unit": "px"}` |
| `css:borderColor` | 0.3% | `css-color`, `tombstone`, `conditional` | — | `{"type": "css-color", "value": "#222020ff"}` |
| `css:left` | 0.3% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "-0.5", "unit": "px"}` |
| `css:borderTopWidth;borderRightWidth;borderBottomWidth;borderLeftWidth` | 0.3% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "2", "unit": "px"}` |
| `css:textShadow` | 0.2% | `tombstone`, `css-box-shadow` | — | `{"type": "css-box-shadow", "xOffset": {"type": "css-number-u…` |
| `css:boxShadow` | 0.2% | `css-box-shadow`, `tombstone` | — | `{"type": "css-box-shadow", "xOffset": {"type": "css-number-u…` |
| `css:marginLeft` | 0.2% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:borderBottomLeftRadius` | 0.1% | `css-length` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:overflow` | 0.1% | `css-string` | — | `{"type": "css-string", "value": "hidden"}` |
| `css:marginRight` | 0.1% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "5", "unit": "px"}` |
| `css:borderBottomRightRadius` | 0.1% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:transform[translate]` | 0.1% | `css-transform-translate` | — | `{"type": "css-transform-translate", "y": {"type": "css-lengt…` |
| `css:borderTopStyle;borderRightStyle;borderBottomStyle;borderLeftStyle` | 0.1% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "solid"}` |
| `css:marginLeft;marginRight` | 0.0% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:transform[scale]` | 0.0% | `css-transform-scale` | — | `{"type": "css-transform-scale", "value": {"type": "css-numbe…` |
| `css:transform[rotate]` | 0.0% | `css-transform-rotate` | — | `{"type": "css-transform-rotate", "value": {"type": "css-numb…` |
| `css:bottom` | 0.0% | `tombstone` | — |  |

### `img` (1573 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `prop:image` | 93.1% | `property-image`, `conditional` | — | `{"type": "property-image", "rendering": {"type": "literal"},…` |
| `css:width` | 84.5% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "60", "unit": "px"}` |
| `css:height` | 61.3% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "auto", "unit": "none"}` |
| `prop:custom-css` | 5.4% | `property-custom-css`, `conditional`, `tombstone` | — | `{"type": "property-custom-css", "properties": [{"type": "cus…` |
| `css:display` | 3.9% | `css-string`, `conditional`, `tombstone` | — | `{"type": "css-string", "value": "none"}` |
| `css:position` | 3.7% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "absolute"}` |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 3.5% | `css-length`, `conditional`, `referential` | — | `{"type": "css-length", "value": "8", "unit": "px"}` |
| `css:top` | 1.8% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:left` | 1.6% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "-3", "unit": "px"}` |
| `css:right` | 1.5% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:marginTop` | 1.5% | `css-length`, `tombstone` | — | `{"type": "css-length", "unit": "px", "value": "50"}` |
| `css:zIndex` | 1.5% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "0"}` |
| `css:marginBottom` | 1.4% | `tombstone`, `css-length` | — | `{"type": "css-length", "unit": "px", "value": "-3"}` |
| `css:bottom` | 1.3% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "-5", "unit": "px"}` |
| `css:opacity` | 1.1% | `css-percentage`, `conditional`, `tombstone` | — | `{"type": "css-percentage", "value": "40", "unit": "%"}` |
| `css:paddingLeft;paddingRight` | 1.1% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "10", "unit": "px"}` |
| `css:marginRight` | 0.9% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "12", "unit": "px"}` |
| `css:maxWidth` | 0.7% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "340", "unit": "px"}` |
| `css:transform[translate]` | 0.7% | `css-transform-translate`, `conditional` | — | `{"type": "css-transform-translate", "x": {"type": "css-lengt…` |
| `css:paddingTop;paddingBottom` | 0.6% | `css-length`, `tombstone`, `conditional` | — | `{"type": "css-length", "value": "50", "unit": "px"}` |
| `css:maxHeight` | 0.5% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "50", "unit": "px"}` |
| `css:borderColor` | 0.4% | `css-color`, `conditional`, `referential` | — | `{"type": "css-color", "value": "#5b4e54ff"}` |
| `css:borderTopLeftRadius` | 0.4% | `css-length` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:borderTopRightRadius` | 0.4% | `css-length` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:borderTopWidth;borderRightWidth;borderBottomWidth;borderLeftWidth` | 0.4% | `css-length` | — | `{"type": "css-length", "value": "1", "unit": "px"}` |
| `prop:click-behavior` | 0.4% | `property-click-behavior`, `tombstone` | — | `{"type": "property-click-behavior", "clickActions": [{"type"…` |
| `css:transition` | 0.3% | `css-transition`, `tombstone` | — | `{"type": "css-transition", "property": "all", "timingFunctio…` |
| `css:transform[rotate]` | 0.2% | `css-transform-rotate`, `tombstone` | — | `{"type": "css-transform-rotate", "value": {"type": "css-numb…` |
| `css:backgroundColor` | 0.2% | `tombstone`, `conditional`, `css-color` | — | `{"type": "css-color", "value": "#ffffffff"}` |
| `css:marginLeft` | 0.2% | `css-length` | — | `{"type": "css-length", "value": "auto", "unit": "none"}` |
| `css:paddingTop` | 0.1% | `css-length` | — | `{"type": "css-length", "value": "50", "unit": "px"}` |
| `css:backgroundImage` | 0.1% | `css-background-image` | — | `{"type": "css-background-image", "functions": [{"type": "lin…` |
| `css:borderTopStyle;borderRightStyle;borderBottomStyle;borderLeftStyle` | 0.1% | `css-string` | — | `{"type": "css-string", "value": "solid"}` |
| `css:marginLeft;marginRight` | 0.1% | `tombstone` | — |  |
| `css:minHeight` | 0.1% | `tombstone` | — |  |
| `css:transform[scale]` | 0.1% | `css-transform-scale` | — | `{"type": "css-transform-scale", "value": {"type": "css-numbe…` |
| `css:boxShadow` | 0.1% | `tombstone` | — |  |
| `css:minWidth` | 0.1% | `tombstone` | — |  |

### `icon` (1079 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `css:color` | 114.7% | `conditional`, `referential`, `css-color` | — | `{"type": "css-color", "value": "#615f60ff"}` |
| `prop:icon` | 95.7% | `property-icon`, `conditional` | — | `{"type": "property-icon", "name": "ChevronDown", "strokeLine…` |
| `css:width` | 64.3% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "16", "unit": "px"}` |
| `css:height` | 62.2% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "16", "unit": "px"}` |
| `css:transform[scale]` | 26.9% | `css-transform-scale`, `tombstone`, `conditional` | — | `{"type": "css-transform-scale", "value": {"type": "css-numbe…` |
| `css:opacity` | 16.9% | `css-percentage`, `tombstone`, `conditional` | — | `{"type": "css-percentage", "value": "0", "unit": "%"}` |
| `css:display` | 6.8% | `css-string`, `conditional`, `tombstone` | — | `{"type": "css-string", "value": "none"}` |
| `css:marginTop` | 4.1% | `tombstone`, `css-length` | — | `{"type": "css-length", "unit": "px", "value": "-2"}` |
| `css:paddingRight` | 3.0% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:paddingLeft;paddingRight` | 1.9% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:transition` | 1.9% | `css-transition` | — | `{"type": "css-transition", "property": "color, background-co…` |
| `prop:click-behavior` | 1.6% | `property-click-behavior` | — | `{"type": "property-click-behavior", "clickActions": [], "ani…` |
| `css:transform[rotate]` | 1.6% | `css-transform-rotate`, `conditional`, `tombstone` | — | `{"type": "css-transform-rotate", "value": {"type": "css-numb…` |
| `css:paddingTop;paddingBottom` | 1.6% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:position` | 1.5% | `css-string`, `tombstone` | — | `{"type": "css-string", "value": "absolute"}` |
| `css:paddingLeft` | 1.3% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:right` | 1.1% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:top` | 0.8% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "15", "unit": "px"}` |
| `css:marginRight` | 0.6% | `css-length` | — | `{"type": "css-length", "value": "15", "unit": "px"}` |
| `css:marginBottom` | 0.4% | `css-length` | — | `{"type": "css-length", "value": "5", "unit": "px"}` |
| `css:bottom` | 0.4% | `tombstone` | — |  |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 0.2% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "999", "unit": "px"}` |
| `css:transform[translate]` | 0.2% | `css-transform-translate` | — | `{"type": "css-transform-translate", "x": {"type": "css-lengt…` |
| `css:left` | 0.2% | `tombstone`, `css-length` | — | `{"type": "css-length", "unit": "raw", "value": "calc(50% + 4…` |
| `css:zIndex` | 0.1% | `css-string` | — | `{"type": "css-string", "value": "1"}` |
| `css:overflow` | 0.1% | `tombstone` | — |  |

### `navigation` (40 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `prop:navigation` | 100.0% | `property-navigation` | — | `{"type": "property-navigation", "transition": "push"}` |
| `css:width` | 97.5% | `css-length` | — | `{"type": "css-length", "value": "100", "unit": "%"}` |
| `css:height` | 90.0% | `css-length` | — | `{"type": "css-length", "value": "100", "unit": "vh"}` |
| `prop:custom-css` | 87.5% | `property-custom-css` | — | `{"type": "property-custom-css", "properties": []}` |
| `css:backgroundColor` | 10.0% | `conditional`, `referential` | — |  |
| `css:paddingTop` | 2.5% | `tombstone` | — |  |

### `video` (32 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `prop:video` | 93.8% | `property-video`, `conditional` | — | `{"type": "property-video", "src": "https://user-content.supe…` |
| `css:width` | 78.1% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "100", "unit": "%"}` |
| `css:height` | 59.4% | `css-length`, `tombstone` | — | `{"type": "css-length", "unit": "raw", "value": "calc(100vh-4…` |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 12.5% | `css-length` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:position` | 9.4% | `css-string` | — | `{"type": "css-string", "value": "absolute"}` |
| `css:top` | 9.4% | `css-length` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:left` | 9.4% | `css-length` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:zIndex` | 9.4% | `css-string` | — | `{"type": "css-string", "value": "1"}` |
| `css:transform[translate]` | 9.4% | `css-transform-translate`, `conditional` | — | `{"type": "css-transform-translate", "x": {"type": "css-lengt…` |
| `prop:custom-css` | 6.2% | `property-custom-css` | — | `{"type": "property-custom-css", "properties": [{"type": "cus…` |
| `css:transition` | 6.2% | `css-transition` | — | `{"type": "css-transition", "property": "opacity, background-…` |
| `css:backgroundImage` | 6.2% | `css-background-image` | — | `{"type": "css-background-image", "functions": [{"type": "ima…` |
| `prop:click-behavior` | 3.1% | `property-click-behavior` | — | `{"type": "property-click-behavior", "clickActions": [], "ani…` |
| `css:transform[scale]` | 3.1% | `css-transform-scale` | — | `{"type": "css-transform-scale", "value": {"type": "css-numbe…` |
| `css:paddingTop` | 3.1% | `css-length` | — | `{"type": "css-length", "unit": "px", "value": "48"}` |
| `css:right` | 3.1% | `css-length` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:bottom` | 3.1% | `css-length` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |

### `drawer` (12 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `css:paddingLeft;paddingRight` | 100.0% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "16", "unit": "px"}` |
| `css:minHeight` | 100.0% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "150", "unit": "px"}` |
| `css:paddingTop;paddingBottom` | 91.7% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "24", "unit": "px"}` |
| `prop:drawer` | 91.7% | `property-drawer` | — | `{"type": "property-drawer", "dismissible": true, "detents": …` |
| `css:backgroundColor` | 83.3% | `conditional`, `referential`, `css-color` | — | `{"type": "css-color", "value": "#000000ff"}` |
| `css:maxHeight` | 25.0% | `tombstone` | — |  |
| `css:position` | 16.7% | `css-string` | — | `{"type": "css-string", "value": "relative"}` |
| `css:paddingBottom` | 16.7% | `css-length` | — | `{"type": "css-length", "value": "34", "unit": "px"}` |
| `css:height` | 16.7% | `css-length` | — | `{"type": "css-length", "value": "90", "unit": "vh"}` |
| `css:paddingTop` | 16.7% | `css-length` | — | `{"type": "css-length", "value": "10", "unit": "px"}` |
| `css:width` | 8.3% | `css-length` | — | `{"type": "css-length", "value": "100", "unit": "vw"}` |
| `css:opacity` | 8.3% | `css-percentage` | — | `{"type": "css-percentage", "value": "100", "unit": "%"}` |
| `css:overflow` | 8.3% | `tombstone` | — |  |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 8.3% | `css-length` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `css:borderBottomLeftRadius` | 8.3% | `css-length` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |
| `css:borderBottomRightRadius` | 8.3% | `css-length` | — | `{"type": "css-length", "value": "0", "unit": "px"}` |

### `multiple-choice` (8 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `prop:multiple-choice` | 100.0% | `property-multiple-choice` | — | `{"type": "property-multiple-choice", "selectionMode": "singl…` |
| `css:paddingTop` | 37.5% | `css-length` | — | `{"type": "css-length", "value": "32", "unit": "px"}` |
| `prop:stack` | 25.0% | `property-stack` | `wrap=wrap` | `{"type": "property-stack", "axis": "x", "reverse": false, "c…` |
| `prop:custom-css` | 12.5% | `property-custom-css` | — | `{"type": "property-custom-css", "properties": [{"type": "cus…` |

### `choice-item` (8 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `css:backgroundColor` | 175.0% | `css-color`, `conditional`, `referential` | — | `{"type": "css-color", "value": "#f5f5f5ff"}` |
| `css:borderColor` | 150.0% | `css-color`, `conditional`, `referential` | — | `{"type": "css-color", "value": "#000000ff"}` |
| `css:paddingTop;paddingBottom` | 112.5% | `css-length`, `conditional`, `referential` | — | `{"type": "css-length", "value": "6", "unit": "px"}` |
| `css:paddingLeft;paddingRight` | 100.0% | `conditional`, `referential`, `css-length` | — | `{"type": "css-length", "value": "12", "unit": "px"}` |
| `prop:click-behavior` | 62.5% | `property-click-behavior` | — | `{"type": "property-click-behavior", "clickActions": [{"type"…` |
| `prop:stack` | 37.5% | `property-stack` | `wrap=nowrap` | `{"type": "property-stack", "axis": "y", "reverse": false, "c…` |
| `css:minHeight` | 37.5% | `css-length` | — | `{"type": "css-length", "value": "65", "unit": "px"}` |
| `css:transition` | 37.5% | `css-transition` | — | `{"type": "css-transition", "property": "all", "timingFunctio…` |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 25.0% | `css-length` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:borderTopWidth;borderRightWidth;borderBottomWidth;borderLeftWidth` | 25.0% | `css-length` | — | `{"type": "css-length", "value": "2", "unit": "px"}` |
| `css:width` | 25.0% | `css-length` | — | `{"type": "css-length", "value": "30", "unit": "%"}` |
| `prop:custom-css` | 12.5% | `property-custom-css` | — | `{"type": "property-custom-css", "properties": [{"type": "cus…` |
| `css:position` | 12.5% | `css-string` | — | `{"type": "css-string", "value": "relative"}` |

### `lottie` (6 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `prop:lottie` | 100.0% | `property-lottie` | — | `{"type": "property-lottie", "src": "https://user-content.sup…` |
| `css:marginTop` | 50.0% | `css-length` | — | `{"type": "css-length", "value": "10", "unit": "%"}` |
| `css:width` | 50.0% | `css-length` | — | `{"type": "css-length", "value": "60", "unit": "%"}` |

### `indicator` (3 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `css:display` | 200.0% | `css-string`, `conditional` | — | `{"type": "css-string", "value": ""}` |
| `prop:indicator` | 100.0% | `property-indicator` | — | `{"type": "property-indicator", "currentIndex": {"type": "sta…` |
| `css:paddingLeft;paddingRight` | 100.0% | `css-length`, `conditional`, `referential` | — | `{"type": "css-length", "value": "20", "unit": "px"}` |
| `prop:stack` | 100.0% | `property-stack` | `wrap=nowrap` | `{"type": "property-stack", "axis": "x", "reverse": false, "c…` |
| `css:opacity` | 66.7% | `conditional`, `css-percentage` | — | `{"type": "css-percentage", "value": "0", "unit": "%"}` |
| `css:position` | 33.3% | `css-string` | — | `{"type": "css-string", "value": "fixed"}` |
| `css:zIndex` | 33.3% | `css-string` | — | `{"type": "css-string", "value": "3"}` |
| `css:top` | 33.3% | `css-length` | — | `{"type": "css-length", "value": "70", "unit": "px"}` |
| `css:width` | 33.3% | `css-length` | — | `{"type": "css-length", "value": "100", "unit": "%"}` |
| `css:paddingTop` | 33.3% | `css-length` | — | `{"type": "css-length", "value": "80", "unit": "px"}` |
| `css:paddingTop;paddingBottom` | 33.3% | `tombstone` | — |  |
| `css:marginTop` | 33.3% | `css-length` | — | `{"type": "css-length", "unit": "px", "value": "5"}` |
| `css:transition` | 33.3% | `css-transition` | — | `{"type": "css-transition", "property": "opacity, background-…` |
| `css:height` | 33.3% | `css-length` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |

### `indicator-item` (3 instances)

| property | %set | inner types | enums | example |
|---|---|---|---|---|
| `css:borderTopLeftRadius` | 133.3% | `conditional`, `css-length` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:borderBottomLeftRadius` | 133.3% | `conditional`, `css-length` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:borderTopRightRadius` | 133.3% | `conditional`, `css-length` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:borderBottomRightRadius` | 133.3% | `conditional`, `css-length` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius` | 100.0% | `tombstone`, `css-length` | — | `{"type": "css-length", "value": "4", "unit": "px"}` |
| `prop:stack` | 66.7% | `property-stack` | `wrap=nowrap` | `{"type": "property-stack", "axis": "x", "reverse": false, "c…` |
| `css:width` | 66.7% | `css-length`, `tombstone` | — | `{"type": "css-length", "value": "90", "unit": "px"}` |
| `css:height` | 66.7% | `css-length` | — | `{"type": "css-length", "value": "3", "unit": "px"}` |
| `css:backgroundColor` | 33.3% | `tombstone` | — |  |
| `css:transition` | 33.3% | `css-transition` | — | `{"type": "css-transition", "property": "color, background-co…` |
| `css:opacity` | 33.3% | `css-percentage` | — | `{"type": "css-percentage", "value": "100", "unit": "%"}` |
| `css:overflow` | 33.3% | `css-string` | — | `{"type": "css-string", "value": "hidden"}` |

## Click behaviors

All values seen on `clickBehavior` (top-level node field, not under `properties`):

| kind | count |
|---|---|
| `set-state` | 522 |
| `set-product-index` | 490 |
| `open-url` | 253 |
| `close` | 178 |
| `purchase` | 138 |
| `restore` | 104 |
| `custom-in-app` | 36 |
| `navigate-page` | 17 |
| `select-choice` | 5 |
| `request-permission` | 5 |
| `set-attribute` | 4 |
| `custom-placement` | 1 |

Examples:

- on `stack`: `{"type": "set-state", "stateId": "state:node.7TjYqFXHDOBuLuKehTsdX.currentIndex", "operation": {"type": "increment"}, "value": {"type": "variable-number", "valu`
- on `stack`: `{"type": "close"}`
- on `stack`: `{"type": "close"}`
- on `stack`: `{"type": "set-state", "stateId": "state:node.7TjYqFXHDOBuLuKehTsdX.currentIndex", "operation": {"type": "decrement"}, "value": {"type": "variable-number", "valu`
- on `stack`: `{"type": "close"}`
- on `stack`: `{"type": "set-product-index", "index": 0}`
- on `stack`: `{"type": "set-product-index", "index": 1}`
- on `stack`: `{"type": "purchase", "reference": {"type": "by-selected"}}`

## Fonts

| family | count | weights | kind |
|---|---|---|---|
| SF Pro Text | 1498 | 100,300,300italic,400,400italic,500,500italic,600,600italic,700,800 | custom |
| System Font | 747 | 200,300,400,400italic,500,600,700,800,900,normal | system |
| SF Pro Display | 369 | 400,500,600,700,900 | custom |
| Inter | 318 | 400,500,600,700,800 | google |
| Poppins | 211 | 100,200,300,300italic,400,400italic,500,500italic,600,700,700italic | google,system |
| Montserrat | 139 | 400,500,600,700,800,900 | google |
| Gellix | 113 | 500,600 | custom |
| DM Sans | 87 | 400,500,600,700 | google |
| Eudoxus Sans | 69 | 500,700 | custom |
| Matter | 67 | 500,500italic,600 | custom |
| Euclid Circular A | 56 | 500,600,700 | custom |
| SF Pro Rounded | 55 | 400,500,600,700 | custom |
| Figtree | 53 | 300,500,600,700 | google |
| Right Grotesk | 43 | 500,700,900 | custom |
| Afacad | 41 | 400,500,600,700 | google |
| Clash Display | 39 | 400,500,600 | custom |
| Recoleta | 37 | 400 | custom |
| Graphik | 30 | 400,500,600,700 | custom |
| Maax | 28 | 400,500,700 | custom |
| Avenir Next | 24 | 500,600,700,900 | custom |
| Plus Jakarta Sans | 22 | 300,400,500,600 | google |
| Magazine Grotesque | 18 | 400,600,700 | custom |
| Azo Sans | 18 | 100,300,500,700 | custom |
| Klavika | 13 | 300,500,700 | custom |
| Open Sans | 13 | 400,500,600,700 | google |

## Icons (top 60)

Icon names usable in `prop:icon` / `name`:

`Check`, `X`, `ChevronLeft`, `ChevronDown`, `UnlockKeyhole`, `Minus`, `BellRing`, `LockKeyhole`, `ChevronUp`, `ChevronRight`, `Dot`, `ArrowRight`, `Gift`, `Star`, `MessageSquareText`, `Crown`, `ArrowLeft`, `Heart`, `CheckCircle2`, `Bell`, `Flame`, `AudioLines`, `ShieldCheck`, `BookOpenText`, `Compass`, `Megaphone`, `RotateCcw`, `Undo2`, `Zap`, `Plus`, `Shapes`, `Plane`, `ArrowBigLeftDash`, `CloudDrizzle`, `Medal`, `Wallet2`, `CalendarX2`, `Coins`, `Siren`, `XOctagon`, `LayoutList`, `Radar`, `Infinity`, `Ban`, `Sparkles`, `RefreshCcw`, `Eye`, `Mail`, `ShieldBan`, `Handshake`, `User`, `GaugeCircle`, `ShieldPlus`, `Package`, `Globe2`, `Music4`, `ScrollText`, `CheckCheck`, `UserRound`, `Tv`

## Interface tokens (theme)

Reference these via `{type: referential, stateId: <token>}` in any color/style prop:

| token | templates_using |
|---|---|
| `state:style.interface.background.light` | 208 |
| `state:style.interface.primary.light` | 208 |
| `state:style.interface.text.light` | 208 |
| `state:style.interface.border.light` | 130 |
| `state:style.interface.secondary.light` | 65 |
| `state:style.interface.productSelectedBg.light` | 44 |
| `state:style.interface.elementBackground.light` | 39 |
| `state:style.interface.productBg.light` | 23 |
| `state:style.interface.text50.light` | 21 |
| `state:style.interface.text2.light` | 20 |
| `state:style.interface.background.dark` | 16 |
| `state:style.interface.primary.dark` | 16 |
| `state:style.interface.text.dark` | 16 |
| `state:style.interface.border.dark` | 13 |
| `state:style.interface.secondary.dark` | 11 |
| `state:style.interface.textSecondary.light` | 11 |
| `state:style.interface.cardBg.light` | 10 |
| `state:style.interface.textLight.light` | 8 |
| `state:style.interface.productSelectedBg.dark` | 8 |
| `state:style.interface.borderSelected.light` | 7 |
| `state:style.interface.ctaText.light` | 6 |
| `state:style.interface.ctaText.dark` | 6 |
| `state:style.interface.text50.dark` | 6 |
| `state:style.interface.elementBg.light` | 6 |
| `state:style.interface.controlBackground.light` | 6 |
| `state:style.interface.textColor.light` | 6 |
| `state:style.interface.elementBackground.dark` | 4 |
| `state:style.interface.drawerBg.light` | 4 |
| `state:style.interface.text3.light` | 4 |
| `state:style.interface.gold.light` | 3 |
| `state:style.interface.borderUnselected.light` | 3 |
| `state:style.interface.textGray.light` | 2 |
| `state:style.interface.primaryLight.light` | 2 |
| `state:style.interface.unselected.light` | 2 |
| `state:style.interface.pageIndicatorOn.light` | 2 |
| `state:style.interface.pageIndicatorOff.light` | 2 |
| `state:style.interface.borderInactive.light` | 2 |
| `state:style.interface.countdownBg.light` | 2 |
| `state:style.interface.brandColor.light` | 2 |
| `state:style.interface.primaryText.light` | 2 |
| `state:style.interface.selectedCardText.light` | 2 |
| `state:style.interface.subtitle.light` | 2 |
| `state:style.interface.subtitle.dark` | 2 |
| `state:style.interface.selectorSubtitle.light` | 2 |
| `state:style.interface.selectorSubtitle.dark` | 2 |
| `state:style.interface.selectedProductBg.light` | 2 |
| `state:style.interface.selectedPrimaryBg.light` | 2 |
| `state:style.interface.selectedSecondaryBg.light` | 2 |
| `state:style.interface.bulletsText.light` | 2 |
| `state:style.interface.toggleOn.light` | 2 |
| `state:style.interface.productBgSelected.light` | 2 |
| `state:style.interface.productSelectorBg.light` | 2 |
| `state:style.interface.iconBorder.light` | 2 |
| `state:style.interface.toggleOffBg.light` | 2 |
| `state:style.interface.pickerBg.light` | 2 |
| `state:style.interface.tabBg.light` | 2 |
| `state:style.interface.productBg1.light` | 1 |
| `state:style.interface.productBg2.light` | 1 |
| `state:style.interface.productBorder1.light` | 1 |
| `state:style.interface.productBorder2.light` | 1 |
| `state:style.interface.onAccent.light` | 1 |
| `state:style.interface.backgroundSecondary.light` | 1 |
| `state:style.interface.backgroundSecondary.dark` | 1 |
| `state:style.interface.unselectedBorderColor.light` | 1 |
| `state:style.interface.unselectedBorderColor.dark` | 1 |
| `state:style.interface.green.light` | 1 |
| `state:style.interface.primaryGreen.light` | 1 |
| `state:style.interface.textDark.light` | 1 |
| `state:style.interface.inactiveBorder.light` | 1 |
| `state:style.interface.activeCardBg.light` | 1 |
| `state:style.interface.subtext.light` | 1 |
| `state:style.interface.greenMid.light` | 1 |
| `state:style.interface.primaryButtonColor.light` | 1 |
| `state:style.interface.primaryButtonColor.dark` | 1 |
| `state:style.interface.starColor.light` | 1 |
| `state:style.interface.starColor.dark` | 1 |
| `state:style.interface.darkText.light` | 1 |
| `state:style.interface.darkText.dark` | 1 |
| `state:style.interface.surface.light` | 1 |
| `state:style.interface.surface.dark` | 1 |
| `state:style.interface.textOnButton.light` | 1 |
| `state:style.interface.textOnButton.dark` | 1 |
| `state:style.interface.clear.light` | 1 |
| `state:style.interface.clear.dark` | 1 |
| `state:style.interface.surfacePresented.light` | 1 |
| `state:style.interface.surfacePresented.dark` | 1 |
| `state:style.interface.backgroundLight.light` | 1 |
| `state:style.interface.backgroundLight.dark` | 1 |
| `state:style.interface.textSecondary.dark` | 1 |
| `state:style.interface.corners.light` | 1 |
| `state:style.interface.unselectedProductBackground.light` | 1 |
| `state:style.interface.selectedProductBackground.light` | 1 |
| `state:style.interface.gradientGold.light` | 1 |
| `state:style.interface.textSubtle.light` | 1 |
| `state:style.interface.textLink.light` | 1 |
| `state:style.interface.footerLink.light` | 1 |
| `state:style.interface.footerLink.dark` | 1 |
| `state:style.interface.linkButton.light` | 1 |
| `state:style.interface.linkButton.dark` | 1 |
| `state:style.interface.badgeText.light` | 1 |
| `state:style.interface.badgeText.dark` | 1 |
| `state:style.interface.slideTitle.light` | 1 |
| `state:style.interface.slideTitle.dark` | 1 |
| `state:style.interface.primaryText.dark` | 1 |
| `state:style.interface.backgroundSelected.light` | 1 |
| `state:style.interface.backgroundProducts.light` | 1 |
| `state:style.interface.heading.light` | 1 |
| `state:style.interface.content.light` | 1 |
| `state:style.interface.textColor.dark` | 1 |
| `state:style.interface.controlBackground.dark` | 1 |
| `state:style.interface.cardBg.dark` | 1 |
| `state:style.interface.text2.dark` | 1 |
| `state:style.interface.drawerBg.dark` | 1 |
| `state:style.interface.footerText.light` | 1 |
| `state:style.interface.footerText.dark` | 1 |
| `state:style.interface.iconBg.light` | 1 |
| `state:style.interface.dark.light` | 1 |
| `state:style.interface.darkThd.light` | 1 |
| `state:style.interface.productSelectorBorder.light` | 1 |
| `state:style.interface.brandTextColor.light` | 1 |
| `state:style.interface.productBgUnselected.light` | 1 |
| `state:style.interface.text2Product.light` | 1 |
| `state:style.interface.lightText80.light` | 1 |
| `state:style.interface.lightText30.light` | 1 |
| `state:style.interface.lightText40.light` | 1 |
| `state:style.interface.freeTrialBg.light` | 1 |
| `state:style.interface.freeTrialBorder.light` | 1 |
| `state:style.interface.prodBorder.light` | 1 |
| `state:style.interface.prodSelectedBorder.light` | 1 |
| `state:style.interface.softBlack.light` | 1 |
| `state:style.interface.toggleOff.light` | 1 |
| `state:style.interface.inverseFaded.light` | 1 |
| `state:style.interface.lightBlue.light` | 1 |
| `state:style.interface.timeline.light` | 1 |
| `state:style.interface.periodlySelectedText.light` | 1 |
| `state:style.interface.periodlyText.light` | 1 |
| `state:style.interface.priceSelectedText.light` | 1 |
| `state:style.interface.priceText.light` | 1 |
| `state:style.interface.alt.light` | 1 |
| `state:style.interface.divider.light` | 1 |
| `state:style.interface.textWhite60.light` | 1 |
| `state:style.interface.iconUnselected.light` | 1 |
| `state:style.interface.activeToggle.light` | 1 |
| `state:style.interface.backgroundDiamond.light` | 1 |
| `state:style.interface.primaryDiamond.light` | 1 |
| `state:style.interface.textDiamond.light` | 1 |
| `state:style.interface.prodBgDiamond.light` | 1 |
| `state:style.interface.tablePremiumHighlight.light` | 1 |
| `state:style.interface.badgeTableFree.light` | 1 |
| `state:style.interface.buttonForeground.light` | 1 |
| `state:style.interface.platinum.light` | 1 |
| `state:style.interface.basicPrimary.light` | 1 |
| `state:style.interface.proPrimary.light` | 1 |
| `state:style.interface.maxPrimary.light` | 1 |
| `state:style.interface.bulletsBg.light` | 1 |
| `state:style.interface.basicButton.light` | 1 |
| `state:style.interface.textButtonLabel.light` | 1 |
| `state:style.interface.productBorderDefault.light` | 1 |
| `state:style.interface.productText.light` | 1 |
| `state:style.interface.selectedProductText.light` | 1 |
| `state:style.interface.toggleOnBg.light` | 1 |
| `state:style.interface.secondaryFont.light` | 1 |
| `state:style.interface.secondaryFont.dark` | 1 |
| `state:style.interface.adaptiveWhite.light` | 1 |
| `state:style.interface.adaptiveWhite.dark` | 1 |
| `state:style.interface.text2Tab.light` | 1 |
| `state:style.interface.pickerBg.dark` | 1 |
| `state:style.interface.tabBg.dark` | 1 |
| `state:style.interface.reversed.light` | 1 |
| `state:style.interface.reversed.dark` | 1 |
| `state:style.interface.selectedTab.light` | 1 |
| `state:style.interface.selectedTab.dark` | 1 |
| `state:style.interface.textAlt.light` | 1 |
| `state:style.interface.textAltLight.light` | 1 |
| `state:style.interface.badge.light` | 1 |
| `state:style.interface.secondaryButton.light` | 1 |
| `state:style.interface.textAlt.dark` | 1 |
| `state:style.interface.textLight.dark` | 1 |
| `state:style.interface.textAltLight.dark` | 1 |
| `state:style.interface.badge.dark` | 1 |
| `state:style.interface.secondaryButton.dark` | 1 |
| `state:style.interface.productSelectorBg.dark` | 1 |
| `state:style.interface.iconBorder.dark` | 1 |

## Conditional operators seen

Conditional values use `{type: conditional, options: [{condition: {stateId, operator, value}, value: ...}, ...]}`.

Operators in use:

- `=` (2972×)
- `>` (210×)
- `<=` (112×)
- `!=` (67×)
- `<` (6×)
- `>=` (6×)
- `contains` (2×)

## Units

- `px` (26021×)
- `%` (3836×)
- `vw` (1035×)
- `none` (357×)
- `vh` (208×)
- `raw` (184×)

## Image hosts seen

- `user-content.superwalleditor.com` (1279×)
- `static.superwallassets.com` (127×)
- `skaiweather.com` (2×)
- `notability.com` (1×)

---
Regenerate with `python3 scripts/mine_full_grammar.py`.
