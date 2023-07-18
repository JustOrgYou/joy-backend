from pydantic import BaseModel


class Entry(BaseModel):
    pk: int
    text: str


class PostEntriesBody(BaseModel):
    entries: list[Entry]
    force_update: bool | None


class DeleteEntriesBody(BaseModel):
    ids: list[int]


class PostSimilarityBody(BaseModel):
    pk_list: list[int] | None
    threshold: float


class SimilarityAnswer(BaseModel):
    similarity_list: list[list[int]]
