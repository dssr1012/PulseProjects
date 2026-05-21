# Context Overflow Prevention Guide

## Current Configuration
- **Primary Model**: `deepseek-v4-flash` (1,000,000 token context window)
- **Fallback Models**: `deepseek-v3.2`, `deepseek-v4-pro`, `DeepSeek-V3`
- **Compaction**: 100,000 token floor with aggressive strategy
- **Auto-reset**: Sessions reset at 80% context usage or 100 messages

## How to Avoid Context Overflow

### 1. **Manual Session Management**
```
/reset           # Reset current session (starts fresh)
/new             # Start new session (alternative to /reset)
/status          # Check current token usage
```

### 2. **Automatic Protection**
The configuration now includes:
- **Auto-reset at 80%**: Sessions automatically reset when context reaches 800k tokens
- **Message limit**: Sessions reset after 100 messages
- **Time limit**: Sessions reset after 4 hours

### 3. **Best Practices**

#### **For Long Conversations:**
1. **Use `/reset` periodically** - Especially after completing major tasks
2. **Summarize before resetting** - Save important information to memory files
3. **Use sub-agents** - Spawn isolated sessions for complex tasks

#### **For Memory Management:**
```bash
# Save important context before resetting
echo "Summary of previous conversation..." >> /root/.openclaw/workspace/memory/YYYY-MM-DD.md
```

#### **Check Current Usage:**
```
/status
```

### 4. **Emergency Recovery**
If you get "Context overflow" error:
1. **Immediately use `/reset`** - This clears the conversation history
2. **Check `/status`** - Verify the reset was successful
3. **Continue from where you left off** - Reference memory files if needed

### 5. **Proactive Monitoring**
Create a cron job to check context usage:
```bash
# Add to HEARTBEAT.md
- Check context usage with /status every 30 minutes
- Auto-reset if >70% usage
```

## Configuration Details

### Model Context Windows:
- `deepseek-v4-flash`: 1,000,000 tokens ✅ **PRIMARY**
- `deepseek-v3.2`: 160,000 tokens
- `deepseek-v4-pro`: 128,000 tokens
- `DeepSeek-V3`: 128,000 tokens

### Why deepseek-v4-flash?
- 6x larger context than deepseek-v3.2
- Lower cost per token
- Same reasoning capabilities
- Better for long conversations

## Testing
To test the new configuration:
1. Restart OpenClaw gateway
2. Start a new session
3. Run `/status` to verify model
4. Test with long conversations

## Troubleshooting
If context overflow still occurs:
1. Check `/status` for actual token usage
2. Verify model is `deepseek-v4-flash`
3. Ensure configuration was reloaded
4. Consider reducing `compaction.reserveTokensFloor`