"""
@BY: Yang LIU
@DATE: 10-09-2020
"""


def neighbors(pattern, d):
    chars = "ACGT"
    if d == 0:
        return [pattern]
    r2 = neighbors(pattern[1:], d-1)
    r = [c + r3 for r3 in r2 for c in chars if c != pattern[0]]
    if (d < len(pattern)):
        r2 = neighbors(pattern[1:], d)
        r += [pattern[0] + r3 for r3 in r2]
    return r

def neighbors2(pattern, d):
    return sum([neighbors(pattern, d2) for d2 in range(d + 1)], [])


if __name__ == "__main__":
    pattern = 'ACG'
    d = 1
    print(neighbors2(pattern, d))
