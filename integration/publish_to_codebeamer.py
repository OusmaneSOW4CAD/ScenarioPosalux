import os
import json
import requests

# =====================================
# CONFIGURATION
# =====================================

BASE_URL = "https://pdm13-1-codebeamer.connexateurs.com/cb/api/v3"

TEST_SET_RUN_ID = 33898
TEST_CASE_ID = 1218

USER = os.environ["CODEBEAMER_USER"]
PASSWORD = os.environ["CODEBEAMER_PASSWORD"]

# =====================================
# LECTURE RESULTAT SIMULATION
# =====================================

with open("result.json", "r") as f:
    data = json.load(f)

stress = data["max_stress"]
limit = data["limit"]

result = "PASSED" if stress <= limit else "FAILED"

# =====================================
# PAYLOAD CODEBEAMER
# =====================================

payload = {
    "parentResultPropagation": True,
    "updateRequestModels": [
        {
            "result": result,
            "conclusion": (
                f"Simulation virtuelle ANSYS\n"
                f"Stress={stress} MPa\n"
                f"Limite={limit} MPa\n"
                f"Résultat={result}"
            ),
            "runTime": 10,
            "testCaseReference": {
                "id": TEST_CASE_ID,
                "name": "Access to Lens Cleaning Training Material",
                "type": "TrackerItemReference",
                "commonItemId": TEST_CASE_ID,
                "trackerKey": "TESTCASE",
                "trackerTypeId": 16,
                "uri": f"/item/{TEST_CASE_ID}"
            }
        }
    ]
}

# =====================================
# APPEL API
# =====================================

url = f"{BASE_URL}/testruns/{TEST_SET_RUN_ID}"

print("=" * 80)
print("URL")
print(url)

print("=" * 80)
print("PAYLOAD")
print(json.dumps(payload, indent=2))

response = requests.put(
    url,
    json=payload,
    auth=(USER, PASSWORD),
    headers={
        "accept": "application/json",
        "Content-Type": "application/json"
    },
    timeout=30
)

print("=" * 80)
print("STATUS")
print(response.status_code)

print("=" * 80)
print("HEADERS")
print(dict(response.headers))

print("=" * 80)
print("BODY")

try:
    print(json.dumps(response.json(), indent=2))
except Exception:
    print(response.text)

print("=" * 80)

# =====================================
# SI ERREUR : RECUPERER LE TEST RUN
# =====================================

if response.status_code != 200:

    print("\n")
    print("RECUPERATION DU TEST RUN")
    print("=" * 80)

    get_url = f"{BASE_URL}/items/{TEST_SET_RUN_ID}"

    r = requests.get(
        get_url,
        auth=(USER, PASSWORD),
        headers={"accept": "application/json"}
    )

    print("GET STATUS:", r.status_code)

    try:
        data = r.json()

        print("ID:", data.get("id"))
        print("TYPE:", data.get("typeName"))
        print("NAME:", data.get("name"))
        print("TRACKER:", data.get("tracker", {}).get("name"))

    except Exception:
        print(r.text)
`
