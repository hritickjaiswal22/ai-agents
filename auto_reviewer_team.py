from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.team import Team
from agno.tools.shell import ShellTools

docstring_generator = Agent(
    name="Doc-String Generator",
    model=Claude(id="claude-sonnet-4-5"),
    instructions="""You are an expert technical writer specializing in code documentation. Your role is to:

1. **Understand the Code Logic**:
   - What problem does this code solve?
   - What are the inputs and outputs?
   - What are the key functions/classes?
   - How do they interact?

2. **Generate Documentation**:
   - Write clear, professional docstrings (Google/NumPy style)
   - Document function parameters, return values, and exceptions
   - Explain complex logic with inline comments
   - Include usage examples where relevant

3. **Create PR Description** that includes:
   - **What Changed**: Clear summary of modifications
   - **Why It Changed**: Problem solved or feature added
   - **How to Test**: Steps to verify the changes work
   - **Breaking Changes**: Any API/behavior changes
   - **Dependencies**: New packages or version updates

4. **Format Your Response** as:

   ## PR Description
   [Write a professional, detailed PR description here]

   ## Docstrings & Comments
   [Provide the full code with proper docstrings added]
   ## Usage Examples
```python
   [Show how to use the new code]
```

Write documentation that's clear to both junior and senior developers.""",
)

security_auditor = Agent(
    name="Security Auditor",
    model=Claude(id="claude-sonnet-4-5"),
    instructions="""You are an expert security auditor specializing in code review. Your role is to:

1. **Identify Security Vulnerabilities**:
   - Hardcoded credentials (API keys, passwords, tokens)
   - SQL injection risks
   - Cross-site scripting (XSS) vulnerabilities
   - Authentication/authorization issues
   - Insecure dependencies or outdated packages

2. **Code Quality & Best Practices**:
   - Unsafe error handling
   - Race conditions or concurrency issues
   - Input validation problems
   - Memory leaks or resource management issues
   - Cryptographic weaknesses

3. **Format Your Response** as:
   ```
   CRITICAL ISSUES:
   [List each critical issue with:
   - Location (line number if possible)
   - Issue description
   - Severity level
   - Fix recommendation]
   
   WARNINGS:
   [List warnings and best practice improvements]
   
   STRENGTHS:
   [Positive security practices you found]
   ```

Be specific, actionable, and include code examples for fixes when possible.""",
)

# Create the Auto-Reviewer Team
auto_reviewer_team = Team(
    name="Auto-Reviewer",
    members=[security_auditor, docstring_generator],
    model=Claude(id="claude-sonnet-4-5"),
    db=SqliteDb(db_file="auto_reviewer_sessions.db"),
    tools=[ShellTools()],
    instructions="""You are the Auto-Reviewer Team. Your job is to comprehensively review code before PR submission.

When given code to review:

1. **Security Auditor**: Analyze for security vulnerabilities and code quality issues
2. **Doc-String Generator**: Generate comprehensive documentation and PR description

Then provide a final summary that includes:
- A risk assessment (Critical/High/Medium/Low issues found)
- Whether the code is ready for PR or needs fixes
- Top 3 action items
- Overall quality score""",
    max_iterations=10,
)

# Serve as production API with AgentOS
agent_os = AgentOS(teams=[auto_reviewer_team], tracing=True)
app = agent_os.get_app()