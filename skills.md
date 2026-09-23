# AI Agent Skills & Tooling Reference

This document outlines the specific skills, commands, and workflows AI agents can utilize when working on the NotGooglePlus-Django repository.

## 1. Environment & Dependencies (Poetry)
- **Install dependencies:** `poetry install`
- **Add a package:** `poetry add <package>`
- **Add a dev package:** `poetry add --group dev <package>`
- **Run a command in virtualenv:** `poetry run <command>`

## 2. Django Management Commands
- **Migrations:** `poetry run python manage.py makemigrations` and `poetry run python manage.py migrate`
- **Create Superuser:** `poetry run python manage.py createsuperuser`
- **Collect Static:** `poetry run python manage.py collectstatic`
- **Seed Data:** 
  - `poetry run python manage.py posts --count=3`
  - `poetry run python manage.py articles --count=3`
  - `poetry run python manage.py seed_audio_posts --count=3`

## 3. Running Services (Local)
- **Django Server:** `poetry run python manage.py runserver --settings=notgoogleplus.settings.development`
- **Daphne (WebSockets):** `poetry run daphne -b 127.0.0.1 -p 8001 notgoogleplus.asgi:channel_layer`
- **WebSocket Worker:** `poetry run python manage.py runworker --settings=notgoogleplus.settings.development`
- **Celery Worker:** `poetry run celery -A notgoogleplus_django worker -l INFO -Q celery,transcriptions_queue --pool=solo`

## 4. Docker & Infrastructure
- **Start Backing Services Only:** `docker compose up -d redis localstack clickhouse`
- **Full Stack Build & Run:** `docker compose up --build`
- **Execute command in Web Container:** `docker compose exec web <command>`
- **Stop all services:** `docker compose down`

## 5. Code Quality & Linting
- **Linting (Ruff):** `poetry run ruff check .`
- **Auto-fix Linting:** `poetry run ruff check . --fix`
- **Formatting (Ruff):** `poetry run ruff format .`
