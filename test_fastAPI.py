import requests
from fastapi import FastAPI
from dotenv import load_dotenv
import os


app = FastAPI()
load_dotenv()
URL = os.getenv('URL')


@app.get("/services")
async def get_services():

    headers = {"key": 'bot_9e7f010f-657d-4e4d-b4b8-0f5db12106ec'}
    response = requests.get(URL, headers=headers)
    services = response.json()
    return {"services": services}


@app.post("/services/{service_id}")
def read_item(payload: dict):

    headers = {"key": 'bot_9e7f010f-657d-4e4d-b4b8-0f5db12106ec'}
    response = requests.post(URL, json=payload, headers=headers).json()
    return {"service": response}
