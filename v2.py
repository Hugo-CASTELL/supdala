import json
from classes import *

def is_queue_containing_students(students_next_queue):
    return len(students_next_queue) > 0

def is_queue_containing_schools(schools_next_queue):
    return len(schools_next_queue) > 0

def are_all_schools_not_full(schools):
    return sum([len(school.students) for school in schools]) < sum([school.max_capacity for school in schools])

def school_matching(dict_students : dict[str, Student], dict_schools : dict[str, School], proposer='students'):
    schools = list(dict_schools.values())
    students_next_queue = list(dict_students.values())

    while is_queue_containing_students(students_next_queue):
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
                school = student.pop_school(dict_schools)

                # If the school has not reached its capacity, student is accepted if ranked in preferences
                if school.is_not_full():
                    school.accept_if_listed(student)

                # If the school is full, check if the student is preferred over the least preferred student
                else:
                    school.replace_if_least_preferred_student_exists(student)

            # Prepare for the next iteration
            if not student.should_do_his_math_homework() and student.school is None:
                students_next_queue.append(student)

    print( {school.name: [student.name for student in school.students] for school in schools})


def student_matching(dict_students: dict[str, Student], dict_schools: dict[str, School], proposer='schools'):
    schools = list(dict_schools.values())
    schools_next_queue = list(dict_schools.values())

    while is_queue_containing_schools(schools_next_queue) and are_all_schools_not_full(schools):
        # Prepare the next queue of students
        schools_queue = schools_next_queue.copy()
        schools_next_queue.clear()

        while schools_queue:
            # Get a free school
            school = schools_queue.pop()

            for student in school.students:
                if not student.still_accepting(school):
                    school.remove_student(student)

            if not school.is_full():
                student = school.pop_student(dict_students)
                student.accept_or_refuse(school)

            # Prepare for the next iteration
            if not school.should_be_better():
                schools_next_queue.append(school) 

    print({school.name: [student.name for student in school.students] for school in schools})

def deep_copy(list_of_str):
    return [str(item) for item in list_of_str]

if __name__ == "__main__":
    # Getting data from json file
    with open("data.json", "r") as f:
        data = json.load(f)

        students = [Student(name, deep_copy(ordered_preferences)) for name, ordered_preferences in data["students"].items()]
        schools = [School(name, deep_copy(ordered_preferences), data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        students2 = [Student(name, deep_copy(ordered_preferences)) for name, ordered_preferences in data["students"].items()]
        schools2 = [School(name, deep_copy(ordered_preferences), data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        f.close()
    
    # Running the school matching algorithm
    print("Student Matching:")
    student_matching({student.name: student for student in students}, {school.name: school for school in schools}, proposer='schools')
    print("School Matching:")
    school_matching({student.name: student for student in students2}, {school.name: school for school in schools2}, proposer='students')
