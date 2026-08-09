def restriction(value, bottom=None, top=None, *, lst=None):
    if lst is not None and isinstance(lst, list):
        lst_str = [str(item) for item in lst]
        value_str = str(value)
        if value_str not in lst_str:
            return lst[len(lst) // 2]
    if value is None:
        return value
    if bottom is not None:
        value = max(value, bottom)
    if top is not None:
        value = min(value, top)
    return value


def to_list(param):
    if isinstance(param, str):
        return [param]
    return param if param else []
