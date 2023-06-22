from sentence_transformers import (
    SentenceTransformer,
)
from sklearn.metrics.pairwise import (
    cosine_similarity,
)


class SimilarityProvider:
    model = SentenceTransformer("bert-base-nli-mean-tokens")

    @classmethod
    def encode_question(cls, question: str) -> list[float]:
        return cls.model.encode(question).tolist()

    @staticmethod
    def get_similarity(vec1: list[float], vec2: list[float]) -> float:
        return cosine_similarity([vec1], [vec2])[0][0]
