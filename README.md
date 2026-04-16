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

When you ask Claude to do anything with your paywall, it'll say:

> I need to connect your Superwall account first.

It'll give you a tiny snippet to paste in your browser console. That
snippet copies 2 tokens to your clipboard. You paste them back. Done.

**Nothing scary happens.** No passwords. No browser extensions. Just 2
tokens that let Claude talk to Superwall on your behalf. They're stored
locally and never uploaded anywhere.

### Step 3: Just talk

Say things like:

| What you say | What happens |
|---|---|
| "pull my paywall 206207" | Downloads your paywall so Claude can see it |
| "change the primary color to #8C59D9" | Updates the brand color |
| "make the background white" | Flips the theme |
| "add a screen for users with a free trial" | Adds a conditional screen |
| "change the CTA text to white" | Fixes contrast on buttons |
| "rebuild this from this screenshot" | Matches a reference image |
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

# Pull
snap = c.get_snapshot(paywall_id=206207)

# Edit
store = snap['snapshot']['store']
store['state:style.interface.primary.light']['defaultValue']['value'] = '#8C59D9ff'

# Push
c.push_snapshot(paywall_id=206207, application_id=37837, snapshot=snap['snapshot'])
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
