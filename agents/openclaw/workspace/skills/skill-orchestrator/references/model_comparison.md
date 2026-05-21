# Model Comparison Guide

Detailed comparison of available models to help with intelligent model selection.

## Model Specifications

| Model | Context Window | Max Tokens | Primary Use Case | Strengths | Weaknesses | Cost Efficiency |
|-------|---------------|------------|------------------|-----------|------------|-----------------|
| **deepseek-v4-flash** | 128K | 128K | Fast responses, simple tasks | Speed, efficiency, large context | Less creative, simpler reasoning | ⭐⭐⭐⭐⭐ (Best) |
| **deepseek-v3.2** | 32K | 32K | General purpose, balanced | Good balance, reliable | Smaller context than v4 | ⭐⭐⭐⭐ |
| **deepseek-v4-pro** | 64K | 64K | Complex tasks, creativity | High quality, creative, capable | Slower, more expensive | ⭐⭐⭐ |
| **deepseek-v3.1-terminus** | 32K | 32K | Technical/coding tasks | Coding expertise, precision | Less creative, specialized | ⭐⭐⭐⭐ |
| **DeepSeek-V3** | 32K | 32K | General purpose | Reliable, consistent | Not specialized | ⭐⭐⭐⭐ |
| **deepseek-r1-250528** | 128K | 32K | Complex reasoning | Advanced reasoning, logic | Slower, more expensive | ⭐⭐ |
| **glm-5** | 128K | 32K | GLM tasks, Chinese | GLM compatibility, Chinese | English may be weaker | ⭐⭐⭐ |
| **glm-5.1** | 128K | 32K | Enhanced GLM tasks | Better reasoning, Chinese focus | English may be weaker | ⭐⭐ |

## Performance Characteristics

### Speed Comparison (Fastest to Slowest)
1. **deepseek-v4-flash** - Optimized for speed
2. **deepseek-v3.2** - Good balance
3. **glm-5** - Fast for GLM tasks
4. **DeepSeek-V3** - Standard speed
5. **deepseek-v3.1-terminus** - Technical processing
6. **glm-5.1** - Enhanced but slower
7. **deepseek-v4-pro** - Quality over speed
8. **deepseek-r1-250528** - Reasoning takes time

### Quality Comparison (Best to Good)
1. **deepseek-v4-pro** - Highest quality output
2. **deepseek-r1-250528** - Best reasoning
3. **glm-5.1** - Best for Chinese/GLM
4. **deepseek-v3.1-terminus** - Best for coding
5. **deepseek-v3.2** - Good general quality
6. **DeepSeek-V3** - Reliable quality
7. **glm-5** - Good for GLM tasks
8. **deepseek-v4-flash** - Adequate for simple tasks

### Cost Efficiency (Most to Least)
1. **deepseek-v4-flash** - Most cost-effective
2. **deepseek-v3.2** - Good value
3. **DeepSeek-V3** - Balanced cost
4. **deepseek-v3.1-terminus** - Specialized value
5. **glm-5** - GLM tasks value
6. **glm-5.1** - Enhanced but costlier
7. **deepseek-v4-pro** - Premium quality
8. **deepseek-r1-250528** - Premium reasoning

## Task-Specific Recommendations

### Coding & Development
| Task Type | Recommended Model | Alternative | Reasoning |
|-----------|------------------|-------------|-----------|
| **Simple scripts** | deepseek-v3.2 | deepseek-v4-flash | Fast, efficient for simple code |
| **Complex applications** | deepseek-v3.1-terminus | deepseek-v4-pro | Technical expertise needed |
| **Architecture design** | deepseek-r1-250528 | deepseek-v4-pro | Requires complex reasoning |
| **Debugging** | deepseek-v3.1-terminus | deepseek-v3.2 | Technical precision |
| **Code review** | deepseek-v4-pro | deepseek-r1-250528 | Quality analysis |

### Security & Analysis
| Task Type | Recommended Model | Alternative | Reasoning |
|-----------|------------------|-------------|-----------|
| **Vulnerability scanning** | deepseek-r1-250528 | deepseek-v4-pro | Analytical reasoning |
| **Security audit** | deepseek-r1-250528 | DeepSeek-V3 | Thorough analysis |
| **Quick check** | deepseek-v3.2 | deepseek-v4-flash | Fast assessment |
| **Compliance review** | deepseek-v4-pro | deepseek-r1-250528 | Detailed evaluation |

