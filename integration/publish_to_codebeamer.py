import os
import json
import random
import requests

BASE_URL = "https://pdm13-1-codebeamer.connexateurs.com/cb/api/v3"

TEST_SET_RUN_ID = 33912

USER = os.environ["CODEBEAMER_USER"]
PASSWORD = os.environ["CODEBEAMER_PASSWORD"]

# Récupération du Test Set Run
response = requests.get(
    f"{BASE_URL}/items/{TEST_SET_RUN_ID}",
    auth=(USER, PASSWORD),
    headers={"accept": "application/json"}
)

response.raise_for_status()

testrun = response.json()

updates = []

# Recherche de tous les Test Cases du Test Set
for field in testrun["customFields"]:

    if field["name"] != "Test Cases":
        continue

    for row in field["values"]:

        testcase = row[0]["values"][0]

        test_case_id = testcase["id"]
        test_case_name = testcase["name"]

        # Simulation ANSYS
        stress = round(random.uniform(100, 250), 2)
        limit = 200

        result = (
            "PASSED"
            if stress <= limit
            else "FAILED"
        )

        updates.append(
            {
                "result": result,
                "conclusion": (
                    f"Simulation virtuelle\n"
                    f"Stress={stress} MPa\n"
                    f"Limit={limit} MPa"
                ),
                "runTime": 10,
                "testCaseReference": {
                    "id": test_case_id,
                    "name": test_case_name,
                    "type": "TrackerItemReference",
                    "commonItemId": test_case_id,
                    "trackerKey": "TESTCASE",
                    "trackerTypeId": 16,
                    "uri": f"/item/{test_case_id}"
                }
            }
        )

payload = {
    "parentResultPropagation": True,
    "updateRequestModels": updates
}

print(json.dumps(payload, indent=2))

response = requests.put(
    f"{BASE_URL}/testruns/{TEST_SET_RUN_ID}",
    json=payload,
    auth=(USER, PASSWORD),
    headers={
        "accept": "application/json",
        "Content-Type": "application/json"
    }
)

print("STATUS =", response.status_code)
print(response.text)
