FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.9.28 /uv /uvx /bin/

# Install Java runtime (required by tika)
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-21-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application into the container.
COPY . /src

# Install the application dependencies.
WORKDIR /src
RUN uv sync --frozen --no-cache

# Add a non-root user to run the application.
RUN useradd -m mceng
USER mceng

EXPOSE 8000

# Run the application.
CMD ["/src/.venv/bin/fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]
