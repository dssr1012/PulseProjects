---
name: security-checker
description: Comprehensive security assessment for AI interactions, applications, and systems. Use when evaluating security of AI conversations, application deployments, API integrations, or system configurations. Includes threat modeling, vulnerability assessment, privacy checks, and security best practices for AI-powered applications.
---

# Security Checker

Comprehensive security assessment tool for AI interactions, applications, and systems. This skill provides structured security evaluation workflows for identifying vulnerabilities, assessing risks, and implementing security best practices.

## Quick Assessment Framework

When starting a security assessment:

1. **Identify Scope**: What system/application/conversation needs checking?
2. **Threat Model**: Who are potential attackers? What assets need protection?
3. **Check Categories**: Authentication, authorization, data protection, API security, etc.
4. **Generate Report**: Document findings and recommendations
5. **Remediation Plan**: Prioritized fixes and improvements

## AI Conversation Security Assessment

### 1. Conversation Analysis Checklist

**✅ Privacy Protection**
- [ ] No personally identifiable information (PII) exposed
- [ ] No sensitive credentials shared in plain text
- [ ] No confidential business information disclosed
- [ ] Proper data anonymization applied where needed

**✅ Prompt Security**
- [ ] No prompt injection vulnerabilities
- [ ] Input validation and sanitization in place
- [ ] Context boundaries maintained
- [ ] No unauthorized system access through prompts

**✅ Output Safety**
- [ ] Content filtering for harmful outputs
- [ ] Hallucination detection and mitigation
- [ ] Fact-checking mechanisms
- [ ] Ethical guidelines followed

### 2. Conversation Security Script
Create `conversation_security.py`:

```python
import re
from typing import List, Dict, Tuple

class ConversationSecurityAnalyzer:
    def __init__(self):
        self.pii_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone numbers
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{3}[-.]?\d{2}[-.]?\d{4}\b',  # SSN (US)
            r'\b[A-Z]{2}\d{6,7}\b',  # Passport numbers
            r'\b\d{16}\b',  # Credit card numbers
        ]
        
    def analyze_conversation(self, messages: List[Dict]) -> Dict:
        """Analyze conversation for security issues"""
        findings = {
            "pii_detected": [],
            "sensitive_keywords": [],
            "security_risks": [],
            "recommendations": []
        }
        
        for msg in messages:
            content = msg.get("content", "")
            # Check for PII
            pii_found = self._check_pii(content)
            if pii_found:
                findings["pii_detected"].extend(pii_found)
            
            # Check for sensitive information
            sensitive = self._check_sensitive_content(content)
            if sensitive:
                findings["sensitive_keywords"].extend(sensitive)
            
            # Check for security risks
            risks = self._check_security_risks(content)
            if risks:
                findings["security_risks"].extend(risks)
        
        return findings
    
    def _check_pii(self, text: str) -> List[str]:
        """Check for personally identifiable information"""
        pii_found = []
        for pattern in self.pii_patterns:
            matches = re.findall(pattern, text)
            if matches:
                pii_found.extend(matches)
        return pii_found
    
    def _check_sensitive_content(self, text: str) -> List[str]:
        """Check for sensitive keywords"""
        sensitive_terms = [
            "password", "secret", "key", "token", "credential",
            "api_key", "private", "confidential", "restricted"
        ]
        found = []
        for term in sensitive_terms:
            if term.lower() in text.lower():
                found.append(term)
        return found
    
    def _check_security_risks(self, text: str) -> List[str]:
        """Check for security risk indicators"""
        risks = []
        
        # Command injection patterns
        if any(cmd in text.lower() for cmd in ["rm -rf", "sudo", "chmod 777", "eval(", "exec("]):
            risks.append("Potential command injection")
        
        # SQL injection patterns
        if any(pattern in text.lower() for pattern in ["' or '1'='1", "union select", "drop table"]):
            risks.append("Potential SQL injection pattern")
        
        # Path traversal
        if any(pattern in text for pattern in ["../", "..\\", "/etc/passwd"]):
            risks.append("Potential path traversal")
        
        return risks
```

