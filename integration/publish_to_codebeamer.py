import json
import os
import requests

BASE_URL = "https://pdm13-1-codebeamer.connexateurs.com/cb/api/v3"
TEST_RUN_ID = 33902

USER = os.environ["CODEBEAMER_USER"]
PASSWORD = os.environ["CODEBEAMER_PASSWORD"]

with open("result.json", "r") as f:
    data = json.load(f)

stress = data["max_stress"]
limit = data["limit"]

result = "PASSED" if stress <= limit else "FAILED"

payload = {
    "parentResultPropagation": True,
    "updateRequestModels": [
        {
            "testCaseReference": {
                "id": 1218
            },
            "result": result,
            "conclusion": (
                f"Simulation virtuelle ANSYS\n"
                f"Stress={stress} MPa\n"
                f"Limite={limit} MPa\n"
                f"Résultat={result}"
            ),
            "runTime": 10
        }
    ]
}

url = f"{BASE_URL}/testruns/{TEST_RUN_ID}"

print("URL =", url)
print("Payload =")
print(json.dumps(payload, indent=2))

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

try:
    print(json.dumps(response.json(), indent=2))
except Exception:
    print(response.text)
