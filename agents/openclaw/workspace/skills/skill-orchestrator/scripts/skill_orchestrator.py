#!/usr/bin/env python3
"""
Skill Orchestrator - Intelligent skill and model selection system.

Analyzes task requirements and recommends optimal skill-model combinations.
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

class TaskDomain(Enum):
    """Task domain categories."""
    CODING = "coding"
    SECURITY = "security"
    AUTOMATION = "automation"
    SYSTEM = "system"
    SKILL = "skill"
    WEATHER = "weather"
    TERMINAL = "terminal"
    WORKFLOW = "workflow"
    INBOX = "inbox"
    GENERAL = "general"

class ComplexityLevel(Enum):
    """Task complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    CREATIVE = "creative"

class ModelType(Enum):
    """Model type categories."""
    GENERAL = "general"
    TECHNICAL = "technical"
    REASONING = "reasoning"
    CREATIVE = "creative"
    FAST = "fast"

@dataclass
class TaskAnalysis:
    """Analysis of a task."""
    domain: TaskDomain
    complexity: ComplexityLevel
    technical: bool
    urgency: str = "normal"
    precision: str = "standard"
    creativity: str = "medium"
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

@dataclass
class SkillRecommendation:
    """Skill recommendation result."""
    skill: str
    model: str
    confidence: float
    reasoning: str
    alternatives: List[Dict[str, Any]]

