import numpy as np

from multiprocessing import Process, Queue, Pool
from queue import Empty, Full
import os
import time
from itertools import repeat, product


def compute_single(plain: list, coord: tuple) -> bool:
    """Takes a coordinate tuple (r, c) and computes if that populant will be alive in the next tick."""

    neighbors = 0
    r, c = coord

    # print('Checking index ({}, {}) of plain that is {}x{}'.format(r, c, len(plain), len(plain[0])))

    t = r > 0
    b = r < len(plain) - 1
    l = c > 0
    rr = c < len(plain[0]) - 1 if len(plain) > 0 else False

    if t:
        neighbors += 1 if plain[r - 1][c] else 0
        if rr:
            neighbors += 1 if plain[r - 1][c + 1] else 0
        if l:
            neighbors += 1 if plain[r - 1][c - 1] else 0
    if b:
        neighbors += 1 if plain[r + 1][c] else 0
        if rr:
            neighbors += 1 if plain[r + 1][c + 1] else 0
        if l:
            neighbors += 1 if plain[r + 1][c - 1] else 0
    if l:
        neighbors += 1 if plain[r][c - 1] else 0
    if rr:
        neighbors += 1 if plain[r][c + 1] else 0
    # neighbors.append(plain[r][c])

    if neighbors > 3:
        return False
    elif neighbors == 3:
        return True
    elif neighbors == 2:
        return plain[r][c]
    else:
        return False


class LifePlain:
    """
    Represents a plain that gets simulated.
    """

    def __init__(self, height, width):
        self.board = [[False for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width
        self.area = height * width

        self.pool = Pool(os.cpu_count())  # This is the pool used for multiprocessing

        rows = range(self.height)
        cols = range(self.width)
        self.coords = list(product(rows, cols, repeat=1))

    def __del__(self):
        self.pool.close()  # It's very important to close this to release the processes

    def construct(self, r: int, c: int, blueprint: list):
        """Sets the states of the populants according to the contents of the blueprint (a 2d array of true/false values)
        Starting at the row and column specified."""

        for rr, rv in enumerate(blueprint):
            for cc, v in enumerate(rv):
                if r + rr >= self.height or c + cc >= self.width:
                    print('Blueprint too large, skipping extra coordinates')
                self.board[r + rr][c + cc] = v

    def tick(self):
        """Computes the next board state of the plain, uses multi-core processing to accelerate processing"""

        self.board = np.resize(self.pool.starmap(compute_single, product([self.board], self.coords, repeat=1)),
                               (self.height, self.width))

    def __str__(self) -> str:
        result = ''
        for r in self.board:
            for p in r:
                result += '█' if p else ' '
            result += '\033[E'
        return result
