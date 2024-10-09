# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables for Poetry installation
ENV POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the project files
COPY ./src /app/src
COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Expose the FastAPI default port
EXPOSE 8000

# Command to run the FastAPI server
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
