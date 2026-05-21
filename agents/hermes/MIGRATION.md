# Hermes Migration Report

## Migration Summary
**Date**: 2026-05-22
**Source**: OpenClaw Agent (clawdbot-demo)
**Target**: Hermes Agent v0.14.0
**Status**: 🔄 Migrating to Singapore ECS

## Region Correction
- **Incorrect deployment**: Santiago region (local OpenClaw gateway host) — **CLEANED UP**
- **Correct target**: Singapore ECS (`ead35200-fe09-4323-9b04-94a4338db760`)

## Santiago Cleanup (Completed)
- ✅ Hermes CLI (`/usr/local/bin/hermes`) removed
- ✅ Installation directory (`/usr/local/lib/hermes-agent/`) removed
- ✅ Config directory (`/root/.hermes/`) removed
- ✅ Playwright cache (`/root/.cache/ms-playwright/`) removed
- ✅ Shell profile references cleaned
- ✅ No Hermes processes or systemd services remain
- ✅ Port 18790 freed

## Architecture (Singapore Target)

```
┌─────────────────────────────────────────────────────────────┐
│              Singapore ECS (ead35200)                        │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │  OpenClaw    │    │   Hermes     │                      │
│  │  Port: 18789 │    │  Port: 18790 │                      │
│  └──────┬───────┘    └──────┬───────┘                      │
│         └───────┬───────────┘                               │
│                 │                                           │
│         ┌───────▼────────┐                                  │
│         │  Local Models  │                                  │
│         │  (vLLM/Ollama) │                                  │
│         └────────────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

## Model Configuration
Models will be mapped from the local OpenClaw model path on the Singapore ECS.
Exact paths to be determined during Singapore audit (Task 3).

## Configuration Mapping

| Setting | OpenClaw | Hermes |
|---------|----------|--------|
| Primary Model | TBD (from Singapore audit) | Same |
| Provider | TBD | custom (local) |
| Gateway Port | 18789 | 18790 |
| Config Format | JSON | YAML |
| MCP | Built-in tools | mcp_servers: block |

## Pending Items
1. Audit Singapore ECS — identify OpenClaw config and model paths
2. Install Hermes on Singapore ECS
3. Configure model mapping (local paths, not API)
4. Set up MCP servers block
5. Run inference test
6. Update repository with final Singapore configuration
