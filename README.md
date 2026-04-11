# superwall-vibedesign-kit

> Reverse-engineered Superwall paywall toolkit. Read, write, and template any
> paywall programmatically — the same API the Superwall web editor uses.

The official [Superwall MCP](https://superwall.com) only lets you create
paywall *records* — it can't touch design, content, or layout. This kit
does everything the web editor does, because it calls the same tRPC
endpoints the editor calls. You can pull a paywall as JSON, edit it in
Python, and push it back with one command.

It also contains a **complete reverse-engineered schema** for Superwall's
v4 paywall format, distilled from analyzing every public template in their
library.

## Why

Building paywalls by hand in the Superwall editor is slow, non-scriptable,
and not AI-automatable. If you ship many apps (or want an AI to design
paywalls from a screenshot), you need code access. The official API
doesn't provide it. This does.

## What's inside

```
src/superwall_kit/     Python client
  auth.py                Loads session cookie + CSRF from .secrets/
  client.py              Typed tRPC wrapper: get_snapshot, push, etc.

data/
  catalog/               Machine-readable schema extracted from 196 templates
                         (node types, property shapes, state vars, conditional ops)
  templates/             [gitignored] Your locally-pulled Superwall templates

docs/
  METHOD.md              Endpoint catalog + tRPC wire format + auth
  SCHEMA.md              Complete v4 snapshot schema reference
  PATTERNS.md            Design pattern synthesis across 196 templates
  patterns-bucket-*.md   Raw per-cluster analyses

scripts/
  pull_templates.py      Bulk pull every template in your workspace
  build_catalog.py       Regenerate data/catalog from data/templates
```

## Quickstart

```bash
git clone https://github.com/azeribatman/superwall-vibedesign-kit
cd superwall-vibedesign-kit
```

### 1. Get your auth

In Chrome, log into Superwall and open any paywall editor. Open DevTools
→ Network → click any `/api/trpc/` request → right-click → **Copy as cURL**.

From that cURL, extract:

- The full `Cookie:` header string → save to `.secrets/cookie.txt`
- The `anti-csrf:` header value → save to `.secrets/csrf.txt`

```bash
mkdir -p .secrets
pbpaste > .secrets/cookie.txt   # or paste manually
echo "YOUR_CSRF_TOKEN" > .secrets/csrf.txt
chmod 600 .secrets/*
```

Both files are `.gitignore`d.

### 2. Pull a paywall

```python
from superwall_kit import SuperwallClient

c = SuperwallClient()
snap = c.get_snapshot(paywall_id=206207)
print(snap["version"])
print(len(snap["snapshot"]["store"]), "nodes")
```

### 3. Edit + push

```python
store = snap["snapshot"]["store"]

# Change the brand color (theme token)
store["state:style.interface.primary.light"]["defaultValue"]["value"] = "#8C59D9ff"

# Change the paywall name
store["paywall:paywall"]["name"] = "My New Paywall"

# Push it live (prepare + promote in one call)
new_version = c.push_snapshot(
    paywall_id=206207,
    application_id=37837,
    snapshot=snap["snapshot"],
)
print("now on version", new_version)
```

### 4. Bulk-pull the template library

```bash
python3 scripts/pull_templates.py   # ~2 min, saves to data/templates/
python3 scripts/build_catalog.py    # regenerates data/catalog/
```

## Schema highlights

(See `docs/SCHEMA.md` for the full reference.)

Paywall snapshots are flat key-value stores. Every record — nodes, states,
theme tokens, products — lives in `snapshot.store["<record_id>"]`. The node
tree is formed via `parentId` pointers, not nesting.

**12 native node types:**
`stack`, `text`, `img`, `icon`, `navigation`, `video`, `drawer`,
`multiple-choice`, `choice-item`, `lottie`, `indicator`, `indicator-item`.

**65 CSS/prop keys.** Nearly every real CSS property plus `prop:stack`,
`prop:navigation`, `prop:click-behavior`, `prop:text`, etc.

**Every value is one of 4 wrapper types:**
- `literal` — static value
- `conditional` — switch on state with query rules (8 operators)
- `referential` — pull from a state variable
- `tombstone` — use default

**15+ theme tokens** exist under `state:style.interface.*`, including the
non-obvious ones designers use for contrast: `productSelectedBg`,
`elementBackground`, `cardBg`, `ctaText`, `borderSelected`.

**Navigation state** is exposed as `state:node.<navId>.currentIndex`. You
can both *query* it in conditionals and *set* it from click behaviors —
this is how "jump to screen 3" is implemented.

## Design patterns (from 196 templates)

See `docs/PATTERNS.md` for the full writeup. Highlights:

- Most "real" paywalls are single-page product pickers. Multi-screen is
  rare (<10% of templates).
- Designers fake drawers with `state.modalOpen` + plain stacks — the
  native `drawer` node is used by only 2 templates out of 196.
- Only 2 templates use the native `multiple-choice` quiz components. The
  rest fake quizzes with stacks + `state.question*` bools.
- Clever trick: 5 FAQ templates share a **single scalar**
  `state:params.answerOpened` — opening one row auto-closes the previous.
- `state.enableFreeTrial` is a common canonical switch: flips selected
  product + rewrites CTA copy + shows/hides trial UI in one toggle.

## Disclaimer

- This project uses **undocumented internal Superwall APIs**. They can
  break whenever Superwall redeploys their frontend. Yearly maintenance
  expected.
- Not affiliated with, endorsed by, or supported by Superwall. This is
  an independent research project. **Review Superwall's Terms of
  Service before using this in production.**
- All template analysis in `docs/PATTERNS.md` and `docs/patterns-*.md` is
  derived from aggregate schema/structure. No template content is
  redistributed in this repo — `data/templates/` is gitignored and must
  be pulled from your own Superwall workspace.
- Cookies expire. Rotate them when you start seeing `HTTP 403 FORBIDDEN`.
- Auth is workspace-scoped. Switching Superwall orgs requires a fresh
  cookie export.

## License

MIT. See `LICENSE`.

## Contributing

PRs welcome. The schema catalog is the most valuable part — if you find a
node type, property, state variable, or conditional pattern not documented
in `docs/SCHEMA.md`, please open an issue or PR with an example.
