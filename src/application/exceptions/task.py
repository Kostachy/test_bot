from dataclasses import dataclass

from src.application.common.exception import ApplicationError


@dataclass
class TaskAlreadyExistsError(ApplicationError):
    task_id: int

    @property
    def description(self) -> str:
        return f"Задача с id {self.task_id} уже существует"


@dataclass
class TaskNotFoundError(ApplicationError):
    task_id: int

    @property
    def description(self) -> str:
        return f"Задача с id {self.task_id} не найдена"
