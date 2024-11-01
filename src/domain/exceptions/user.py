from dataclasses import dataclass

from src.domain.common.exceptions import DomainError


@dataclass
class InvalidUserNameError(DomainError):
    message: str

    @property
    def description(self) -> str:
        return f"ОШИБКА: {self.message}"


@dataclass
class InvalidUserLoginError(DomainError):
    @property
    def description(self) -> str:
        return "Логин должен состоять минимум из 6 символов и минимум одной цифры. Минимум один символ должен быть в верхнем регистре и один в нижнем!"
