# superwall-vibedesign-kit

> **Design Superwall paywalls by talking to Claude.** Change colors, rewrite
> copy, add screens, rebuild from a screenshot — all in plain English. No
> dragging elements around the editor.

The official Superwall MCP can create paywall *records*, but it can't touch
design, content, layout, or conditional logic. This toolkit fills that gap
by calling the same tRPC endpoints the Superwall web editor uses, wrapped
in a Claude Code plugin so you never see code unless you want to.

## What you can do

> "Change my paywall's primary color to purple"

> "Rebuild this paywall to match this screenshot" *(attach image)*

> "Add a trial reminder screen that only shows if the user is eligible"

> "Duplicate the Blinkist template into my new app and swap the products"

> "Make the CTA button text white so it reads on the purple background"

Claude does the technical work. You just describe what you want.

---

## Install (for vibe coders — 2 minutes)

You need [Claude Code](https://claude.com/claude-code) installed.

```bash
git clone https://github.com/azeribatman/superwall-vibedesign-kit
cd superwall-vibedesign-kit
claude
```

That's it. When Claude Code opens in this folder, it auto-reads
`CLAUDE.md` and instantly knows how to help you with Superwall.

The first thing you ask (e.g. "pull my paywall") will walk you through a
30-second login. One Copy-as-cURL from Chrome DevTools, done.

---

## First command to try

```
change my paywall 206207 primary color to #8C59D9
```

Claude will:
1. Walk you through logging in (if not already)
2. Pull your paywall
3. Show you what's inside
4. Make the change
5. Confirm before pushing
6. Push it live

---

## For devs who want the Python library directly

```python
import sys; sys.path.insert(0, 'src')
from superwall_kit import SuperwallClient

c = SuperwallClient()

# Pull
snap = c.get_snapshot(paywall_id=206207)

# Edit — it's a flat dict of records
store = snap['snapshot']['store']
store['state:style.interface.primary.light']['defaultValue']['value'] = '#8C59D9ff'
store['paywall:paywall']['name'] = 'My New Paywall'

# Push (prepare + promote in one call)
new_version = c.push_snapshot(
    paywall_id=206207,
    application_id=37837,
    snapshot=snap['snapshot'],
)
```

See `docs/SCHEMA.md` for the full schema reference,
`docs/METHOD.md` for the tRPC endpoint catalog, and `docs/PATTERNS.md`
for design patterns across 196 real templates.

---

## Authentication (one-time, 30 seconds)

We don't read your system cookie jar. You paste one cURL from Chrome
DevTools and we extract the session cookie. That's it.

1. Open Superwall in Chrome, log in to the workspace you want to edit
2. Open any paywall in the editor
3. Open DevTools → **Network** tab → reload
4. Click any request with `/api/trpc/` in the URL
5. Right-click → **Copy** → **Copy as cURL**
6. Either:
   - Paste it directly into Claude Code chat (Claude saves it), or
   - Run `python3 scripts/login.py` and paste when prompted

Saved to `.secrets/cookie.txt` (gitignored). The anti-CSRF token lives
inside the cookie, so no separate file needed.

---

## What's in this repo

```
CLAUDE.md                     Instructions Claude reads on entry
.claude-plugin/plugin.json    Plugin metadata
skills/superwall/SKILL.md     Auto-activating skill when you mention paywalls
commands/sw-login.md          /sw-login — walks through auth
commands/sw-pull.md           /sw-pull <id> — pull a paywall
commands/sw-push.md           /sw-push <id> <app> — push changes

src/superwall_kit/            Python client (auth, tRPC wrapper)
  auth.py
  client.py

scripts/
  login.py                    Paste-a-cURL login flow
  pull_templates.py           Bulk pull every v4 template in your workspace
  build_catalog.py            Regenerate schema catalog

data/
  catalog/                    Machine-readable schema (committed)
  templates/                  Your pulled templates (gitignored)
  pulled/                     Paywalls Claude has pulled for editing (gitignored)

docs/
  METHOD.md                   tRPC endpoint reference
  SCHEMA.md                   Complete v4 snapshot schema
  PATTERNS.md                 Design patterns from 196 templates
  patterns-bucket-*.md        Raw per-bucket analyses
```

---

## Schema highlights

- **12 node types**: `stack`, `text`, `img`, `icon`, `navigation`,
  `video`, `drawer`, `multiple-choice`, `choice-item`, `lottie`,
  `indicator`, `indicator-item`
- **65 CSS/prop keys** — everything the editor supports
- **4 value wrappers**: `literal`, `conditional`, `referential`, `tombstone`
- **8 conditional operators**: `=`, `!=`, `<`, `<=`, `>`, `>=`, `contains`, `?`
- **15+ theme tokens** under `state:style.interface.*` — including the
  non-obvious ones: `productSelectedBg`, `elementBackground`, `cardBg`,
  `ctaText`, `borderSelected`
- **Navigation state**: `state:node.<navId>.currentIndex` — you can read
  AND write this from click behaviors, enabling "jump to screen 3"

---

## Design pattern insights

From analyzing all 196 public Superwall v4 templates:

- Most real paywalls are **single-page product pickers**. Multi-screen
  flows are in <10% of templates.
- Designers **fake drawers** with `state.modalOpen` + plain stacks — the
  native `drawer` node is used by only 2 templates.
- Only 2 templates use native `multiple-choice` quiz components. The rest
  fake quizzes with stacks + `state.question*` bools.
- Clever trick: 5 FAQ templates share a single scalar
  `state:params.answerOpened` — opening one row auto-closes the previous.
- `state.enableFreeTrial` is a canonical switch: flips selected product +
  rewrites CTA copy + shows/hides trial UI in one toggle.

See `docs/PATTERNS.md` for the full writeup.

---

## Disclaimer

- This project uses **undocumented internal Superwall APIs**. They can
  break whenever Superwall redeploys. Yearly maintenance expected.
- Not affiliated with, endorsed by, or supported by Superwall. This is
  an independent research project. **Review Superwall's Terms of
  Service before using in production.**
- No template content is redistributed. `data/templates/` is gitignored
  and must be pulled from your own Superwall workspace with
  `scripts/pull_templates.py`.
- Cookies expire. If you start seeing `HTTP 403 FORBIDDEN`, re-run
  `/sw-login`.
- Auth is workspace-scoped. Switching Superwall workspaces requires a
  fresh login.

---

## License

MIT. See `LICENSE`.

## Contributing

PRs welcome. The schema catalog is the most valuable part — if you find
a node type, property, state variable, or conditional pattern not
documented in `docs/SCHEMA.md`, please open an issue or PR with an
example template.
