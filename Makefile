package_dir := "src"

.PHONY: up
up:  ## Run app in docker container
	docker compose up --build -d

.PHONY: down
down:  ## Stop docker containers
	docker compose down

.PHONY: migrate
migrate:  ## migrate
	docker compose exec tg_bot alembic upgrade head
