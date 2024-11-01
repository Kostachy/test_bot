import re
from dataclasses import dataclass

from src.domain.common.value_objects.base import ValueObject
from src.domain.exceptions.user import InvalidUserLoginError


@dataclass(frozen=True)
class UserLogin(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if not self.value:
            raise InvalidUserLoginError()
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{7,19}$", self.value):
            raise InvalidUserLoginError()
