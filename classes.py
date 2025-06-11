class School:
    def __init__(self, name, ordered_preferences, max_capacity):
        self.name = name
        self.ordered_student_preferences = ordered_preferences
        self.max_capacity = max_capacity

        self.students = []

    def is_full(self):
        return len(self.students) == self.max_capacity

    def is_not_full(self):
        return len(self.students) < self.max_capacity

    def accept_if_listed(self, student):
        if student.name in self.ordered_student_preferences:
            self.students.append(student)
            student.school = self

    def add_student(self, student) -> None:
        self.students.append(student)

    def remove_least_wanted_student(self, candidate_name) -> bool:
        index_student = self.ordered_student_preferences.index(candidate_name)
        for student_name in reversed(self.ordered_student_preferences):
            student = next((s for s in self.students if s.name == student_name), None)
            if student is not None and self.ordered_student_preferences.index(student.name) > index_student:
                self.students.remove(student)
                return True
        return False

    def replace_if_least_preferred_student_exists(self, student):
        if self.remove_least_wanted_student(student.name):
            self.accept_if_listed(student)

    def student_is_still_accepted(self, student_name) -> bool:
        return any(student.name == student_name for student in self.students)
    
    def remove_student(self, student) -> None:
        self.students.remove(student)

    def should_be_better(self) -> bool:
        return len(self.students) < self.max_capacity and len(self.ordered_student_preferences) == 0
    
    def pop_student(self, dict_students):
        return dict_students[self.ordered_student_preferences.pop(0)]

class Student:
    def __init__(self, name, ordered_preferences):
        self.name = name
        self.ordered_school_preferences = ordered_preferences
        self.school: School | None = None

    def pop_school(self, dict_schools) -> School:
        return dict_schools[self.ordered_school_preferences.pop(0)]

    def should_do_his_math_homework(self):
        return len(self.ordered_school_preferences) == 0
    
    def still_accepting(self, school: School) -> bool:
        return school.name == self.school.name
    
    def accept_or_refuse(self, school: School) -> bool:
        if self.school is None:
            self.school = school
            school.add_student(self)
            return True
        elif self.ordered_school_preferences.index(school.name) < self.ordered_school_preferences.index(self.school.name):
            self.school.remove_student(self)
            self.school = school
            school.add_student(self)
            return True
        return False