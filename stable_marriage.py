import json
from classes import *
from utils import *

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

    return schools, iterations

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

    return schools, iterations

if __name__ == "__main__":
    # Getting data from json file
    with open("shuffled_data.json", "r") as f:
        data = json.load(f)

        students = [Student(name, deep_copy(ordered_preferences)) for name, ordered_preferences in data["students"].items()]
        schools = [School(name, deep_copy(ordered_preferences), data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

        students2 = [Student(name, deep_copy(ordered_preferences)) for name, ordered_preferences in data["students"].items()]
        schools2 = [School(name, deep_copy(ordered_preferences), data["capacity"][name]) for name, ordered_preferences in data["schools"].items()]

    # Printing context
        f.close()
    
    # Running the school matching algorithm
    student_matching_schools, iterations_student_matching = student_matching({student.name: student for student in students}, {school.name: school for school in schools})
    school_matching_schools, iterations_school_matching = school_matching({student.name: student for student in students2}, {school.name: school for school in schools2})

    # Displaying results
    print("")

    print("Context:")
    print(f"Students count : {len(students)}")
    print(f"Schools count : {len(schools)}")
    print(f"Schools max capacity : {get_all_schools_max_capacity(schools)}")

    afficher("Student Matching (last word by students iterating schools preferences)", student_matching_schools, iterations_student_matching)
    afficher("School Matching (last word by schools iterating students preferences)", school_matching_schools, iterations_school_matching)

    print("")


