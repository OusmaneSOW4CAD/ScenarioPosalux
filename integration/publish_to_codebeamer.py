import json
import requests

CODEBEAMER_URL = "https://pdm13-1-codebeamer.connexateurs.com/"
USER = "user_posalux"
PASSWORD = "5nZ0i6SzyZgVbutlonger"

TEST_RUN_ID = 33902
TEST_CASE_RUN_ID = 1218

with open("result.json") as f:
    data = json.load(f)

status = (
    "PASSED"
    if data["max_stress"] <= data["limit"]
    else "FAILED"
)

payload = {
    str(TEST_CASE_RUN_ID): {
        "success": status,
        "conclusion":
            f"Stress={data['max_stress']} MPa "
            f"Limit={data['limit']} MPa"
    }
}

url = (
    f"{CODEBEAMER_URL}"
    f"/rest/testmanagement/testrun/"
    f"{TEST_RUN_ID}/result"
)

response = requests.put(
    url,
    json=payload,
    auth=(USER, PASSWORD)
)

print(response.status_code)
print("Response :", response.text)
