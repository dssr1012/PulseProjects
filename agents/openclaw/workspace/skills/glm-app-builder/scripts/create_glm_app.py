#!/usr/bin/env python3
"""
GLM Application Creator Script

This script creates a basic GLM-powered application with security best practices.
"""

import os
import sys
import argparse
from pathlib import Path

def create_project_structure(project_name: str, app_type: str = "web"):
    """Create project structure based on application type"""
    
    project_path = Path(project_name)
    
    if project_path.exists():
        print(f"Error: Directory '{project_name}' already exists")
        sys.exit(1)
    
    # Create directory structure
    directories = [
        project_path,
        project_path / "src",
        project_path / "tests",
        project_path / "config",
        project_path / "logs",
    ]
    
    if app_type == "web":
        directories.extend([
            project_path / "static",
            project_path / "templates",
        ])
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create files based on app type
    if app_type == "web":
        create_web_app(project_path)
    elif app_type == "api":
        create_api_app(project_path)
    elif app_type == "cli":
        create_cli_app(project_path)
    else:
        print(f"Unknown app type: {app_type}")
        sys.exit(1)
    
    print(f"\n✅ Project '{project_name}' created successfully!")
    print(f"📁 Location: {project_path.absolute()}")
    print("\nNext steps:")
    print(f"1. cd {project_name}")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("4. pip install -r requirements.txt")
    print("5. Set your GLM_API_KEY in .env file")
    
    if app_type == "web":
        print("6. python src/app.py")
    elif app_type == "cli":
        print("6. pip install -e .")
        print("7. glm-cli --help")

def create_web_app(project_path: Path):
    """Create a web application structure"""
    
    # Create requirements.txt
    requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
openai==1.3.0
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.1
jinja2==3.1.2
"""
    
    (project_path / "requirements.txt").write_text(requirements)
    
    # Create .env file
    env_content = """# GLM Configuration
GLM_API_KEY=your_api_key_here
GLM_BASE_URL=https://api-ap-southeast-1.modelarts-maas.com/openai/v1
MODEL=glm-5

# Application Configuration
DEBUG=True
PORT=8000
HOST=0.0.0.0

