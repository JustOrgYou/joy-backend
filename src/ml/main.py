import itertools
import logging
import os

import fastapi
import uvicorn
from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.responses import (
    JSONResponse,
)

from src.ml.classes import (
    DeleteEntriesBody,
    PostEntriesBody,
    PostSimilarityBody,
    SimilarityAnswer,
    process_entry,
)
from src.ml.similarity_providers import (
    SimilarityProvider,
)

app = FastAPI()

HTTP_HOST = os.getenv("HTTP_HOST", "0.0.0.0")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8082"))


def compare(vec1: list[float], vec2: list[float]):
    return SimilarityProvider.get_similarity(vec1, vec2)


@app.post("/entries", response_class=JSONResponse)
async def post_entries(body: PostEntriesBody):
    if body.force_update is None:
        body.force_update = False

    for e in body.entries:
        if e.pk not in processed_entries_dict or body.force_update:
            processed_entries_dict[e.pk] = process_entry(e)
        else:
            logging.warning(f"{e.pk} is already in dict")

    # pprint.pprint(processed_entries_dict)
    pk_list = sorted(list(processed_entries_dict.keys()))
    return {"pk_list": str(pk_list)}


@app.delete("/entries", response_class=JSONResponse)
async def delete_entries(body: DeleteEntriesBody):
    for i in body.ids:
        if i in processed_entries_dict:
            processed_entries_dict.pop(i)
        else:
            logging.error(f"PK {i} not in dict")

    return {"detail": "OK"}


@app.post("/similarity")
async def get_similarity(body: PostSimilarityBody):
    result_list: list[list[int]] = list()

    pk_list = body.pk_list
    if pk_list is None:
        pk_list = list(processed_entries_dict.keys())

    for pk1 in pk_list:
        if pk1 not in processed_entries_dict:
            raise HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"Item not found: {pk1}",
            )

    # Example: [(1, 2), (1, 3), (2, 3)]
    possible_similar: list[list[int]] = list(itertools.combinations(pk_list, 2))

    for pk1, pk2 in possible_similar:
        pe1 = processed_entries_dict[pk1]
        pe2 = processed_entries_dict[pk2]

        similarity: float = compare(pe1, pe2)

        logging.info(f"{pk1, pk2}: {similarity}, {body.threshold}")

        if similarity >= body.threshold:
            result_list.append([pk1, pk2])

    return SimilarityAnswer(similarity_list=result_list)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    processed_entries_dict: dict[int, list[float]] = dict()

    uvicorn.run(app=app, host=HTTP_HOST, port=HTTP_PORT)
