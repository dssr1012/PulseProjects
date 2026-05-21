# Hermes Migration Report

## Migration Summary
**Date**: 2026-05-22
**Source**: OpenClaw Agent (clawdbot-demo)
**Target**: Hermes Agent v0.14.0
**Status**: ✅ Complete — Deployed on Singapore ECS

## Region Correction
- **Incorrect deployment**: Santiago region (local host) — **CLEANED UP**
- **Correct deployment**: Singapore ECS (`ead35200-fe09-4323-9b04-94a4338db760`) — **DEPLOYED**

## Architecture (Singapore ECS)

```
┌─────────────────────────────────────────────────────────────┐
│              Singapore ECS (ap-southeast-3)                  │
│              Public IP: 111.119.246.171                      │
│              Private IP: 172.16.1.25                         │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │  OpenClaw    │    │   Hermes     │                      │
│  │  Port: 18789 │    │  Port: 18790 │                      │
│  │  (existing)  │    │  (new)       │                      │
│  └──────┬───────┘    └──────┬───────┘                      │
│         └───────┬───────────┘                               │
│                 │                                           │
│         ┌───────▼────────┐                                  │
│         │  Huawei Cloud  │                                  │
│         │  ModelArts     │                                  │
│         │  MaaS API      │                                  │
│         │  (OpenAI-comp) │                                  │
│         └────────────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

## Key Finding: No Local Models
**No local LLM models exist on the Singapore ECS.** There are no vLLM, Ollama,
llama.cpp, .gguf files, or HuggingFace cache. All inference is via Huawei Cloud
ModelArts MaaS API (remote). Hermes is configured to use the same API endpoint.

## Santiago Cleanup (Completed)
- ✅ Hermes CLI removed
- ✅ Installation directory removed
- ✅ Config directory removed
- ✅ Playwright cache removed
- ✅ No Hermes processes or services remain
- ✅ Port 18790 freed on Santiago host

## Singapore Deployment (Completed)
- ✅ Hermes v0.14.0 installed
- ✅ Python 3.11.15 venv with OpenAI SDK 2.24.0
- ✅ config.yaml: provider=custom, model=deepseek-v4-flash
- ✅ .env: OPENAI_API_KEY + DEEPSEEK_API_KEY set
- ✅ Fallback chain: v3.2 → v4-pro → v3.1-terminus → V3 → glm-5.1
- ✅ MCP servers: huawei-cloud, filesystem, github
- ✅ Huawei Cloud SDK v3.1.196 installed
- ✅ Gateway port: 18790 (parallel with OpenClaw on 18789)
- ✅ Inference test: PASSED (DeepSeek-V4-Flash, 200 OK)

## Model Configuration

### Primary Model
| Property | Value |
|----------|-------|
| Model | deepseek-v4-flash |
| Context Window | 1,000,000 tokens |
| Max Output | 128,000 tokens |
| Reasoning | ✅ Yes |
| API Endpoint | https://api-ap-southeast-1.modelarts-maas.com/openai/v1 |

### Fallback Chain
1. deepseek-v3.2 (160K ctx)
2. deepseek-v4-pro (128K ctx)
3. deepseek-v3.1-terminus (160K ctx)
4. DeepSeek-V3 (128K ctx)
5. glm-5.1 (128K ctx, no reasoning)

## MCP Servers

| Server | Tools | Status |
|--------|-------|--------|
| huawei-cloud | 6 (ECS, RDS, VPC, EIP, actions, summary) | ✅ Installed |
| filesystem | 14 (file operations) | ✅ Configured |
| github | 26 (repo operations) | ✅ Configured |

## Configuration Mapping

| Setting | OpenClaw | Hermes |
|---------|----------|--------|
| Primary Model | deepseek-v4-flash | deepseek-v4-flash |
| Provider | custom-api-ap-southeast-1-modelarts-maas-com | custom |
| API Endpoint | (same) | (same) |
| Gateway Port | 18789 | 18790 |
| Compaction | safeguard, 50K floor | compression, 50K floor |
| Config Format | JSON | YAML |
| MCP | Built-in tools | mcp_servers: block |

## ECS Instance Details
| Property | Santiago (cleanup) | Singapore (target) |
|----------|-------------------|-------------------|
| ID | f123f778-23f8-4d17-bb9f-6a540b37d0c6 | ead35200-fe09-4323-9b04-94a4338db760 |
| Region | la-south-2 | ap-southeast-3 |
| Public IP | 182.160.24.205 | 111.119.246.171 |
| Status | SHUTOFF | ACTIVE |
| Hermes | Removed | Deployed |

## Gateway Service
- ✅ Systemd user service installed and enabled (`hermes-gateway.service`)
- ✅ Systemd linger enabled (survives logout)
- ✅ Telegram connected (polling mode, 30 commands registered)
- ✅ 46 MCP tools loaded (6 huawei-cloud + 14 filesystem + 26 github)
- ✅ Secret redaction enabled
- ✅ Cron ticker active (60s interval)

## Auth Fix (2026-05-22 03:22)
**Root cause**: Hermes with `provider: custom` reads `CUSTOM_API_KEY` env var, 
not `OPENAI_API_KEY`. The initial config only set `OPENAI_API_KEY` and 
`DEEPSEEK_API_KEY`, causing `ModelArts.81003: Invalid authorization header` (HTTP 401).

**Fix**: Added `CUSTOM_API_KEY` and `CUSTOM_BASE_URL` to `/root/.hermes/.env`.
After restart, all auth errors resolved. Direct API curl returns 200 OK.

## Pending Items
1. **SSL/HTTPS**: Configure if exposing Hermes gateway publicly
2. **Telegram commands**: Customize bot commands via /setcommands in @BotFather