# Security
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if needed)
# DATABASE_URL=postgresql://user:password@localhost/dbname
"""
    
    (project_path / ".env").write_text(env_content)
    
    # Create .gitignore
    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
"""
    
    (project_path / ".gitignore").write_text(gitignore)
    
    # Create main application file
    app_content = '''#!/usr/bin/env python3
"""
GLM-Powered Web Application

A FastAPI web application with GLM model integration.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GLM Web Application",
    description="A web application powered by GLM models",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize GLM client
try:
    client = OpenAI(
        api_key=os.getenv("GLM_API_KEY"),
        base_url=os.getenv("GLM_BASE_URL", "https://api-ap-southeast-1.modelarts-maas.com/openai/v1")
    )
    DEFAULT_MODEL = os.getenv("MODEL", "glm-5")
    logger.info(f"GLM client initialized with model: {DEFAULT_MODEL}")
except Exception as e:
    logger.error(f"Failed to initialize GLM client: {e}")
    client = None

# Pydantic models
class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=1000)
    model: Optional[str] = Field(default=DEFAULT_MODEL)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=1000, ge=1, le=4000)

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    model: str
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": DEFAULT_MODEL,
        "glm_available": client is not None
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint for GLM model"""
    if not client:
        raise HTTPException(status_code=503, detail="GLM service unavailable")
    
    try:
        import time
        start_time = time.time()
        
        # Call GLM API
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": request.message}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        processing_time = time.time() - start_time
        
        # Extract response
        chat_response = response.choices[0].message.content
        
        return ChatResponse(
            response=chat_response,
            model=response.model,
            tokens_used=response.usage.total_tokens if response.usage else None,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"GLM API error: {e}")
        raise HTTPException(status_code=500, detail=f"GLM API error: {str(e)}")

@app.get("/api/models")
async def list_models():
    """List available GLM models"""
    if not client:
        raise HTTPException(status_code=503, detail="GLM service unavailable")
    
    try:
        # Note: This assumes the API supports listing models
        # Adjust based on actual API capabilities
        return {
            "available_models": ["glm-5", "glm-5.1"],
            "default_model": DEFAULT_MODEL,
            "base_url": os.getenv("GLM_BASE_URL")
        }
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing models: {str(e)}")

# Security middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # CORS headers (adjust as needed)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    uvicorn.run(
        "src.app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
'''
    
    (project_path / "src" / "app.py").write_text(app_content)
    
    # Create HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GLM Web Application</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 800px;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .content {
            padding: 30px;
        }
        
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .model-selector {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .model-selector select {
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }
        
        .model-selector select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .message-input {
            position: relative;
        }
        
        .message-input textarea {
            width: 100%;
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            font-size: 1rem;
            resize: vertical;
            min-height: 120px;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        
        .message-input textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }
        
        .temperature-slider {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .temperature-slider input {
            width: 150px;
        }
        
        .temperature-value {
            font-weight: bold;
            color: #667eea;
            min-width: 40px;
        }
        
        .send-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .send-button:active {
            transform: translateY(0);
        }
        
        .send-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .response-container {
            margin-top: 30px;
        }
        
        .response-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .response-header h3 {
            color: #333;
        }
        
        .stats {
            display: flex;
            gap: 15px;
            font-size: 0.9rem;
            color: #666;
        }
        
        .stat {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .response-content {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            line-height: 1.6;
            white-space: pre-wrap;
            font-size: 1.05rem;
            border-left: 4px solid #667eea;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: #fee;
            color: #c00;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 4px solid #c00;
            display: none;
        }
        
        .error.active {
            display: block;
        }
        
        .health-status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .health-status.healthy {
            background: #d4edda;
            color: #155724;
        }
        
        .health-status.unhealthy {
            background: #f8d7da;
            color: #721c24;
        }
        
        @media (max-width: 600px) {
            .container {
                border-radius: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .controls {
                flex-direction: column;
                gap: 15px;
                align-items: stretch;
            }
            
            .temperature-slider {
                justify-content: space-between;
            }
            
            .send-button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>GLM Web Application</h1>
            <p>Powered by GLM AI Models</p>
            <div style="margin-top: 15px;">
                <span class="health-status" id="healthStatus">Checking...</span>
            </div>
        </div>
        
        <div class="content">
            <div class="chat-container">
                <div class="model-selector">
                    <label for="modelSelect">Model:</label>
                    <select id="modelSelect">
                        <option value="glm-5">GLM-5</option>
                        <option value="glm-5.1">GLM-5.1</option>
                    </select>
                </div>
                
                <div class="message-input">
                    <textarea 
                        id="messageInput" 
                        placeholder="Type your message here... (Press Shift+Enter for new line, Enter to send)"
                        rows="4"
                    ></textarea>
                    <div class="controls">
                        <div class="temperature-slider">
                            <span>Temperature:</span>
                            <input type="range" id="temperatureSlider" min="0" max="20" value="7" step="1">
                            <span class="temperature-value" id="temperatureValue">0.7</span>
                        </div>
                        <button class="send-button" id="sendButton" onclick="sendMessage()">
                            Send Message
                        </button>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Thinking...</p>
                </div>
                
                <div class="error" id="error"></div>
                
                <div class="response-container" id="responseContainer" style="display: none;">
                    <div class="response-header">
                        <h3>Response</h3>
                        <div class="stats">
                            <div class="stat" id="modelStat">
                                <span>Model:</span>
                                <strong id="modelName">-</strong>
                            </div>
                            <div class="stat" id="tokensStat">
                                <span>Tokens:</span>
                                <strong id="tokensUsed">-</strong>
                            </div>
                            <div class="stat" id="timeStat">
                                <span>Time:</span>
                                <strong id="processingTime">-</strong>s
                            </div>
                        </div>
                    </div>
                    <div class="response-content" id="responseContent">
                        <!-- Response will appear here -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Update temperature display
        const tempSlider = document.getElementById('temperatureSlider');
        const tempValue = document.getElementById('temperatureValue');
        
        tempSlider.addEventListener('input', function() {
            tempValue.textContent = (this.value / 10).toFixed(1);
        });
        
        // Handle Enter key (send) and Shift+Enter (new line)
        const messageInput = document.getElementById('messageInput');
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Check health status
        async function checkHealth() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                
                const healthStatus = document.getElementById('healthStatus');
                if (data.status === 'healthy' && data.glm_available) {
                    healthStatus.textContent = '✅ Healthy';
                    healthStatus.className = 'health-status healthy';
                } else {
                    healthStatus.textContent = '⚠️ Issues';
                    healthStatus.className = 'health-status unhealthy';
                }
            } catch (error) {
                const healthStatus = document.getElementById('healthStatus');
                healthStatus.textContent = '❌ Unreachable';
                healthStatus.className = 'health-status unhealthy';
            }
        }
        
        // Send message to GLM API
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) {
                showError('Please enter a message');
                return;
            }
            
            const model = document.getElementById('modelSelect').value;
            const temperature = parseFloat(tempValue.textContent);
            
            // Show loading, hide previous response and error
            document.getElementById('loading').classList.add('active');
            document.getElementById('responseContainer').style.display = 'none';
            document.getElementById('error').classList.remove('active');
            
            // Disable send button
            const sendButton = document.getElementById('sendButton');
            sendButton.disabled = true;
            sendButton.textContent = 'Sending...';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        model: model,
                        temperature: temperature,
                        max_tokens: 1000
                    })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Unknown error');
                }
                
                // Update response display
                document.getElementById('responseContent').textContent = data.response;
                document.getElementById('modelName').textContent = data.model;
                document.getElementById('tokensUsed').textContent = data.tokens_used || 'N/A';
                document.getElementById('processingTime').textContent = data.processing_time ? data.processing_time.toFixed(2) : 'N/A';
                
                // Show response container
                document.getElementById('responseContainer').style.display = 'block';
                
                // Clear input
                messageInput.value = '';
                
            } catch (error) {
                showError(error.message);
            } finally {
                // Hide loading, re-enable button
                document.getElementById('loading').classList.remove('active');
                sendButton.disabled = false;
                sendButton.textContent = 'Send Message';
            }
        }
        
        // Show error message
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = `Error: ${message}`;
            errorDiv.classList.add('active');
        }
        
        // Check health on page load
        checkHealth();
        
        // Check health every 30 seconds
        setInterval(checkHealth, 30000);
