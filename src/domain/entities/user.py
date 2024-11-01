from dataclasses import dataclass
from datetime import datetime

from src.domain.value_objects.login import UserLogin
from src.domain.value_objects.username import UserName


@dataclass
class User:
    """Сущность Пользователь. Представляет собой анемичную модель из DDD"""
    id: int | None
    name: UserName
    login: UserLogin
    created_at: datetime | None
