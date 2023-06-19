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
    FileResponse,
    JSONResponse,
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
@app.get("/json/{username}", response_class=JSONResponse)
@raise_proper_http
async def get_json(
    username: str,
):
    json_answer: dict = {
        "ans": f"OK (username: {username})",
    }

    return JSONResponse(json_answer)
    # return FileResponse(path=path, media_type="text/calendar")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    uvicorn.run(app=app, host=HTTP_HOST, port=HTTP_PORT)
