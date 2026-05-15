# OpenClaw Configuration

This repository contains the OpenClaw configuration with externalized secrets for secure version control.

## 🚀 Quick Start

### 1. Clone this repository
```bash
git clone <your-repo-url> ~/.openclaw-config
cd ~/.openclaw-config
```

### 2. Set up the configuration
```bash
# Copy example configuration
cp openclaw.json.example ~/.openclaw/openclaw.json

# Create secrets file from template
cp secrets.json.example ~/.openclaw/secrets.json

# Edit secrets file with your actual API keys
nano ~/.openclaw/secrets.json
```

### 3. Restart OpenClaw
```bash
openclaw gateway restart
```

## 📁 File Structure

```
~/.openclaw/
├── openclaw.json          # Main configuration (created from example)
├── secrets.json           # API keys and tokens (NOT in git)
├── secrets.json.example   # Template for secrets (in git)
├── .gitignore            # Git ignore rules
└── workspace/            # Agent workspace files
```

## 🔐 Secrets Management

### Creating secrets.json
1. Copy `secrets.json.example` to `secrets.json`
2. Fill in your actual API keys:

```json
{
  "gateway": {
    "auth": {
      "token": "YOUR_GATEWAY_AUTH_TOKEN_HERE"
    }
  },
  "providers": {
    "your-provider-name": {
      "apiKey": "YOUR_PROVIDER_API_KEY_HERE"
    }
  },
  "telegram": {
    "botToken": "YOUR_TELEGRAM_BOT_TOKEN_HERE"
  },
  "google": {
    "apiKey": "YOUR_GOOGLE_API_KEY_HERE"
  }
}
```

### Supported Secret Sources
OpenClaw supports multiple secret sources:

1. **File-based** (recommended for local development):
   ```json
   { "source": "file", "provider": "default", "id": "/path/to/secret" }
   ```

2. **Environment variables**:
   ```json
   { "source": "env", "provider": "default", "id": "ENV_VAR_NAME" }
   ```

3. **External command** (for vaults):
   ```json
   { "source": "exec", "provider": "default", "id": "command-to-run" }
   ```

## ⚙️ Configuration Features

### Context Management
- **Primary model**: deepseek-v4-flash (1M context window)
- **Fallback models**: Multiple models configured for automatic fallback
- **Auto-compaction**: Enabled with safeguard mode
- **Context pruning**: Automatic cleanup of old tool results
- **Memory protection**: Auto-save before compaction

### Model Fallback Chain
```json
"fallbacks": [
  "custom-api-ap-southeast-1-modelarts-maas-com/deepseek-v3.2",
  "custom-api-ap-southeast-1-modelarts-maas-com/deepseek-v4-pro",
  "custom-api-ap-southeast-1-modelarts-maas-com/deepseek-v3.1-terminus",
  "custom-api-ap-southeast-1-modelarts-maas-com/DeepSeek-V3",
  "custom-api-ap-southeast-1-modelarts-maas-com/glm-5.1"
]
```

### Skills Configuration
- **Enabled skills**: Browser automation, GLM app builder, security checker, etc.
- **Skill orchestration**: Intelligent skill and model selection
- **Context-aware execution**: Automatic skill matching based on task

## 🔧 Customization

### Adding New Providers
1. Add provider configuration to `openclaw.json`
2. Add API key to `secrets.json`
3. Update model configurations as needed

### Modifying Skills
Edit the `skills.entries` section in `openclaw.json` to enable/disable skills:

```json
"skills": {
  "entries": {
    "skill-name": {
      "enabled": true
    }
  }
}
```

### Adjusting Context Settings
- **Compaction**: Modify `agents.defaults.compaction` settings
- **Pruning**: Adjust `agents.defaults.contextPruning` values
- **Memory**: Configure `agents.defaults.memory` settings

## 🚨 Security Notes

### NEVER Commit to Git:
- `secrets.json` (contains actual API keys)
- `.env.key` (encryption key)
- Any file with real credentials
- Session files
- Log files

### ALWAYS Use .gitignore:
The provided `.gitignore` excludes:
- All secret files
- Logs and temporary files
- Session data
- Cache files
- IDE files

### Environment Variables Alternative
For production deployments, consider using environment variables:

```bash
# Set environment variables
export OPENCLAW_GATEWAY_TOKEN="your-token"
export MODEL_API_KEY="your-api-key"
export TELEGRAM_BOT_TOKEN="your-bot-token"

# Update openclaw.json to use env vars:
"token": { "source": "env", "provider": "default", "id": "OPENCLAW_GATEWAY_TOKEN" }
```

## 🔄 Updating Configuration

### 1. Pull latest changes
```bash
cd ~/.openclaw-config
git pull
```

### 2. Compare with current config
```bash
# Check for differences
diff ~/.openclaw/openclaw.json openclaw.json.example

# Apply updates if needed
cp openclaw.json.example ~/.openclaw/openclaw.json.new
# Manually merge changes, then:
mv ~/.openclaw/openclaw.json.new ~/.openclaw/openclaw.json
```

### 3. Restart gateway
```bash
openclaw gateway restart
```

## 🐛 Troubleshooting

### Configuration Errors
```bash
# Validate configuration
openclaw config validate

# Check logs
journalctl --user -u openclaw-gateway.service -n 100 --no-pager
```

### Secret Resolution Issues
1. Verify `secrets.json` exists and is readable
2. Check file permissions: `chmod 600 ~/.openclaw/secrets.json`
3. Confirm JSON syntax is valid
4. Restart gateway after changes

### Gateway Won't Start
```bash
# Check status
openclaw gateway status

# View detailed logs
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

## 📚 Additional Resources

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [Secrets Management](https://docs.openclaw.ai/gateway/secrets)
- [Skills Guide](https://docs.openclaw.ai/concepts/skills)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes to example files only
4. Update documentation if needed
5. Submit a pull request

## 📄 License

This configuration is provided as-is. Ensure you comply with the terms of service for all API providers.

---

**Remember**: Never commit actual secrets to version control. Use the example files as templates only.