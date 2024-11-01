from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.value_objects.task_state import TaskState
from src.infrastructure.db.models.base import TimedBaseModel

if TYPE_CHECKING:
    from src.infrastructure.db.models.user import User
else:
    User = "User"


class Task(TimedBaseModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    state: Mapped[TaskState] = mapped_column(default=TaskState.PENDING)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped[User] = relationship(back_populates="tasks")
