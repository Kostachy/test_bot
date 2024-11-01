from dataclasses import dataclass

from src.application.common.exception import ApplicationError


@dataclass
class UserAlreadyExistsError(ApplicationError):
    user_id: int

    @property
    def description(self) -> str:
        return f"Пользователь с id {self.user_id} уже существует"


@dataclass
class UserNotFoundError(ApplicationError):
    user_id: int

    @property
    def description(self) -> str:
        return f"Пользователь с id {self.user_id} не найден"


@dataclass
class UserLoginNotUniqueError(ApplicationError):
    login: str

    @property
    def description(self) -> str:
        return f"Логин с id {self.login} не найден"
