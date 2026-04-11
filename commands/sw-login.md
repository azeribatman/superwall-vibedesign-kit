---
description: Authenticate with Superwall by pasting a Copy-as-cURL from DevTools
argument-hint: (none)
allowed-tools: [Bash, Read, Write, Edit]
---

# /sw-login — Set up Superwall authentication

Guide the user through connecting their Superwall account to this toolkit.

## Steps to run

1. Tell the user:

   > I'll walk you through connecting your Superwall account. It's a
   > one-time setup and takes about 30 seconds.
   >
   > **Step 1:** Open Superwall in Chrome and log in to the workspace
   > whose paywalls you want to edit.
   >
   > **Step 2:** Open any paywall in the editor (URL starts with
   > `superwall.com/applications/.../paywalls/...`).
   >
   > **Step 3:** Open DevTools (Cmd+Opt+I), go to the **Network** tab,
   > and reload the page. Click any request in the list whose URL
   > contains `/api/trpc/`.
   >
   > **Step 4:** Right-click that request → **Copy** → **Copy as cURL**.
   >
   > **Step 5:** Paste the entire cURL command here and tell me when done.

2. Wait for the user to paste the cURL as their next message.

3. When they paste, extract the cookie string from the cURL. Look for
   either `-b '...'`, `--cookie '...'`, or `-H 'cookie: ...'` in the text.

4. Save the cookie to `.secrets/cookie.txt`:

   ```bash
   mkdir -p .secrets
   # Write the extracted cookie string to .secrets/cookie.txt
   ```

5. Verify the cookie contains `paywall_sAntiCsrfToken=...` — if not, tell
   the user the auth didn't work and ask them to re-try.

6. Run a smoke test:

   ```bash
   python3 -c "
   import sys; sys.path.insert(0,'src')
   from superwall_kit import SuperwallClient
   c = SuperwallClient()
   print('logged in:', c.query('user.getSelf', {}).get('id','?'))
   "
   ```

7. If the smoke test passes, tell the user:

   > ✅ Connected! You're logged in. You can now ask me things like:
   >
   > - "Pull paywall 206207 and show me what's inside"
   > - "Change my paywall's primary color to #8C59D9"
   > - "Add a trial reminder screen"
   > - "Rebuild this paywall to match this screenshot"

## Alternative

If the user prefers, they can also just run the login script directly:

```bash
python3 scripts/login.py
```

And paste the cURL when prompted. Same result.

## Security notes

- The cookie is stored in `.secrets/cookie.txt` which is gitignored
- The CSRF token is extracted from inside the cookie automatically — no
  separate file needed
- Nothing is uploaded anywhere. The cookie stays local.
- Cookies expire; if you start getting `HTTP 403` errors later, just run
  `/sw-login` again to refresh.
