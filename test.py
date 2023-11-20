import os

import oss2
from dotenv import load_dotenv
from requests import request

load_dotenv()

oss_access_key_id = os.getenv("OSS_ACCESS_KEY_ID")
oss_access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET")
oss_endpoint = os.getenv("OSS_ENDPOINT")
oss_bucket = os.getenv("OSS_BUCKET")

oss_auth = oss2.Auth(oss_access_key_id, oss_access_key_secret)
oss_bucket = oss2.Bucket(oss_auth, oss_endpoint, oss_bucket)

xata_api_key = os.getenv("XATA_API_KEY")
xata_url = os.getenv("XATA_URL")

headers = {
    "Authorization": f"Bearer {xata_api_key}",
    "Content-Type": "application/json",
}
resp = request("GET", xata_url, headers=headers)

print(resp.json())
