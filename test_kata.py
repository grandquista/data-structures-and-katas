from re import search

from kata import kata


def test_kata():
    """
    Test kata.
    """
    for j in range(2000):
        sample = bin(j)[2:]
        for i in range(1, 19):
            match = search(kata(i), sample)
            if j % i == 0:
                assert match, (i, j, bin(j))
            else:
                assert not match, (i, j)
