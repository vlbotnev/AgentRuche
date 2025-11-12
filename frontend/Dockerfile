# frontend/Dockerfile
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /bin/

WORKDIR /app

# Copy only the dependency file first to leverage Docker cache
COPY pyproject.toml ./

ENV UV_LINK_MODE=copy

# Install dependencies
RUN uv sync

# Copy the rest of the application code
COPY . .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]