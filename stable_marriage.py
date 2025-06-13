import json
from classes import *

def get_all_schools_max_capacity(schools):
    return sum([school.max_capacity for school in schools])

def get_all_students_count(schools):
    return sum([len(school.get_students()) for school in schools])

def is_queue_containing_students(students_next_queue):
    return len(students_next_queue) > 0

def is_queue_containing_schools(schools_next_queue):
    return len(schools_next_queue) > 0

def are_all_schools_not_full(schools):
    return get_all_students_count(schools) < get_all_schools_max_capacity(schools)

def school_matching(dict_students : dict[str, Student], dict_schools : dict[str, School]):
    schools = list(dict_schools.values())
    students_next_queue = list(dict_students.values())
    iterations = 0

    while is_queue_containing_students(students_next_queue):
        iterations += 1

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
                if not school.is_full():
                    school.accept_if_listed(student)

                # If the school is full, check if the student is preferred over the least preferred student
                else:
                    school.replace_if_least_preferred_student_exists(student)

            # Prepare for the next iteration
            if student.school is None and not student.should_do_his_math_homework():
                students_next_queue.append(student)

    return schools,iterations


def student_matching(dict_students: dict[str, Student], dict_schools: dict[str, School]):
    schools = list(dict_schools.values())
    schools_next_queue = list(dict_schools.values())
    iterations = 0

    while is_queue_containing_schools(schools_next_queue) and are_all_schools_not_full(schools):
        iterations += 1

        # Prepare the next queue of students
        schools_queue = schools_next_queue.copy()
        schools_next_queue.clear()

        while schools_queue:
            # Get a free school
            school = schools_queue.pop()

            for student in school.get_students():
                if not student.still_accepting(school):
                    school.remove_student(student)

            if not school.is_full() and school.has_candidates_to_contact():
                student = school.pop_student(dict_students)
                if student.accept_or_refuse(school):
                    school.add_student(student)

            # Prepare for the next iteration
            if not school.is_full() and not school.should_lower_its_standards() :
                schools_next_queue.append(school) 

    return schools,iterations

def deep_copy(list_of_str):
    return [str(item) for item in list_of_str]

def afficher(schools):
    for school in schools:
        students = school.get_students()
        print(f"\t{school.name} ({len(students)}/{school.max_capacity}): {[student.name for student in students]}")

    

if __name__ == "__main__":
    # Getting data from json file
    with open("shuffled_data.json", "r") as f:
        data = json.load(f)

        students = [Student(name, deep_copy(ordered_preferences)) for name, ordered_preferences in data["students"].items()]
        schools = [School(name, deep_copy(ordered_preferences), data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        students2 = [Student(name, deep_copy(ordered_preferences)) for name, ordered_preferences in data["students"].items()]
        schools2 = [School(name, deep_copy(ordered_preferences), data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        f.close()

    # Printing context
    print("")

    print("Context:")
    print(f"Students count : {len(students)}")
    print(f"Schools count : {len(schools)}")
    print(f"Schools max capacity : {get_all_schools_max_capacity(schools)}")
    
    # Running the school matching algorithm
    print("\nStudent Matching (last word by students iterating schools preferences) :")
    student_matching_schools, iterations = student_matching({student.name: student for student in students}, {school.name: school for school in schools})
    afficher(student_matching_schools)
    print(f"Iterations: {iterations}")
    all_students_count = get_all_students_count(student_matching_schools)
    all_school_max_cap = get_all_schools_max_capacity(student_matching_schools)
    print(f"Students matched on school capacity: {all_students_count}/{all_school_max_cap} ({all_students_count/all_school_max_cap*100}%)")

    print("\nSchool Matching (last word by schools iterating students preferences) :")
    school_matching_schools, iterations = school_matching({student.name: student for student in students2}, {school.name: school for school in schools2})
    afficher(school_matching_schools)
    print(f"Iterations: {iterations}")
    all_students_count = get_all_students_count(school_matching_schools)
    all_school_max_cap = get_all_schools_max_capacity(school_matching_schools)
    print(f"Students matched on school capacity: {all_students_count}/{all_school_max_cap} ({all_students_count/all_school_max_cap*100}%)")


    print("")


