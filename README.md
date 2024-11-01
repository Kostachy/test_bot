### Инструкция

1. git clone `https://github.com/Kostachy/test_bot.git`
2. Установить .env переменные как в .env.example
    - `TG_BOT_TOKEN`- token from BotFather
    - `TG_BOT_API_ID` - API_ID from https://my.telegram.org/apps
    - `TG_BOT_API_HASH` - API_HASH from from https://my.telegram.org/apps
3. Запустить докер через `make up`
4. Прогнать миграции через `make migrate`
5. Для просмотра логов `docker compose logs app.tg_bot -f`
6. Для остановки и удаления контейнеров `make down`


## Общее описание задачи и ее контекста.
Разрабатываете бота для управления задачами.

## Обзор выбранных технологий и инструментов.
Стeк: Python 3.11, SQLalchemy, alembic, asyncpg, pyrogram.

## Архитектурное описание решения
Реализована Чистая архитектура с элементами тактический паттернов из DDD.

