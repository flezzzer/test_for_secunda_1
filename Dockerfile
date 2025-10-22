FROM python:3.12-slim

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
 && poetry install --without dev --no-interaction --no-ansi

COPY . /app

CMD alembic upgrade head && python -m app.test_data && uvicorn app.main:app --host 0.0.0.0 --port 8000

