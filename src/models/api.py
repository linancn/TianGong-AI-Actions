from typing import List, Optional

from pydantic import BaseModel

from src.models.lca_models import Source
from src.models.models import (
    Document,
    DocumentMetadataFilter,
    Query,
    QueryResult,
    QueryResultNeat,
)


class UpsertRequest(BaseModel):
    documents: List[Document]


class UpsertResponse(BaseModel):
    ids: List[str]


class QueryRequest(BaseModel):
    queries: List[Query]


class QueryResponse(BaseModel):
    results: List[QueryResult]


class QueryResponseNeat(BaseModel):
    results: List[QueryResultNeat]


class DeleteRequest(BaseModel):
    ids: Optional[List[str]] = None
    filter: Optional[DocumentMetadataFilter] = None
    delete_all: Optional[bool] = False


class DeleteResponse(BaseModel):
    success: bool


class QueryLCASourceRequest(BaseModel):
    """
    Send a query to the LCA source database.
    """
    queries: str


class QueryLCASourceResponse(BaseModel):
    sources: List[Source]
