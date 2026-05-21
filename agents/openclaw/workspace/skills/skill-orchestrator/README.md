# Skill Orchestrator

Intelligent skill and model selection system that analyzes task requirements and recommends optimal skill-model combinations for maximum effectiveness and efficiency.

## Overview

The Skill Orchestrator is a meta-skill that:
1. **Analyzes** task descriptions to understand requirements
2. **Selects** the most appropriate skill for the task
3. **Recommends** the optimal model for that skill+task combination
4. **Explains** the reasoning behind each recommendation

## Quick Start

### Basic Usage

```bash
# Analyze a task and get recommendations
python scripts/skill_orchestrator.py "Build a secure web application with user authentication"

# Interactive mode
python scripts/skill_orchestrator.py -i

# JSON output
python scripts/skill_orchestrator.py "Check my code for security vulnerabilities" -j
```

### Integration with OpenClaw

When you ask OpenClaw to perform a task, the Skill Orchestrator will:

1. Automatically analyze your request
2. Determine the best skill to use
3. Select the optimal model for that task
4. Provide reasoning for the selection

## How It Works

### 1. Task Analysis
The orchestrator analyzes your request to determine:
- **Domain**: What type of task is it? (coding, security, automation, etc.)
- **Complexity**: How complex is the task? (simple, moderate, complex, creative)
- **Technical**: Does it require technical expertise?
- **Urgency**: How quickly is it needed?
- **Precision**: How accurate does it need to be?
- **Creativity**: How creative does the response need to be?

### 2. Skill Selection
Based on the analysis, it selects from available skills:
- `glm-app-builder` - Application development with GLM
- `security-checker` - Security assessment and auditing
- `browser-automation` - Web automation tasks
- `healthcheck` - System health and diagnostics
- `skill-creator` - Skill creation and management
- `weather` - Weather information
- `tmux` - Terminal session management
- `taskflow` - Workflow coordination
- `taskflow-inbox-triage` - Inbox processing

### 3. Model Recommendation
Selects the optimal model based on task requirements:
- `deepseek-v4-flash` - Fast, efficient for simple tasks
- `deepseek-v3.2` - Balanced for general tasks
- `deepseek-v4-pro` - High quality for complex/creative tasks
- `deepseek-v3.1-terminus` - Technical/coding expertise
- `deepseek-r1-250528` - Advanced reasoning capabilities
- `glm-5` - GLM tasks and Chinese language
- `glm-5.1` - Enhanced GLM capabilities

## Usage Examples

### Example 1: Application Development
```bash
$ python scripts/skill_orchestrator.py "Build a Flask API with JWT authentication"

============================================================
SKILL ORCHESTRATOR RECOMMENDATION
============================================================
Task: Build a Flask API with JWT authentication

📊 ANALYSIS
----------------------------------------
🎯 Primary Recommendation
   Skill:    glm-app-builder
   Model:    deepseek-v3.1-terminus
   Confidence: 85.0%
   Reasoning: Task domain 'coding' maps to skill 'glm-app-builder'. Selected 'deepseek-v3.1-terminus' for moderate technical task (technical).

🔄 Alternative Options
----------------------------------------
1. Skill: glm-app-builder, Model: deepseek-v3.2
   Reason: Alternative model for moderate tasks (Confidence: 60.0%)

💡 Usage Suggestions
----------------------------------------
1. Use the 'glm-app-builder' skill for this task
2. Set model to 'deepseek-v3.1-terminus'
3. Reference the skill's documentation for specific guidance

============================================================
```

### Example 2: Security Assessment
```bash
$ python scripts/skill_orchestrator.py "Perform a comprehensive security audit of my web application"

============================================================
SKILL ORCHESTRATOR RECOMMENDATION
============================================================
Task: Perform a comprehensive security audit of my web application

📊 ANALYSIS
----------------------------------------
🎯 Primary Recommendation
   Skill:    security-checker
   Model:    deepseek-r1-250528
   Confidence: 87.5%
   Reasoning: Task domain 'security' maps to skill 'security-checker'. Selected 'deepseek-r1-250528' for complex reasoning task.

🔄 Alternative Options
----------------------------------------
1. Skill: security-checker, Model: deepseek-v4-pro
   Reason: Alternative model for complex tasks (Confidence: 60.0%)

💡 Usage Suggestions
----------------------------------------
1. Use the 'security-checker' skill for this task
2. Set model to 'deepseek-r1-250528'
3. Reference the skill's documentation for specific guidance

============================================================
```

