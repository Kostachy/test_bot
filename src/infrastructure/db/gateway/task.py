from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.gateway import TaskGateway
from src.application.exceptions.task import TaskAlreadyExistsError
from src.domain.entities.task import Task
from src.infrastructure.db import models
from src.infrastructure.db.exceptions import GatewayError


class SqlTaskGateway(TaskGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks_by_id(self, task_id: int) -> Task | None:
        query = select(models.Task).where(models.Task.id == task_id)
        result = await self.session.execute(query)
        tasks_from_db = result.scalar_one_or_none()
        if not tasks_from_db:
            return None
        return Task(
            id=tasks_from_db.id,
            name=tasks_from_db.name,
            description=tasks_from_db.description,
            state=tasks_from_db.state,
            user_id=tasks_from_db.user_id,
        )

    async def get_all_tasks_by_user_id(self, user_id: int) -> Sequence[Task]:
        query = (
            select(models.Task)
            .where(models.Task.user_id == user_id)
            .order_by(models.Task.created_at)
        )
        result = await self.session.execute(query)
        tasks_from_db = result.scalars().unique().all()
        if not tasks_from_db:
            return []
        return [
            Task(
                id=task.id,
                name=task.name,
                description=task.description,
                state=task.state,
                user_id=task.user_id,
            )
            for task in tasks_from_db
        ]

    async def save_task(self, task: Task) -> int:
        task_to_save = models.Task(
            name=task.name,
            description=task.description,
            state=task.state,
            user_id=task.user_id,
        )
        self.session.add(task_to_save)
        try:
            await self.session.flush((task_to_save,))
        except IntegrityError as err:
            self._parse_error(err, task)
        return task_to_save.id

    async def update_task(self, task: Task) -> int:
        task_to_save = models.Task(
            id=task.id,
            name=task.name,
            description=task.description,
            state=task.state,
        )
        await self.session.merge(task_to_save)
        try:
            await self.session.flush((task_to_save,))
        except IntegrityError as err:
            self._parse_error(err, task)
        return task_to_save.id

    async def delete_task(self, task: Task) -> int:
        query = delete(models.Task).where(models.Task.id == task.id)
        try:
            await self.session.execute(query)
        except IntegrityError as err:
            self._parse_error(err, task)
        return task.id

    def _parse_error(self, err: DBAPIError, task: Task) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_tasks":
                raise TaskAlreadyExistsError(task.id) from err
            case _:
                raise GatewayError from err

    async def commit(self) -> None:
        await self.session.commit()
