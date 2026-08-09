def ensure(obj, condition, func):
    if isinstance(condition, bool) and not condition:
        return func(obj)
    elif not condition(obj):
        return func(obj)
    return obj


def unpack_collection(collection):
    if isinstance(collection, (list, tuple)) and len(collection) == 1:
        return collection[0] if isinstance(collection[0], (list, tuple)) else collection
    return collection
