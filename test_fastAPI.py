from typing import Union
import requests
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/services")
async def get_services(key: str = Header('')):
    if key is None:
        return {"error": "API key is missing"}

    url = "https://tonai.tech/api/public/v1/services"
    headers = {"key": 'Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890'}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to retrieve services"}

    services = response.json()

    return {"services": services}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
