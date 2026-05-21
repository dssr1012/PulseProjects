---
name: skill-orchestrator
description: Intelligent skill and model selection system. Use when you need to determine which skill and which model is best suited for a given task. Analyzes task requirements, complexity, and context to recommend optimal skill-model combinations from available options.
---

# Skill Orchestrator

Intelligent skill and model selection system that analyzes task requirements and recommends the optimal skill-model combination for maximum effectiveness and efficiency.

## Quick Decision Guide

When you receive a task request:

1. **Analyze the task** - What's being asked? What's the goal?
2. **Determine skill category** - Which domain does this belong to?
3. **Assess complexity** - Simple, moderate, or complex?
4. **Consider constraints** - Time, cost, accuracy requirements?
5. **Select skill** - Which available skill best matches?
6. **Choose model** - Which model is optimal for this skill+task?

## Available Skills & Models

### Skills Inventory
- **glm-app-builder**: Building applications with GLM models
- **security-checker**: Security assessment and vulnerability scanning
- **skill-creator**: Creating, editing, and managing skills
- **browser-automation**: Web automation and browser control
- **healthcheck**: System health and security auditing
- **node-connect**: Node pairing and connection diagnostics
- **weather**: Weather information and forecasts
- **tmux**: Remote tmux session control
- **taskflow**: Multi-step workflow coordination
- **taskflow-inbox-triage**: Inbox processing and routing

### Available Models
- **deepseek-v4-flash**: Fast, efficient, general purpose (128K context)
- **deepseek-v3.2**: Balanced performance (32K context)
- **deepseek-v4-pro**: High capability, complex tasks (64K context)
- **deepseek-v3.1-terminus**: Specialized for coding/technical tasks
- **DeepSeek-V3**: General purpose, good balance
- **deepseek-r1-250528**: Reasoning-focused, complex problem solving
- **glm-5**: General purpose GLM model
- **glm-5.1**: Enhanced GLM model with better reasoning

## Skill Selection Matrix

### By Task Category

| Task Category | Primary Skill | Alternative Skills | Best Model | Reasoning |
|--------------|---------------|-------------------|------------|-----------|
| **Application Development** | glm-app-builder | skill-creator | deepseek-v3.1-terminus | Coding expertise, architectural thinking |
| **Security Assessment** | security-checker | healthcheck | deepseek-r1-250528 | Analytical reasoning, pattern recognition |
| **Skill Creation/Editing** | skill-creator | - | deepseek-v4-pro | Creative, structured thinking |
| **Web Automation** | browser-automation | - | deepseek-v4-flash | Fast, procedural execution |
| **System Health** | healthcheck | security-checker | DeepSeek-V3 | Systematic, thorough analysis |
| **Node/Connection Issues** | node-connect | - | deepseek-v3.2 | Technical troubleshooting |
| **Weather Information** | weather | - | deepseek-v4-flash | Simple, factual responses |
| **Terminal Control** | tmux | - | deepseek-v3.2 | Technical, command-oriented |
| **Workflow Coordination** | taskflow | taskflow-inbox-triage | deepseek-r1-250528 | Complex planning, state management |
| **Inbox Processing** | taskflow-inbox-trio | taskflow | glm-5.1 | Categorization, routing decisions |

### By Complexity Level

| Complexity | Recommended Model | Reasoning |
|------------|------------------|-----------|
| **Simple** (factual, straightforward) | deepseek-v4-flash | Fast, cost-effective for simple tasks |
| **Moderate** (analysis, multi-step) | deepseek-v3.2 or glm-5 | Balanced performance for typical tasks |
| **Complex** (reasoning, planning) | deepseek-r1-250528 | Advanced reasoning for complex problems |
| **Creative** (generation, design) | deepseek-v4-pro or glm-5.1 | High creativity and quality output |
| **Technical** (coding, debugging) | deepseek-v3.1-terminus | Specialized for technical tasks |

## Decision Workflow

