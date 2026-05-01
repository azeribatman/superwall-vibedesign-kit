---
name: superwall
description: This skill activates when the user mentions Superwall, paywalls, or asks to edit, design, change colors/text, rebuild, duplicate, pull, push, list, or modify anything related to Superwall paywalls. Use phrases like "my paywall", "change the paywall", "edit the Superwall", "rebuild this paywall", "make the CTA purple", "add a trial screen", "duplicate this template", or anything referencing `superwall.com`, `paywall id`, or `application id`.
version: 0.1.0
license: MIT
---

# Superwall Paywall Editing

You have access to `superwall-vibedesign-kit` — a Python toolkit that reads
and writes Superwall paywalls via Superwall's internal tRPC API. Use this
when the user wants to do anything to a Superwall paywall beyond what the
official Superwall MCP can do (the official MCP only handles metadata, not
design/content/layout).

## When to use this skill

- User wants to edit any paywall content, colors, text, layout, or screens
- User wants to pull/download a paywall as JSON
- User wants to rebuild a paywall from a screenshot
- User wants to duplicate or swap a template
- User asks "change my Superwall paywall" or similar

## When NOT to use this skill

- User wants to list/archive paywall records (use the official
  Superwall MCP if available — it's simpler for those)
- User wants to manage products, campaigns, entitlements, webhooks (those
  are in the official MCP)

> Note: creating a brand-new paywall record is **not** available in this
> kit's API surface either. The user must create the empty paywall via
> the Superwall dashboard UI (one click in the sidebar), then we push
> the full snapshot here. See `docs/GOTCHAS.md` for the full workflow.

## First-run check: is the user authenticated?

Before any operation, verify `.secrets/cookie.txt` exists in the repo
root. If it doesn't, the user needs to run the login flow first.

```bash
test -f .secrets/cookie.txt
```

If missing, tell the user:

> I need to authenticate with your Superwall account first. Please:
>
> 1. Open Superwall in Chrome and log in
> 2. Navigate to any paywall editor
> 3. Open DevTools → Network tab → click any `/api/trpc/` request
> 4. Right-click that request → Copy → **Copy as cURL**
> 5. Run: `python3 scripts/login.py`
> 6. Paste the cURL when prompted and press Ctrl+D

Then run `python3 scripts/login.py` after they've pasted.

## Core operations

All operations go through the `SuperwallClient` in `src/superwall_kit/`.
Don't write new HTTP code — use the client.

### Pulling a paywall

```python
import sys
sys.path.insert(0, 'src')
from superwall_kit import SuperwallClient

c = SuperwallClient()
snap = c.get_snapshot(paywall_id=206207)
# snap['snapshot']['store'] is the full design
```

If you don't know the paywall ID, ask the user — it's in the Superwall
editor URL: `https://superwall.com/applications/<app>/paywalls/<paywall_id>`.
You also need the `application_id` from the same URL for push operations.

### Editing the snapshot

The snapshot is a flat key-value store keyed by record id. Records include
nodes (`node:<hash>`), states (`state:<path>`), products, and theme tokens.
Read `docs/SCHEMA.md` for the complete schema reference — it's essential
context before making any non-trivial edit.

Common edits:

- **Change theme colors**: modify `store['state:style.interface.<token>.light']['defaultValue']['value']` (or `.dark`). Tokens include `primary`, `background`, `text`, `ctaText`, `border`, `productSelectedBg`.
- **Replace text strings**: walk the store and find nodes where `properties/prop:text` wraps a `property-text` with the source string; replace the inner `value`.
- **Swap product identifiers**: update `store['paywall_product:<key>']['identifier']`.
- **Hide a screen conditionally**: add `css:display` conditional to the page node using `state:products.hasIntroductoryOffer` or similar.
- **Jump to a specific screen**: change click behaviors to `set-state` on `state:node.<navId>.currentIndex`.

### Pushing changes

```python
new_version = c.push_snapshot(
    paywall_id=206207,
    application_id=37837,
    snapshot=snap['snapshot'],
)
print(f"live at version {new_version}")
```

This calls `prepareSnapshotForPromotion` then `promoteFromSnapshot`. The
editor will show the new version immediately.

## Reference material

Before doing anything non-trivial, read these files in the repo:

- `docs/GOTCHAS.md` — **READ FIRST** if you're about to build/push a paywall. Documents which API endpoints don't exist, required-but-easy-to-miss validation fields, schema quirks (icon-name casing, action-type enum, properties that crash the editor), layout traps, and the iOS SDK consumer pattern for decline chains.
- `docs/METHOD.md` — tRPC endpoints and auth
- `docs/SCHEMA.md` — complete v4 snapshot schema (nodes, properties, states, conditionals)
- `docs/PATTERNS.md` — design patterns observed across 196 templates
- `data/catalog/` — machine-readable schema (node types, property shapes, state variables)
- `data/templates/` — 196 pulled templates if available (bulk-pull with `scripts/pull_templates.py`)

## Safety rules

1. **Always pull-before-push.** Never construct a snapshot from scratch
   unless duplicating a known template. Mutate existing structures.
2. **Preserve unmodified records.** Only change what the user asked for.
3. **Validate the user's paywall ID before pushing.** A wrong ID
   overwrites the wrong paywall.
4. **Show the user what you're about to change** before pushing if the
   change is substantial (new screens, deleted nodes, color changes).
5. **Respect workspace boundaries.** If a write returns `HTTP 403
   FORBIDDEN`, the cookie is for a different Superwall workspace than
   the target paywall. Ask the user to re-authenticate in the right one.
6. **The API can accept a snapshot that crashes the editor.** Push
   succeeding does not mean the paywall renders. The editor's
   "Something's gone wrong" page typically signals an unrecognized
   property (e.g. lowercase icon names, `css:webkitLineClamp`) or a
   bad action type. See `docs/GOTCHAS.md` for the running list. After
   any non-trivial push, ask the user to reload the editor and
   confirm.

## Typical workflows

### "Change my paywall's button color to green"

1. Pull the paywall
2. Update `state:style.interface.primary.light` defaultValue to `#22c55eff`
3. Push
4. Tell the user the new version number

### "Duplicate this template for Alavai"

1. Find the template in `data/templates/` or pull it
2. Update `paywall:paywall` name + identifier
3. Update `paywallId` and `applicationId` in the request
4. Remap `paywall_product:*` identifiers to Alavai's product IDs
5. Push to target paywall

### "Rebuild this paywall from this screenshot"

1. Describe the screenshot's layout in terms of sections
2. Find the closest-matching template in `data/catalog/templates_index.json`
   (by node count, nodeTypes)
3. Pull that template as a starting point
4. Rewrite text/colors/products to match the screenshot
5. Push

### "Add a screen that says X if user has no trial"

1. Pull
2. Find the navigation node, copy an existing page as a sibling
3. Add a conditional `css:display` using
   `state:products.hasIntroductoryOffer = false`
4. Rewrite text content
5. Push

### "Build a brand-new paywall from scratch"

There's no working `paywalls.createPaywall` endpoint in the API.
Instead:

1. Ask the user to create an empty paywall in the Superwall web
   dashboard (or duplicate any existing one) and send you the new
   paywall ID.
2. Pull that ID's snapshot.
3. Reset the platform records: `paywall:paywall.name`,
   `featureGating`, `localizationProvider`; and every
   `paywall_product:*` to a real ASC identifier (literal `"missing"`
   is rejected).
4. Drop all existing `node:*` records and build a fresh node tree
   using the helper patterns documented in `docs/SCHEMA.md` and the
   gotchas in `docs/GOTCHAS.md`.
5. Push with `prepare` + `promote`. Both calls require non-null
   `title` and `description` strings.
6. Ask the user to reload the editor and confirm the layout renders
   (no "Something's gone wrong"). If it does, see `docs/GOTCHAS.md`
   for the running list of editor-crash causes.
