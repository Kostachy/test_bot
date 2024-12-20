import re
from dataclasses import dataclass

from src.domain.common.value_objects.base import ValueObject
from src.domain.exceptions.user import InvalidUserNameError


@dataclass(frozen=True)
class UserName(ValueObject[str]):
    """Объект-значение для валидации имени пользователя"""

    value: str

    MAX_LENGTH = 60
    MIN_LENGTH = 3

    def _validate(self) -> None:
        """
        Метода проверяет, что имен больше 3 и меньше 60 символов,
        а также не содержит числа и не является пустым.
        """

        if len(self.value) > self.MAX_LENGTH:
            raise InvalidUserNameError("Имя пользователя слишком длинная!")
        if len(self.value) < self.MIN_LENGTH:
            raise InvalidUserNameError("Имя пользователя слишком короткая!")
        if not self.value:
            raise InvalidUserNameError("Поле не может быть пустым!")
        if bool(re.search(r"\d", self.value)):
            raise InvalidUserNameError(
                "Имя пользователя не может содержать цифр!",
            )
