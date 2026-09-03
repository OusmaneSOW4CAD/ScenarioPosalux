import json

with open("results.json") as f:
    data = json.load(f)

status = (
    "PASSED"
    if data["max_stress_mpa"] <= data["stress_limit_mpa"]
    else "FAILED"
)

print(f"Test {data['test_case_run_id']} : {status}")
