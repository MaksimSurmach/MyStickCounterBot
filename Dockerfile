FROM python:3.11.9-slim-bullseye
LABEL authors="maxsurm@gmail.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false &&  \
    poetry install --no-dev --no-interaction --no-ansi --no-root

# Copy project
COPY mystickcounterbot /app/mystickcounterbot
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Run entrypoint
CMD ["python", "mystickcounterbot/main.py"]
