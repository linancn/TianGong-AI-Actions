import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src.datastore.factory import get_datastore
from src.lcadata.lca_query import query_lca_source
from src.models.api import (
    QueryLCASourceRequest,
    QueryLCASourceResponse,
    QueryRequest,
    QueryResponseNeat,
)

load_dotenv()

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
assert BEARER_TOKEN is not None


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials


@asynccontextmanager
async def lifespan(app: FastAPI):
    global datastore
    datastore = await get_datastore()

    yield
    datastore = None


app = FastAPI(dependencies=[Depends(validate_token)], lifespan=lifespan)

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello GPT"}


@app.post(
    "/query",
    response_model=QueryResponseNeat,
)
async def query_main(
    request: QueryRequest = Body(...),
):
    try:
        results = await datastore.query(
            request.queries,
        )
        return QueryResponseNeat(results=results)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post(
    "/lca-source-query",
    response_model=QueryLCASourceResponse,
)
async def query_source(
    request: QueryLCASourceRequest = Body(...),
):
    try:
        results = await query_lca_source(request.queries)
        return QueryLCASourceResponse(sources=results)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
