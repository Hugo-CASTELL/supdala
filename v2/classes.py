class School:
    def __init__(self, name, ordered_preferences, max_capacity):
        self.name = name
        self.max_capacity = max_capacity

        self.ordered_student_preferences = ordered_preferences
        self.student_name_to_preference = {student_name: i for i, student_name in enumerate(ordered_preferences)}

        self._students = {} # preference -> student
        self._preference_max_accepted = -1

    def _get_preference(self, student_name: str) -> int | None:
        return self.student_name_to_preference.get(student_name)

    def add_student(self, student):
        preference = self._get_preference(student.name)
        self._students[preference] = student
        student.school = self

        if preference > self._preference_max_accepted:
            self._preference_max_accepted = preference

    def is_full(self):
        return len(self._students) == self.max_capacity

    def accept_if_listed(self, student):
        if self._get_preference(student.name) is not None:
            self.add_student(student)

    def replace_if_least_preferred_student_exists(self, student):
        preference_candidate = self._get_preference(student.name)
        if preference_candidate is not None:

            # If the candidate is less preferred than the least preferred already accepted
            if preference_candidate > self._preference_max_accepted:
                return False

            # Add the student and pop the max
            else:
                self.add_student(student)
                self.remove_student(student)
                return True
        else:
            return False

    def student_is_still_accepted(self, student_name) -> bool:
        return self._students[self._get_preference(student_name)] is not None
    
    def remove_student(self, student) -> None:
        preference = self._get_preference(student.name)
        self._students.pop(preference)

        if preference == self._preference_max_accepted:
            self._preference_max_accepted = max(list(self._students.keys())) if len(self._students) > 0 else -1

    def should_lower_its_standards(self) -> bool:
        return len(self._students) < self.max_capacity and not self.has_candidates_to_contact()

    def pop_student(self, dict_students):
        return dict_students[self.ordered_student_preferences.pop(0)]

    def get_students(self):
        return list(self._students.values())

    def has_candidates_to_contact(self):
        return len(self.ordered_student_preferences) > 0


class Student:
    def __init__(self, name, ordered_preferences):
        self.name = name
        self.school: School | None = None

        self.ordered_school_preferences = ordered_preferences
        self.school_name_to_preference = {school_name: i for i, school_name in enumerate(ordered_preferences)}

    def _get_preference(self, school_name: str) -> int | None:
        return self.school_name_to_preference.get(school_name)

    def pop_school(self, dict_schools) -> School:
        return dict_schools[self.ordered_school_preferences.pop(0)]

    def should_do_his_math_homework(self):
        return len(self.ordered_school_preferences) == 0
    
    def still_accepting(self, school: School) -> bool:
        return school.name == self.school.name
    
    def accept_or_refuse(self, school: School) -> bool:
        school_preference = self._get_preference(school.name)

        # If the student doesn't want to go to this school, refuse
        if school_preference is None:
            return False

        # If not accepted a school yet, accepts by default
        elif self.school is None:
            return True

        # Else it tests if he prefers the school between the suggested and the one he already accepted
        elif school_preference < self._get_preference(self.school.name):
            return True

        return False