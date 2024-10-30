from dataclasses import dataclass
from datetime import datetime

from src.domain.value_objects.user.login import UserLogin
from src.domain.value_objects.user.username import UserName


@dataclass
class User:
    id: int
    name: UserName
    login: UserLogin
    created_at: datetime
