def dict_inter(dict1, dict2):
    return {key: dict1[key] for key in dict1 if key in dict2}


def dict_union(dict1, dict2):
    union_dict = dict1.copy()
    union_dict.update(dict2)
    return union_dict


def dict_diff(dict1, dict2):
    return {key: dict1[key] for key in dict1 if key not in dict2}
