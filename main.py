import requests

r = requests.get('localhost/5000/create_model',
                 {"iterations": 2, "prompt": "A simple office chair with arm rests and a back."})
print(r.status_code)
