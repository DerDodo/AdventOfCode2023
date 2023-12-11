
def clamp(n):
    return max(-1, min(1, n))


def transpose(l1):
    # https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
    l2 = list(map(list, zip(*l1)))
    return l2
