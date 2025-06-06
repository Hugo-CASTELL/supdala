class School:
    def __init__(self, name, ordered_preferences, max_capacity):
        self.name = name
        self.ordered_student_preferences = ordered_preferences
        self.max_capacity = max_capacity

        self.chosen_ones = []

    def add_student(self, student) -> None:
        self.ordered_student_preferences.append(student)

    def remove_least_wanted_student(self) -> bool:
        for student in reversed(self.ordered_student_preferences):
            if student in self.chosen_ones:
                self.chosen_ones.remove(student)
                return True
        return False

class Student:
    def __init__(self, name, ordered_preferences):
        self.name = name
        self.ordered_school_preferences = ordered_preferences