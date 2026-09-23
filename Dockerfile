# Use official Python 3.14 alpine image
FROM python:3.14-alpine

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.4.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONOPTIMIZE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    curl \
    build-base \
    mariadb-dev \
    postgresql-dev \
    gcc \
    musl-dev

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only dependency files first (for better caching)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root

# Copy project files
COPY . /app/

# Collect static files (optional, if using Django staticfiles)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
