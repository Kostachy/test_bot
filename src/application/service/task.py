from typing import Sequence

from src.application.common.gateway import TaskGateway
from src.application.exceptions.task import TaskNotFoundError
from src.domain.entities.task import Task
from src.domain.value_objects.task_state import TaskState


class TaskService:
    def __init__(self, gateway: TaskGateway):
        self._gateway = gateway

    async def get_all_users_tasks(self, user_id: int) -> Sequence[Task]:
        tasks = await self._gateway.get_all_tasks_by_user_id(user_id)
        return tasks

    async def find_task_by_id(self, task_id: int) -> Task:
        task = await self._gateway.get_tasks_by_id(task_id=task_id)
        return task

    async def add_new_task(self, name: str, description: str, user_id: int) -> int:
        new_task = Task(
            id=None,
            name=name,
            description=description,
            state=TaskState.PENDING,
            user_id=user_id,
        )
        new_task_id = await self._gateway.save_task(new_task)
        await self._gateway.commit()
        return new_task_id

    async def change_task_to_done(self, task: Task) -> int | None:
        task = await self._gateway.get_tasks_by_id(task_id=task.id)
        if task is None:
            raise TaskNotFoundError
        task.change_to_done()
        new_task_id = await self._gateway.update_task(task)
        await self._gateway.commit()
        return new_task_id

    async def delete_task(self, task: Task) -> int | None:
        task = await self._gateway.get_tasks_by_id(task_id=task.id)
        if task is None:
            raise TaskNotFoundError
        new_task_id = await self._gateway.delete_task(task)
        await self._gateway.commit()
        return new_task_id
