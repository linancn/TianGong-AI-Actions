import os

from dotenv import load_dotenv
from requests import request

load_dotenv()

xata_api_key = os.getenv("XATA_API_KEY")
xata_url = os.getenv("XATA_URL")

headers = {
    "Authorization": f"Bearer {xata_api_key}",
    "Content-Type": "application/json",
}
resp = request("GET", xata_url, headers=headers)

print(resp.json())
