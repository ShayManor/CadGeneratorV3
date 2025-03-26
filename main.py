import requests

r = requests.post('http://127.0.0.1:5000/create_model',
                 {"iterations": 2, "prompt": "A simple office chair with arm rests and a back.", "name": "chair"})
print(r.status_code)
