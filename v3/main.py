import json
import time

from classes import Courtier, Courted
from utils import deepcopy
from stable_marriage_v3 import stable_marriage

if __name__ == "__main__":

    # Getting data from json file
    with open("../medium.json", "r") as f:
        data = json.load(f)

        schools_courted = {name: Courted(name, deepcopy(ordered_preferences), data["capacity"][name]) for name, ordered_preferences in data["schools"].items()}
        students_serenading = [Courtier(name, [schools_courted[name] for name in deepcopy(ordered_preferences)], 1) for name, ordered_preferences in data["students"].items()]

        students_courted = {name: Courted(name, deepcopy(ordered_preferences), 1) for name, ordered_preferences in data["students"].items()}
        schools_serenading = [Courtier(name, [students_courted[name] for name in deepcopy(ordered_preferences)], data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        # Printing context
        f.close()

    # Running the school matching algorithm and displaying results
    print("")

    print("Context:")
    print(f"Students count : {len(students_serenading)}")
    print(f"Schools count : {len(schools_serenading)}")
    print(f"Schools max capacity : {sum([capacity for name, capacity in data['capacity'].items()])}")

    scenarios = [
        ("Student serenade", lambda: stable_marriage(students_serenading, list(schools_courted.values()))),
        ("School serenade", lambda: stable_marriage(schools_serenading, list(students_courted.values())))
    ]

    for title, run_stable_marriage in scenarios:
        start_time = time.perf_counter()
        days_spent, courtiers, courted_persons = run_stable_marriage()
        end_time = time.perf_counter() - start_time

        print("")

        print(title)
        for school in courted_persons if title == "Student serenade" else courtiers:
            print(f"\t{school}")
        print(f"Spent time: {round(end_time * 1000)} ms ({end_time:.3f} s)")
        print(f"Days : {days_spent}")

        print("")
