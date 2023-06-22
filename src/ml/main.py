import functools
import logging
import os
import pprint

import fastapi
import uvicorn
from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.ml.classes import Entry, process_entry, SimilarityAnswer, compare

app = FastAPI()

HTTP_HOST = os.getenv("HTTP_HOST", "0.0.0.0")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8082"))


class PostEntriesBody(BaseModel):
    entries: list[Entry]


@app.post("/entries", response_class=JSONResponse)
async def post_entries(body: PostEntriesBody):
    for e in body.entries:
        if e.pk not in processed_entries_dict:
            processed_entries_dict[e.pk] = process_entry(e)
        else:
            logging.warning(f"{e.pk} is already in dict")

    # pprint.pprint(processed_entries_dict)
    pk_list = sorted(list(processed_entries_dict.keys()))
    return {
        "pk_list": str(pk_list)
    }


class DeleteEntriesBody(BaseModel):
    ids: list[int]


@app.delete("/entries", response_class=JSONResponse)
async def delete_entries(body: DeleteEntriesBody):
    for i in body.ids:
        if i in processed_entries_dict:
            processed_entries_dict.pop(i)
        else:
            logging.error(f"PK {i} not in dict")

    return {"detail": "OK"}


@app.get("/similarity")
async def get_similarity(pk1: int, pk2: int):
    if pk1 not in processed_entries_dict or pk2 not in processed_entries_dict:
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item not found"
        )

    # pe1 = list(filter(lambda x: x.pk == pk1, processed_entries_dict))[0]
    # pe2 = list(filter(lambda x: x.pk == pk2, processed_entries_dict))[0]

    pe1 = processed_entries_dict[pk1]
    pe2 = processed_entries_dict[pk2]

    return SimilarityAnswer(
        similarity=compare(pe1, pe2)
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    processed_entries_dict: dict[int, list[float]] = dict()

    uvicorn.run(app=app, host=HTTP_HOST, port=HTTP_PORT)
