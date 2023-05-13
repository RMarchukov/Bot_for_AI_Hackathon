import requests
import json

API_KEY = 'Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890'

url = "https://tonai.tech/api/public/v1/services"
headers = {"key": API_KEY}

response = json.loads(requests.get(url, headers=headers).text)
for service in response['services']:
    print(service['name'])

payload = {
    'service_id': "qdfmo6h8dn62wyx",
    'input_text': 'Ask some question'
}
headers = {"key": "Smoove_ff5acd56-d794-44ae-ad87-9a9b02705890"}
response = json.loads(requests.post(url, json=payload, headers=headers).text)
print(response)
