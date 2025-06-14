def is_any_courted_not_married(courted_persons):
    for courted in courted_persons:
        if not courted.has_promised_marriage():
            return True
    return False

def deepcopy(string_list: list[str]):
    return [str(s) for s in string_list]