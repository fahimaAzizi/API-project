import requests

BASE ="http://127.0.0.1:5000"
requests = requests.get(BASE+"HELLLOWOLD")
print(requests.json())