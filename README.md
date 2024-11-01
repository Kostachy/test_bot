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
7. Для старта бота пропишите команду `/start` (в самом меню бота)


### Общее описание задачи и ее контекста.
Разработка бота для управления задачами.

### Обзор выбранных технологий и инструментов.
Стeк: Python 3.11, SQLalchemy, alembic, asyncpg, pyrogram.

### Архитектурное описание решения
Реализована Чистая архитектура с элементами тактический паттернов из DDD.

### Описание основных классов и функций, их назначения и взаимодействия.
Domain layer:
 - Сущности User, Task представляют собой корневые сущности.
 - Объекты-значения UserLogin, UserName задают правила и ограничения для экземпляров этого класса.

Application layer:
 - в пакете Commonn содержаться интерфейсы для сервисного слоя
 - в пакете Service содержаться компоненты реализующие прикладную бизнес логику, на вход принимают интерфейсы Gateway, что позволяет не привязываться к деталям реализации.

Infrastructure layer:
 - Содержит слоя доступа к данным, реализует интерфейсы UserGateway и TaskGateway, так же сразу маппит из моделей алхимии в модели Сущностей из Domain layer.

Presentation layer:
 - Представляет собой слой представления. Этот слой может быть чем угодно (тг бот, API, голый html и т.д.)


### Диаграмма компонентов и взаимодействий.
[UML Class diagram](assets/UML%20Class%20diagram%20by%20Dmitry%20Ermakov.pdf)
