import json
import os

import oss2
from dotenv import load_dotenv
from xata import XataClient

from src.models.lca_models import Source

load_dotenv()

oss_access_key_id = os.getenv("OSS_ACCESS_KEY_ID")
oss_access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET")
oss_endpoint = os.getenv("OSS_ENDPOINT")
oss_bucket = os.getenv("OSS_BUCKET")

oss_auth = oss2.Auth(oss_access_key_id, oss_access_key_secret)
oss_bucket = oss2.Bucket(oss_auth, oss_endpoint, oss_bucket)

xata_api_key = os.getenv("XATA_API_KEY")
xata_database_url = os.getenv("XATA_DATABASE_URL")

xata_client = XataClient(api_key=xata_api_key, db_url=xata_database_url)


async def query_lca_source(query: str):
    results = xata_client.data().search_table("source", {"query": query})

    lca_source_results = []

    for record in results["records"]:
        for field in ["classification", "data_set_format", "short_name"]:
            if field in record and isinstance(record[field], str):
                record[field] = json.loads(record[field])
        lca_source_result = Source(**record)
        lca_source_results.append(lca_source_result)

    return lca_source_results
