# Nexus Protocol v0.6

**Status:** Draft — implemented in `nexus-core` 0.6.x.

## Overview

Nexus OS is a two-plane system:

- **Control plane** — `nexus-console`. Owns wizards, deployers, credentials vault, cross-instance registry.
- **Data plane** — `nexus-platform`. Runs the actual agents, LLM router, spaces, memory. One process per instance.

They communicate over signed HTTPS. Console holds an Ed25519 keypair; each Platform holds its own. Public keys are exchanged during bootstrap and pinned.

## Endpoints

### Platform-side

| Method | Path            | Auth                | Purpose                                                     |
|--------|-----------------|---------------------|-------------------------------------------------------------|
| POST   | `/_bootstrap`   | `X-Bootstrap-Token` | One-time handshake. Exchanges public keys + applies manifest.|
| POST   | `/_commands`    | Signed JWT (Console key) | Apply a `Command`. Returns `CommandResult`.            |
| GET    | `/_health`      | none                | Liveness probe.                                             |
| GET    | `/_status`      | Signed JWT (Console key) | Full instance status (spaces, agents, budget).         |

### Console-side

| Method | Path                | Auth                     | Purpose                                        |
|--------|---------------------|--------------------------|------------------------------------------------|
| POST   | `/callbacks/notify` | Signed JWT (Platform key)| Receives `NotificationEnvelope` from Platform. |

## Bootstrap flow

```
Console                                  Platform (fresh)
  │                                         │
  │  deploy container/service               │
  ├────────────────────────────────────────▶│  starts with BOOTSTRAP_TOKEN=<one-time>
  │                                         │
  │  POST /_bootstrap                       │
  │  X-Bootstrap-Token: <one-time>          │
  │  body: BootstrapRequest {               │
  │    instance_id,                         │
  │    console_public_key_pem,              │
  │    console_webhook_url,                 │
  │    manifest: InstanceManifest }         │
  ├────────────────────────────────────────▶│
  │                                         │  1. verify token (constant-time)
  │                                         │  2. generate own keypair
  │                                         │  3. persist console pub key + webhook
  │                                         │  4. apply manifest (LLM router, areas, spaces)
  │                                         │  5. burn BOOTSTRAP_TOKEN
  │                                         │
  │  BootstrapResponse {                    │
  │    status: ok,                          │
  │    platform_public_key_pem,             │
  │    platform_version,                    │
  │    applied_areas }                      │
  │◀────────────────────────────────────────┤
  │                                         │
  │  store platform pub key                 │
```

After bootstrap:

- Console signs every command with its private key. Platform verifies with the pinned public key.
- Platform signs every notification with its private key. Console verifies with the pinned public key.
- `BOOTSTRAP_TOKEN` is single-use; a re-bootstrap requires operator intervention.

## Envelope format

Both directions share the same envelope shape (only the top-level type differs):

```json
{
  "cmd_id": "uuid",
  "instance_id": "uuid",
  "issued_at": 1720000000,
  "expires_at": 1720000300,
  "command": { "kind": "...", "payload": {...} }
}
```

JWT header: `{ "alg": "EdDSA", "kid": "console" | "platform", "typ": "JWT" }`.

Default lifetime: 300 seconds. Expired envelopes are rejected before the payload is even parsed.

## Version compatibility

- `apiVersion: nexus.v0.6` — this protocol.
- Console and Platform MUST share the same `MAJOR.MINOR` of `nexus-core`. Mismatch → bootstrap returns `INVALID_TOKEN` with `error_detail` explaining the version drift.
- `PATCH` bumps are always backwards-compatible.

## Errors

| Situation                        | HTTP | Body                                                     |
|----------------------------------|------|----------------------------------------------------------|
| Bad bootstrap token              | 401  | `{"status":"invalid_token","error_detail":"..."}`         |
| Expired command JWT              | 401  | `{"status":"rejected","error_code":"expired"}`            |
| Bad JWT signature                | 401  | `{"status":"rejected","error_code":"invalid_signature"}`  |
| Command unknown for this version | 400  | `{"status":"rejected","error_code":"unknown_command"}`    |
| Apply failed                     | 500  | `{"status":"failed","detail":"..."}`                      |
