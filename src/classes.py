import datetime

from pydantic import BaseModel

# import pydantic.dataclasses


# @pydantic.dataclasses.dataclass
class Task(BaseModel):
    title: str
    body: str

    children: list["Task"] | None

    priority: int | None  # Option[Unsigned Integer]
    keyword: str
    tags: list[str]

    scheduled: datetime.datetime | None
    deadline: datetime.datetime | None
    properties: list[str]


# @dataclasses.dataclass
class Notebook(BaseModel):
    tasks: list[Task]
    keywords: list[str]
