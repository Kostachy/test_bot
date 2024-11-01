from src.application.common.gateway import UserGateway
from src.application.exceptions.user import UserNotFoundError
from src.domain.entities.user import User
from src.domain.value_objects.login import UserLogin
from src.domain.value_objects.username import UserName


class UserService:
    """Класс содержащий бизнес логику для работы с Пользователем"""

    def __init__(self, gateway: UserGateway):
        self._gateway = gateway

    async def get_current_user(self, user_id: int) -> User | None:
        user = await self._gateway.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    async def check_login(self, user_id: int, input_login: str) -> bool:
        user = await self._gateway.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        if user.login.to_raw() == input_login:
            return True
        return False

    async def register_new_user(
        self, user_id: int, name: str, login: str
    ) -> User | None:
        checked_user = await self._gateway.get_user_by_id(user_id)
        if checked_user is None:
            username = UserName(name)
            user_login = UserLogin(login)
            user = User(id=user_id, name=username, login=user_login, created_at=None)
            await self._gateway.save_user(user)
            await self._gateway.commit()
            return user
