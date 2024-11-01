import logging

from pyrogram import Client
from pyrogram_patch import patch
from pyrogram_patch.fsm.storages import MemoryStorage

from src.config import load_config
from src.infrastructure.db.factory import create_engine, create_session_maker
from src.presentation.tg_bot.handlers.registration_handler import auth_router
from src.presentation.tg_bot.handlers.task_handler import task_router
from src.presentation.tg_bot.middleware.gateway_middleware import GatewayMiddleware
from src.presentation.tg_bot.middleware.session_middleware import SessionMiddleware


def main() -> Client:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    settings = load_config()
    engine = create_engine(database_url=settings.database.database_url)
    session_maker = create_session_maker(engine)

    app = Client(
        name="Test_tg_bot",
        api_id=settings.tg_bot.api_id,
        api_hash=settings.tg_bot.api_hash,
        bot_token=settings.tg_bot.token,
    )
    patch_manager = patch(app)
    patch_manager.set_storage(MemoryStorage())
    patch_manager.include_middleware(SessionMiddleware(session_maker))
    patch_manager.include_middleware(GatewayMiddleware())
    patch_manager.include_router(auth_router)
    patch_manager.include_router(task_router)

    return app


if __name__ == "__main__":
    main().run()
