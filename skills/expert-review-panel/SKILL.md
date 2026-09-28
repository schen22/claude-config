---
name: expert-review-panel
description: Rigorous multi-expert code review with iterative improvement until quality threshold is met. Use when the user asks to "review with experts", "expert panel review", "iterate until perfect", "high quality review", "review until 90+", or wants comprehensive architectural review before finalizing changes. Triggers on phrases like "have experts review", "iterate on quality", or "don't return until it's excellent".
version: 1.0.0
---

# Expert Review Panel Skill

Before returning changes to the user, convene a panel of world-class experts to review the work. Each expert provides detailed feedback and a score. Iterate on improvements until the average score exceeds the quality threshold (default: 90/100).

## The Expert Panel

Assemble 10 experts, each bringing a specialized lens:

### 1. Software Architect

- Overall system design and structure
- Separation of concerns
- Modularity and composability
- Design patterns (appropriate use, not overuse)
- Dependency management
- Future extensibility without over-engineering

### 2. Security Engineer

- Input validation and sanitization
- Authentication and authorization
- Injection vulnerabilities (SQL, XSS, command)
- Secrets management
- Data exposure risks
- Principle of least privilege
- OWASP Top 10 compliance

### 3. Performance Engineer

- Algorithmic complexity (time and space)
- Database query efficiency
- Memory management and leaks
- Caching opportunities
- Lazy loading and pagination
- Bundle size and load time
- Hot paths and bottlenecks

### 4. Database Architect

- Schema design and normalization
- Index strategy
- Query optimization
- Data integrity constraints
- Migration safety
- Connection pooling
- Transaction handling

### 5. API Designer

- RESTful principles / GraphQL best practices
- Versioning strategy
- Error response consistency
- Pagination and filtering
- Rate limiting considerations
- Documentation completeness
- Backward compatibility

### 6. UX Engineer

- User flow coherence
- Error message clarity
- Loading and empty states
- Accessibility (WCAG compliance)
- Responsive design
- Keyboard navigation
- Perceived performance

### 7. Reliability Engineer (SRE)

- Error handling completeness
- Retry logic and backoff
- Circuit breakers
- Observability (logging, metrics, tracing)
- Graceful degradation
- Failure mode analysis
- Recovery procedures

### 8. Code Quality Specialist

- Readability and clarity
- Naming conventions
- Function size and complexity
- DRY without over-abstraction. Does similar code need to be unified?
- Comments where needed (not obvious)
- Consistent style
- Test coverage and quality

### 9. Domain Expert

- Business logic correctness. If the domain is tax, check the IRS rules. If the domain is Residential Energy Quality Assurance, check the RESNET standards.
- Edge case handling
- Domain modeling accuracy
- Terminology consistency
- Regulatory compliance
- Real-world scenario coverage

### 10. Maintainability Advocate

- Onboarding friction for new developers
- Debug-ability
- Change impact radius
- Technical debt implications
- Documentation needs. Did we update relevant docs? Are they clear?
- Upgrade path clarity

## Review Process

### Step 1: Initial Review

Each expert reviews the changeset independently and provides:

```
## [Expert Name] Review

**Score: XX/100**

### Strengths
- [What's done well]

### Critical Issues (Must Fix)
- [Issue]: [Specific location and recommendation]

### Improvements (Should Fix)
- [Issue]: [Specific location and recommendation]

### Minor Suggestions
- [Suggestion]

### Specific Recommendations for Score Improvement
To raise this score, I would need to see:
- [Concrete change 1]
- [Concrete change 2]
```

### Step 2: Calculate Average

Sum all expert scores and divide by 10. If average < 90, proceed to Step 3.

### Step 3: Prioritized Improvement

Address feedback in order:

1. All "Critical Issues" from any expert
2. "Improvements" from experts with lowest scores
3. Patterns appearing across multiple experts
4. Quick wins that boost multiple scores

### Step 4: Re-review

After improvements, have each affected expert re-review their area and provide updated scores.

### Step 5: Iterate

Repeat Steps 2-4 until average score >= 90/100.

## Output Format

Present the review as:

```markdown
# Expert Panel Review - Iteration [N]

## Summary

- **Average Score:** [XX]/100
- **Threshold:** 90/100
- **Status:** [PASSED / NEEDS IMPROVEMENT]

## Individual Expert Scores

| Expert                   | Score | Key Concern |
| ------------------------ | ----- | ----------- |
| Software Architect       | XX    | [One-liner] |
| Security Engineer        | XX    | [One-liner] |
| Performance Engineer     | XX    | [One-liner] |
| Database Architect       | XX    | [One-liner] |
| API Designer             | XX    | [One-liner] |
| UX Engineer              | XX    | [One-liner] |
| Reliability Engineer     | XX    | [One-liner] |
| Code Quality Specialist  | XX    | [One-liner] |
| Domain Expert            | XX    | [One-liner] |
| Maintainability Advocate | XX    | [One-liner] |

## Detailed Feedback

[Full feedback from each expert]

## Improvement Plan

[If not passed: specific changes to make, in priority order]
```

## Scoring Guidelines

Experts should score based on:

- **90-100:** Production-ready, exemplary code. Minor nitpicks only.
- **80-89:** Good code with small improvements needed. No significant issues.
- **70-79:** Acceptable but has notable issues that should be addressed.
- **60-69:** Concerning issues that pose real risks if shipped.
- **Below 60:** Significant problems requiring substantial rework.

Scores should be honest and critical. A 90+ average means the code is genuinely excellent, not just "good enough."

## Execution Instructions

1. **Complete your changes first** - finish the implementation before invoking the panel
2. **Run the full panel** - all 10 experts review simultaneously
3. **Be genuinely critical** - experts should find real issues, not rubber-stamp
4. **Prioritize ruthlessly** - fix critical issues first, don't get lost in nitpicks
5. **Make real improvements** - actually modify the code, don't just acknowledge feedback
6. **Re-review honestly** - scores should only improve if the code actually improved
7. **Iterate until passing** - don't stop at 85 and call it close enough
8. **Show the journey** - display each iteration so the user sees the improvement process

## Customization

The user may specify:

- Different threshold (e.g., "iterate until 95+")
- Subset of experts (e.g., "just security and performance")
- Additional domain-specific experts
- Focus areas to weight more heavily

Adapt the panel composition and threshold accordingly.
