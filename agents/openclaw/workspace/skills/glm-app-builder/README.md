# GLM Application Builder Skill

A comprehensive skill for building applications using GLM models (glm-5, glm-5.1).

## What This Skill Provides

### 1. **Application Templates**
- Web applications (FastAPI + frontend)
- API services
- Data processing pipelines
- CLI tools
- Automation scripts

### 2. **GLM Integration**
- Complete API integration examples
- Model selection guidance
- Prompt engineering patterns
- Error handling and retry logic
- Cost optimization strategies

### 3. **Security Best Practices**
- Environment variable management
- Input validation and sanitization
- API key protection
- Rate limiting implementation
- Secure deployment configurations

### 4. **Deployment Ready**
- Docker configurations
- Kubernetes manifests
- Environment setup scripts
- Monitoring and logging
- Performance optimization

## Quick Start

### Create a New GLM Application

```bash
# Navigate to your project directory
cd /path/to/your/projects

# Run the GLM app creator script
python /path/to/skills/glm-app-builder/scripts/create_glm_app.py my-glm-app --type web
```

### Available Application Types

1. **Web Application** (`--type web`)
   - FastAPI backend
   - HTML/JavaScript frontend
   - Real-time chat interface
   - Health monitoring

2. **API Service** (`--type api`)
   - RESTful API endpoints
   - Authentication/authorization
   - Rate limiting
   - Comprehensive error handling

3. **CLI Tool** (`--type cli`)
   - Command-line interface
   - Configuration management
   - Batch processing
   - Script automation

## Key Features

### 🚀 **Easy Setup**
- One-command project generation
- Pre-configured environment
- Ready-to-run templates

### 🔒 **Security First**
- Built-in security headers
- Input validation
- API key management
- Secure defaults

### 📊 **Monitoring & Logging**
- Request/response logging
- Token usage tracking
- Performance metrics
- Error tracking

### 🐳 **Container Ready**
- Dockerfile included
- Docker Compose configuration
- Kubernetes manifests
- Health checks

## Usage Examples

### Basic Web Application
```python
from glm_app_builder import create_web_app

app = create_web_app(
    model="glm-5",
    api_key="your-api-key",
    features=["chat", "file_processing", "streaming"]
)
```

### API Service
```python
from glm_app_builder import create_api_service

service = create_api_service(
    model="glm-5.1",
    rate_limit="100/hour",
    authentication=True
)
```

### Data Pipeline
```python
from glm_app_builder import create_data_pipeline

pipeline = create_data_pipeline(
    model="glm-5",
    batch_size=10,
    parallel_processing=True
)
```

## Configuration

### Environment Variables
```bash
# Required
GLM_API_KEY=your_api_key_here
GLM_BASE_URL=https://api-ap-southeast-1.modelarts-maas.com/openai/v1

# Optional
MODEL=glm-5  # or glm-5.1
DEBUG=False
PORT=8000
HOST=0.0.0.0
```

### Model Selection
- **glm-5**: General purpose, faster, cost-effective
- **glm-5.1**: Enhanced capabilities, better for complex tasks

## Security Considerations

1. **API Key Protection**
   - Never commit API keys to version control
   - Use environment variables or secret management
   - Rotate keys regularly

2. **Input Validation**
   - Validate all user inputs
   - Sanitize prompts to prevent injection
   - Implement content filtering

3. **Rate Limiting**
   - Prevent API abuse
   - Implement exponential backoff
   - Monitor usage patterns

4. **Error Handling**
   - Graceful degradation
   - User-friendly error messages
   - Comprehensive logging

## Deployment

### Docker
```bash
# Build the image
docker build -t my-glm-app .

# Run the container
docker run -p 8000:8000 --env-file .env my-glm-app
```

### Docker Compose
```yaml
version: '3.8'
services:
  glm-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GLM_API_KEY=${GLM_API_KEY}
    restart: unless-stopped
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: glm-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: glm-app
        image: my-glm-app:latest
        env:
        - name: GLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: glm-secrets
              key: api-key
```

## Monitoring

### Health Checks
```bash
# Check application health
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "model": "glm-5",
  "glm_available": true
}
```

### Metrics
- Token usage per request
- Response times
- Error rates
- Model performance

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check API key validity
   - Verify network connectivity
   - Confirm base URL is correct

2. **Rate Limiting**
   - Implement exponential backoff
   - Reduce request frequency
   - Use request batching

3. **Model Availability**
   - Check model name spelling
   - Verify regional availability
   - Try alternative model

### Debug Mode
```bash
# Enable debug logging
DEBUG=True python src/app.py

# Check logs
tail -f logs/app.log
```

## Resources

### Documentation
- [GLM API Reference](references/glm_api.md)
- [Deployment Guide](references/deployment.md)
- [Security Guidelines](references/security.md)

### Examples
- [Chat Application](examples/chat_app.py)
- [Document Processor](examples/document_processor.py)
- [API Gateway](examples/api_gateway.py)

### Tools
- [Project Creator](scripts/create_glm_app.py)
- [Configuration Generator](scripts/generate_config.py)
- [Deployment Scripts](scripts/deploy/)

## Support

For issues and questions:
1. Check the troubleshooting guide
2. Review API documentation
3. Examine application logs
4. Contact support if needed

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This skill is provided under the MIT License.

---

**Note**: Always follow security best practices when deploying AI applications. Never expose API keys in client-side code and implement proper authentication and authorization.
