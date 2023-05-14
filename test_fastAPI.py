import requests
from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/services")
async def get_services():

    url = "https://tonai.tech/api/public/v1/services"
    headers = {"key": 'Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890'}

    response = requests.get(url, headers=headers)

    services = response.json()

    return {"services": services}


@app.get("/services/{service_id}")
def read_item(service_id: str, text: str):
    url = "https://tonai.tech/api/public/v1/services"
    headers = {"key": 'Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890'}

    payload = {
        'service_id': service_id,
        'input_text': text
    }

    response = json.loads(requests.post(url, json=payload, headers=headers).text)
    return {"service": response}
