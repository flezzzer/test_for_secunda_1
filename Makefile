.PHONY: build run stop logs shell db migrate seed down clean help

help:
	@echo "Доступные команды:"
	@echo "  build    - собрать Docker образы"
	@echo "  run      - поднять проект (API + DB)"
	@echo "  stop     - остановить контейнеры"
	@echo "  down     - удалить контейнеры и тома"
	@echo "  logs     - показать логи API"
	@echo "  shell    - bash в API контейнере"
	@echo "  db       - подключиться к PostgreSQL"
	@echo "  migrate  - применить миграции Alembic"
	@echo "  seed     - заполнить тестовыми данными"
	@echo "  clean    - удалить контейнеры, тома и кеш Docker"

build:
	docker-compose build

run:
	docker-compose up --build

stop:
	docker-compose stop

down:
	docker-compose down -v

logs:
	docker-compose logs -f fastapi

shell:
	docker exec -it fastapi_app bash

db:
	docker exec -it postgres_db psql -U postgres -d org_catalog

migrate:
	docker exec -it fastapi_app alembic upgrade head

seed:
	docker exec -it fastapi_app poetry run python -m app.test_data

clean:
	docker-compose down -v
	docker system prune -f
