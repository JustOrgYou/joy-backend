import logging
import httpx
import uvicorn
from fastapi import (
    FastAPI,
)
from fastapi.responses import (
    JSONResponse,
)

from src.master.classes import (
    PostTasksBody,
)
from src.ml.classes import (
    Entry,
    PostEntriesBody,
    PostSimilarityBody,
)
from pydantic import BaseSettings


class MySettings(BaseSettings):
    ML_HOST: str = "http://localhost:8082"
    URL_CREATE: str = f"{ML_HOST}/entries"
    URL_SIMILARITY: str = f"{ML_HOST}/similarity"

    HTTP_HOST: str = "0.0.0.0"
    HTTP_PORT: int = 8081


app = FastAPI(
    title="Master service",
    version="0.1"
)
settings = MySettings()


@app.post("/tasks", response_class=JSONResponse)
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

        r = await client.post(settings.URL_SIMILARITY, json=similarity_body)

    return r.json()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    uvicorn.run(app=app, host=settings.HTTP_HOST, port=settings.HTTP_PORT)
