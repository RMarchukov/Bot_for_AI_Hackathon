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
def read_item(service_id: str, text: str, optional1: str = None, optional2: str = None, optional3: str = None):
    url = "https://tonai.tech/api/public/v1/services"
    headers = {"key": 'Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890'}

    # payload = {'service_id': service_id}
    # if service_id == "":
    #     payload['input_text'] = text
    # elif service_id == "z3vvmcbnwdynx2x":
    #     payload['request'] = text
    # elif service_id == "gas59jwbg2sjtrj":
    #     payload['job_title'] = text
    #     payload['skill_set'] = optional1
    #     payload['language'] = optional2
    #     payload['additional_prompt'] = optional3
    # elif service_id == "g9g32xxqbhyjojz":
    #     payload['name'] = text
    #     payload['language'] = optional1
    #     payload['additional_prompt'] = optional2
    # elif service_id == "if6vectzvq6tr74":
    #     payload['topic'] = text
    #     payload['language'] = optional1
    #     payload['additional_prompt'] = optional2


    response = json.loads(requests.post(url, json=payload, headers=headers).text)
    return {"service": response}
