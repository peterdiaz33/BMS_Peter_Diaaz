Overview
This document explains how developers should contribute to the Insights Hub platform. It defines the workflow, coding standards, branching strategy, commit conventions, pull request rules, and review guidelines.

The goal is to ensure consistency, quality, and maintainability across all services and applications.

1. Contribution Workflow
All contributions follow this workflow:

Fork or clone the repository

Create a feature branch

Write code + tests

Run all tests locally

Submit a Pull Request (PR)

Request review

Address feedback

Merge into main

2. Branching Strategy
Use the following branches:

main → stable production-ready code

develop → integration branch

feature/<name> → new features

fix/<name> → bug fixes

docs/<name> → documentation updates

Examples:
Code
feature/add-tenant-validation
fix/batch-job-timeout
docs/update-deployment-guide

3. Coding Standards
Python Style
Follow PEP8

Use type hints

Use async/await for all service calls

Keep functions small and focused

Avoid circular imports

Use dependency injection where possible

Folder Structure
Core logic → platform_core/

Microservices → platform_services/

Applications → apps/

Documentation → root .md files

Logging
Always use:

Code
get_logger(app_name, tenant)
Never use print() in production code.


4. Testing Requirements
Every contribution must include tests:

Unit tests for core logic

Integration tests for service interactions

Tenant isolation tests

Security tests

Batch job tests (if applicable)

Run tests:

Code
pytest
All tests must pass before merging.


5. Commit Message Conventions
Use Conventional Commits:

Format:
Code
<type>(scope): description
Types:
feat → new feature

fix → bug fix

docs → documentation

test → testing

refactor → code improvement

chore → maintenance

Examples:
Code
feat(auth): add tenant validation
fix(data-proxy): correct SQL parsing
docs(readme): update architecture section
test(batch): add job scheduling tests


6. Pull Request Guidelines
Every PR must include:

Clear description

What changed

Why it changed

How to test it

Screenshots (if UI)

Linked issue (if applicable)

PR Requirements:
All tests pass

No linting errors

No commented-out code

No unused imports

No secrets or credentials

Tenant isolation preserved


7. Code Review Guidelines
Reviewers must check:

Correctness

Readability

Security

Tenant isolation

Logging consistency

Error handling

Performance impact

Documentation updates

Reviewers should:

Be constructive

Suggest improvements

Avoid blocking unnecessarily

Ensure architectural consistency


8. Security Rules for Contributors
Contributors must:

Never commit secrets

Never expose tenant data

Validate all inputs

Use secure headers

Avoid unsafe SQL

Follow security.md guidelines


9. Release Process
Merge feature branches into develop

Run full test suite

Create release branch

Tag version:

Code
v1.0.0
Merge into main

Deploy using deployment guide

Update CHANGELOG.md


Final Notes
This contribution guide ensures:

High-quality code

Consistent architecture

Safe multi-tenant behavior

Secure development practices

Smooth collaboration