FROM python:3.12-slim

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
 && poetry install --without dev --no-interaction --no-ansi

COPY . /app

CMD ["poetry", "run", "python", "app/test_data.py"]

