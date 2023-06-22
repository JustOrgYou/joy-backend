import functools
import logging
import os

import fastapi
import uvicorn
from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.responses import (
    PlainTextResponse, JSONResponse
)

from src.master.classes import (
    Task,
)
import httpx
from src.ml.classes import Entry

ML_HOST = "http://localhost:8082"
URL_CREATE = f"{ML_HOST}/entries"
URL_SIMILARITY = f"{ML_HOST}/similarity"


app = FastAPI()

HTTP_HOST = os.getenv("HTTP_HOST", "0.0.0.0")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8081"))


def raise_proper_http(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
            ) from e

        return result

    return wrapper


# pylint: disable=too-many-arguments
@app.post("/tasks", response_class=JSONResponse)
# @raise_proper_http
async def post_task(
        tasks: list[Task],
        # threshold: int
):

    serialized_tasks: list[dict] = list()

    for t in tasks:
        e = Entry(
            pk=t.pk, text=t.form_representation_string()
        )
        serialized_tasks.append(e.dict())

    create_body = {
        "entries": serialized_tasks
    }

    client = httpx.AsyncClient()
    r = await client.post(URL_CREATE, json=create_body)

    print(r)
    return {"detail": "OK"}


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    uvicorn.run(app=app, host=HTTP_HOST, port=HTTP_PORT)
