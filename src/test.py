import json
import os

import oss2
from dotenv import load_dotenv
from xata import XataClient

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


def filter_lca_source():
    lca_source_results = xata_client.data().query(
        "source",
        {
            "columns": ["link_to_digital_file"],
            "filter": {"$exists": "link_to_digital_file"},
        },
    )
    for record in lca_source_results["records"]:
        file_key = json.loads(record["link_to_digital_file"])
        record["link_to_digital_file"] = oss_bucket.sign_url("GET", "external_docs/" + file_key[0], 120)
    return lca_source_results


filter_lca_source()
