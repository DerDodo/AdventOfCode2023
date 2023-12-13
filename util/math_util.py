
def clamp(n):
    return max(-1, min(1, n))


def transpose(l):
    # https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
    return list(map(list, zip(*l)))
