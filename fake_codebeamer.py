import json

with open("results.json") as f:
    data = json.load(f)

status = (
    "PASSED"
    if data["max_stress_mpa"] <= data["stress_limit_mpa"]
    else "FAILED"
)

report = {
    "testCase": data["test_case_run_id"],
    "status": status
}

with open("test_run_result.json", "w") as f:
    json.dump(report, f, indent=4)

print(report)
