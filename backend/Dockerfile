FROM python:3.12.7-slim

# Install Poetry (adjust version as needed)
ENV POETRY_VERSION=1.8.4
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Set workdir
WORKDIR /app

# Copy poetry files for dependency install
COPY pyproject.toml poetry.lock /app/

# Install dependencies
# --no-root: do not install the current package itself as a library
# --without dev: skip dev dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --without dev

# Copy the rest of your backend code
COPY . /app

# Expose the port FastAPI will listen on
EXPOSE 8002

# Run FastAPI with uvicorn, referencing your main app
CMD ["poetry", "run", "uvicorn", "infrastructure.api.main:app", \
     "--host", "0.0.0.0", "--port", "8002", "--log-level", "debug"]
