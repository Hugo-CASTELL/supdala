import json

from classes import Courtier, Courted
from utils import deepcopy
from stable_marriage_v3 import stable_marriage

if __name__ == "__main__":

    # Getting data from json file
    with open("mydata.json", "r") as f:
        data = json.load(f)

        students_courted = {name: Courted(name, deepcopy(ordered_preferences), 1) for name, ordered_preferences in data["students"].items()}
        schools_serenading = [Courtier(name, [students_courted[name] for name in deepcopy(ordered_preferences)], data["capacities"][name]) for name, ordered_preferences in data["schools"].items()]

        # Printing context
        f.close()

    stable_marriage(schools_serenading, list(students_courted.values()))
