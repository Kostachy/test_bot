package_dir := "src"

.PHONY: up
up:  ## Run app in docker container
	docker compose --profile tg_bot up --build -d

.PHONY: down
down:  ## Stop docker containers
	docker compose --profile tg_bot down
