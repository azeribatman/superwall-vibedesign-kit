# superwall-vibedesign-kit

You are helping a user edit Superwall paywalls by talking to them in plain
English. This repo is a toolkit that reads/writes Superwall paywalls via
Superwall's internal tRPC API (not the public MCP, which can't touch
paywall design).

## Your job

When the user asks you to do anything with Superwall paywalls, use the
tools in this repo to get it done. Don't make them paste JSON, hand-edit
files, or learn the schema. Do the technical work and talk to them in
plain language.

## First thing to check: auth

Before any operation, check if `.secrets/cookie.txt` exists. If it doesn't,
the user hasn't logged in yet and you need to walk them through it:

> I need to connect to your Superwall account first. It takes 30 seconds:
>
> 1. Open Superwall in Chrome, log in to the workspace whose paywalls
>    you want to edit.
> 2. Open any paywall in the editor.
> 3. Open DevTools (Cmd+Opt+I) → **Network** tab → reload the page.
> 4. Click any request in the list whose URL contains `/api/trpc/`.
> 5. Right-click it → **Copy** → **Copy as cURL**.
> 6. Paste the entire cURL into chat here.

When the user pastes the cURL, extract the cookie (look for `-b '...'`,
`--cookie '...'`, or `-H 'cookie: ...'` in the text), save it to
`.secrets/cookie.txt`, and run a smoke test:

```bash
mkdir -p .secrets
# write the extracted cookie string to .secrets/cookie.txt
python3 -c "
import sys; sys.path.insert(0,'src')
from superwall_kit import SuperwallClient
c = SuperwallClient()
print('logged in as user', c.query('user.getSelf', {}).get('id','?'))
"
```

If it says "logged in", confirm to the user: "✅ connected, what do you
want to do?"

## How to do things

### Pull a paywall

The user will give you a paywall ID (or say "my paywall" — ask them for
the ID). Paywall IDs appear in editor URLs like
`https://superwall.com/applications/<APP>/paywalls/<PAYWALL>`.

```python
import sys; sys.path.insert(0, 'src')
from superwall_kit import SuperwallClient
c = SuperwallClient()
snap = c.get_snapshot(paywall_id=<ID>)
# snap['snapshot']['store'] is the full design
```

Save pulled snapshots to `data/pulled/<id>.json` so you can mutate them
between steps without re-pulling.

### Edit

The snapshot is a flat dict keyed by record ID. Key concepts:

- **Theme colors** live in `state:style.interface.<token>.light` /
  `.dark`. Tokens include `primary`, `background`, `text`, `ctaText`,
  `border`, `productSelectedBg`, `cardBg`, `elementBackground`,
  `secondary`, `borderSelected`.
- **Nodes** have type `stack`, `text`, `img`, `icon`, `navigation`,
  `video`, `drawer`, `multiple-choice`, `lottie`, `indicator`.
- **Properties** live in both `node['properties']` and
  `node['defaultProperties']` — check both when reading; write to
  `properties`.
- **Values** are wrapped: `{type: "literal", value: {...}}`,
  `{type: "conditional", options: [...]}`, `{type: "referential",
  stateId: "..."}`, `{type: "tombstone"}`.
- **Conditionals** switch on state. Operators: `=`, `!=`, `<`, `<=`,
  `>`, `>=`, `contains`, `?`.
- **Products** are in `paywall_product:<key>` records with an
  `identifier` field (like `com.your.annual`).

The full schema reference is in `docs/SCHEMA.md` — **read it before
making non-trivial edits**. Design patterns across 196 templates are
catalogued in `docs/PATTERNS.md`.

### Push

```python
new_version = c.push_snapshot(
    paywall_id=<ID>,
    application_id=<APP_ID>,
    snapshot=snap['snapshot'],
)
```

This calls `prepareSnapshotForPromotion` then `promoteFromSnapshot`.
**Always show the user a summary of changes and get explicit confirmation
before pushing anything substantial.**

## Rules

1. **Always pull before editing.** Never construct a snapshot from scratch
   unless duplicating a known template from `data/templates/`.
2. **Preserve unmodified records.** Only change what the user asked for.
3. **Confirm destructive or substantial changes.** Show a summary first.
4. **Don't dump JSON at the user.** They want plain English. Summarize.
5. **If push returns 403**, the cookie is for a different workspace.
   Tell the user to `/sw-login` in the right one.
6. **Don't add backwards-compat hacks** — mutate cleanly. This is a
   research project, not production code.

## Reference files to read when needed

- `docs/SCHEMA.md` — complete schema (read before non-trivial edits)
- `docs/METHOD.md` — tRPC endpoints + auth + wire format
- `docs/PATTERNS.md` — design patterns from 196 templates
- `data/catalog/node_types.json`, `properties.json`, `state_ids.json`,
  `conditional_fields.json` — machine-readable schema catalogs
- `data/templates/<id>.json` — pulled templates (if user has run
  `scripts/pull_templates.py`)

## Typical requests + how to handle them

**"Change my paywall's button color to green"** → pull, update
`state:style.interface.primary.light` default value, push.

**"Rebuild this paywall from this screenshot"** → find the closest
template archetype in `data/catalog/templates_index.json`, pull it, rewrite
text/colors/products to match the screenshot, push. Use
`docs/PATTERNS.md` to pick the right starting template.

**"Add a trial reminder screen"** → pull, find the navigation node, add a
new page stack as a sibling of existing pages, wrap it in a conditional
`css:display` on `state:products.hasIntroductoryOffer`, push.

**"Duplicate a template for my new app"** → pull template snapshot,
update `paywall:paywall` fields (name/identifier/databaseId), remap
`paywall_product:*` identifiers, push to target paywall.

**"Make the CTA text white"** → check if `state:style.interface.ctaText`
exists — if so, use it. Otherwise add explicit white `css:color` literal
on the Continue text nodes inside `Purchase Selected` stacks.

## Don't

- Don't ask the user to edit JSON by hand
- Don't make them understand the schema — you handle it
- Don't push without pulling first
- Don't push without summarizing changes
- Don't add new dependencies — stdlib + the existing client only
