---
description: Authenticate with Superwall (20 seconds — paste a console snippet output)
argument-hint: (none)
allowed-tools: [Bash, Read, Write, Edit]
---

# /sw-login — Connect your Superwall account

Walk the user through authenticating with Superwall.

## Steps

1. Tell the user:

   > I'll connect your Superwall account. Takes 20 seconds:
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

2. Wait for the user to paste. They'll paste 2 lines like:
   ```
   accounts_superwall_token=Fe26.2*1*...
   paywall_sAntiCsrfToken=ZkSmz...
   ```
   If they paste a full Copy-as-cURL instead, that also works — extract
   the 2 tokens from the cookie string inside `-b '...'`.

3. Extract the two values and save:

   ```bash
   mkdir -p .secrets
   # Build: accounts_superwall_token=<TOKEN>; paywall_sAntiCsrfToken=<CSRF>
   # Write to .secrets/cookie.txt
   chmod 600 .secrets/cookie.txt
   ```

4. Smoke test:

   ```bash
   python3 -c "
   import sys; sys.path.insert(0,'src')
   from superwall_kit import SuperwallClient
   c = SuperwallClient()
   u = c.query('user.getSelf', {})
   print('logged in:', u.get('user',{}).get('id', '?'))
   "
   ```

5. If it prints a user id, tell the user:

   > Connected! You can now ask me things like:
   >
   > - "Pull paywall 206207 and show me what's inside"
   > - "Change my paywall's primary color to purple"
   > - "Rebuild this paywall to match this screenshot"

6. If it fails, the token is expired or from a different workspace.
   Ask the user to re-run the snippet after logging into the right
   Superwall workspace.
