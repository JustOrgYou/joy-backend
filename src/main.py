import dataclasses
import functools
import json
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
    PlainTextResponse,
)

from src.classes import (
    Task,
)


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
@app.post("/post/task", response_class=PlainTextResponse)
# @raise_proper_http
async def post_task(
        tasks: list[Task],
        threshold: int
):
    if len(tasks) > 0:
        return tasks[0]

    return Task.schema_json()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    uvicorn.run(app=app, host=HTTP_HOST, port=HTTP_PORT)