### Example 3: Simple Query
```bash
$ python scripts/skill_orchestrator.py "What's the weather in Tokyo tomorrow?"

============================================================
SKILL ORCHESTRATOR RECOMMENDATION
============================================================
Task: What's the weather in Tokyo tomorrow?

📊 ANALYSIS
----------------------------------------
🎯 Primary Recommendation
   Skill:    weather
   Model:    deepseek-v4-flash
   Confidence: 80.0%
   Reasoning: Task domain 'weather' maps to skill 'weather'. Selected 'deepseek-v4-flash' for simple general task.

🔄 Alternative Options
----------------------------------------
1. Skill: weather, Model: deepseek-v3.2
   Reason: Alternative model for simple tasks (Confidence: 60.0%)

💡 Usage Suggestions
----------------------------------------
1. Use the 'weather' skill for this task
2. Set model to 'deepseek-v4-flash'
3. Reference the skill's documentation for specific guidance

============================================================
```

## Integration Methods

### 1. Automatic Integration
The orchestrator can be integrated into OpenClaw to automatically analyze every request and suggest skill/model combinations.

### 2. Manual Invocation
Explicitly ask for recommendations:
```
"Which skill and model should I use for building a GLM-powered chatbot?"
```

### 3. API Integration
Use the Python module directly in your code:
```python
from skill_orchestrator import SkillOrchestrator

orchestrator = SkillOrchestrator()
recommendation = orchestrator.recommend("Build a secure REST API")
print(f"Use {recommendation.skill} with {recommendation.model}")
```

## Configuration

### Customizing Selection Rules
Edit `scripts/skill_orchestrator.py` to modify:
- Domain detection keywords
- Complexity assessment logic
- Skill mapping preferences
- Model selection matrix

### Adding New Skills
1. Add skill to `skill_mapping` dictionary
2. Define domain keywords
3. Update model recommendations if needed

### Adding New Models
1. Add model to `available_models` list
2. Update `model_matrix` with appropriate placements
3. Adjust performance characteristics in references

## Advanced Features

### Skill Chaining
For complex tasks requiring multiple skills:
```python
# Build then secure an application
tasks = [
    "Design a web application architecture",
    "Implement the backend API",
    "Add authentication and authorization",
    "Perform security audit",
    "Optimize performance"
]

for task in tasks:
    recommendation = orchestrator.recommend(task)
    print(f"Task: {task}")
    print(f"  Skill: {recommendation.skill}")
    print(f"  Model: {recommendation.model}")
```

### Context-Aware Decisions
The orchestrator considers:
- Previous interactions (if tracked)
- User preferences
- Time constraints
- Resource availability

### Learning & Adaptation
- Tracks success rates of recommendations
- Adjusts based on user feedback
- Learns from historical performance data

## Command Line Interface

### Basic Commands
```bash
# Get recommendation for a task
python scripts/skill_orchestrator.py "your task description"

# Interactive mode
python scripts/skill_orchestrator.py -i

# JSON output (for integration)
python scripts/skill_orchestrator.py "task" -j

# Verbose output with detailed analysis
python scripts/skill_orchestrator.py "task" -v

# Help
python scripts/skill_orchestrator.py --help
```

### Output Formats

**Human-readable:**
```
============================================================
SKILL ORCHESTRATOR RECOMMENDATION
============================================================
Task: Build a web application
...
```

**JSON:**
```json
{
  "task": "Build a web application",
  "recommendation": {
    "skill": "glm-app-builder",
    "model": "deepseek-v3.1-terminus",
    "confidence": 0.85,
    "reasoning": "..."
  },
  "alternatives": [...]
}
```

## Best Practices

### 1. Be Specific in Requests
- ❌ "Help me with coding"
- ✅ "Build a Python Flask API with SQLAlchemy and JWT authentication"

### 2. Consider Constraints
- Mention if it's urgent
- Specify if quality is critical
- Note any technical requirements

### 3. Review Recommendations
- Check the reasoning
- Consider alternatives
- Adjust based on experience

### 4. Provide Feedback
- Report if recommendations were good
- Suggest improvements
- Help train the system

## Troubleshooting

### Common Issues

