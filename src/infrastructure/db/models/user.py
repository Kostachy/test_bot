from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import TimedBaseModel

if TYPE_CHECKING:
    from src.infrastructure.db.models.task import Task
else:
    Task = "Task"


class User(TimedBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    login: Mapped[str] = mapped_column(unique=True)

    tasks: Mapped[list[Task]] = relationship(back_populates="user")
