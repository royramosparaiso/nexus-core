# Nexus Core SDK

**Contratos compartidos entre [Nexus Console](https://github.com/royramosparaiso/nexus-console) y [Nexus Platform](https://github.com/royramosparaiso/nexus-platform).**

Un paquete, dos lenguajes:

- **Python** (`nexus-core`) — usado por Console (control plane) y Platform (data plane).
- **TypeScript** (`@nexus-os/core`) — usado por las UIs de Console y Platform, y por integraciones externas.

Los tipos, los contratos JWT y el cliente HTTP tipado están definidos una sola vez y se generan en paralelo para ambos ecosistemas. La versión del paquete = versión del protocolo (semver estricto).

> **Impulsado por Ironbat Digital LLC.** Licencia MIT.

## Qué hay dentro

| Módulo | Qué expone |
|---|---|
| `contracts/` | Enums, literales y payloads del protocolo Console↔Platform (comandos, notificaciones, respuestas). |
| `models/` | Modelos compartidos: `Persona`, `Instance`, `Space`, `User`, `Area`, `Agent`, `MemoryScope`. |
| `jwt/` | Emisión y verificación de tokens Ed25519, con claims obligatorios del protocolo. |
| `client/` | Cliente HTTP tipado que firma llamadas a Platform y verifica notificaciones desde Platform. |

## Instalación

**Python (Console/Platform backends):**

```bash
pip install nexus-core
```

**TypeScript (UIs y toolings):**

```bash
npm install @nexus-os/core
```

Ambos paquetes comparten `MAJOR.MINOR` — el `PATCH` puede divergir para fixes de un lado. Un cliente con `MAJOR.MINOR` distinto al backend hace fallar el handshake explícitamente.

## Versionado del protocolo

- `0.6.x` — v0.6 del protocolo Nexus OS (RFC-002 draft, ver [nexus-console/docs/rfc](https://github.com/royramosparaiso/nexus-console/tree/main/docs/rfc)).
- Un breaking change en el protocolo requiere `MINOR` bump antes de v1.0, `MAJOR` bump después.

## Uso rápido

### Python

```python
from nexus_core.jwt import ConsoleKeypair, sign_command
from nexus_core.contracts import Command, CommandKind

kp = ConsoleKeypair.generate()
cmd = Command(kind=CommandKind.CREATE_SPACE, payload={"name": "acme-space"})
token = sign_command(kp, instance_id="uuid...", command=cmd)
```

### TypeScript

```ts
import { Command, CommandKind } from "@nexus-os/core";

const cmd: Command = {
  kind: CommandKind.CreateSpace,
  payload: { name: "acme-space" },
};
```

## Estructura del repo

```
nexus-core/
├── python/         # nexus-core (PyPI package)
│   ├── nexus_core/
│   │   ├── contracts/
│   │   ├── models/
│   │   ├── jwt/
│   │   └── client/
│   └── tests/
├── ts/             # @nexus-os/core (npm package)
│   ├── src/
│   │   ├── contracts/
│   │   ├── models/
│   │   ├── jwt/
│   │   └── client/
│   └── tests/
└── docs/           # Protocol spec
```

## Roadmap

- [x] Python: types, contracts, JWT sign/verify
- [x] TypeScript: types, contracts (mirror)
- [ ] Python: HTTP client with retries + circuit breaker
- [ ] TypeScript: HTTP client (fetch wrapper)
- [ ] Cross-language contract tests (JSON Schema fixtures)
- [ ] Publish to PyPI + npm on tag
- [ ] Auto-generate TS types from Python via `datamodel-code-generator`

## Licencia

MIT — ver [LICENSE](LICENSE).
