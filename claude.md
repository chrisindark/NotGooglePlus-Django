# AI Assistant Guidelines for NotGooglePlus-Django

This document contains rules and context for AI assistants (Claude, Codex, Antigravity, etc.) operating in this repository.

## Project Context
- **Framework**: Django & Django REST Framework (DRF)
- **Language**: Python 3.14+
- **Dependency Management**: Poetry
- **Async & Real-time**: Django Channels & Daphne
- **Background Processing**: Celery & Redis
- **Storage & Cloud**: LocalStack (S3)
- **Analytics DB**: ClickHouse
- **AI/Audio Pipeline**: Whisper (speech-to-text) -> DeepSeek-R1 / Qwen (summarization)

## Coding Standards
1. **Formatting**: The project uses `ruff` for linting and formatting. Ensure all generated Python code adheres to standard PEP-8 style and is compatible with `ruff`.
2. **Type Hints**: Use Python type hints where possible to improve code readability and static analysis.
3. **Views & APIs**: Prefer Class-Based Views (CBVs) or ViewSets using DRF over function-based views.
4. **Business Logic**: Keep views and models thin. Place complex business logic in the `services/` directory or domain-specific modules.
5. **Settings**: The project uses multiple environment-based settings files (e.g., `notgoogleplus.settings.development`). Avoid hardcoding configuration values; use environment variables (`.env`).

## Development Workflow
- **Migrations**: Always run `poetry run python manage.py makemigrations` and `poetry run python manage.py migrate` when models are modified. Never manually edit migration files unless strictly necessary for data migrations.
- **Dependencies**: Do not use `pip install`. Use `poetry add <package>` for production dependencies and `poetry add --group dev <package>` for dev dependencies.
- **Docker**: When testing integration between Celery, Redis, LocalStack, and Django, rely on `docker-compose.yml`.
