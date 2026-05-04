FROM ghcr.io/astral-sh/uv:0.8.3-python3.13-bookworm-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml README.md ./
COPY uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev

EXPOSE 8080

CMD ["uvicorn", "omi_rest_api_gateway.main:app", "--host", "0.0.0.0", "--port", "8080"]
