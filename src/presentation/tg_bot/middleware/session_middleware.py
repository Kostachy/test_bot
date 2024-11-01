from pyrogram_patch.middlewares import PatchHelper
from pyrogram_patch.middlewares.middleware_types import OnUpdateMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SessionMiddleware(OnUpdateMiddleware):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self.session_maker = session_maker

    async def __call__(self, update, client, patch_helper: PatchHelper):
        async with self.session_maker() as session:
            patch_helper.data["sqlalchemy_session"] = session
