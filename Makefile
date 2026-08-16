.PHONY: setup safety test up down logs smoke

setup:
	@test -f .env || cp .env.example .env
	@echo "Edit .env and set OPENAI_API_KEY plus random local passwords before starting."

safety:
	bash ./scripts/public-safety-check.sh

test:
	python -m pytest -q

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f gateway

smoke:
	bash ./examples/curl.sh
