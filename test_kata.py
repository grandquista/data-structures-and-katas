from kata import kata
from re import search


def test_kata():
    i = 1
    for j in range(200):
        sample = bin(j)[2:]
        for i in range(1, 19):
            match = search(kata(i), sample)
            if j % i == 0:
                assert match, (i, j)
            else:
                assert not match, (i, j)
