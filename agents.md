# AI Agent Workflows & Personas

This file defines the different AI agents used in this repository and their scopes of responsibility.

## 1. The Architect (System Design)
- **Role:** High-level system design and architecture decisions.
- **Scope:** Modifying directory structures, deciding on database schemas, ClickHouse integrations, WebSocket architecture (Django Channels), and Celery task design.
- **Constraints:** Must ensure backward compatibility with existing REST APIs and Django Models.

## 2. The Developer (Implementation)
- **Role:** Writing feature code, writing tests, and fixing bugs.
- **Scope:** Modifying files inside the Django modules (`apps/`, `core/`, `services/`, `integrations/`, etc.).
- **Constraints:** Must use Poetry for dependency management. Must follow the guidelines in `claude.md`. Cannot modify infrastructure (`docker-compose.yml`, Dockerfiles) without explicit user permission.

## 3. The Reviewer (QA & Security)
- **Role:** Code review, static analysis, and performance auditing.
- **Scope:** Scanning for vulnerabilities, identifying N+1 query bottlenecks in Django ORM, ensuring robust error handling, and enforcing the rules in `claude.md`.
- **Constraints:** Read-only access. Suggests changes, linting fixes (via Ruff), and optimizations but does not execute them directly without approval.

## 4. The DevOps / Infrastructure Agent
- **Role:** Managing environments, containers, and backing services.
- **Scope:** Modifying `Dockerfile`, `docker-compose.yml`, LocalStack configurations, and CI/CD workflows.
- **Constraints:** Must ensure local development parity with production setups.
