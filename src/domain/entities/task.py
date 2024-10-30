from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: int
    name: str
    description: str
    deadline: datetime
