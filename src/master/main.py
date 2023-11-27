import logging
import os

import httpx
import uvicorn
from fastapi import (
    FastAPI,
)

from pydantic import BaseSettings


import src.domain.similarity.classes as classes
from src.domain.similarity.classes import (
    Entry,
    PostEntriesBody,
    PostSimilarityBody,
    StatusResponse,
)
from src.master.classes import (
    PostTasksBody,
)


class MySettings(BaseSettings):
    ML_HOST: str = f"http://{os.environ['ML_HOST']}:8082"
    URL_CREATE: str = f"{ML_HOST}/entries"
    URL_ALL_ENTRIES: str = f"{ML_HOST}/all_entries"
    URL_SIMILARITY: str = f"{ML_HOST}/similarity"

    HTTP_HOST: str = "0.0.0.0"
    HTTP_PORT: int = 8081


app = FastAPI(title="Master service", version="0.1")
settings = MySettings()
print(f"Connect to ml via: {settings.ML_HOST}")


@app.post("/tasks", response_model=classes.SimilarityAnswer)
async def post_task(body: PostTasksBody):
    serialized_tasks: list[dict] = list()

    for t in body.tasks:
        e = Entry(pk=t.pk, text=t.form_representation_string())
        serialized_tasks.append(e.dict())

    async with httpx.AsyncClient() as client:
        # fmt: off
        create_body: dict = PostEntriesBody(
            entries=serialized_tasks,
            force_update=True
        ).dict()

        await client.post(settings.URL_CREATE, json=create_body)

        similarity_body: dict = PostSimilarityBody(
            pk_list=[t.pk for t in body.tasks],
            threshold=body.threshold
        ).dict()
        # fmt: on

        r: classes.SimilarityAnswer = await client.post(
            settings.URL_SIMILARITY, json=similarity_body
        )

    return r.json()


# delete all entries
@app.delete("/entries", response_model=StatusResponse)
async def delete_entries():
    async with httpx.AsyncClient() as client:
        r: StatusResponse = await client.delete(settings.URL_ALL_ENTRIES)
        return r.json()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    uvicorn.run(app=app, host=settings.HTTP_HOST, port=settings.HTTP_PORT)