### Step 1: Task Analysis
```python
def analyze_task(task_description: str) -> dict:
    """Analyze task requirements and characteristics"""
    
    analysis = {
        "domain": None,           # coding, security, automation, etc.
        "complexity": "moderate", # simple, moderate, complex
        "urgency": "normal",      # urgent, normal, background
        "precision": "standard",  # high, standard, approximate
        "creativity": "medium",   # high, medium, low
        "technical": False,       # technical vs non-technical
    }
    
    # Domain detection
    domain_keywords = {
        "coding": ["build", "create", "develop", "program", "code", "app", "api"],
        "security": ["security", "check", "audit", "vulnerability", "scan", "assess"],
        "automation": ["automate", "script", "browser", "web", "scrape"],
        "system": ["health", "check", "status", "diagnose", "troubleshoot"],
        "skill": ["skill", "create", "edit", "update", "manage"],
        "weather": ["weather", "forecast", "temperature", "rain"],
        "terminal": ["tmux", "terminal", "session", "remote"],
        "workflow": ["taskflow", "coordinate", "orchestrate", "manage"],
        "inbox": ["inbox", "triage", "process", "categorize"],
    }
    
    task_lower = task_description.lower()
    for domain, keywords in domain_keywords.items():
        if any(keyword in task_lower for keyword in keywords):
            analysis["domain"] = domain
            break
    
    # Complexity assessment
    complexity_indicators = {
        "simple": ["show", "tell", "what is", "simple", "quick"],
        "complex": ["complex", "complicated", "difficult", "challenging", "reason"],
        "creative": ["create", "design", "invent", "original", "novel"],
    }
    
    for level, indicators in complexity_indicators.items():
        if any(indicator in task_lower for indicator in indicators):
            analysis["complexity"] = level
            break
    
    # Technical vs non-technical
    technical_terms = ["code", "program", "debug", "api", "database", "server", "config"]
    analysis["technical"] = any(term in task_lower for term in technical_terms)
    
    return analysis
```

### Step 2: Skill Selection
```python
def select_skill(task_analysis: dict) -> str:
    """Select the most appropriate skill for the task"""
    
    domain_to_skill = {
        "coding": "glm-app-builder",
        "security": "security-checker",
        "automation": "browser-automation",
        "system": "healthcheck",
        "skill": "skill-creator",
        "weather": "weather",
        "terminal": "tmux",
        "workflow": "taskflow",
        "inbox": "taskflow-inbox-triage",
    }
    
    # Primary skill based on domain
    primary_skill = domain_to_skill.get(task_analysis["domain"])
    
    # Fallback logic
    if not primary_skill:
        if task_analysis["technical"]:
            return "glm-app-builder"  # Default for technical tasks
        else:
            return None  # No specific skill needed
    
    return primary_skill
```

### Step 3: Model Selection
```python
def select_model(task_analysis: dict, skill: str) -> str:
    """Select the optimal model for the task and skill"""
    
    # Model selection matrix
    model_matrix = {
        "simple": {
            "general": "deepseek-v4-flash",
            "technical": "deepseek-v3.2",
            "creative": "glm-5",
        },
        "moderate": {
            "general": "deepseek-v3.2",
            "technical": "deepseek-v3.1-terminus",
            "creative": "deepseek-v4-pro",
            "reasoning": "deepseek-r1-250528",
        },
        "complex": {
            "general": "deepseek-r1-250528",
            "technical": "deepseek-v3.1-terminus",
            "creative": "deepseek-v4-pro",
            "reasoning": "deepseek-r1-250528",
        },
        "creative": {
            "general": "deepseek-v4-pro",
            "technical": "glm-5.1",
            "writing": "glm-5.1",
        }
    }
    
    # Determine model type
    if task_analysis["technical"]:
        model_type = "technical"
    elif task_analysis["complexity"] == "creative":
        model_type = "creative"
    elif "reason" in task_analysis.get("keywords", []):
        model_type = "reasoning"
    else:
        model_type = "general"
    
    # Get complexity level
    complexity = task_analysis["complexity"]
    
    # Select model
    if complexity in model_matrix and model_type in model_matrix[complexity]:
        return model_matrix[complexity][model_type]
    
    # Default fallbacks
    if task_analysis["technical"]:
        return "deepseek-v3.1-terminus"
    elif complexity == "complex":
        return "deepseek-r1-250528"
    else:
        return "deepseek-v3.2"
```

