from plain import LifePlain
from file import read_rle

import os
import sys


def create_glider(r: int, c: int, plain: LifePlain) -> LifePlain:
    """Inserts a simple glider at the given row and column"""

    plain.construct(r, c, [
        [False, False, True],
        [True, False, True],
        [False, True, True]
    ])

    return plain


def create_generator(r: int, c: int, plain: LifePlain) -> LifePlain:
    """Inserts a small generator at the given row and column"""

    plain.construct(r, c, [
        [True, True, True, False, True],
        [True, False, False, False, False],
        [False, False, False, True, True],
        [False, True, True, False, True],
        [True, False, True, False, True]
    ])

    return plain


def create_gun(r: int, c: int, plain: LifePlain) -> LifePlain:
    """Creates a simple glider gun"""

    bp = [[False for _ in range(37)] for _ in range(9)]

    bp[0][24] = True

    bp[1][22] = True
    bp[1][24] = True

    bp[2][12] = True
    bp[2][13] = True
    bp[2][20] = True
    bp[2][21] = True
    bp[2][34] = True
    bp[2][35] = True

    bp[3][11] = True
    bp[3][15] = True
    bp[3][20] = True
    bp[3][21] = True
    bp[3][34] = True
    bp[3][35] = True

    bp[4][0] = True
    bp[4][1] = True
    bp[4][10] = True
    bp[4][16] = True
    bp[4][20] = True
    bp[4][21] = True

    bp[5][0] = True
    bp[5][1] = True
    bp[5][10] = True
    bp[5][14] = True
    bp[5][16] = True
    bp[5][17] = True
    bp[5][22] = True
    bp[5][24] = True

    bp[6][10] = True
    bp[6][16] = True
    bp[6][24] = True

    bp[7][11] = True
    bp[7][15] = True

    bp[8][12] = True
    bp[8][13] = True

    plain.construct(r, c, bp)

    return plain


if __name__ == '__main__':
    try:
        termsize = os.get_terminal_size()
        p = LifePlain(termsize.lines, termsize.columns)
        # create_generator(termsize.line // 2, termsize.cloumns // 2, p)
    except Exception:
        p = LifePlain(20, 20)

    try:
        blueprint = read_rle(sys.argv[1])
        r = int(input('Row: '))
        c = int(input('Column: '))
        p.construct(r, c, blueprint)
    except Exception:
        create_gun(10, 20, p)
        # create_glider(1, 1, p)

        # blueprint = read_rle('test.rle')
        # p.construct(6, 4, blueprint)

    # create_gun(10, 20, p)

    while True:
        print('\033[2J\033[H' + str(p), end='')
        p.tick()
        # input('Press enter to continue')
