import heapq

class School:
    def __init__(self, name, ordered_preferences, max_capacity):
        self.name = name
        self.max_capacity = max_capacity

        self.ordered_student_preferences = ordered_preferences
        self.student_name_to_preference = {student_name: i for i, student_name in enumerate(ordered_preferences)}

        self.students = {} # priority -> student

    def _get_priority(self, student_name: str) -> int:
        return self.student_name_to_preference[student_name]

    def _add_student(self, student):
        priority = self._get_priority(student.name)
        self.students[priority] = student
        student.school = self

    def is_full(self):
        return len(self.students) == self.max_capacity

    def accept_if_listed(self, student):
        if self.student_name_to_preference[student] is not None:
            self._add_student(student)

    def replace_if_least_preferred_student_exists(self, student):
        index_candidate = self.student_name_to_preference[student.name]
        index_max = max(self.students.keys())

        # If the candidate is less preferred than the least preferred already accepted
        if index_candidate > index_max:
            return False

        # Add the student and pop the max
        else:
            self._add_student(student)
            self.students.pop(index_max)
            return True

    def student_is_still_accepted(self, student_name) -> bool:
        return self.students[self._get_priority(student_name)] is not None
    
    def remove_student(self, student) -> None:
        self.students.pop(self._get_priority(student.name))

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
        # If not accepted a school yet, accepts by default
        if self.school is None:
            return True

        # Else it tests if he prefers the school between the suggested and the one he already accepted
        elif self.ordered_school_preferences.index(school.name) < self.ordered_school_preferences.index(self.school.name):
            return True

        return False