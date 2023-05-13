from typing import Union
import requests
from fastapi import FastAPI, Header
import json

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


# @app.get("/services/{name}")
# async def get_service(name: str):
#     if name is None:
#         return {"error": "API key is missing"}
#
#     url = "https://tonai.tech/api/public/v1/services"
#     headers = {"key": 'Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890'}
#
#     response = requests.get(url, headers=headers)
#
#     if response.status_code != 200:
#         return {"error": "Failed to retrieve services"}
#
#     name = response.json()
#
#     return {"name": name}


@app.get("/services/{name}")
async def get_service(name: str):
    if name is None:
        return {"error": "API key is missing"}

    url = "https://dev.tonai.tech/api/public/v1/services"
    payload = {
        'service_id': "qdfmo6h8dn62wyx",
        'input_text': 'Ask some question'
    }
    headers = {"key": 'Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890'}

    response = json.loads(requests.post(url, json=payload, headers=headers).text)
    print(response)
    return response
