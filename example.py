import json
from classes import *

def school_matching(students : list[Student], schools : list[School], proposer='students'):
    students_next_queue = students.copy()
    students_queue = []

    while len(students_next_queue) > 0 and sum([len(school.students) for school in schools]) < sum([school.max_capacity for school in schools]):
        # Prepare the next queue of students
        students_queue = students_next_queue.copy()
        students_next_queue.clear()
    
        while students_queue:
            # Get a free student
            student = students_queue.pop()

            # Iterate through the student's preferences
            for school_name in student.ordered_school_preferences:
                school = next((s for s in schools if s.name == school_name), None)

                # If the school has not reached its capacity, add the student
                if len(school.students) < school.max_capacity:
                    school.add_student(student)
                    student.school = school

                # If the school is full, check if the student is preferred over the least preferred student
                else: 
                    if school.remove_least_wanted_student(student.name):
                        school.add_student(student)
                        student.school = school
                
                if student.school != None:
                    break

            # Prepare for the next iteration
            if student.school is None:
                students_next_queue.append(student)

    print( {school.name: [student.name for student in school.students] for school in schools})

if __name__ == "__main__":
    # Getting data from json file
    with open("data.json", "r") as f:
        data = json.load(f)

        students = [Student(name, ordered_preferences) for name, ordered_preferences in data["students"].items()]
        schools = [School(name, ordered_preferences, data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        f.close()
    
    # Running the school matching algorithm
    school_matching(students, schools, proposer='students')
