import os
import json
import requests

BASE_URL = "https://pdm13-1-codebeamer.connexateurs.com/cb/api/v3"

USER = os.environ["CODEBEAMER_USER"]
PASSWORD = os.environ["CODEBEAMER_PASSWORD"]

TEST_SET_RUN_ID = 33898

with open("results.json") as f:
    results = json.load(f)

updates = []

for item in results:

    updates.append(
        {
            "result": item["result"],
            "conclusion":
                f"Stress={item['stress']} MPa",
            "runTime": 10,
            "testCaseReference": {
                "id": item["testCaseId"],
                "name": item["testCaseName"],
                "type": "TrackerItemReference",
                "commonItemId": item["testCaseId"],
                "trackerKey": "TESTCASE",
                "trackerTypeId": 16,
                "uri": f"/item/{item['testCaseId']}"
            }
        }
    )

payload = {
    "parentResultPropagation": True,
    "updateRequestModels": updates
}

response = requests.put(
    f"{BASE_URL}/testruns/{TEST_SET_RUN_ID}",
    json=payload,
    auth=(USER, PASSWORD)
)

print(response.status_code)
print(response.text)
