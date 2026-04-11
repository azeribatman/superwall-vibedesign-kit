---
description: Push changes back to Superwall (prepare + promote snapshot)
argument-hint: <paywall-id> <application-id>
allowed-tools: [Bash, Read]
---

# /sw-push — Promote edited snapshot to live

Push the edited snapshot at `data/pulled/$1.json` to Superwall paywall `$1`
in application `$2`.

## Steps

1. Confirm `.secrets/cookie.txt` exists. If not, tell the user to run
   `/sw-login`.

2. Confirm `data/pulled/$1.json` exists. If not, the user needs to
   `/sw-pull <id>` first.

3. Before pushing, **show the user a summary of changes** if you made
   edits in this conversation. E.g., "I'm about to change: primary color,
   3 text strings, 1 product identifier. Push?"

4. Wait for explicit confirmation.

5. Push:

   ```bash
   python3 -c "
   import sys, json
   sys.path.insert(0,'src')
   from superwall_kit import SuperwallClient
   c = SuperwallClient()
   snap = json.loads(open('data/pulled/$1.json').read())
   v = c.push_snapshot(paywall_id=$1, application_id=$2, snapshot=snap['snapshot'])
   print(f'✅ live at version {v}')
   print(f'   view: https://superwall.com/applications/$2/paywalls/$1')
   "
   ```

6. Report the new version number and the editor URL to the user.

## Safety rules

- Never push without a pull first — you don't know what's in the
  paywall otherwise.
- Never push to a paywall ID the user didn't explicitly mention.
- If the user is unsure about a change, offer to show them a diff of
  what changed before pushing.
- If push returns `HTTP 403 FORBIDDEN`, the cookie is for a different
  workspace than the target paywall. Ask the user to `/sw-login` with
  the right workspace.
