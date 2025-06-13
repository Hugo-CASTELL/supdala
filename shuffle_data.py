import json
import random

# Load the data from the provided JSON string (simulated here as a variable)
with open("./data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Shuffle the preferences for each student
for student, preferences in data["students"].items():
    random.shuffle(preferences)

# Save the shuffled data
shuffled_path = "./shuffled_data.json"
with open(shuffled_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)