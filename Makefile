.PHONY: setup db-up db-down db-reset api web test check

setup: db-up
	cd backend && uv sync
	cd frontend && pnpm install
	$(MAKE) db-reset

db-up:
	docker compose up -d --wait database

db-down:
	docker compose down -v

db-reset:
	cd backend && uv run python -m src.seed

api:
	cd backend && uv run uvicorn src.app:app --reload --port 8000

web:
	cd frontend && pnpm dev

test:
	cd backend && uv run pytest
	cd frontend && pnpm test

check:
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy src
	cd frontend && pnpm typecheck
