# superwall-vibedesign-kit

**Edit your Superwall paywalls by talking to Claude. In plain English.**

No code. No dragging stuff around the editor. Just say what you want.

> "make my paywall purple"

> "add a trial screen"

> "rebuild this to match this screenshot" *(attach image)*

> "change the button text to white"

Claude handles everything under the hood.

---

## How it works (3 steps)

### Step 1: Clone this repo and open Claude Code

```bash
git clone https://github.com/azeribatman/superwall-vibedesign-kit
cd superwall-vibedesign-kit
claude
```

Don't have Claude Code? Get it at [claude.com/claude-code](https://claude.com/claude-code)

### Step 2: Connect your Superwall account (one time, 20 seconds)

Claude needs two tokens from your Superwall account so it can pull/push paywalls on your behalf. **No passwords, no browser extensions** — they live locally in `.secrets/cookie.txt` and are never uploaded anywhere.

Easiest way:

1. **Open [superwall.com](https://superwall.com) in Chrome** and log in to your workspace.
2. **Open the editor for any paywall** (or any page on superwall.com — doesn't matter which).
3. **Open DevTools** (Mac: `Cmd + Option + I`, Windows/Linux: `Ctrl + Shift + I`) and click the **Console** tab.
4. **Paste this and hit Enter:**

   ```js
   copy(`accounts_superwall_token=${document.cookie.match(/accounts_superwall_token=([^;]+)/)[1]}\npaywall_sAntiCsrfToken=${document.cookie.match(/paywall_sAntiCsrfToken=([^;]+)/)[1]}`)
   ```

   The console will say `undefined` — that's fine, it just means the snippet ran and copied 2 lines to your clipboard.

5. **Paste those 2 lines back to Claude.** That's it. Claude saves them and you're connected.

**Tokens expire roughly every 30 days.** When they do, Claude will tell you (`HTTP 403`) and you just run the same 20-second snippet again.

> ℹ️ Already logged into the wrong workspace? Open superwall.com → top-left dropdown → switch workspace → log in to the right one → re-run the snippet.

#### Alternative: Copy-as-cURL

If the snippet above doesn't work in your browser (some Chrome settings disable `copy()`), there's a backup path:

1. Open DevTools → **Network** tab on superwall.com.
2. Click any request that starts with `/api/trpc/...`.
3. Right-click → **Copy** → **Copy as cURL**.
4. Paste the whole cURL into Claude — it'll extract the tokens automatically.

### Step 3: Just talk

> **Tip:** Paywall and app IDs live in the Superwall editor URL — `https://superwall.com/applications/<APP_ID>/paywalls/<PAYWALL_ID>`. Grab them from any paywall in your dashboard.

Say things like:

| What you say | What happens |
|---|---|
| "pull my paywall 206207" | Downloads your paywall so Claude can see it |
| "change the primary color to #8C59D9" | Updates the brand color |
| "make the background white" | Flips the theme |
| "add a screen for users with a free trial" | Adds a conditional screen |
| "change the CTA text to white" | Fixes contrast on buttons |
| "rebuild this from this screenshot" *(attach image)* | Matches a reference image |
| "build me a swipable Citizen-style paywall in app 12345" | Generates the multi-page carousel from scratch |
| "duplicate the Blinkist template for my app" | Copies a template + swaps products |

Claude always shows you what it's about to change and asks before
pushing anything live.

---

## What's included

This repo has a **complete schema reference** for how Superwall paywalls
are built internally — every node type, every property, every conditional
operator. Claude reads this so you don't have to.

When you need a template, Claude **pulls it fresh from Superwall** using
your account. All 196+ public templates are accessible on demand — no
stale copies, always up to date. Just say "show me the templates" or
"use the Blinkist template as a starting point".

---

## FAQ

**Do I need to know how to code?**
No. Claude handles everything. You just describe what you want in
normal English.

**What's Claude Code?**
It's a CLI tool from Anthropic that lets you talk to Claude while it
reads and edits files. Think of it as an AI assistant that lives in
your terminal. Get it at [claude.com/claude-code](https://claude.com/claude-code)

**Is this official Superwall software?**
No. This is an independent project that uses Superwall's internal API
(the same one their web editor uses). It's not endorsed by Superwall.

**What can't it do?**
It can't create a brand new Superwall account, manage billing, or do
things outside the paywall editor (like campaigns or webhooks). For
those, use the official Superwall dashboard or their MCP.

**My tokens expired / I'm getting errors**
Re-run the login flow. Tokens expire roughly monthly. Claude will tell
you when it happens.

**Can I use this with a different AI tool?**
The Python library (`src/superwall_kit/`) works standalone. But the
magic is in the Claude Code integration — the `CLAUDE.md` file teaches
Claude exactly how to use it.

**Is this safe?**
Your tokens are stored locally in `.secrets/` (gitignored). Claude
always asks before pushing changes. You can review every change before
it goes live.

---

## For developers

If you want to use the Python library directly (without Claude Code):

```python
import sys; sys.path.insert(0, 'src')
from superwall_kit import SuperwallClient

c = SuperwallClient()

# Pull (your paywall ID — find it in the editor URL)
snap = c.get_snapshot(paywall_id=YOUR_PAYWALL_ID)

# Edit
store = snap['snapshot']['store']
store['state:style.interface.primary.light']['defaultValue']['value'] = '#8C59D9ff'

# Push
c.push_snapshot(
    paywall_id=YOUR_PAYWALL_ID,
    application_id=YOUR_APP_ID,
    snapshot=snap['snapshot'],
)
```

Reference docs:
- `docs/SCHEMA.md` — complete snapshot schema
- `docs/METHOD.md` — tRPC endpoints + auth
- `docs/PATTERNS.md` — design patterns from 196 templates

---

## Disclaimer

This project uses undocumented internal Superwall APIs. They can change
without notice. Not affiliated with or endorsed by Superwall. Review
their Terms of Service before using in production. Tokens expire monthly.

## License

MIT
