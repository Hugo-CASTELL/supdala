import json
from classes import *


if __name__ == "__main__":
    # Getting data from json file
    with open("data.json", "r") as f:
        data = json.load(f)

        students = [Student(name, ordered_preferences) for name, ordered_preferences in data["students"].items()]
        schools = [School(name, ordered_preferences, data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        f.close()

    print(students)
    print(schools)
