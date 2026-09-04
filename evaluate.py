import json

with open("result.json") as f:
    data = json.load(f)

status = (
    "PASSED"
    if data["max_stress"] <= data["limit"]
    else "FAILED"
)

print(status)
