# Hermes Migration Report

## Migration Summary
**Date**: 2026-05-22
**Source**: OpenClaw Agent (clawdbot-demo)
**Target**: Hermes Agent v0.14.0
**Status**: ✅ Complete (local), ⏸️ Pending ECS deployment

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ECS Instance (SHUTOFF)                    │
│                  182.160.24.205                             │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │  OpenClaw    │    │   Hermes     │                      │
│  │  Port: 18789 │    │  Port: 18790 │                      │
│  │  (existing)  │    │  (new)       │                      │
│  └──────┬───────┘    └──────┬───────┘                      │
│         │                   │                               │
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

## Key Finding: API-Based Models
**No local LLM models exist on disk.** Both OpenClaw and Hermes consume
the same Huawei Cloud ModelArts MaaS API endpoint. There are no vLLM,
Ollama, or local quantized models. Models are accessed remotely via
OpenAI-compatible API.

- **API Endpoint**: `https://api-ap-southeast-1.modelarts-maas.com/openai/v1`
- **API Type**: OpenAI-compatible completions
- **Auth**: Bearer token (API key)

## Model Configuration

### Primary Model
| Property | Value |
|----------|-------|
| Model | deepseek-v4-flash |
| Context Window | 1,000,000 tokens |
| Max Output | 128,000 tokens |
| Reasoning | ✅ Yes |
| Cost | $0.135/M input, $0.27/M output |

### Fallback Chain
1. deepseek-v3.2 (160K ctx, reasoning ✅)
2. deepseek-v4-pro (128K ctx, reasoning ✅)
3. deepseek-v3.1-terminus (160K ctx, reasoning ✅)
4. DeepSeek-V3 (128K ctx, reasoning ✅)
5. glm-5.1 (128K ctx, reasoning ❌)

### Additional Available Models
- deepseek-r1-250528 (128K ctx, reasoning ✅)
- glm-5 (128K ctx, reasoning ❌)

## Configuration Mapping

| Setting | OpenClaw | Hermes |
|---------|----------|--------|
| Primary Model | deepseek-v4-flash | deepseek-v4-flash |
| Provider | custom-api-ap-southeast-1-modelarts-maas-com | custom |
| API Endpoint | (same) | (same) |
| API Key | secrets.json → providers.*.apiKey | .env → OPENAI_API_KEY |
| Fallbacks | 5 models (config) | 5 models (config.yaml fallback_models) |
| Compaction | safeguard, 50K floor | compression, 50K floor |
| Gateway Port | 18789 | 18790 |
| Config Format | JSON | YAML |
| MCP | Built-in tools | mcp_servers: block |

## MCP Servers Configured

### 1. Huawei Cloud (custom)
- **Tools**: list_ecs_instances, list_rds_instances, list_vpcs, list_eips, list_security_groups, ecs_action, get_infrastructure_summary
- **SDK**: huaweicloudsdkpython v3.1.196
- **Region**: la-south-2

### 2. Filesystem (npx @modelcontextprotocol/server-filesystem)
- **Tools**: 14 file operations (read, write, edit, list, search, etc.)
- **Paths**: /root/PulseProjects, /root/PulseExpends

### 3. GitHub (npx @modelcontextprotocol/server-github)
- **Tools**: 26 repo operations (search, create, PR, issues, etc.)

## Parallel Operation
Both services can run simultaneously:
- **OpenClaw**: Port 18789 (existing Telegram bot)
- **Hermes**: Port 18790 (CLI mode; Telegram requires separate bot token)

## Inference Test Results
✅ **API test passed**: Direct curl to ModelArts MaaS endpoint
- Model: DeepSeek-V4-Flash
- Response: "Hello!"
- Tokens: 10 prompt + 21 completion (18 reasoning)
- Latency: <2s

## Installation Details

| Component | Version | Path |
|-----------|---------|------|
| Hermes Agent | 0.14.0 | /usr/local/lib/hermes-agent |
| Hermes CLI | /usr/local/bin/hermes | |
| Python | 3.11.15 | venv at /usr/local/lib/hermes-agent/venv |
| Playwright | Chromium 148.0 | /root/.cache/ms-playwright/ |
| Huawei SDK | 3.1.196 | In Hermes venv |
| Bundled Skills | 89 | ~/.hermes/skills/ |

## Security Audit
- ✅ No API keys in config.yaml (all in .env)
- ✅ .env is gitignored
- ✅ .env.example uses placeholders
- ✅ secrets.json not committed
- ✅ Huawei Cloud AK/SK not in repo

## Pending Items
1. **ECS Deployment**: Instance is SHUTOFF — start via Huawei Cloud Console or API
2. **Telegram Bot**: Create new bot via @BotFather for Hermes gateway
3. **Huawei Cloud Credentials**: Set HW_ACCESS_KEY and HW_SECRET_KEY in .env
4. **SSL/HTTPS**: Configure for Hermes gateway if exposed publicly
5. **Service Migration**: Once Hermes is verified, transition Telegram bot token

## Cost Impact
No additional model costs — both agents share the same ModelArts MaaS API
endpoint and key. Costs are per-token regardless of which agent makes the call.
