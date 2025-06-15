from typing import Any

from utils import *
from classes import Courtier, Courted


def serenade(courtier: Courtier, courted: Courted, tomorrow_queue: set[Courtier], courted_single_from_rumours: set[Courted]):
    # If the courted person doesn't want of the courtier, the person doesn't even show to the window and the courtier gets a refusal
    if not courted.will_appear_at_the_window_for(courtier):
        return

    # Else the serenade starts
    else:
        # Either, the courted person has not already promised marriage and accept by default
        if not courted.has_promised_marriage():
            courted.accept_proposal(courtier)
            courtier.enjoy_and_write_marriage_promise(courted)

        # Or the courted person has already promised marriage to someone else and compare
        else:
            # The courted person debates and choose which proposal to refuse
            refused_courtier = courted.debate(courtier)

            # If our current courtier won
            if refused_courtier != courtier :
                courtier.enjoy_and_write_marriage_promise(courted)
                # The refused courtier will receive a carrier pigeon informing the cancellation of the marriage
                refused_courtier.drink_and_cross_out_marriage_promise(courted)
                if refused_courtier.has_courted_persons_to_serenade():
                    # The refused courtier will need to search love again tomorrow if there are other courted to serenade
                    tomorrow_queue.add(refused_courtier)

            # The refused courtier was drunk at the bar and let a rumour grow in the village
            # about this courted person has found love (between some bad words of course...)
            remove(courted_single_from_rumours, courted)

def stable_marriage(courtiers: list[Courtier], courted_persons: list[Courted]) -> tuple[
    int | Any, list[Courtier], list[Courted]]:
    # Initialize a queue as a set so no doubles can be present
    day = 0
    tomorrow_queue: set[Courtier] = set(courtiers.copy())

    # Rumour grows fast in the village about who is still single or not
    courted_single_from_rumours = set(courted_persons.copy())

    # While there are courtiers with courted on their list and courted persons are not all already married, we continue to find stability
    while tomorrow_queue and courted_single_from_rumours:
        # A new day starts
        day += 1
        today_queue = tomorrow_queue.copy()
        tomorrow_queue.clear()

        # Every courtier that doesn't have a marriage promise will serenade today
        while today_queue:

            # Get the next courtier
            courtier = today_queue.pop()

            # Pop the most preferred courted still on his list
            courted = courtier.pop_next_courted_person_to_serenade()

            # The courtier serenades the courted
            serenade(courtier, courted, tomorrow_queue, courted_single_from_rumours)

            # If the courtier didn't succeed and the courtier still have courted on his list
            if not courtier.has_a_marriage_promise() and courtier.has_courted_persons_to_serenade():
                # He will try serenading somebody else tomorrow
                tomorrow_queue.add(courtier)

    return day, courtiers, courted_persons