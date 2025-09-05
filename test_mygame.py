def test_rotate_cw90():
    map = [[1,2,3],
           [4,5,6],
           [7,8,9]]

    m = list(zip(*map[::-1]))
    assert m[0] == (7,4,1)
    assert m[1] == (8,5,2)
    assert m[2] == (9,6,3)


def test_rotate_ccw90():
    map = [[1,2,3],[4,5,6],[7,8,9]]

    m = list(zip(*map))[::-1]
    assert m[0] == (3,6,9)
    assert m[1] == (2,5,8)
    assert m[2] == (1,4,7)