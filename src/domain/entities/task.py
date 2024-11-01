from dataclasses import dataclass

from src.domain.value_objects.task_state import TaskState


@dataclass
class Task:
    """Сущность Задача. Представляет собой анемичную модель из DDD"""
    id: int | None
    name: str
    description: str
    state: TaskState
    user_id: int

    def change_to_done(self) -> None:
        self.state = TaskState.DONE
