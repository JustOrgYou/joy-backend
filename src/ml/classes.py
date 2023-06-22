import dataclasses

from pydantic import BaseModel

from src.ml.similarity_providers import SimilarityProvider


# Used for API Validation & Serialization
class Entry(BaseModel):
    pk: int
    text: str


@dataclasses.dataclass
class ProcessedEntry:
    pk: int
    vector: list[float]


def compare(vec1: list[float], vec2: list[float]):
    return SimilarityProvider.get_similarity(vec1, vec2)


class SimilarityAnswer(BaseModel):
    similarity: float


def process_entry(entry: Entry) -> list[float]:
    return SimilarityProvider.encode_question(entry.text)
