#!/usr/bin/env python3
"""
Security Scanner for AI Applications

Comprehensive security assessment tool for AI-powered applications.
Checks for common vulnerabilities and security best practices.
"""

import os
import sys
import json
import re
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any
import yaml
try:
    import toml
except ImportError:
    toml = None

class SecurityScanner:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.findings = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "info": [],
            "passed": []
        }
        
    def log(self, message: str, level: str = "info"):
        """Log messages based on verbosity"""
        if self.verbose or level in ["critical", "high", "error"]:
            print(f"[{level.upper()}] {message}")
    
    def add_finding(self, level: str, category: str, message: str, file: str = None, line: int = None):
        """Add a security finding"""
        finding = {
            "category": category,
            "message": message,
            "file": file,
            "line": line
        }
        self.findings[level].append(finding)
        self.log(f"{category}: {message}", level)
    
    def scan_directory(self, directory: str) -> Dict[str, List]:
        """Scan a directory for security issues"""
        self.log(f"Scanning directory: {directory}")
        
        # Run all security checks
        self.check_env_files(directory)
        self.check_config_files(directory)
        self.check_source_code(directory)
        self.check_dependencies(directory)
        self.check_permissions(directory)
        self.check_ai_specific(directory)
        
        return self.findings
    
    def check_env_files(self, directory: str):
        """Check for security issues in environment files"""
        env_files = [".env", ".env.local", ".env.production", ".env.development"]
        
        for env_file in env_files:
            file_path = Path(directory) / env_file
            if file_path.exists():
                self.log(f"Checking environment file: {env_file}")
                self._check_env_file(file_path)
    
    def _check_env_file(self, file_path: Path):
        """Check a specific .env file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Check for hardcoded secrets
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Check for sensitive keys
                    sensitive_keywords = [
                        'key', 'secret', 'token', 'password', 'credential',
                        'api_key', 'private_key', 'secret_key', 'access_key',
                        'auth', 'jwt', 'session'
                    ]
                    
                    for keyword in sensitive_keywords:
                        if keyword in key.lower():
                            # Check if value looks like a secret
                            if value and not value.startswith('${') and len(value) > 10:
                                self.add_finding(
                                    "high",
                                    "Hardcoded Secret",
                                    f"Hardcoded {key} found in {file_path.name}",
                                    str(file_path),
                                    i
                                )
                
                # Check for commented secrets
                if '#' in line:
                    comment_part = line.split('#')[1]
                    if any(keyword in comment_part.lower() for keyword in ['password=', 'key=', 'secret=']):
                        self.add_finding(
                            "medium",
                            "Commented Secret",
                            f"Commented secret found in {file_path.name}",
                            str(file_path),
                            i
                        )
        
        except Exception as e:
            self.log(f"Error checking {file_path}: {e}", "error")
    
    def check_config_files(self, directory: str):
        """Check configuration files for security issues"""
        config_patterns = [
            "*.json", "*.yaml", "*.yml", "*.toml", "*.ini",
            "config/*", "configs/*", "configuration/*"
        ]
        
        for pattern in config_patterns:
            for file_path in Path(directory).rglob(pattern):
                if file_path.is_file():
                    self._check_config_file(file_path)
    
    def _check_config_file(self, file_path: Path):
        """Check a specific config file"""
        try:
            content = file_path.read_text()
            
            # Check for hardcoded credentials in config files
            credential_patterns = [
                r'"password"\s*:\s*"[^"]+"',
                r"'password'\s*:\s*'[^']+'",
                r'"api[_-]?key"\s*:\s*"[^"]+"',
                r"'api[_-]?key'\s*:\s*'[^']+'",
                r'"secret"\s*:\s*"[^"]+"',
                r"'secret'\s*:\s*'[^']+'",
                r'"token"\s*:\s*"[^"]+"',
                r"'token'\s*:\s*'[^']+'",
            ]
            
            for i, line in enumerate(content.split('\n'), 1):
                for pattern in credential_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.add_finding(
                            "high",
                            "Hardcoded Credential",
                            f"Hardcoded credential found in {file_path.name}",
                            str(file_path),
                            i
                        )
            
            # Check for insecure configurations
            insecure_patterns = [
                (r'debug\s*[:=]\s*true', "Debug mode enabled in production"),
                (r'debug\s*[:=]\s*"true"', "Debug mode enabled in production"),
                (r'debug\s*[:=]\s*\'true\'', "Debug mode enabled in production"),
                (r'cors\s*[:=]\s*\*', "Overly permissive CORS configuration"),
                (r'https?\s*[:=]\s*false', "HTTPS disabled"),
            ]
            
            for pattern, message in insecure_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.add_finding(
                        "medium",
                        "Insecure Configuration",
                        f"{message} in {file_path.name}",
                        str(file_path)
                    )
        
        except Exception as e:
            self.log(f"Error checking {file_path}: {e}", "error")
    
    def check_source_code(self, directory: str):
        """Check source code for security vulnerabilities"""
        code_extensions = ['.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c']
        
        for ext in code_extensions:
            for file_path in Path(directory).rglob(f"*{ext}"):
                if file_path.is_file():
                    self._check_source_file(file_path)
    
    def _check_source_file(self, file_path: Path):
        """Check a specific source file for vulnerabilities"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            # Check for common vulnerabilities
            for i, line in enumerate(lines, 1):
                line_lower = line.lower()
                
                # SQL Injection patterns
                sql_patterns = [
                    (r'execute\(.*\+', "Potential SQL injection"),
                    (r'executescalar\(.*\+', "Potential SQL injection"),
                    (r'query\(.*\+', "Potential SQL injection"),
                ]
                
                for pattern, message in sql_patterns:
                    if re.search(pattern, line):
                        self.add_finding(
                            "critical",
                            "SQL Injection",
                            f"{message} in {file_path.name}",
                            str(file_path),
                            i
                        )
                
                # Command Injection patterns
                cmd_patterns = [
                    (r'os\.system\(', "Potential command injection"),
                    (r'subprocess\.call\(', "Potential command injection"),
                    (r'subprocess\.popen\(', "Potential command injection"),
                    (r'eval\(', "Potential code injection"),
                    (r'exec\(', "Potential code injection"),
                ]
                
                for pattern, message in cmd_patterns:
                    if pattern in line_lower and 'import' not in line_lower:
                        self.add_finding(
                            "critical",
                            "Command Injection",
                            f"{message} in {file_path.name}",
                            str(file_path),
                            i
                        )
                
                # Hardcoded secrets in code
                secret_patterns = [
                    (r'password\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded password"),
                    (r'api[_-]?key\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded API key"),
                    (r'secret[_-]?key\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded secret key"),
                    (r'token\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded token"),
                ]
                
                for pattern, message in secret_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.add_finding(
                            "high",
                            "Hardcoded Secret",
                            f"{message} in {file_path.name}",
                            str(file_path),
                            i
                        )
                
                # Insecure randomness
                if 'random.random()' in line or 'math.random()' in line:
                    self.add_finding(
                        "medium",
                        "Insecure Randomness",
                        f"Insecure random function in {file_path.name}",
                        str(file_path),
                        i
                    )
        
        except Exception as e:
            self.log(f"Error checking {file_path}: {e}", "error")
    
    def check_dependencies(self, directory: str):
        """Check dependencies for known vulnerabilities"""
        dependency_files = [
            "requirements.txt", "package.json", "Cargo.toml", 
            "go.mod", "pom.xml", "build.gradle", "Gemfile"
        ]
        
        for dep_file in dependency_files:
            file_path = Path(directory) / dep_file
            if file_path.exists():
                self.log(f"Checking dependencies in: {dep_file}")
                self._check_dependency_file(file_path)
    
    def _check_dependency_file(self, file_path: Path):
        """Check a specific dependency file"""
        try:
            content = file_path.read_text()
            
            # Known vulnerable packages (example list - should be updated regularly)
            vulnerable_packages = {
                "python": {
                    "django": "<2.2.0",
                    "flask": "<1.1.0",
                    "requests": "<2.20.0",
                    "urllib3": "<1.26.0",
                },
                "javascript": {
                    "lodash": "<4.17.19",
                    "jquery": "<3.5.0",
                    "express": "<4.17.0",
                }
            }
            
            # Simple check for outdated packages
            # In production, integrate with actual vulnerability databases
            if file_path.name == "requirements.txt":
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        for pkg, min_version in vulnerable_packages.get("python", {}).items():
                            if pkg in line.lower() and f">={min_version}" not in line:
                                self.add_finding(
                                    "high",
                                    "Outdated Dependency",
                                    f"Potentially vulnerable package: {line}",
                                    str(file_path)
                                )
        
        except Exception as e:
            self.log(f"Error checking {file_path}: {e}", "error")
    
    def check_permissions(self, directory: str):
        """Check file permissions for security issues"""
        try:
            for file_path in Path(directory).rglob("*"):
                if file_path.is_file():
                    stat = file_path.stat()
                    
                    # Check for world-writable files
                    if stat.st_mode & 0o002:
                        self.add_finding(
                            "high",
                            "Insecure Permissions",
                            f"World-writable file: {file_path.relative_to(directory)}",
                            str(file_path)
                        )
                    
                    # Check for suid/sgid files
                    if stat.st_mode & 0o4000 or stat.st_mode & 0o2000:
                        self.add_finding(
                            "high",
                            "SUID/SGID File",
                            f"SUID/SGID file found: {file_path.relative_to(directory)}",
                            str(file_path)
                        )
        
        except Exception as e:
            self.log(f"Error checking permissions: {e}", "error")
    
    def check_ai_specific(self, directory: str):
        """Check for AI-specific security issues"""
        ai_patterns = [
            "*.py", "*.ipynb", "*.md", "*.txt", "*.json", "*.yaml", "*.yml"
        ]
        
        for pattern in ai_patterns:
            for file_path in Path(directory).rglob(pattern):
                if file_path.is_file():
                    try:
                        content = file_path.read_text()
                        
                        # Check for hardcoded AI API keys
                        ai_key_patterns = [
                            r'openai[_-]?api[_-]?key\s*[:=]\s*["\'][^"\']{20,}["\']',
                            r'anthropic[_-]?api[_-]?key\s*[:=]\s*["\'][^"\']{20,}["\']',
                            r'cohere[_-]?api[_-]?key\s*[:=]\s*["\'][^"\']{20,}["\']',
                            r'huggingface[_-]?token\s*[:=]\s*["\'][^"\']{20,}["\']',
                            r'api[_-]?key\s*[:=]\s*["\']sk-[^"\']+["\']',  # OpenAI format
                        ]
                        
                        for i, line in enumerate(content.split('\n'), 1):
                            for pattern in ai_key_patterns:
                                if re.search(pattern, line, re.IGNORECASE):
                                    self.add_finding(
                                        "critical",
                                        "Hardcoded AI API Key",
                                        f"AI API key found in {file_path.name}",
                                        str(file_path),
                                        i
                                    )
                        
                        # Check for prompt injection vulnerabilities
                        if any(ext in file_path.suffix for ext in ['.py', '.ipynb']):
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if 'user_input' in line or 'prompt =' in line:
                                    # Look for concatenation without sanitization
                                    if '+' in line or 'f"' in line or 'f\'' in line:
                                        if 'sanitize' not in line and 'escape' not in line:
                                            self.add_finding(
                                                "high",
                                                "Prompt Injection Risk",
                                                f"Unsanitized user input in {file_path.name}",
                                                str(file_path),
                                                i
                                            )
        
                    except Exception as e:
                        self.log(f"Error checking AI file {file_path}: {e}", "error")
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate a security report"""
        report = {
            "summary": {
                "critical": len(self.findings["critical"]),
                "high": len(self.findings["high"]),
                "medium": len(self.findings["medium"]),
                "low": len(self.findings["low"]),
                "info": len(self.findings["info"]),
                "passed": len(self.findings["passed"]),
                "total": sum(len(v) for v in self.findings.values())
            },
            "findings": self.findings,
            "recommendations": self._generate_recommendations()
        }
        
        report_json = json.dumps(report, indent=2)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_json)
            self.log(f"Report saved to: {output_file}")
        
        return report_json
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        # Critical findings recommendations
        if self.findings["critical"]:
            recommendations.append({
                "priority": "critical",
                "action": "Immediate",
                "recommendation": "Fix all critical vulnerabilities immediately",
                "details": "Critical vulnerabilities pose immediate security risks"
            })
        
        # Hardcoded secrets recommendations
        hardcoded_secrets = [f for f in self.findings["critical"] + self.findings["high"] 
                           if "Hardcoded" in f["category"]]
        if hardcoded_secrets:
            recommendations.append({
                "priority": "high",
                "action": "Immediate",
                "recommendation": "Move all secrets to environment variables or secret management",
                "details": f"Found {len(hardcoded_secrets)} hardcoded secrets"
            })
        
        # SQL injection recommendations
        sql_injections = [f for f in self.findings["critical"] 
                         if "SQL Injection" in f["category"]]
        if sql_injections:
            recommendations.append({
                "priority": "critical",
                "action": "Immediate",
                "recommendation": "Use parameterized queries or ORM",
                "details": f"Found {len(sql_injections)} potential SQL injection vulnerabilities"
            })
        
        # Command injection recommendations
        cmd_injections = [f for f in self.findings["critical"] 
                         if "Command Injection" in f["category"]]
        if cmd_injections:
            recommendations.append({
                "priority": "critical",
                "action": "Immediate",
                "recommendation": "Use subprocess with shell=False and validate inputs",
                "details": f"Found {len(cmd_injections)} potential command injection vulnerabilities"
            })
        
        # Dependency recommendations
        outdated_deps = [f for f in self.findings["high"] 
                        if "Outdated Dependency" in f["category"]]
        if outdated_deps:
            recommendations.append({
                "priority": "high",
                "action": "Soon",
                "recommendation": "Update dependencies to latest secure versions",
                "details": f"Found {len(outdated_deps)} potentially vulnerable dependencies"
            })
        
        # Permission recommendations
        insecure_perms = [f for f in self.findings["high"] 
                         if "Insecure Permissions" in f["category"]]
        if insecure_perms:
            recommendations.append({
                "priority": "high",
                "action": "Soon",
                "recommendation": "Fix file permissions (remove world-writable)",
                "details": f"Found {len(insecure_perms)} files with insecure permissions"
            })
        
        # General security recommendations
        recommendations.extend([
            {
                "priority": "medium",
                "action": "Recommended",
                "recommendation": "Implement input validation and sanitization",
                "details": "All user inputs should be validated and sanitized"
            },
            {
                "priority": "medium",
                "action": "Recommended",
                "recommendation": "Add security headers to web applications",
                "details": "Implement CSP, HSTS, X-Frame-Options, etc."
            },
            {
                "priority": "medium",
                "action": "Recommended",
                "recommendation": "Implement rate limiting",
                "details": "Prevent brute force and DoS attacks"
            },
            {
                "priority": "low",
                "action": "Optional",
                "recommendation": "Add security testing to CI/CD pipeline",
                "details": "Automate security checks"
            }
        ])
        
        return recommendations

def main():
    parser = argparse.ArgumentParser(description="Security Scanner for AI Applications")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("-o", "--output", help="Output JSON report file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    args = parser.parse_args()
    
    # Validate directory
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
    
    # Run security scan
    scanner = SecurityScanner(verbose=args.verbose)
    findings = scanner.scan_directory(str(directory))
    
    # Generate report
    report = scanner.generate_report(args.output)
    
    # Print summary
    print("\n" + "="*60)
    print("SECURITY SCAN SUMMARY")
    print("="*60)
    
    for level in ["critical", "high", "medium", "low", "info", "passed"]:
        count = len(findings[level])
        if count > 0:
            print(f"{level.upper():<10}: {count}")
    
    total = sum(len(v) for v in findings.values())
    print(f"{'TOTAL':<10}: {total}")
    
    # Print recommendations
    recommendations = scanner._generate_recommendations()
    if recommendations:
        print("\n" + "="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        
        for rec in recommendations:
            print(f"\n[{rec['priority'].upper()}] {rec['action']}: {rec['recommendation']}")
            print(f"    Details: {rec['details']}")
    
    # Exit code based on findings
    if findings["critical"]:
        print("\n❌ Critical vulnerabilities found!")
        sys.exit(1)
    elif findings["high"]:
        print("\n⚠️  High severity vulnerabilities found!")
        sys.exit(2)
    else:
        print("\n✅ No critical or high severity vulnerabilities found!")
        sys.exit(0)

if __name__ == "__main__":
    main()