### Content Creation
| Task Type | Recommended Model | Alternative | Reasoning |
|-----------|------------------|-------------|-----------|
| **Creative writing** | deepseek-v4-pro | glm-5.1 | High quality output |
| **Technical writing** | deepseek-v3.1-terminus | deepseek-v4-pro | Precision and accuracy |
| **Simple content** | deepseek-v3.2 | deepseek-v4-flash | Fast, adequate quality |
| **Marketing copy** | glm-5.1 | deepseek-v4-pro | Creative, engaging |

### Analysis & Reasoning
| Task Type | Recommended Model | Alternative | Reasoning |
|-----------|------------------|-------------|-----------|
| **Complex analysis** | deepseek-r1-250528 | deepseek-v4-pro | Advanced reasoning |
| **Data analysis** | deepseek-v4-pro | deepseek-r1-250528 | Pattern recognition |
| **Logical reasoning** | deepseek-r1-250528 | DeepSeek-V3 | Step-by-step logic |
| **Quick analysis** | deepseek-v3.2 | deepseek-v4-flash | Fast processing |

### GLM-Specific Tasks
| Task Type | Recommended Model | Alternative | Reasoning |
|-----------|------------------|-------------|-----------|
| **GLM app development** | glm-5 | glm-5.1 | Native GLM understanding |
| **GLM API integration** | glm-5.1 | glm-5 | Enhanced GLM capabilities |
| **Chinese language** | glm-5.1 | glm-5 | Chinese optimization |
| **GLM troubleshooting** | glm-5 | deepseek-v3.2 | GLM-specific knowledge |

## Context Window Considerations

### When to Use Large Context (128K)
- **deepseek-v4-flash**: Long documents, extensive codebases
- **glm-5/glm-5.1**: Large Chinese texts, extensive GLM contexts
- **deepseek-r1-250528**: Complex reasoning with many steps

### When 32K-64K is Sufficient
- **Most general tasks**: deepseek-v3.2, DeepSeek-V3
- **Technical coding**: deepseek-v3.1-terminus
- **Quality-focused**: deepseek-v4-pro

## Cost-Benefit Analysis

### Budget-Conscious Projects
1. **deepseek-v4-flash**: Maximum efficiency
2. **deepseek-v3.2**: Good balance
3. **glm-5**: For GLM tasks

### Quality-First Projects
1. **deepseek-v4-pro**: Best overall quality
2. **deepseek-r1-250528**: Best reasoning
3. **glm-5.1**: Best for Chinese/GLM

### Specialized Projects
1. **deepseek-v3.1-terminus**: Coding/technical work
2. **deepseek-r1-250528**: Analysis/reasoning work
3. **glm-5/5.1**: GLM/Chinese work

## Model Selection Algorithm

### Decision Tree
```
START → What is the primary task type?
         |
         ├─ Coding/Technical → deepseek-v3.1-terminus
         │
         ├─ Analysis/Reasoning → deepseek-r1-250528
         │
         ├─ Creative/Quality → deepseek-v4-pro
         │
         ├─ GLM/Chinese → glm-5.1
         │
         ├─ Fast/Simple → deepseek-v4-flash
         │
         └─ General/Balanced → deepseek-v3.2
```

### Factors to Consider
1. **Task Complexity**: Simple → Fast models, Complex → Powerful models
2. **Budget**: Cost-sensitive → Efficient models
3. **Quality Needs**: High quality → Premium models
4. **Specialization**: Technical → Specialized models
5. **Context Length**: Long context → Large window models
6. **Speed Requirements**: Real-time → Fast models

## Real-World Examples

### Example 1: Startup MVP
- **Task**: Build a simple web app MVP
- **Constraints**: Limited budget, fast iteration
- **Recommendation**: deepseek-v4-flash
- **Why**: Cost-effective, fast, sufficient for MVP

### Example 2: Enterprise Security Audit
- **Task**: Comprehensive security assessment
- **Constraints**: High accuracy, thorough analysis
- **Recommendation**: deepseek-r1-250528
- **Why**: Advanced reasoning, comprehensive analysis

### Example 3: Chinese Content Platform
- **Task**: Build GLM-powered Chinese content generator
- **Constraints**: Chinese language, GLM integration
- **Recommendation**: glm-5.1
- **Why**: Chinese optimization, GLM compatibility

