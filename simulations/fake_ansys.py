import json
import random

stress = round(random.uniform(0, 250), 2)

result = {
    "max_stress": stress,
    "limit": 200
}

with open("result.json", "w") as f:
    json.dump(result, f, indent=4)

print(result)
