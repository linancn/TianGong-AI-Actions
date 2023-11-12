from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello GPT"}


# @app.on_startup
# async def startup():
#     global datastore
#     datastore = await get_datastore()


# @app.on_shutdown
# async def shutdown_event():
#     # your shutdown code

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
