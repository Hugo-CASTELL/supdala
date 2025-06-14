from dichotomic_list import DichotomicList

class Courtier:
    def __init__(self, name, ordered_courted_to_serenade: list[object], max_marriages):
        self.name = name
        self._ordered_courted_to_serenade = ordered_courted_to_serenade

        self._marriage_promises: dict[str, object] = {}
        self._max_marriages = max_marriages

    def has_courted_persons_to_serenade(self):
        return len(self._ordered_courted_to_serenade) > 0

    def pop_next_courted_person_to_serenade(self) -> object:
        return self._ordered_courted_to_serenade.pop(0)

    def has_a_marriage_promise(self):
        return len(self._marriage_promises) == self._max_marriages

    def enjoy_and_write_marriage_promise(self, courted: object):
        self._marriage_promises[courted.name] = courted

    def drink_and_cross_out_marriage_promise(self, courted: object):
        self._marriage_promises.pop(courted.name)

    def __str__(self):
        return f"{self.name} -> {str([name for name in self._marriage_promises.keys()])}"


class Courted:
    def __init__(self, name, ordered_courtier_names, max_marriages):
        self.name = name
        self._preferences: dict[str, int] = {courtier_name: i for i, courtier_name in enumerate(ordered_courtier_names)}

        self._marriage_promises: DichotomicList = DichotomicList(max_marriages)

    def will_appear_at_the_window_for(self, courtier: Courtier) -> bool:
        return self._preferences.get(courtier.name) is not None

    def has_promised_marriage(self) -> bool:
        # As the courted is polygamous, we return the max capacity of marriages is reached
        return self._marriage_promises.is_full()

    def accept_proposal(self, courtier: Courtier) -> None:
        self._marriage_promises.insert(self._preferences[courtier.name], courtier)


    def debate(self, courtier: Courtier) -> Courtier:
        return self._marriage_promises.insert_and_pop(self._preferences[courtier.name], courtier)

    def __str__(self):
        return f"{self.name} -> {self._marriage_promises}"