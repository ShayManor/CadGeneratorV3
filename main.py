import os

import requests

# r = requests.post('http://127.0.0.1:5000/create_model',
#                   {"iterations": 3, "prompt": "A simple mug for coffee with a handle.", "name": "Mug"})
r = requests.post('https://cadalix-675492064948.us-central1.run.app/get_model', headers={"X-API-Key": 'shaymanor123'}, data={"name": "Mug"})
print(r.status_code)
print(r.content)
# data = {
#     "iterations": "2",
#     "prompt": "A simple office chair with arm rests and a back.",
#     "name": "chair",
# }
# print(create_model_2(data))
