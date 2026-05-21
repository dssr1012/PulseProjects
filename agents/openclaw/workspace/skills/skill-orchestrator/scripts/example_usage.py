#!/usr/bin/env python3
"""
Example usage of the Skill Orchestrator.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_orchestrator import SkillOrchestrator

def example_basic():
    """Basic usage example."""
    
    print("🔧 Basic Usage Example")
    print("=" * 60)
    
    orchestrator = SkillOrchestrator()
    
    # Example tasks
    tasks = [
        "Build a web application with user authentication",
        "Check my website for security vulnerabilities",
        "What's the weather forecast for tomorrow?",
        "Create a new skill for OpenClaw",
        "Automate browser testing for my application",
    ]
    
    for task in tasks:
        print(f"\nTask: {task}")
        print("-" * 40)
        
        recommendation = orchestrator.recommend(task)
        
        print(f"Recommended Skill: {recommendation.skill or 'General capabilities'}")
        print(f"Recommended Model: {recommendation.model}")
        print(f"Confidence: {recommendation.confidence:.1%}")
        print(f"Reasoning: {recommendation.reasoning}")
        
        if recommendation.alternatives:
            print(f"Alternatives: {len(recommendation.alternatives)} options available")

def example_cli():
    """Command-line interface example."""
    
    print("\n💻 Command Line Usage")
    print("=" * 60)
    
    print("""
Run the orchestrator from command line:

# Basic usage
python skill_orchestrator.py "Build a REST API with authentication"

# Interactive mode
python skill_orchestrator.py -i

# JSON output (for integration)
python skill_orchestrator.py "Check security" -j

# Verbose output with analysis
python skill_orchestrator.py "Create a new skill" -v
""")

def example_integration():
    """Integration example in your own code."""
    
    print("\n🔗 Integration Example")
    print("=" * 60)
    
    code = '''
from skill_orchestrator import SkillOrchestrator

# Initialize orchestrator
orchestrator = SkillOrchestrator()

# Analyze a task
task = "Build a microservices architecture with Docker and Kubernetes"
recommendation = orchestrator.recommend(task)

print(f"Task: {task}")
print(f"Skill: {recommendation.skill}")
print(f"Model: {recommendation.model}")
print(f"Confidence: {recommendation.confidence:.1%}")

# Use the recommendation
if recommendation.skill:
    print(f"Using skill: {recommendation.skill}")
    print(f"Setting model to: {recommendation.model}")
else:
    print("Using general capabilities")
    
# Show alternatives
if recommendation.alternatives:
    print("\\nAlternative options:")
    for alt in recommendation.alternatives[:3]:
        print(f"  - {alt['skill']} with {alt['model']} ({alt['confidence']:.1%})")
'''
    
    print(code)

def example_complex_task():
    """Example with a complex task."""
    
    print("\n🎯 Complex Task Analysis")
    print("=" * 60)
    
    orchestrator = SkillOrchestrator()
    
    complex_task = """
    Build a secure e-commerce platform with:
    1. User authentication (OAuth2, JWT)
    2. Product catalog with search and filtering
    3. Shopping cart and checkout
    4. Payment integration (Stripe, PayPal)
    5. Order management system
    6. Admin dashboard
    7. Security audit and penetration testing
    8. Deployment to AWS with CI/CD
    """
    
    print(f"Task: {complex_task.strip()[:100]}...")
    print("-" * 40)
    
    recommendation = orchestrator.recommend(complex_task)
    
    print(f"Skill: {recommendation.skill}")
    print(f"Model: {recommendation.model}")
    print(f"Confidence: {recommendation.confidence:.1%}")
    print(f"Reasoning: {recommendation.reasoning}")
    
    print("\nThis complex task involves multiple aspects:")
    print("1. Application development (glm-app-builder)")
    print("2. Security assessment (security-checker)")
    print("3. Deployment automation (general)")
    print("\nThe orchestrator selected the primary skill for the main task.")

def main():
    """Run all examples."""
    
    print("🚀 SKILL ORCHESTRATOR - USAGE EXAMPLES")
    print("=" * 60)
    
    example_basic()
    example_cli()
    example_integration()
    example_complex_task()
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("\nThe Skill Orchestrator helps you:")
    print("1. Identify the right skill for any task")
    print("2. Select the optimal model for that skill")
    print("3. Understand why each choice was made")
    print("4. Explore alternative options")
    print("\nTry it with your own tasks!")

if __name__ == "__main__":
    main()
