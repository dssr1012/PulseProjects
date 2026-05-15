# OpenClaw Configuration Structure

This repository contains the OpenClaw configuration with externalized secrets for secure version control.

## Repository Structure

### Configuration Files
- `openclaw.json.example` - Main configuration template (safe to share)
- `secrets.json.example` - Secrets template (fill with your own keys)
- `.gitignore` - Git ignore rules to protect secrets
- `README.md` - Setup and usage instructions
- `STRUCTURE.md` - This file

### Workspace Files
- `workspace/AGENTS.md` - Agent workspace configuration
- `workspace/SOUL.md` - Agent personality and behavior
- `workspace/USER.md` - User information and preferences
- `workspace/IDENTITY.md` - Agent identity
- `workspace/TOOLS.md` - Local tool notes and configurations
- `workspace/HEARTBEAT.md` - Heartbeat tasks and monitoring
- `workspace/context_management.md` - Context management strategies

### Excluded from Git (via .gitignore)
- `openclaw.json` - Actual configuration (generated from example)
- `secrets.json` - Actual API keys and tokens
- `logs/` - Log files
- `credentials/` - Authentication credentials
- `telegram/` - Telegram session data
- `tui/` - TUI session data
- `plugins/installs.json` - Plugin installation data
- `identity/device.json` - Device identification
- `exec-approvals.json` - Execution approvals
- `update-check.json` - Update check data
- `workspace/.git/` - Workspace git repository
- `workspace/memory/` - Agent memory files
- `workspace/.openclaw/` - Workspace runtime data
- `workspace/skills/` - Skill implementations

## Setup Process

### For New Installation
1. Clone this repository
2. Copy `openclaw.json.example` to `openclaw.json`
3. Copy `secrets.json.example` to `secrets.json`
4. Edit `secrets.json` with your actual API keys
5. Restart OpenClaw gateway

### For Existing Installation
1. Backup your current `openclaw.json` and `secrets.json`
2. Clone this repository to a temporary location
3. Compare and merge configuration changes
4. Update `secrets.json` with any new secret paths
5. Restart OpenClaw gateway

## Security Notes

### Protected Files
The following files contain sensitive information and are excluded from Git:
- **`secrets.json`** - Contains all API keys and tokens
- **`openclaw.json`** - May contain secret references (though using SecretRef)
- **`*.session` files** - Session data and authentication tokens
- **Log files** - May contain sensitive information

### Best Practices
1. **Never commit** `secrets.json` or any file with actual API keys
2. **Use SecretRef** in `openclaw.json` to reference secrets
3. **Regularly audit** `.gitignore` to ensure no secrets are tracked
4. **Use environment variables** in production for better security
5. **Rotate keys** periodically and update `secrets.json`

## Version Control Strategy

### What to Commit
- Configuration templates and examples
- Documentation and setup instructions
- Workspace structure and agent personality
- Skill configurations (without secrets)
- Context management strategies

### What NOT to Commit
- Actual API keys and tokens
- Session data and authentication tokens
- User-specific preferences (unless anonymized)
- Log files and runtime data
- Temporary files and caches

## Maintenance

### Updating Configuration
1. Make changes to `openclaw.json.example`
2. Test changes locally
3. Update documentation if needed
4. Commit and push changes
5. Notify team members to update their local `openclaw.json`

### Adding New Secrets
1. Add secret reference to `openclaw.json.example`
2. Add placeholder to `secrets.json.example`
3. Update documentation
4. Team members add actual secret to their local `secrets.json`

### Backup Strategy
- Regular backups of `secrets.json` (encrypted)
- Version control for configuration templates
- Documentation of all secret references
- Recovery procedures for lost secrets