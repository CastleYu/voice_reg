MAXEDGE = 50


def report(content: str, *args: str, color: str = 'default'):
    def str_len(string):
        leng = 0
        for char in string:
            if u'\u4e00' <= char <= u'\u9fff':
                leng += 2
            else:
                leng += 1
        return leng

    if color == 'red':
        print('\033[31m', end='')
    elif color == 'green':
        print('\033[32m', end='')
    elif color == 'yellow':
        print('\033[33m', end='')
    elif color == 'blue':
        print('\033[34m', end='')
    else:
        print('\033[0m', end='')

    for i in args:
        content += i
    length = str_len(content)
    length = length if length < MAXEDGE else MAXEDGE

    print('═' * length)
    print(content)
    print('═' * length + '\033[0m')
    return 0