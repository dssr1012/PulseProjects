---
name: glm-app-builder
description: Build applications using GLM models with structured workflows for web apps, APIs, data processing, and automation. Use when user requests to create an application, web service, API, or automation tool using GLM models (glm-5, glm-5.1). Includes project setup, model integration, deployment guidance, and best practices for GLM-based applications.
---

# GLM Application Builder

Build production-ready applications using GLM models. This skill provides structured workflows for creating web apps, APIs, data processing pipelines, and automation tools powered by GLM models.

## Quick Start

When starting a GLM application project:

1. **Choose your GLM model**:
   - `glm-5`: General purpose, good for most applications
   - `glm-5.1`: Enhanced capabilities, better for complex reasoning tasks

2. **Select application type**:
   - Web application (Flask/FastAPI + frontend)
   - API service (FastAPI/Express)
   - Data processing pipeline
   - Automation/scripting tool
   - Chat/assistant application

3. **Follow the appropriate workflow below**

## Web Application Workflow

### 1. Project Setup
```bash
# Create project structure
mkdir my-glm-app
cd my-glm-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn openai python-dotenv
```

### 2. Environment Configuration
Create `.env`:
```env
GLM_API_KEY=your_api_key_here
GLM_BASE_URL=https://api-ap-southeast-1.modelarts-maas.com/openai/v1
MODEL=glm-5  # or glm-5.1
PORT=8000
```

### 3. Basic GLM Integration
Create `app.py`:
```python
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GLM Application")

client = OpenAI(
    api_key=os.getenv("GLM_API_KEY"),
    base_url=os.getenv("GLM_BASE_URL")
)

class ChatRequest(BaseModel):
    message: str
    model: str = os.getenv("MODEL", "glm-5")
    temperature: float = 0.7

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.message}],
            temperature=request.temperature
        )
        return {
            "response": response.choices[0].message.content,
            "model": response.model,
            "usage": response.usage.dict() if response.usage else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": os.getenv("MODEL")}
```

### 4. Frontend Integration
Create `templates/index.html` for a simple web interface or use a React/Vue frontend.

## API Service Workflow

### 1. Advanced GLM Features
Create `glm_service.py` with enhanced capabilities:

```python
import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GLM_API_KEY"),
            base_url=os.getenv("GLM_BASE_URL")
        )
        self.default_model = os.getenv("MODEL", "glm-5")
    
    def chat_completion(self, messages: List[dict], model: Optional[str] = None, **kwargs):
        """Basic chat completion"""
        return self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            **kwargs
        )
    
    def streaming_chat(self, messages: List[dict], model: Optional[str] = None, **kwargs):
        """Streaming response for real-time applications"""
        return self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            stream=True,
            **kwargs
        )
    
    def function_calling(self, messages: List[dict], functions: List[dict], model: Optional[str] = None):
        """GLM function calling support"""
        return self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            functions=functions,
            function_call="auto"
        )
```

### 2. Rate Limiting & Error Handling
Implement robust error handling and rate limiting for production use.

## Data Processing Pipeline

### 1. Batch Processing with GLM
Create `data_processor.py`:

```python
import asyncio
from typing import List, Any
import aiohttp
import json

class GLMDataProcessor:
    def __init__(self, api_key: str, base_url: str, model: str = "glm-5"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.session = None
    
    async def process_batch(self, items: List[Any], process_func) -> List[Any]:
        """Process batch of items using GLM"""
        results = []
        for item in items:
            try:
                result = await self._process_single(item, process_func)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "item": item})
        return results
    
    async def _process_single(self, item: Any, process_func):
        # Implement specific processing logic
        pass
```

## Deployment Guidelines

### 1. Docker Setup
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  glm-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GLM_API_KEY=${GLM_API_KEY}
      - GLM_BASE_URL=${GLM_BASE_URL}
      - MODEL=${MODEL:-glm-5}
    restart: unless-stopped
```

### 3. Environment Variables Management
Use secrets management for production:
- Kubernetes Secrets
- AWS Secrets Manager
- HashiCorp Vault
- .env files for development only

## Best Practices

### 1. Model Selection
- **glm-5**: General tasks, good balance of speed and quality
- **glm-5.1**: Complex reasoning, better for analytical tasks

### 2. Prompt Engineering
- Be specific and structured in prompts
- Use system messages to set context
- Include examples for complex tasks
- Chain multiple calls for multi-step reasoning

### 3. Error Handling
- Implement retry logic with exponential backoff
- Log errors with context for debugging
- Set appropriate timeouts
- Handle rate limits gracefully

### 4. Monitoring
- Track token usage per request
- Monitor response times
- Log model choices and parameters
- Set up alerts for error rates

## Common Patterns

### 1. Chat Application
```python
# See references/chat_patterns.md for complete chat implementation
```

### 2. Document Processing
```python
# See references/document_processing.md for OCR + GLM workflows
```

### 3. Code Generation
```python
# See references/code_generation.md for GLM-assisted coding
```

## Testing

### 1. Unit Tests
```python
import pytest
from unittest.mock import Mock, patch
from app import GLMService

def test_glm_service_initialization():
    service = GLMService()
    assert service.default_model == "glm-5"
```

### 2. Integration Tests
Test actual API calls in staging environment.

## Security Considerations

1. **API Key Protection**: Never hardcode keys, use environment variables
2. **Input Validation**: Sanitize all user inputs
3. **Rate Limiting**: Prevent abuse
4. **Content Filtering**: Implement moderation layer if needed

## Performance Optimization

1. **Caching**: Cache frequent similar queries
2. **Batching**: Process multiple requests together when possible
3. **Streaming**: Use streaming for real-time applications
4. **Model Switching**: Use glm-5 for simple tasks, glm-5.1 for complex ones

## References

- [GLM API Documentation](references/glm_api.md) - Complete API reference
- [Deployment Guides](references/deployment.md) - Cloud deployment options
- [Example Projects](references/examples.md) - Sample applications
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
