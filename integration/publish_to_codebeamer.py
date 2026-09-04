import os
import json
import requests

# ==================================================
# CONFIGURATION
# ==================================================

BASE_URL = "https://pdm13-1-codebeamer.connexateurs.com/cb/api/v3"

TEST_SET_RUN_ID = 33898
TEST_CASE_ID = 1218
TEST_CASE_ID = 1216

USER = os.environ["CODEBEAMER_USER"]
PASSWORD = os.environ["CODEBEAMER_PASSWORD"]

# ==================================================
# LECTURE RESULTAT SIMULATION
# ==================================================

with open("result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

stress = data["max_stress"]
limit = data["limit"]

result = "PASSED" if stress <= limit else "FAILED"

# ==================================================
# PAYLOAD
# ==================================================

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

# ==================================================
# APPEL API CODEBEAMER
# ==================================================

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
print("RESPONSE")

try:
    print(json.dumps(response.json(), indent=2))
except Exception:
    print(response.text)

# ==================================================
# DIAGNOSTIC EN CAS D'ERREUR
# ==================================================

if response.status_code != 200:

    print("\n")
    print("=" * 80)
    print("DIAGNOSTIC TEST RUN")
    print("=" * 80)

    diagnostic_url = f"{BASE_URL}/items/{TEST_SET_RUN_ID}"

    diagnostic_response = requests.get(
        diagnostic_url,
        auth=(USER, PASSWORD),
        headers={
            "accept": "application/json"
        },
        timeout=30
    )

    print("Diagnostic status :", diagnostic_response.status_code)

    try:
        diagnostic_data = diagnostic_response.json()

        print("ID :", diagnostic_data.get("id"))
        print("Nom :", diagnostic_data.get("name"))
        print("Type :", diagnostic_data.get("typeName"))

        if "tracker" in diagnostic_data:
            print(
                "Tracker :",
                diagnostic_data["tracker"].get("name")
            )

    except Exception:
        print(diagnostic_response.text)
