# OWASP Security Cheat Sheets

## OWASP Top 10 2021

### 1. Broken Access Control
**Prevention:**
- Implement proper authorization checks
- Deny by default
- Log access control failures
- Rate limit API access
- Invalidate JWT tokens after logout

**Code Example:**
```python
from functools import wraps
from flask import request, jsonify

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = get_current_user_role()
            if user_role != role:
                return jsonify({"error": "Insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/admin")
@require_role("admin")
def admin_panel():
    return "Admin panel"
```

### 2. Cryptographic Failures
**Prevention:**
- Use strong algorithms (AES-256, RSA-2048+)
- Never store passwords plaintext
- Use HTTPS everywhere
- Hash passwords with bcrypt/Argon2
- Rotate keys regularly

**Code Example:**
```python
import bcrypt
from cryptography.fernet import Fernet

# Password hashing
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Encryption
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_data(data: str) -> bytes:
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted: bytes) -> str:
    return cipher.decrypt(encrypted).decode()
```

### 3. Injection
**Prevention:**
- Use parameterized queries
- Validate and sanitize all inputs
- Use ORM with built-in protection
- Implement content security policy
- Escape output

**SQL Injection Prevention:**
```python
# BAD - Vulnerable
query = f"SELECT * FROM users WHERE username = '{username}'"

# GOOD - Parameterized
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))

# BEST - ORM
user = User.query.filter_by(username=username).first()
```

### 4. Insecure Design
**Prevention:**
- Threat modeling during design
- Secure by default principles
- Fail securely
- Defense in depth
- Least privilege

**Threat Modeling Questions:**
1. What are we building?
2. What can go wrong?
3. What are we doing about it?
4. Did we do a good job?

### 5. Security Misconfiguration
**Checklist:**
- [ ] Default accounts changed/disabled
- [ ] Error handling doesn't leak info
- [ ] Security headers set
- [ ] Unused features disabled
- [ ] Up-to-date software

**Security Headers:**
```python
SECURITY_HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
```

### 6. Vulnerable and Outdated Components
**Prevention:**
- Regular dependency updates
- Vulnerability scanning
- Software composition analysis
- Patch management process

**Tools:**
```bash
# Python
pip-audit
safety check

# Node.js
npm audit
npx snyk test

# Container
trivy image myapp:latest
```

### 7. Identification and Authentication Failures
**Prevention:**
- MFA implementation
- Strong password policies
- Secure password recovery
- Session management
- Limit failed attempts

**Password Policy:**
```python
import re

def validate_password(password: str) -> bool:
    """Enforce strong password policy"""
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True
```

### 8. Software and Data Integrity Failures
**Prevention:**
- Code signing
- Integrity checks
- Secure CI/CD pipeline
- Dependency verification
- Immutable infrastructure

**Integrity Check:**
```python
import hashlib

def verify_integrity(file_path: str, expected_hash: str) -> bool:
    """Verify file integrity"""
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_hash
```

### 9. Security Logging and Monitoring Failures
**Prevention:**
- Log security events
- Monitor for anomalies
- Alert on suspicious activity
- Retain logs appropriately
- Regular log review

**Security Logging:**
```python
import logging
import json
from datetime import datetime

security_logger = logging.getLogger("security")

def log_security_event(event_type: str, user: str, details: dict):
    """Log security events"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user": user,
        "details": details,
        "ip": request.remote_addr if request else None
    }
    security_logger.warning(json.dumps(log_entry))
```

### 10. Server-Side Request Forgery (SSRF)
**Prevention:**
- Validate and sanitize URLs
- Use allowlists for internal resources
- Disable unused URL schemes
- Use network segmentation

**SSRF Protection:**
```python
from urllib.parse import urlparse
import ipaddress

def is_safe_url(url: str, allowed_domains: list) -> bool:
    """Check if URL is safe to fetch"""
    parsed = urlparse(url)
    
    # Check scheme
    if parsed.scheme not in ['http', 'https']:
        return False
    
    # Check domain against allowlist
    if parsed.hostname not in allowed_domains:
        return False
    
    # Check for internal IPs
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private:
            return False
    except ValueError:
        pass  # Not an IP address
    
    return True
```