### Step 4: Combined Recommendation
```python
def recommend_skill_model(task_description: str) -> dict:
    """Complete recommendation pipeline"""
    
    # Analyze task
    analysis = analyze_task(task_description)
    
    # Select skill
    skill = select_skill(analysis)
    
    # Select model
    model = select_model(analysis, skill)
    
    # Generate reasoning
    reasoning = generate_reasoning(analysis, skill, model)
    
    return {
        "task": task_description,
        "analysis": analysis,
        "recommended_skill": skill,
        "recommended_model": model,
        "reasoning": reasoning,
        "alternative_options": get_alternatives(analysis, skill, model)
    }
```

## Usage Examples

### Example 1: Application Development
**Task:** "Build a web application that uses GLM models to summarize PDF documents"

**Orchestrator Analysis:**
```
Domain: coding (keywords: build, web application, GLM models)
Complexity: complex (multi-component application)
Technical: True (coding, API integration)
Skill: glm-app-builder
Model: deepseek-v3.1-terminus (technical, complex coding)
Reasoning: Technical coding task requiring architectural design and GLM integration
```

### Example 2: Security Assessment
**Task:** "Check my Flask application for security vulnerabilities and suggest fixes"

**Orchestrator Analysis:**
```
Domain: security (keywords: security, vulnerabilities, check)
Complexity: moderate (analysis + recommendations)
Technical: True (Flask, application security)
Skill: security-checker
Model: deepseek-r1-250528 (analytical reasoning)
Reasoning: Security analysis requires careful reasoning about vulnerabilities and fixes
```

### Example 3: Simple Query
**Task:** "What's the weather in Shanghai tomorrow?"

**Orchestrator Analysis:**
```
Domain: weather (keywords: weather, Shanghai)
Complexity: simple (factual query)
Technical: False
Skill: weather
Model: deepseek-v4-flash (fast, simple task)
Reasoning: Simple factual query, fastest model is sufficient
```

## Interactive Decision Assistant

Use this interactive flowchart for manual decisions:

```
START → Analyze Task
         ↓
   Is it about building apps? → YES → Use glm-app-builder
         ↓ NO
   Is it about security? → YES → Use security-checker
         ↓ NO
   Is it web automation? → YES → Use browser-automation
         ↓ NO
   Is it system health? → YES → Use healthcheck
         ↓ NO
   Is it skill creation? → YES → Use skill-creator
         ↓ NO
   Is it weather? → YES → Use weather
         ↓ NO
   Is it terminal control? → YES → Use tmux
         ↓ NO
   Is it workflow? → YES → Use taskflow
         ↓ NO
   Is it inbox? → YES → Use taskflow-inbox-triage
         ↓ NO
   Use general capabilities
```

## Model Selection Guidelines

### When to use each model:

**deepseek-v4-flash** (Fast, 128K context):
- Simple factual queries
- Quick responses needed
- High volume tasks
- Cost-sensitive operations

**deepseek-v3.2** (Balanced, 32K context):
- General conversation
- Moderate complexity tasks
- Code review and debugging
- Everyday assistance

**deepseek-v4-pro** (High capability, 64K context):
- Creative writing
- Complex problem solving
- Strategic planning
- Quality-focused outputs

**deepseek-v3.1-terminus** (Technical specialist):
- Code generation
- Technical documentation
- System design
- Algorithm implementation

**deepseek-r1-250528** (Reasoning focused):
- Logical reasoning
- Mathematical problems
- Security analysis
- Complex decision making

**glm-5** (General GLM):
- GLM-specific tasks
- Chinese language tasks
- General assistance

**glm-5.1** (Enhanced GLM):
- Complex GLM tasks
- Advanced reasoning in Chinese
- Quality-focused GLM work

