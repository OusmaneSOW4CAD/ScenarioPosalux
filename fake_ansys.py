import json
import random

stress = random.uniform(150, 250)

result = {
    "test_case_run_id": 12345,
    "max_stress_mpa": stress,
    "stress_limit_mpa": 200
}

with open("results.json", "w") as f:
    json.dump(result, f, indent=2)
