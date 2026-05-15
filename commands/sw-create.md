---
description: Create a brand-new Superwall paywall from scratch (optionally to match a screenshot). Composes records via primitives, never clones.
argument-hint: <application_id> [name]
allowed-tools: [Bash, Read, Write, Edit]
---

# /sw-create — Build a new Superwall paywall from scratch

Args: `$ARGUMENTS` → first token is `application_id`, remainder is the
paywall `name` (defaults to "test").

## Steps

1. **Auth check.** If `.secrets/cookie.txt` is missing, run `/sw-login`
   first. Otherwise smoke-test with `c.query("user.getSelf", {})`.

2. **Look at any screenshot the user attached.** Describe its sections
   (header / hero / checklist / cards / CTA / footer). If there's no
   screenshot, ask: "What should it look like? Paste a screenshot or
   describe sections."

3. **Create the paywall record:**
   ```python
   import sys; sys.path.insert(0,"src")
   from superwall_kit import SuperwallClient
   c = SuperwallClient()
   r = c.create_paywall(application_id=APP)
   pid = r["paywall"]["id"]
   ```

4. **Compose with `Scratch`.** Use the layout rules in
   `skills/superwall/SKILL.md` → Strategy A. Reference `docs/REFERENCE.md`
   for every property/value type. Use `ref_token()` for all themable
   colors so the user can re-theme later in one call.

5. **Validate locally.**
   ```python
   from superwall_kit import validate_snapshot, summarize
   issues = validate_snapshot({"snapshot": snap})
   print(summarize(issues))
   ```
   If there are `error`-level issues, fix before pushing.

6. **Push.**
   ```python
   ver = c.push_snapshot(paywall_id=pid, application_id=APP, snapshot=snap)
   ```

7. **Tell the user (plain English):**
   > Pushed v{ver}. Open
   > https://superwall.com/applications/{APP}/paywalls/{pid}
   > and reload — tell me what to adjust.

8. **Iterate.** When they give feedback (sizes, spacing, colors), edit
   the compose script and push again to the same `pid`.

## Common pitfalls (already in SKILL.md but recap)

- Borders need `border_color` + `border_width` (helper adds `borderStyle: solid`)
- Padding uses `{"x": ..., "y": ..., "top": ...}` dict, **no** shorthand
- Equal-width cards: parent `main="stretch"`, no child widths
- Full-width CTA: parent `cross="stretch"`, no `width` on CTA
- Centered pill: wrap in extra row stack with `main="center"`
