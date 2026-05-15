# superwall-kit: Method

The Superwall web editor talks to its backend via a private tRPC API at
`https://superwall.com/api/trpc/`. Everything the editor can do is available
through that API with the right session cookie + `anti-csrf` header.

We use that API directly. No browser automation, no MCP, no screen scraping.

## Auth

Two values from a logged-in Chrome session:

- `cookie.txt` — the full `Cookie:` header string from any tRPC request
  (includes `accounts_superwall_token` which is what actually authenticates).
- `csrf.txt` — the `anti-csrf` header value.

Both live in `.secrets/` (gitignored). Grab them once per workspace from
DevTools → Network → Copy as cURL on any `/api/trpc/` request.

## Endpoint catalog (discovered from JS bundles + HAR)

### Editor snapshot ops (private paywall API)

| Endpoint | Method | Use |
|---|---|---|
| `paywalls.getLatestSnapshotByVersion` | GET | Pull full paywall JSON |
| `paywalls.prepareSnapshotForPromotion` | POST | Stage a new snapshot, returns `snapshotIdentifier` |
| `paywalls.promoteFromSnapshot` | POST | Promote staged snapshot → live version bump |
| `paywalls.getAllSnapshots` | GET | List all snapshots for a paywall |
| `paywalls.saveSnapshot` | POST | Alt: save without promoting |
| `paywalls.saveSnapshotAndPromote` | POST | Alt: combined save+promote |

### Template library

| Endpoint | Use |
|---|---|
| `blitzMigration.paywalls.getPaywallTemplates` | Paginated template list (`{take, skip, applicationId, v4Only}`) |

Each template record has `id` = paywallId; fetch full snapshot via
`paywalls.getLatestSnapshotByVersion`.

### Dashboard paywall ops

| Endpoint | Use |
|---|---|
| `paywalls.getPaywalls` | List paywalls in an app |
| `paywalls.getPaywall` | Get one paywall |
| `paywalls.createPaywall` | Create new |
| `paywalls.duplicatePaywall` | Clone |
| `paywalls.archivePaywall` / `unarchivePaywall` | Toggle visibility |
| `paywalls.getPaywallPreviewsEfficiently` | Preview URLs (PNG) |
| `paywalls.getProductsFromAllPaywalls` | Products attached across paywalls |

### Localization

| Endpoint | Use |
|---|---|
| `localization.createTextResource` | New text resource |
| `localization.updateTextResource` | Update |
| `localization.upsertTextResourceVariant` | Language variant |
| `localization.getResourceExistenceByPartialProps` | Check if exists |

### Assets (images/icons/fonts)

| Endpoint | Use |
|---|---|
| `assets.list` | List uploaded assets |
| `assets.create` | Create asset record |
| `assets.generateUploadInstructions` | Get presigned S3 upload URL |

### AI helpers

| Endpoint | Use |
|---|---|
| `ai.generateImage` | AI image generation |
| `ai.removeBackground` | Background removal |

## tRPC batch wire format

Queries:
```
GET /api/trpc/<endpoint>?batch=1&input=<url-encoded-json>
```
Where `input` = `{"0":{"json": <your payload>}}`.

Mutations:
```
POST /api/trpc/<endpoint>?batch=1
Body: {"0":{"json": <your payload>}}
```

Response shape:
```json
[{"result":{"data":{"json": <result> }}}]
```
Or error:
```json
[{"error":{"json":{"message":"...","code":-32004,"data":{"code":"NOT_FOUND",...}}}}]
```

## Write pipeline (the important one)

```
# 1. Pull
snap = client.get_snapshot(paywall_id)

# 2. Edit in Python (mutate snap['snapshot']['store'])

# 3. Stage
snapshot_id = client.prepare_snapshot(paywall_id, application_id, snap['snapshot'])

# 4. Promote (bumps version, makes it live in editor)
version = client.promote_snapshot(paywall_id, application_id, snapshot_id)
```

Or shortcut: `client.push_snapshot(paywall_id, application_id, snap['snapshot'])`
