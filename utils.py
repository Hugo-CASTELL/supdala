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

def deep_copy(list_of_str):
    return [str(item) for item in list_of_str]

def afficher(title, schools, iterations):
    print(f"\n{title}:")
    for school in schools:
        students = school.get_students()
        print(f"\t{school.name} ({len(students)}/{school.max_capacity}): {[student.name for student in students]}")
    print(f"Iterations: {iterations}")
    all_students_count = get_all_students_count(schools)
    all_school_max_cap = get_all_schools_max_capacity(schools)
    print(f"Students matched on school capacity: {all_students_count}/{all_school_max_cap} ({all_students_count/all_school_max_cap*100}%)")