class SkillOrchestrator:
    """Main orchestrator class for skill and model selection."""
    
    def __init__(self):
        # Available skills mapping
        self.skill_mapping = {
            TaskDomain.CODING: "glm-app-builder",
            TaskDomain.SECURITY: "security-checker",
            TaskDomain.AUTOMATION: "browser-automation",
            TaskDomain.SYSTEM: "healthcheck",
            TaskDomain.SKILL: "skill-creator",
            TaskDomain.WEATHER: "weather",
            TaskDomain.TERMINAL: "tmux",
            TaskDomain.WORKFLOW: "taskflow",
            TaskDomain.INBOX: "taskflow-inbox-triage",
            TaskDomain.GENERAL: None  # No specific skill
        }
        
        # Available models
        self.available_models = [
            "deepseek-v4-flash",
            "deepseek-v3.2",
            "deepseek-v4-pro",
            "deepseek-v3.1-terminus",
            "DeepSeek-V3",
            "deepseek-r1-250528",
            "glm-5",
            "glm-5.1"
        ]
        
        # Model selection matrix
        self.model_matrix = {
            ComplexityLevel.SIMPLE: {
                ModelType.GENERAL: "deepseek-v4-flash",
                ModelType.TECHNICAL: "deepseek-v3.2",
                ModelType.CREATIVE: "glm-5",
            },
            ComplexityLevel.MODERATE: {
                ModelType.GENERAL: "deepseek-v3.2",
                ModelType.TECHNICAL: "deepseek-v3.1-terminus",
                ModelType.CREATIVE: "deepseek-v4-pro",
                ModelType.REASONING: "deepseek-r1-250528",
            },
            ComplexityLevel.COMPLEX: {
                ModelType.GENERAL: "deepseek-r1-250528",
                ModelType.TECHNICAL: "deepseek-v3.1-terminus",
                ModelType.CREATIVE: "deepseek-v4-pro",
                ModelType.REASONING: "deepseek-r1-250528",
            },
            ComplexityLevel.CREATIVE: {
                ModelType.GENERAL: "deepseek-v4-pro",
                ModelType.TECHNICAL: "glm-5.1",
                ModelType.CREATIVE: "glm-5.1",
            }
        }
        
        # Domain detection keywords
        self.domain_keywords = {
            TaskDomain.CODING: [
                "build", "create", "develop", "program", "code", "app", "api",
                "application", "software", "website", "web app", "backend",
                "frontend", "database", "server", "deploy", "docker", "kubernetes"
            ],
            TaskDomain.SECURITY: [
                "security", "check", "audit", "vulnerability", "scan", "assess",
                "penetration", "harden", "firewall", "encrypt", "authentication",
                "authorization", "secure", "protect", "threat", "risk", "compliance"
            ],
            TaskDomain.AUTOMATION: [
                "automate", "script", "browser", "web", "scrape", "crawl",
                "automation", "bot", "robot", "schedule", "cron", "task",
                "workflow", "pipeline", "automated", "selenium", "puppeteer"
            ],
            TaskDomain.SYSTEM: [
                "health", "check", "status", "diagnose", "troubleshoot",
                "system", "server", "monitor", "performance", "resource",
                "cpu", "memory", "disk", "network", "uptime", "service"
            ],
            TaskDomain.SKILL: [
                "skill", "create", "edit", "update", "manage", "orchestrator",
                "skill.md", "skill file", "new skill", "modify skill"
            ],
            TaskDomain.WEATHER: [
                "weather", "forecast", "temperature", "rain", "snow", "sunny",
                "cloudy", "humidity", "wind", "storm", "climate", "meteorology"
            ],
            TaskDomain.TERMINAL: [
                "tmux", "terminal", "session", "remote", "ssh", "shell",
                "command line", "cli", "console", "terminal multiplexer"
            ],
            TaskDomain.WORKFLOW: [
                "taskflow", "coordinate", "orchestrate", "manage", "workflow",
                "pipeline", "process", "automation", "schedule", "coordination",
                "workflow", "orchestration", "coordination", "multi-step", "sequence"
            ],
            TaskDomain.INBOX: [
                "inbox", "triage", "process", "categorize", "email",
                "message", "notification", "sort", "organize", "priority"
            ]
        }
        
        # Complexity detection keywords
        self.complexity_keywords = {
            ComplexityLevel.SIMPLE: [
                "show", "tell", "what is", "simple", "quick", "easy",
                "basic", "straightforward", "fast", "brief", "short"
            ],
            ComplexityLevel.COMPLEX: [
                "complex", "complicated", "difficult", "challenging", "reason",
                "analyze", "evaluate", "strategize", "plan", "design",
                "architecture", "system", "comprehensive", "detailed"
            ],
            ComplexityLevel.CREATIVE: [
                "create", "design", "invent", "original", "novel", "creative",
                "innovate", "brainstorm", "imagine", "conceptualize", "art",
                "write", "story", "narrative", "poem", "song"
            ]
        }
        
        # Technical keywords
        self.technical_keywords = [
            "code", "program", "debug", "api", "database", "server", "config",
            "algorithm", "function", "class", "method", "variable", "loop",
            "conditional", "framework", "library", "package", "dependency",
            "compile", "execute", "runtime", "syntax", "semantic", "bug",
            "error", "exception", "stack", "trace", "log", "monitor",
            "authentication", "authorization", "security", "vulnerability",
            "encryption", "deployment", "container", "docker", "kubernetes",
            "microservice", "architecture", "design", "implementation"
        ]
    
    def analyze_task(self, task_description: str) -> TaskAnalysis:
        """Analyze a task description to determine its characteristics."""
        
        task_lower = task_description.lower()
        keywords = []
        
        # Detect domain
        domain = TaskDomain.GENERAL
        max_matches = 0
        
        for dom, dom_keywords in self.domain_keywords.items():
            matches = sum(1 for keyword in dom_keywords if keyword in task_lower)
            if matches > max_matches:
                max_matches = matches
                domain = dom
                keywords.extend([k for k in dom_keywords if k in task_lower])
        
        # Detect complexity
        complexity = ComplexityLevel.MODERATE  # Default
        max_complexity_matches = 0
        
        for comp_level, comp_keywords in self.complexity_keywords.items():
            matches = sum(1 for keyword in comp_keywords if keyword in task_lower)
            if matches > max_complexity_matches:
                max_complexity_matches = matches
                complexity = comp_level
                
        # Add matched keywords
        for comp_level, comp_keywords in self.complexity_keywords.items():
            matched = [k for k in comp_keywords if k in task_lower]
            keywords.extend(matched)
        
        # Detect technical nature
        technical_matches = [k for k in self.technical_keywords if k in task_lower]
        technical = len(technical_matches) > 0
        if technical:
            keywords.extend(technical_matches)
        
        # Detect urgency (simple heuristic)
        urgency = "normal"
        if any(word in task_lower for word in ["urgent", "asap", "immediately", "now", "quickly"]):
            urgency = "urgent"
        elif any(word in task_lower for word in ["whenever", "sometime", "no rush", "background"]):
            urgency = "background"
        
        # Detect precision needs
        precision = "standard"
        if any(word in task_lower for word in ["exact", "precise", "accurate", "specific", "detailed"]):
            precision = "high"
        elif any(word in task_lower for word in ["approximate", "rough", "estimate", "ballpark"]):
            precision = "approximate"
        
        # Detect creativity needs
        creativity = "medium"
        if any(word in task_lower for word in ["creative", "innovative", "original", "novel", "unique"]):
            creativity = "high"
        elif any(word in task_lower for word in ["standard", "template", "routine", "formulaic"]):
            creativity = "low"
        
        return TaskAnalysis(
            domain=domain,
            complexity=complexity,
            technical=technical,
            urgency=urgency,
            precision=precision,
            creativity=creativity,
            keywords=list(set(keywords))  # Remove duplicates
        )
    
    def select_skill(self, analysis: TaskAnalysis) -> Tuple[str, float, str]:
        """Select the most appropriate skill for the task."""
        
        skill = self.skill_mapping.get(analysis.domain)
        
        if not skill:
            return None, 0.0, "No specific skill required for this task domain"
        
        # Calculate confidence based on keyword matches
        confidence = 0.5  # Base confidence
        
        # Increase confidence for technical tasks with technical skills
        if analysis.technical and analysis.domain in [TaskDomain.CODING, TaskDomain.SECURITY, TaskDomain.SYSTEM]:
            confidence += 0.2
        
        # Increase confidence for exact domain matches
        if analysis.domain != TaskDomain.GENERAL:
            confidence += 0.2
        
        # Cap confidence at 0.95
        confidence = min(confidence, 0.95)
        
        reasoning = f"Task domain '{analysis.domain.value}' maps to skill '{skill}'"
        if analysis.technical:
            reasoning += " (technical task)"
        
        return skill, confidence, reasoning
    
    def select_model(self, analysis: TaskAnalysis, skill: str = None) -> Tuple[str, float, str]:
        """Select the optimal model for the task."""
        
        # Determine model type
        if analysis.technical:
            model_type = ModelType.TECHNICAL
        elif analysis.complexity == ComplexityLevel.CREATIVE:
            model_type = ModelType.CREATIVE
        elif analysis.complexity == ComplexityLevel.COMPLEX:
            model_type = ModelType.REASONING
        elif any(word in analysis.keywords for word in ["analyze", "evaluate", "reason", "logic", "complex"]):
            model_type = ModelType.REASONING
        elif analysis.urgency == "urgent":
            model_type = ModelType.FAST
        else:
            model_type = ModelType.GENERAL
        
        # Get model from matrix
        model = None
        if analysis.complexity in self.model_matrix:
            if model_type in self.model_matrix[analysis.complexity]:
                model = self.model_matrix[analysis.complexity][model_type]
        
        # Fallback logic
        if not model:
            if analysis.technical:
                model = "deepseek-v3.1-terminus"
            elif analysis.complexity == ComplexityLevel.COMPLEX:
                model = "deepseek-r1-250528"
            elif analysis.complexity == ComplexityLevel.CREATIVE:
                model = "deepseek-v4-pro"
            elif analysis.urgency == "urgent":
                model = "deepseek-v4-flash"
            else:
                model = "deepseek-v3.2"
        
        # Calculate confidence
        confidence = 0.6  # Base confidence
        
        # Adjust based on complexity match
        if analysis.complexity in self.model_matrix and model_type in self.model_matrix[analysis.complexity]:
            confidence += 0.2
        
        # Adjust for technical tasks
        if analysis.technical and model in ["deepseek-v3.1-terminus", "deepseek-r1-250528"]:
            confidence += 0.1
        
        # Adjust for creative tasks
        if analysis.creativity == "high" and model in ["deepseek-v4-pro", "glm-5.1"]:
            confidence += 0.1
        
        # Cap confidence
        confidence = min(confidence, 0.95)
        
        reasoning = f"Selected '{model}' for {analysis.complexity.value} {model_type.value} task"
        if analysis.technical:
            reasoning += " (technical)"
        if analysis.urgency == "urgent":
            reasoning += " (urgent)"
        
        return model, confidence, reasoning
    
    def get_alternatives(self, analysis: TaskAnalysis, primary_skill: str, primary_model: str) -> List[Dict[str, Any]]:
        """Get alternative skill-model combinations."""
        
        alternatives = []
        
        # Alternative skills for the domain
        if analysis.domain != TaskDomain.GENERAL:
            # Suggest general skill if technical
            if analysis.technical and primary_skill != "glm-app-builder":
                alternatives.append({
                    "skill": "glm-app-builder",
                    "model": primary_model,
                    "reason": "Alternative for technical tasks",
                    "confidence": 0.7
                })
        
        # Alternative models
        if analysis.complexity == ComplexityLevel.COMPLEX:
            alt_models = ["deepseek-v4-pro", "glm-5.1"]
        elif analysis.complexity == ComplexityLevel.MODERATE:
            alt_models = ["deepseek-v3.2", "glm-5"]
        else:  # SIMPLE or CREATIVE
            alt_models = ["deepseek-v4-flash", "deepseek-v3.2"]
        
        for alt_model in alt_models:
            if alt_model != primary_model and alt_model in self.available_models:
                alternatives.append({
                    "skill": primary_skill,
                    "model": alt_model,
                    "reason": f"Alternative model for {analysis.complexity.value} tasks",
                    "confidence": 0.6
                })
        
        return alternatives
    
    def recommend(self, task_description: str) -> SkillRecommendation:
        """Generate complete skill and model recommendation."""
        
        # Analyze task
        analysis = self.analyze_task(task_description)
        
        # Select skill
        skill, skill_confidence, skill_reasoning = self.select_skill(analysis)
        
        # Select model
        model, model_confidence, model_reasoning = self.select_model(analysis, skill)
        
        # Calculate overall confidence
        overall_confidence = (skill_confidence + model_confidence) / 2
        
        # Generate combined reasoning
        reasoning = f"{skill_reasoning}. {model_reasoning}."
        
        # Get alternatives
        alternatives = self.get_alternatives(analysis, skill, model)
        
        return SkillRecommendation(
            skill=skill,
            model=model,
            confidence=overall_confidence,
            reasoning=reasoning,
            alternatives=alternatives
        )
    
    def format_recommendation(self, recommendation: SkillRecommendation, task: str) -> str:
        """Format recommendation for display."""
        
        output = []
        output.append("=" * 60)
        output.append("SKILL ORCHESTRATOR RECOMMENDATION")
        output.append("=" * 60)
        output.append(f"Task: {task}")
        output.append("")
        output.append("📊 ANALYSIS")
        output.append("-" * 40)
        
        # Show recommendation
        output.append(f"🎯 Primary Recommendation")
        output.append(f"   Skill:    {recommendation.skill or 'None (use general capabilities)'}")
        output.append(f"   Model:    {recommendation.model}")
        output.append(f"   Confidence: {recommendation.confidence:.1%}")
        output.append(f"   Reasoning: {recommendation.reasoning}")
        
        # Show alternatives if any
        if recommendation.alternatives:
            output.append("")
            output.append("🔄 Alternative Options")
            output.append("-" * 40)
            for i, alt in enumerate(recommendation.alternatives, 1):
                output.append(f"{i}. Skill: {alt['skill']}, Model: {alt['model']}")
                output.append(f"   Reason: {alt['reason']} (Confidence: {alt['confidence']:.1%})")
        
        output.append("")
        output.append("💡 Usage Suggestions")
        output.append("-" * 40)
        
        if recommendation.skill:
            output.append(f"1. Use the '{recommendation.skill}' skill for this task")
            output.append(f"2. Set model to '{recommendation.model}'")
            output.append(f"3. Reference the skill's documentation for specific guidance")
        else:
            output.append("1. No specific skill required - use general capabilities")
            output.append(f"2. Set model to '{recommendation.model}'")
            output.append("3. Proceed with the task using standard approaches")
        
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)
    
    def interactive_mode(self):
        """Run in interactive mode for testing."""
        print("🎯 Skill Orchestrator - Interactive Mode")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            task = input("\nEnter task description: ").strip()
            
            if task.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not task:
                continue
            
            print("\n" + "=" * 60)
            print("Analyzing task...")
            
            recommendation = self.recommend(task)
            formatted = self.format_recommendation(recommendation, task)
            print(formatted)

