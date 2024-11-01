from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.gateway import UserGateway
from src.application.exceptions.user import (
    UserAlreadyExistsError,
    UserLoginNotUniqueError,
)
from src.domain.entities.user import User
from src.domain.value_objects.login import UserLogin
from src.domain.value_objects.username import UserName
from src.infrastructure.db import models
from src.infrastructure.db.exceptions import GatewayError


class SqlUserGateway(UserGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, id_: int) -> User | None:
        query = select(models.User).where(models.User.id == id_)
        result = await self.session.execute(query)
        user_from_db = result.scalar_one_or_none()
        if user_from_db is not None:
            return User(
                id=user_from_db.id,
                name=UserName(user_from_db.name),
                login=UserLogin(user_from_db.login),
                created_at=user_from_db.created_at,
            )
        return None

    async def save_user(self, user: User) -> int:
        user_to_save = models.User(
            id=user.id,
            name=user.name.to_raw(),
            login=user.login.to_raw(),
        )
        self.session.add(user_to_save)
        try:
            await self.session.flush((user_to_save,))
        except IntegrityError as err:
            self._parse_error(err, user_to_save)
        return user_to_save.id

    def _parse_error(self, err: DBAPIError, user: User) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserAlreadyExistsError(user.id) from err
            case "uq_users_login":
                raise UserLoginNotUniqueError(user.login.to_raw()) from err
            case _:
                raise GatewayError from err

    async def commit(self) -> None:
        await self.session.commit()