## Integration with OpenClaw

### Automatic Skill Detection
The orchestrator can be integrated to automatically:
1. Parse incoming requests
2. Match to available skills
3. Select optimal model
4. Route to appropriate skill

### Manual Override
Users can manually specify:
- Skill preference: "Use the security-checker skill"
- Model preference: "Use glm-5.1 for this"
- Combination: "Check security using deepseek-r1-250528"

### Configuration Options
```yaml
# Example orchestrator configuration
skill_orchestrator:
  auto_detect: true
  default_model: "deepseek-v3.2"
  skill_priorities:
    coding: "glm-app-builder"
    security: "security-checker"
    automation: "browser-automation"
  model_rules:
    simple_tasks: "deepseek-v4-flash"
    complex_reasoning: "deepseek-r1-250528"
    technical_coding: "deepseek-v3.1-terminus"
```

## Best Practices

### 1. Start with Analysis
Always analyze the task before selecting skill/model:
- What is the core requirement?
- What domain does it belong to?
- How complex is it?
- Are there specific constraints?

### 2. Consider Trade-offs
- **Speed vs Quality**: deepseek-v4-flash vs deepseek-v4-pro
- **Cost vs Capability**: Balance token cost with task requirements
- **Specialization**: Use specialized models for technical tasks

### 3. Monitor Performance
- Track which skill-model combinations work best
- Adjust recommendations based on results
- Learn from user feedback

### 4. Provide Transparency
- Explain why a skill/model was chosen
- Offer alternatives when appropriate
- Allow user override when needed

## Troubleshooting

### Common Issues & Solutions

**Issue**: Wrong skill selected
**Solution**: Manually specify skill: "Actually, use the security-checker skill for this"

**Issue**: Model not optimal
**Solution**: Specify model: "Please use deepseek-r1-250528 for better reasoning"

**Issue**: No skill matches
**Solution**: Use general capabilities or ask for clarification

**Issue**: Performance issues
**Solution**: Switch to lighter model (deepseek-v4-flash) or simpler skill

## Advanced Features

### Skill Chaining
For complex tasks that require multiple skills:
```python
# Example: Build and secure an application
task_chain = [
    {"skill": "glm-app-builder", "model": "deepseek-v3.1-terminus", "task": "Build web app"},
    {"skill": "security-checker", "model": "deepseek-r1-250528", "task": "Security audit"},
    {"skill": "glm-app-builder", "model": "deepseek-v3.2", "task": "Implement fixes"}
]
```

### Context Awareness
Consider:
- Previous interactions
- User preferences
- Time of day (urgency)
- Available resources

### Learning & Adaptation
- Track success rates of skill-model combinations
- Adjust recommendations based on outcomes
- Incorporate user feedback into decisions

## References

- [Skill Selection Guide](references/skill_selection.md) - Detailed skill matching criteria
- [Model Comparison](references/model_comparison.md) - Technical model specifications
- [Performance Metrics](references/performance.md) - Speed/cost/quality trade-offs
- [Integration Examples](references/integration.md) - How to integrate with workflows

## Quick Reference Card

### Skill Selection
```
coding → glm-app-builder
security → security-checker
automation → browser-automation
system → healthcheck
skill work → skill-creator
weather → weather
terminal → tmux
workflow → taskflow
inbox → taskflow-inbox-triage
```

### Model Selection
```
simple/fast → deepseek-v4-flash
general → deepseek-v3.2
complex → deepseek-r1-250528
creative → deepseek-v4-pro
technical → deepseek-v3.1-terminus
GLM tasks → glm-5 / glm-5.1
```

### Decision Tree
```
Is it technical? → YES → deepseek-v3.1-terminus
              ↓ NO
Is it complex? → YES → deepseek-r1-250528
              ↓ NO
Is it creative? → YES → deepseek-v4-pro
               ↓ NO
Use deepseek-v3.2
```

Remember: The orchestrator is a guide, not a rule. Always consider context and user preferences!
