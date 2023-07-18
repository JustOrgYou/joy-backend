import datetime

from pydantic import BaseModel

from src.domain.similarity.classes import (
    SimilarityAnswer,
)


# @pydantic.dataclasses.dataclass
class Task(BaseModel):
    pk: int
    title: str
    body: str

    children: list["Task"] | None

    priority: int | None  # Option[Unsigned Integer]
    keyword: str | None
    tags: list[str] | None

    scheduled: datetime.datetime | None
    deadline: datetime.datetime | None

    def form_representation_string(self) -> str:
        return f"{self.title}, {self.body}"


# @dataclasses.dataclass
class Notebook(BaseModel):
    tasks: list[Task]
    keywords: list[str]


class PostTasksBody(BaseModel):
    tasks: list[Task]
    threshold: float
    # force_update: bool


class PostTasksResponse(SimilarityAnswer):
    pass
