---
description: Pull a Superwall paywall as JSON for inspection or editing
argument-hint: <paywall-id>
allowed-tools: [Bash, Read, Write]
---

# /sw-pull — Download a paywall snapshot

Pull paywall `$ARGUMENTS` from Superwall and save it locally.

## Steps

1. Check authentication. Run:
   ```bash
   test -f .secrets/cookie.txt && echo OK || echo MISSING
   ```
   If MISSING, tell the user to run `/sw-login` first.

2. If `$ARGUMENTS` is empty, ask the user for the paywall ID. It's in
   the Superwall editor URL:
   `https://superwall.com/applications/<app_id>/paywalls/<paywall_id>`.

3. Pull the snapshot:

   ```bash
   python3 -c "
   import sys, json
   sys.path.insert(0,'src')
   from superwall_kit import SuperwallClient
   c = SuperwallClient()
   snap = c.get_snapshot($ARGUMENTS)
   # Save to a local file
   import pathlib
   pathlib.Path('data/pulled').mkdir(parents=True, exist_ok=True)
   pathlib.Path(f'data/pulled/$ARGUMENTS.json').write_text(json.dumps(snap))
   store = snap['snapshot']['store']
   print(f'✅ pulled paywall $ARGUMENTS')
   print(f'   version: {snap[\"version\"]}')
   print(f'   nodes: {len(store)}')
   print(f'   saved to: data/pulled/$ARGUMENTS.json')
   "
   ```

4. Summarize what's inside the paywall (without dumping the full JSON):
   - Version number
   - Total node count
   - List of node types + counts
   - Number of pages (if any `navigation` node)
   - Products attached
   - Key theme colors

5. Tell the user: "Pulled. What do you want me to change?"
