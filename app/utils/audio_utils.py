import requests
from utils.config import headers, API_URL

def audio_to_text(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers={"Content-Type": "audio/wav", **headers}, data=data)
    return response.json()