import json

with open("data.json", "r") as f:
    data = json.load(f)

students = data["students"]
schools = data["schools"]
capacities = data["capacity"]

def school_matching(preferences_students, preferences_schools, capacities, proposer='students'):
    matches = {school: [] for school in preferences_schools.keys()}
    free_students = list(preferences_students.keys())

    print(free_students)

    while free_students:
        student = free_students.pop(0)
        student_preferences = preferences_students[student]

        print(matches)

        for school in student_preferences:
            currents_match = matches[school]
            capacity = capacities[school]
            school_preferences = preferences_schools[school]

            if len(currents_match) < capacity:
                matches[school].append(student)
                break

            worst_student = matches[school][0]
            if school_preferences.index(student) < school_preferences.index(worst_student):
                matches[school].remove(worst_student)
                matches[school].append(student)
                free_students.append(worst_student)
                    

    return matches

print(school_matching(students, schools, capacities))