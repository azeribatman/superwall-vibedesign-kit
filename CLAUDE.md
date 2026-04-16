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
the user hasn't logged in yet. Walk them through it:

> I need to connect to your Superwall account first. Takes 20 seconds:
>
> 1. Open **superwall.com** in Chrome and log in.
> 2. Open DevTools (Cmd+Opt+I) → **Console** tab.
> 3. Paste this snippet and press Enter:
>
> ```js
> copy(`accounts_superwall_token=${document.cookie.match(/accounts_superwall_token=([^;]+)/)[1]}\npaywall_sAntiCsrfToken=${document.cookie.match(/paywall_sAntiCsrfToken=([^;]+)/)[1]}`)
> ```
>
> 4. It copies 2 tokens to your clipboard. Paste them here.

When the user pastes 2 lines starting with `accounts_superwall_token=`
and `paywall_sAntiCsrfToken=`, extract the values, build the minimal
cookie string, and save:

```bash
mkdir -p .secrets
cat > .secrets/cookie.txt << 'COOKIE'
accounts_superwall_token=<TOKEN_VALUE>; paywall_sAntiCsrfToken=<CSRF_VALUE>
COOKIE
chmod 600 .secrets/cookie.txt
```

Then smoke test:

```bash
python3 -c "
import sys; sys.path.insert(0,'src')
from superwall_kit import SuperwallClient
c = SuperwallClient()
u = c.query('user.getSelf', {})
print('logged in:', u.get('user',{}).get('id', '?'))
"
```

If it prints a user id, confirm: "Connected! What do you want to do?"

**Fallback:** the user can also paste a full Copy-as-cURL from DevTools
Network tab. Parse `-b '...'` to find the cookie string, then extract
the same 2 tokens. Both methods work — `scripts/login.py` handles both.

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

Templates are NOT shipped with the repo. Pull them on demand from
Superwall using the authenticated client:

```python
templates = c.query('blitzMigration.paywalls.getPaywallTemplates',
    {'take': 250, 'skip': 0, 'applicationId': APP_ID, 'v4Only': True})
# returns {'paywallTemplates': [...], 'count': 196, ...}
# each template has id, name, previews, templateCategories
# fetch full snapshot: c.get_snapshot(template_id)
```

Or bulk-pull all: `python3 scripts/pull_templates.py` (saves to
`data/templates/` which is gitignored).

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
