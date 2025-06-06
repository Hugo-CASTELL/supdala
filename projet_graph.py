import json

with open("data.json", "r") as f:
    data = json.load(f)

students = data["students"]
schools = data["schools"]
capacities = data["capacity"]

def school_matching(preferences_students, preferences_schools, capacities, proposer='students'):
    matches = {school: [] for school in preferences_schools.keys()}
    free_students = list(preferences_students.keys())

    while free_students:

        print(matches)

        # Get a free student
        student = free_students.pop(0)

        # Get the student's preferences
        student_preferences = preferences_students[student]

        # Iterate through the student's preferences
        for school in student_preferences:
            currents_match = matches[school]
            capacity = capacities[school]
            school_preferences = preferences_schools[school]

            # If the school has not reached its capacity, add the student
            if len(currents_match) < capacity:
                matches[school].append(student)
                break
            
            # If the school is full, check if the student is preferred over the worst student
            worst_student = student
            for student in currents_match:
                if school_preferences.index(student) > school_preferences.index(worst_student):
                    worst_student = student
                           
            if school_preferences.index(student) < school_preferences.index(worst_student):
                matches[school].remove(worst_student)
                matches[school].append(student)
                free_students.append(worst_student)
                break
            
    return matches

print(school_matching(students, schools, capacities))