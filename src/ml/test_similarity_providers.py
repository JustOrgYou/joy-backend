from src.ml.similarity_providers import (
    SimilarityProvider,
)

QUESTION: str = "What is the strongest muscle in the humans body?"


def test_sus_encode_question():
    encoded: list[float] = SimilarityProvider.encode_question(QUESTION)
    assert len(encoded) == 768


def test_sus_similarity():
    enc1 = SimilarityProvider.encode_question(QUESTION)
    enc2 = SimilarityProvider.encode_question("Human's body best muscle")

    similarity = SimilarityProvider.get_similarity(enc1, enc2)
    print(similarity)

    assert similarity > 0.7
