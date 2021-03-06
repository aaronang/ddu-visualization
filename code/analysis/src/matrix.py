from functools import reduce


def to_float(s):
    try:
        return float(s)
    except ValueError:
        return -1


def transpose(data):
    if len(data) == 0:
        return []
    return [[row[i] for row in data] for i in range(len(data[0]))]


def unique(matrix):
    return reduce(_uniq, matrix, [])


def _uniq(x, y):
    if y not in x:
        return x + [y]
    else:
        return x
