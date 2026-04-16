# Import builer python image
FROM python:3.14-alpine AS builder
# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.3 /uv /uvx /bin/
# Set workdir
WORKDIR /app
# Exclude development dependencies
ENV UV_NO_DEV=1
# Copy dependency files to the working directory
COPY pyproject.toml uv.lock ./
# Install dependencies
RUN uv sync --locked --no-install-project
# Copy application code
COPY . .
# Install project
RUN uv sync --locked

# Import fresh base python image
FROM python:3.14-alpine
# Copy the application from the builder
COPY --from=builder /app /app
# Set workdir
WORKDIR /app
# Set env
ENV PATH="/app/.venv/bin:$PATH"
# Run migrations on container start, then start the app
CMD ["sh", "-c", "alembic upgrade head && fastapi run src/main.py --port 80"]