**Issue**: Wrong skill selected
**Solution**: Manually specify skill: "Use the security-checker skill for this"

**Issue**: Model not optimal
**Solution**: Specify model: "Use deepseek-r1-250528 for better reasoning"

**Issue**: No skill matches
**Solution**: Use general capabilities or ask for clarification

**Issue**: Performance issues
**Solution**: Switch to lighter model or simpler skill

### Debugging
```bash
# Verbose mode shows detailed analysis
python scripts/skill_orchestrator.py "task" -v

# Check domain detection
python scripts/skill_orchestrator.py "task" -v 2>&1 | grep "Domain:"

# Test with different phrasings
python scripts/skill_orchestrator.py "alternative phrasing of task"
```

## Extending the Orchestrator

### Adding Custom Skills
1. Create your skill in `/skills/your-skill-name/`
2. Add domain mapping in `skill_orchestrator.py`:
```python
self.skill_mapping[TaskDomain.YOUR_DOMAIN] = "your-skill-name"
self.domain_keywords[TaskDomain.YOUR_DOMAIN] = ["keyword1", "keyword2"]
```

### Custom Model Selection
Override model selection for specific skills:
```python
def select_model(self, analysis: TaskAnalysis, skill: str) -> Tuple[str, float, str]:
    # Custom logic for specific skills
    if skill == "your-special-skill":
        return "your-preferred-model", 0.9, "Custom selection for special skill"
    
    # Default logic
    return super().select_model(analysis, skill)
```

### Integration with Other Systems
```python
# Web API endpoint
from flask import Flask, request, jsonify
from skill_orchestrator import SkillOrchestrator

app = Flask(__name__)
orchestrator = SkillOrchestrator()

@app.route('/recommend', methods=['POST'])
def recommend():
    task = request.json.get('task')
    recommendation = orchestrator.recommend(task)
    return jsonify(recommendation.__dict__)
```

## Reference

### Skill Mapping Reference
| Domain | Skill | Typical Tasks |
|--------|-------|---------------|
| coding | glm-app-builder | App development, APIs, coding |
| security | security-checker | Audits, vulnerability scans |
| automation | browser-automation | Web scraping, automation |
| system | healthcheck | System diagnostics, monitoring |
| skill | skill-creator | Skill creation, management |
| weather | weather | Weather queries, forecasts |
| terminal | tmux | Terminal sessions, remote control |
| workflow | taskflow | Workflow coordination |
| inbox | taskflow-inbox-trio | Inbox processing, triage |

### Model Selection Reference
| Task Type | Best Model | Alternatives |
|-----------|------------|--------------|
| Simple/Fast | deepseek-v4-flash | deepseek-v3.2 |
| General | deepseek-v3.2 | DeepSeek-V3 |
| Technical/Coding | deepseek-v3.1-terminus | deepseek-v4-pro |
| Complex/Reasoning | deepseek-r1-250528 | deepseek-v4-pro |
| Creative/Quality | deepseek-v4-pro | glm-5.1 |
| GLM/Chinese | glm-5.1 | glm-5 |

## Contributing

### Reporting Issues
1. Describe the task that caused incorrect recommendation
2. Include the actual and expected recommendation
3. Suggest improvements to the detection logic

### Improving Detection
1. Add new keywords to domain detection
2. Adjust complexity assessment
3. Update model selection matrix
4. Test with diverse task examples

### Adding Tests
```python
def test_orchestrator():
    orchestrator = SkillOrchestrator()
    
    test_cases = [
        ("Build a web app", "glm-app-builder", "deepseek-v3.1-terminus"),
        ("Check security", "security-checker", "deepseek-r1-250528"),
        ("Weather forecast", "weather", "deepseek-v4-flash"),
    ]
    
    for task, expected_skill, expected_model in test_cases:
        recommendation = orchestrator.recommend(task)
        assert recommendation.skill == expected_skill
        assert recommendation.model == expected_model
```

## License

This skill orchestrator is provided under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the reference documentation
3. Test with the interactive mode
4. Report issues with specific examples

## Performance Notes

- **Analysis Speed**: ~10-50ms per task
- **Memory Usage**: Minimal (Python object overhead)
- **Accuracy**: Improves with more specific task descriptions
- **Extensibility**: Easy to add new skills and models

The Skill Orchestrator helps ensure you're always using the right tool for the job, optimizing both effectiveness and efficiency!
