import os

from src.datastore.datastore import DataStore


async def get_datastore() -> DataStore:
    datastore = os.environ.get("DATASTORE")
    assert datastore is not None

    match datastore:
        case "pinecone":
            from src.datastore.providers.pinecone_datastore import PineconeDataStore
        case _:
            raise ValueError(
                f"Unsupported vector database: {datastore}. "
                f"Try one of the following: pinecone"
            )
