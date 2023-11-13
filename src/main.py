import datetime
import os

from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src.datastore.factory import get_datastore
from src.models.api import QueryRequest, QueryResponseNeat
from src.models.models import DocumentChunkWithScoreNeat, QueryResultNeat

load_dotenv()

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
assert BEARER_TOKEN is not None


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials


async def startup():
    global datastore
    datastore = await get_datastore()


app = FastAPI(dependencies=[Depends(validate_token)])
app.add_event_handler("startup", startup)

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
        query_response_neat = QueryResponseNeat(results=[])
        for items in results:
            query_result_neat = QueryResultNeat(results=[])
            for result in items.results:
                text = result.text
                metadata = result.metadata
                date = datetime.fromtimestamp(float(metadata.created_at))
                formatted_date = date.strftime("%Y-%m")
                source_entry = "[{}. {}. {}. {}.]({})".format(
                    metadata.source_id,
                    metadata.source,
                    metadata.author,
                    formatted_date,
                    metadata.url,
                )
                document_chunk_with_score_neat = DocumentChunkWithScoreNeat(
                    text=text,
                    source=source_entry,
                    score=result.score,
                )
                query_result_neat.results.append(document_chunk_with_score_neat)
            query_response_neat.results.append(query_result_neat)
        return query_response_neat
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


# @app.on_shutdown
# async def shutdown_event():
#     # your shutdown code

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
