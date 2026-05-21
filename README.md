# PulseProjects

Central repository for Pulse infrastructure agent configurations.

## Structure

```
PulseProjects/
├── agents/
│   ├── openclaw/           # OpenClaw agent configuration
│   │   ├── config/         # Configuration templates & examples
│   │   │   ├── openclaw.json.example
│   │   │   ├── secrets.json.example
│   │   │   └── STRUCTURE.md
│   │   └── workspace/      # Agent workspace files
│   │       ├── AGENTS.md
│   │       ├── SOUL.md
│   │       ├── USER.md
│   │       ├── IDENTITY.md
│   │       ├── TOOLS.md
│   │       ├── HEARTBEAT.md
│   │       ├── context_management.md
│   │       └── skills/     # Agent skills
│   └── hermes/             # Hermes agent configuration (post-migration)
│       ├── config.yaml     # Hermes configuration (sanitized)
│       ├── .env.example    # Environment variable template
│       └── SOUL.md         # Hermes personality
├── .gitignore
├── LICENSE
└── README.md
```

## Setup

### OpenClaw
1. Copy `agents/openclaw/config/openclaw.json.example` to `openclaw.json`
2. Copy `agents/openclaw/config/secrets.json.example` to `secrets.json`
3. Fill in actual API keys in `secrets.json`
4. Restart OpenClaw gateway

### Hermes
1. Copy `agents/hermes/.env.example` to `~/.hermes/.env`
2. Fill in actual API keys
3. Configure model provider in `config.yaml`

## Security

- **Never commit** `secrets.json`, `.env`, or any file with actual API keys
- All sensitive values use `YOUR_*_HERE` placeholders in example files
- See `.gitignore` for the full list of excluded sensitive files
