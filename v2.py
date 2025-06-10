import json
from classes import *

def is_queue_containing_students(students_next_queue):
    return len(students_next_queue) > 0

def are_all_schools_not_full(schools):
    return sum([len(school.students) for school in schools]) < sum([school.max_capacity for school in schools])

def school_matching(students : list[Student], schools : list[School], proposer='students'):
    students_next_queue = students.copy()

    while is_queue_containing_students(students_next_queue) and are_all_schools_not_full(schools):
        # Prepare the next queue of students
        students_queue = students_next_queue.copy()
        students_next_queue.clear()
    
        while students_queue:
            # Get a free student
            student = students_queue.pop()

            if student.school is not None and student.school.is_full():
                # He asks if he is still accepted
                if not student.school.student_is_still_accepted(student.name):
                    student.school = None

            elif student.school is None:
                school = student.pop_school()

                # If the school has not reached its capacity, student is automatically accepted
                if school.is_not_full():
                    school.accept(student)

                # If the school is full, check if the student is preferred over the least preferred student
                else:
                    school.replace_if_least_preferred_student_exists(student)

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
