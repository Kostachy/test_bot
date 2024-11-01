from pyrogram_patch.middlewares import PatchHelper
from pyrogram_patch.middlewares.middleware_types import OnUpdateMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.gateway.task import SqlTaskGateway
from src.infrastructure.db.gateway.user import SqlUserGateway


class GatewayMiddleware(OnUpdateMiddleware):

    async def __call__(self, update, client, patch_helper: PatchHelper):
        sqlalchemy_session: AsyncSession = patch_helper.data["sqlalchemy_session"]
        patch_helper.data["user_gateway"] = SqlUserGateway(sqlalchemy_session)
        patch_helper.data["task_gateway"] = SqlTaskGateway(sqlalchemy_session)
