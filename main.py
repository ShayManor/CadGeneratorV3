import os

import requests

from src.routes.routes import create_model_2

r = requests.post('http://127.0.0.1:5000/create_model',
                  {"iterations": 3, "prompt": "A simple mug for coffee with a handle.", "name": "Mug"})
print(r.status_code)
# data = {
#     "iterations": "2",
#     "prompt": "A simple office chair with arm rests and a back.",
#     "name": "chair",
# }
# print(create_model_2(data))
