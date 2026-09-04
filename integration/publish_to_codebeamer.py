import json
import requests
import os

CODEBEAMER_URL = "https://pdm13-1-codebeamer.connexateurs.com/cb/api/v3"
TEST_RUN_ID = 33902

USER = os.environ["CODEBEAMER_USER"]
PASSWORD = os.environ["CODEBEAMER_PASSWORD"]

with open("result.json") as f:
    data = json.load(f)

stress = data["max_stress"]
limit = data["limit"]

result = "PASSED" if stress <= limit else "FAILED"

payload = {
    "parentResultPropagation": True,
    "updateRequestModels": [
        {
            "conclusion": (
                f"Simulation virtuelle ANSYS\n"
                f"Stress = {stress} MPa\n"
                f"Limite = {limit} MPa"
            ),
            "result": result,
            "runTime": 10
        }
    ]
}

url = f"{CODEBEAMER_URL}/testruns/{TEST_RUN_ID}"

response = requests.put(
    url,
    json=payload,
    auth=(USER, PASSWORD),
    headers={
        "accept": "application/json",
        "Content-Type": "application/json"
    }
)

print("Status :", response.status_code)
print(response.text)
