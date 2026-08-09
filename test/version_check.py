try:
    raise RuntimeError('111')
except Exception as err:
    print(err)
    print(type(err).__name__)