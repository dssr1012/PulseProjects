# GLM API Reference

## API Endpoints

### Base URL
```
https://api-ap-southeast-1.modelarts-maas.com/openai/v1
```

### Available Models
- `glm-5`: General purpose model
- `glm-5.1`: Enhanced capabilities model

## Authentication

### API Key
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GLM_API_KEY"),
    base_url="https://api-ap-southeast-1.modelarts-maas.com/openai/v1"
)
```

## Chat Completion

### Basic Usage
```python
response = client.chat.completions.create(
    model="glm-5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=1000
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | Required | Model ID (glm-5 or glm-5.1) |
| `messages` | array | Required | Conversation messages |
| `temperature` | float | 0.7 | Creativity (0-2) |
| `max_tokens` | integer | 2048 | Maximum tokens to generate |
| `top_p` | float | 1.0 | Nucleus sampling |
| `frequency_penalty` | float | 0.0 | Reduce repetition |
| `presence_penalty` | float | 0.0 | Encourage new topics |
| `stream` | boolean | false | Stream responses |
| `stop` | string/array | null | Stop sequences |

## Streaming

### Streaming Responses
```python
stream = client.chat.completions.create(
    model="glm-5",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

## Error Handling

### Common Errors
```python
try:
    response = client.chat.completions.create(...)
except openai.APIConnectionError as e:
    print("Connection error:", e)
except openai.RateLimitError as e:
    print("Rate limit exceeded:", e)
except openai.APIStatusError as e:
    print("API error:", e.status_code, e.response)
except Exception as e:
    print("Unexpected error:", e)
```

### Rate Limiting
- Default: 60 requests per minute
- Implement retry with exponential backoff

## Best Practices

### 1. Prompt Engineering
```python
# System message for context
system_message = """
You are an expert Python developer. 
You write clean, efficient, and well-documented code.
Always include error handling and type hints.
"""

# Few-shot learning
messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": "Write a function to calculate factorial"},
    {"role": "assistant", "content": "def factorial(n: int) -> int:\n    if n < 0:\n        raise ValueError('Factorial not defined for negative numbers')\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result"},
    {"role": "user", "content": "Write a function to check if a number is prime"}
]
```

### 2. Token Management
```python
def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars ≈ 1 token)"""
    return len(text) // 4

def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to fit token limit"""
    estimated = estimate_tokens(text)
    if estimated <= max_tokens:
        return text
    
    # Truncate by characters (approximate)
    max_chars = max_tokens * 4
    return text[:max_chars]
```

### 3. Cost Optimization
```python
def optimize_prompt(messages, max_context_tokens=4000):
    """Optimize prompt to reduce token usage"""
    total_tokens = sum(estimate_tokens(msg["content"]) for msg in messages)
    
    if total_tokens > max_context_tokens:
        # Remove oldest messages while keeping system message
        system_msg = messages[0] if messages[0]["role"] == "system" else None
        other_msgs = messages[1:] if system_msg else messages
        
        # Keep most recent messages
        keep_msgs = other_msgs[-10:]  # Keep last 10 messages
        
        if system_msg:
            return [system_msg] + keep_msgs
        return keep_msgs
    
    return messages
```

## Advanced Features

### Function Calling
```python
functions = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        }
    }
]

response = client.chat.completions.create(
    model="glm-5",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    functions=functions,
    function_call="auto"
)
```

### Logging and Monitoring
```python
import logging
from datetime import datetime

class GLMLogger:
    def __init__(self):
        self.logger = logging.getLogger("glm_api")
        
    def log_request(self, model, messages, response):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "model": model,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
            "response_time": response.response_ms if hasattr(response, 'response_ms') else None
        }
        self.logger.info(json.dumps(log_entry))
```

## Performance Tips

### 1. Caching
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_response(prompt_hash: str, model: str):
    """Cache frequent similar queries"""
    pass

def hash_prompt(messages):
    """Create hash for prompt caching"""
    content = "".join(msg["content"] for msg in messages)
    return hashlib.md5(content.encode()).hexdigest()
```

### 2. Batch Processing
```python
def process_batch(queries, model="glm-5", batch_size=5):
    """Process multiple queries in batches"""
    results = []
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        # Process batch concurrently
        batch_results = process_batch_concurrent(batch, model)
        results.extend(batch_results)
    return results
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Check API key is correct
   - Verify base URL is correct
   - Ensure API key has proper permissions

2. **Rate Limiting**
   - Implement exponential backoff
   - Reduce request frequency
   - Use caching for repeated queries

3. **Model Not Available**
   - Check model name spelling
   - Verify model is available in your region
   - Try alternative model

4. **Timeout Errors**
   - Increase timeout settings
   - Implement retry logic
   - Check network connectivity

### Debugging
```python
import http.client

# Enable HTTP debugging
http.client.HTTPConnection.debuglevel = 1

# Or use logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Version Information

### API Version
- Current: v1
- Compatible with OpenAI SDK v1.0+

### SDK Compatibility
```python
# Required packages
# openai>=1.0.0
# python-dotenv>=1.0.0
```

## Support

For API issues:
1. Check error messages and status codes
2. Review request/response logs
3. Test with simple requests first
4. Contact support if issue persists

Remember to always:
- Handle errors gracefully
- Implement retry logic
- Monitor token usage
- Secure API keys properly
