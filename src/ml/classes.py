from pydantic import BaseModel

from src.ml.similarity_providers import (
    SimilarityProvider,
)


def process_entry(entry: "Entry") -> list[float]:
    return SimilarityProvider.encode_question(entry.text)


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