## API Security

### 1. Authentication
```python
# JWT Implementation
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET")

def create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
```

### 2. Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    default_limits=["100 per minute", "10 per second"]
)

@app.route("/api/data")
@limiter.limit("5 per minute")
def get_data():
    return {"data": "sensitive"}
```

### 3. Input Validation
```python
from pydantic import BaseModel, validator, constr
import re

class UserInput(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v
```

## Web Application Security

### 1. Cross-Site Scripting (XSS) Protection
```python
import html

def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent XSS"""
    # Escape HTML entities
    sanitized = html.escape(input_str)
    
    # Remove dangerous attributes
    dangerous_patterns = [
        r'on\w+\s*=',
        r'javascript:',
        r'data:',
        r'vbscript:'
    ]
    
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    return sanitized
```

### 2. Cross-Site Request Forgery (CSRF) Protection
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

@app.before_request
def check_csrf():
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        csrf.protect()
```

### 3. Clickjacking Protection
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
    return response
```

## Database Security

### 1. SQL Injection Prevention
```python
# Using SQLAlchemy (ORM)
from sqlalchemy import text

# SAFE - Parameterized query
stmt = text("SELECT * FROM users WHERE username = :username")
result = db.session.execute(stmt, {"username": username})

# SAFE - ORM query
user = User.query.filter_by(username=username).first()
```

### 2. NoSQL Injection Prevention
```python
# MongoDB example
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.mydb

# UNSAFE
query = {"$where": f"this.username == '{username}'"}

# SAFE
query = {"username": username}
result = db.users.find(query)
```

## File Upload Security

### 1. File Validation
```python
import magic
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/gif'}

def validate_file(file):
    """Validate uploaded file"""
    # Check extension
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, "Invalid file extension"
    
    # Check MIME type
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)  # Reset file pointer
    if mime not in ALLOWED_MIME_TYPES:
        return False, "Invalid file type"
    
    # Check file size (5MB max)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > 5 * 1024 * 1024:
        return False, "File too large"
    
    return True, filename
```

## Security Headers Checklist

### Essential Headers
```python
SECURITY_HEADERS = {
    # Prevent clickjacking
    'X-Frame-Options': 'DENY',
    
    # Prevent MIME sniffing
    'X-Content-Type-Options': 'nosniff',
    
    # XSS protection
    'X-XSS-Protection': '1; mode=block',
    
    # HTTPS enforcement
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    
    # Referrer policy
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    
    # Content Security Policy
    'Content-Security-Policy': "default-src 'self'; script-src 'self'",
    
    # Permissions policy
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
}
```

## Regular Security Audits

### 1. Automated Scanning
```bash
# Dependency scanning
pip-audit
npm audit
snyk test

# Static analysis
bandit -r .
semgrep --config auto

# Container scanning
trivy image myapp:latest

# Secret scanning
gitleaks detect --source .
```

### 2. Manual Checks
- Review access controls
- Test authentication flows
- Verify error handling
- Check logging configuration
- Review third-party dependencies

## Incident Response

### 1. Preparation
- Incident response plan
- Contact list
- Communication channels
- Backup procedures

### 2. Detection & Analysis
- Monitor logs
- Alert on anomalies
- Investigate incidents
- Document findings

### 3. Containment & Eradication
- Isolate affected systems
- Apply patches
- Remove malware
- Change credentials

### 4. Recovery & Lessons
- Restore from backups
- Monitor for recurrence
- Update procedures
- Conduct post-mortem

## Resources

### Tools
- OWASP ZAP: Web app scanner
- Burp Suite: Security testing
- Nmap: Network scanning
- Metasploit: Penetration testing

### References
- OWASP Testing Guide
- OWASP Code Review Guide
- NIST Cybersecurity Framework
- CIS Benchmarks

### Training
- OWASP Web Security Training
- SANS Security Courses
- TryHackMe / HackTheBox
- Security certifications (CISSP, CEH, OSCP)
