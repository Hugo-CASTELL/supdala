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

    def accept(self, student):
        self.students.append(student)

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
        pass

class Student:
    def __init__(self, name, ordered_preferences):
        self.name = name
        self.ordered_school_preferences = ordered_preferences
        self.school: School | None = None

    def pop_school(self) -> School:
        return None