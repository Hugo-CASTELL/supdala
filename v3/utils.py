def remove(set, element):
    # If not present, no errors
    try:
        set.remove(element)
    except KeyError:
        pass

def deepcopy(string_list: list[str]):
    return [str(s) for s in string_list]