def main():
    """Command-line interface for the skill orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Skill Orchestrator - Intelligent skill and model selection")
    parser.add_argument("task", nargs="?", help="Task description to analyze")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    orchestrator = SkillOrchestrator()
    
    if args.interactive:
        orchestrator.interactive_mode()
    elif args.task:
        recommendation = orchestrator.recommend(args.task)
        
        if args.json:
            # JSON output
            result = {
                "task": args.task,
                "recommendation": {
                    "skill": recommendation.skill,
                    "model": recommendation.model,
                    "confidence": recommendation.confidence,
                    "reasoning": recommendation.reasoning,
                },
                "alternatives": recommendation.alternatives
            }
            print(json.dumps(result, indent=2))
        else:
            # Formatted output
            print(orchestrator.format_recommendation(recommendation, args.task))
            
            if args.verbose:
                # Show detailed analysis
                analysis = orchestrator.analyze_task(args.task)
                print("\n📈 Detailed Analysis:")
                print(f"  Domain: {analysis.domain.value}")
                print(f"  Complexity: {analysis.complexity.value}")
                print(f"  Technical: {analysis.technical}")
                print(f"  Urgency: {analysis.urgency}")
                print(f"  Precision: {analysis.precision}")
                print(f"  Creativity: {analysis.creativity}")
                print(f"  Keywords: {', '.join(analysis.keywords[:10])}")
    else:
        # Show help
        print("Skill Orchestrator - Intelligent skill and model selection")
        print("\nExamples:")
        print("  python skill_orchestrator.py \"Build a web application with GLM\"")
        print("  python skill_orchestrator.py \"Check security of my Flask app\"")
        print("  python skill_orchestrator.py -i  # Interactive mode")
        print("  python skill_orchestrator.py \"Simple weather query\" -j  # JSON output")

if __name__ == "__main__":
    main()