## Application Security Assessment

### 1. Web Application Security Checklist

**✅ Authentication & Authorization**
- [ ] Strong password policies enforced
- [ ] Multi-factor authentication available
- [ ] Role-based access control implemented
- [ ] Session management secure
- [ ] Password hashing using bcrypt/Argon2

**✅ API Security**
- [ ] API keys properly secured and rotated
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] Output encoding to prevent XSS
- [ ] CORS properly configured
- [ ] HTTPS enforced

**✅ Data Protection**
- [ ] Encryption at rest for sensitive data
- [ ] Encryption in transit (TLS 1.2+)
- [ ] Data minimization principles followed
- [ ] Proper data retention policies
- [ ] Secure deletion of sensitive data

**✅ GLM-Specific Security**
- [ ] API keys stored in environment variables/secrets
- [ ] Model outputs validated and sanitized
- [ ] Prompt injection protection
- [ ] Context window limits enforced
- [ ] Audit logging for model usage

### 2. Security Configuration Scanner
Create `config_scanner.py`:

```python
import os
import json
import yaml
from typing import Dict, List

class SecurityConfigScanner:
    def __init__(self):
        self.critical_checks = [
            self.check_env_vars,
            self.check_database_config,
            self.check_api_security,
            self.check_authentication
        ]
    
    def scan_configuration(self, config_path: str) -> Dict:
        """Scan configuration files for security issues"""
        findings = {
            "critical": [],
            "warning": [],
            "info": [],
            "passed": []
        }
        
        config = self._load_config(config_path)
        
        for check in self.critical_checks:
            result = check(config)
            findings[result["level"]].append(result["message"])
        
        return findings
    
    def check_env_vars(self, config: Dict) -> Dict:
        """Check for hardcoded secrets"""
        issues = []
        
        # Check for hardcoded API keys
        if config.get("api_key") and not config["api_key"].startswith("${"):
            issues.append("Hardcoded API key found")
        
        # Check for default passwords
        if config.get("password") in ["password", "admin", "123456"]:
            issues.append("Weak/default password detected")
        
        return {
            "level": "critical" if issues else "passed",
            "message": "Environment variables: " + ("; ".join(issues) if issues else "OK")
        }
    
    def check_database_config(self, config: Dict) -> Dict:
        """Check database security configuration"""
        issues = []
        
        db_config = config.get("database", {})
        
        # Check for default ports
        if db_config.get("port") in [3306, 5432, 27017]:
            issues.append("Using default database port")
        
        # Check for weak authentication
        if db_config.get("username") == "root" or db_config.get("username") == "admin":
            issues.append("Using privileged database user")
        
        return {
            "level": "warning" if issues else "passed",
            "message": "Database config: " + ("; ".join(issues) if issues else "OK")
        }
```

## API Security Assessment

### 1. API Security Checklist

**✅ Authentication**
- [ ] API keys/tokens used for authentication
- [ ] JWT tokens properly signed and validated
- [ ] Token expiration implemented
- [ ] Refresh token mechanism secure

**✅ Authorization**
- [ ] Principle of least privilege followed
- [ ] Scope-based access control
- [ ] Resource-level permissions
- [ ] Regular permission reviews

**✅ Input Validation**
- [ ] All inputs validated and sanitized
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] File upload validation

**✅ Monitoring & Logging**
- [ ] All API calls logged
- [ ] Suspicious activity detection
- [ ] Rate limiting logs
- [ ] Error handling without information leakage

### 2. API Security Test Suite
Create `api_security_tests.py`:

```python
import requests
import json
from typing import Dict, List

class APISecurityTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.test_cases = [
            self.test_authentication,
            self.test_input_validation,
            self.test_rate_limiting,
            self.test_error_handling
        ]
    
    def run_security_tests(self) -> Dict:
        """Run comprehensive API security tests"""
        results = {}
        
        for test in self.test_cases:
            test_name = test.__name__
            try:
                result = test()
                results[test_name] = result
            except Exception as e:
                results[test_name] = {"status": "failed", "error": str(e)}
        
        return results
    
    def test_authentication(self) -> Dict:
        """Test authentication mechanisms"""
        # Test without authentication
        response = requests.get(f"{self.base_url}/protected")
        if response.status_code not in [401, 403]:
            return {"status": "failed", "issue": "Missing authentication check"}
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{self.base_url}/protected", headers=headers)
        if response.status_code not in [401, 403]:
            return {"status": "failed", "issue": "Invalid token accepted"}
        
        return {"status": "passed"}
    
    def test_input_validation(self) -> Dict:
        """Test input validation for common attacks"""
        tests = [
            ("/api/users?name=<script>alert(1)</script>", "XSS"),
            ("/api/users?id=1 OR 1=1", "SQL Injection"),
            ("/api/files?path=../../../etc/passwd", "Path Traversal"),
        ]
        
        issues = []
        for endpoint, attack_type in tests:
            response = requests.get(f"{self.base_url}{endpoint}")
            if response.status_code == 200:
                issues.append(f"{attack_type} vulnerability detected")
        
        return {
            "status": "passed" if not issues else "failed",
            "issues": issues
        }
```

## Deployment Security

### 1. Container Security
```yaml
# docker-compose.security.yml
version: '3.8'

services:
  app:
    build: .
    # Security best practices
    user: "1000:1000"  # Non-root user
    read_only: true  # Read-only filesystem
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only necessary capabilities
    networks:
      - internal
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 2. Kubernetes Security
```yaml
# k8s-security.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

## Incident Response

### 1. Security Incident Checklist
```python
# incident_response.py
SECURITY_INCIDENT_CHECKLIST = {
    "detection": [
        "Identify affected systems",
        "Determine scope of breach",
        "Preserve evidence",
        "Notify security team"
    ],
    "containment": [
        "Isolate affected systems",
        "Change compromised credentials",
        "Block malicious IPs",
        "Implement temporary fixes"
    ],
    "eradication": [
        "Remove malware/backdoors",
        "Patch vulnerabilities",
        "Clean infected systems",
        "Update security controls"
    ],
    "recovery": [
        "Restore from clean backups",
        "Monitor for recurrence",
        "Update incident response plan",
        "Conduct post-mortem"
    ]
}
```

## Compliance & Standards

### 1. Security Frameworks
- **OWASP Top 10**: Web application security risks
- **NIST Cybersecurity Framework**: Risk management
- **ISO 27001**: Information security management
- **GDPR**: Data protection and privacy
- **HIPAA**: Healthcare data security

### 2. Security Headers for Web Apps
```python
# security_headers.py
SECURITY_HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
}
```

## Continuous Security

### 1. Automated Security Scanning
```bash
# Security scanning pipeline
#!/bin/bash

# Dependency scanning
pip-audit
npm audit
snyk test

# Static analysis
bandit -r .  # Python security scanning
semgrep --config auto

# Container scanning
trivy image myapp:latest

# Secret scanning
gitleaks detect --source . -v
```

### 2. Security Monitoring Setup
```python
# security_monitoring.py
import logging
from datetime import datetime

class SecurityMonitor:
    def __init__(self):
        self.logger = logging.getLogger("security")
        
    def log_security_event(self, event_type: str, details: Dict):
        """Log security events for monitoring"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details,
            "severity": self._determine_severity(event_type)
        }
        
        self.logger.warning(json.dumps(log_entry))
        
        # Alert if critical
        if log_entry["severity"] == "critical":
            self._send_alert(log_entry)
```

## References

- [OWASP Cheat Sheets](references/owasp_cheatsheets.md) - Security best practices
- [GLM Security Guidelines](references/glm_security.md) - AI-specific security
- [Compliance Checklists](references/compliance.md) - Regulatory requirements
- [Incident Response](references/incident_response.md) - Handling security breaches
- [Security Tools](references/tools.md) - Recommended security tools
