from abc import abstractmethod
from typing import Protocol, Sequence

from src.domain.entities.task import Task
from src.domain.entities.user import User


class UserGateway(Protocol):

    @abstractmethod
    async def get_user_by_id(self, id_: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def save_user(self, user: User) -> int:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError


class TaskGateway(Protocol):

    @abstractmethod
    async def get_all_tasks_by_user_id(self, user_id: int) -> Sequence[Task] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_by_id(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def save_task(self, task: Task) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task: Task) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task: Task) -> int:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