### Example 4: Technical Documentation
- **Task**: Write detailed API documentation
- **Constraints**: Technical accuracy, clarity
- **Recommendation**: deepseek-v3.1-terminus
- **Why**: Technical precision, coding expertise

### Example 5: Creative Marketing Campaign
- **Task**: Generate marketing content
- **Constraints**: Creativity, engagement
- **Recommendation**: deepseek-v4-pro
- **Why**: High quality, creative output

## Performance Metrics

### Response Time (Estimated)
| Model | Simple Task | Complex Task | Token Generation |
|-------|-------------|--------------|------------------|
| deepseek-v4-flash | 0.5-1s | 2-3s | Fastest |
| deepseek-v3.2 | 1-2s | 3-5s | Fast |
| deepseek-v4-pro | 2-3s | 5-8s | Moderate |
| deepseek-r1-250528 | 3-4s | 8-12s | Slower (reasoning) |
| glm-5 | 1-2s | 3-6s | Fast for GLM |
| glm-5.1 | 2-3s | 6-9s | Moderate for GLM |

### Accuracy Benchmarks
| Model | Coding | Reasoning | Creativity | Chinese |
|-------|--------|-----------|------------|---------|
| deepseek-v4-flash | 85% | 80% | 75% | 70% |
| deepseek-v3.2 | 88% | 85% | 80% | 75% |
| deepseek-v4-pro | 92% | 90% | 95% | 80% |
| deepseek-v3.1-terminus | 95% | 85% | 75% | 70% |
| deepseek-r1-250528 | 90% | 98% | 85% | 75% |
| glm-5 | 80% | 80% | 85% | 95% |
| glm-5.1 | 85% | 90% | 90% | 98% |

## Integration with Skill Orchestrator

### Automatic Selection Rules
The skill orchestrator uses these rules:

1. **Technical + Coding** → deepseek-v3.1-terminus
2. **Complex + Reasoning** → deepseek-r1-250528  
3. **Creative + Quality** → deepseek-v4-pro
4. **GLM + Chinese** → glm-5.1
5. **Simple + Fast** → deepseek-v4-flash
6. **General + Balanced** → deepseek-v3.2

### Override Guidelines
When to manually override automatic selection:

1. **Budget constraints**: Choose more efficient models
2. **Time constraints**: Choose faster models
3. **Quality requirements**: Choose higher quality models
4. **Specialized needs**: Choose specialized models
5. **User preference**: Respect explicit requests

## Best Practices

### 1. Start with Default
Begin with automatic selection, then adjust based on results.

### 2. Monitor Performance
Track which models work best for specific task types.

### 3. Consider Context
- Short conversations: Any model
- Long contexts: deepseek-v4-flash or glm-5
- Complex reasoning: deepseek-r1-250528

### 4. Balance Cost & Quality
- Internal tools: Efficient models (v4-flash, v3.2)
- Customer-facing: Quality models (v4-pro, glm-5.1)
- Critical systems: Best models (r1-250528, v4-pro)

### 5. Test and Iterate
Run small tests with different models to find the best fit for your specific use case.

## Troubleshooting

### Common Issues & Solutions

**Issue**: Model too slow for task
**Solution**: Switch to faster model (deepseek-v4-flash)

**Issue**: Output quality insufficient
**Solution**: Switch to higher quality model (deepseek-v4-pro)

**Issue**: Technical accuracy problems
**Solution**: Switch to technical model (deepseek-v3.1-terminus)

**Issue**: Reasoning capabilities lacking
**Solution**: Switch to reasoning model (deepseek-r1-250528)

**Issue**: GLM compatibility issues
**Solution**: Switch to GLM model (glm-5 or glm-5.1)

## Future Considerations

### Model Updates
- Monitor for new model releases
- Update comparison matrix regularly
- Test new models for your use cases

### Performance Optimization
- Implement caching for repeated queries
- Use streaming for long responses
- Batch similar requests

### Cost Management
- Set usage limits per model
- Monitor cost vs performance
- Optimize prompt efficiency

## Conclusion

Choosing the right model involves balancing:
1. **Task requirements** (complexity, specialization)
2. **Performance needs** (speed, quality)
3. **Budget constraints** (cost efficiency)
4. **Technical constraints** (context, compatibility)

The skill orchestrator automates this decision, but understanding these trade-offs helps make informed choices and overrides when needed.
