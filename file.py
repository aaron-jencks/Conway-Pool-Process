import re
import os
import time
import sys
import operator

default_rle = """
x = 5, y = -2
24bo11b$22bobo11b$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o14b$2o8b
o3bob2o4bobo11b$10bo5bo7bo11b$11bo3bo20b$12b2o!
"""

born = re.compile(r"^b(\d+)")
surv = re.compile(r"^s(\d+)")
rle_header = re.compile(r"^x\s*=\s*(\d+),?\s*y\s*=\s*(\d+)")


def rle_decode(text):
    return re.sub(r'(\d+)([^\d])', lambda m: m.group(2) * int(m.group(1)), text)


def encode(text):
    return re.sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1), text)


def read_rle(path: str):
    """Reads an RLE file and returns a 2D blueprint of its contents."""

    with open(path) as fp:
        raw = fp.read()

        rle = "\n".join(l for l in raw.splitlines() if not l.startswith("#") and l not in ("", " "))

        lines = rle.splitlines()
        m = rle_header.match(lines[0])

        if m is not None:
            rle = "\n".join(lines[1:])
            root = [int(x) for x in m.groups()]

        inp = rle_decode(rle)

        new = [[]]

        y = 0

        for c in inp:
            if c == "!":
                return new

            if c == "$":
                y += 1
                new.append([])
                continue

            if c not in ("o, b"):
                continue

            new[y].append(c == "o")

        return new

# class GolTable(object):
#     rle_header = re.compile(r"^x\s*=\s*(\d+),?\s*y\s*=\s*(\d+)")
#
#     def __init__(self, rule="b3/s23", char=[".", "+", "@", "P", "~", "#"]): # LifeHistory-ready charmap.
#         self.coords = {}
#         self.bounds = [None, None, None, None]  # top, left, bottom, right
#         self.max_bounds = self.bounds
#
#         # Display setup
#         self.char = char
#         self.no_char = char[0]
#         self.unknown_char = "?"
#
#         self.rulestring = rule
#
#         if type(rule) is str:
#             b = set()
#             s = set()
#
#             rset = rule.split("/")
#
#             for a in rset:
#                 if born.match(a) is not None:
#                     for x in a[1:]:
#                         b.add(int(x))
#
#                 elif surv.match(a) is not None:
#                     for x in a[1:]:
#                         s.add(int(x))
#
#             self.rules = {
#                 "born": b,
#                 "surv": s,
#             }
#
#         else:
#             self.rules = dict(rules)
#
#     def set_cell(self, x, y, state):
#         if state == 0:
#             if (x, y) in self.coords:
#                 del self.coords[(x, y)]
#                 self.get_bounds()
#
#                 return True
#
#             return False
#
#         else:
#             if (x, y) in self.coords and self.coords[(x, y)] == state:
#                 return False
#
#             self.coords[(x, y)] = state
#
#             self.get_bounds()
#
#             return True
#
#     def get_cell(self, x, y):
#         if (x, y) in self.coords:
#             return self.coords[(x, y)]
#
#         return 0
#
#     def update_bounds(self, top, left, bottom, right):
#         self.bounds = [top, left, bottom, right]
#
#     def _bound(self, c):
#         x = c[0]
#         y = c[1]
#
#         if self.bounds[1] is None or x <= self.bounds[1]:
#             self.bounds[1] = x
#
#         if self.bounds[3] is None or x > self.bounds[3]:
#             self.bounds[3] = x
#
#         if self.bounds[0] is None or y <= self.bounds[0]:
#             self.bounds[0] = y
#
#         if self.bounds[2] is None or y > self.bounds[2]:
#             self.bounds[2] = y
#
#     def _max_bound(self, c):
#         x = c[0]
#         y = c[1]
#
#         if self.max_bounds[1] is None or x <= self.max_bounds[1]:
#             self.max_bounds[1] = x
#
#         if self.max_bounds[3] is None or x > self.max_bounds[3]:
#             self.max_bounds[3] = x
#
#         if self.max_bounds[0] is None or y <= self.max_bounds[0]:
#             self.max_bounds[0] = y
#
#         if self.max_bounds[2] is None or y > self.max_bounds[2]:
#             self.max_bounds[2] = y
#
#     def get_bounds(self, bias=0):
#         self.bounds = [None, None, None, None]
#
#         for c, s in self.coords.items():
#             if s > bias:
#                 self._bound(c)
#                 self._max_bound(c)
#
#     def copy(self, other, rules=False):
#         other.bounds = self.bounds
#         other.coords = self.coords
#
#         if rules:
#             other.rules = self.rules
#
#     def step(self, b=None):
#         if self.population == 0:
#             return False
#
#         if not b:
#             b = self.bounds
#
#         self.get_bounds()
#         other = GolTable()
#
#         for y in xrange(b[0] - 1, b[2] + 2):
#             for x in xrange(b[1] - 1, b[3] + 2):
#                 self._step_cell(x, y, other)
#
#         other.copy(self)
#         del other
#
#         return True
#
#     def neighbors(self, x, y):
#         r = 0
#
#         surrounding = [map(operator.add, (x, y), nc) for nc in neighbors]
#         assert len(surrounding) == 8
#
#         for s in surrounding:
#             r += self.get_cell(*s)
#
#         return r
#
#     def _step_cell(self, x, y, other=None):
#         n = self.neighbors(x, y)
#
#         if not other:
#             other = self
#
#         if n in self.rules["born"] and self.get_cell(x, y) == 0:
#             if type(self.rules["born"]) in (set, list, tuple):
#                 other.set_cell(x, y, 1)
#
#             else:
#                 other.set_cell(x, y, self.rules["born"][n])
#
#         elif n in self.rules["surv"] and self.get_cell(x, y) == 1:
#             other.set_cell(x, y, 1)
#
#     def to_rle(self):
#         out = ""
#
#         for y in xrange(b[0], b[2] + 1):
#             for x in xrange(b[1], b[3] + 1):
#                 out += self.char[self.get_coords[(x, y)]]
#
#             out += "\n"
#
#         return rle_encode(out)
#
#     @classmethod
#     def from_rle(cls, rle, rule="b3/s23", char=[".", "+", "@", "P", "~", ";"]):
#         inp = rle_decode(rle)
#
#         new = cls(rule, char)
#
#         x = 0
#         y = 0
#
#         for c in inp:
#             if c == "\n":
#                 y += 1
#                 continue
#
#             new.set_cell(x, y, char.index(c))
#
#             x += 1
#
#         return new
#
#     @classmethod
#     def from_rle_standard(cls, rle, rule="b3/s23", char=[".", "+", "@", "P", "~", ";"]):
#         rle = "\n".join(l for l in rle.splitlines() if not l.startswith("#") and l not in ("", " "))
#         root = [0, 0]
#
#         lines = rle.splitlines()
#         m = cls.rle_header.match(lines[0])
#
#         if m is not None:
#             rle = "\n".join(lines[1:])
#             root = [int(x) for x in m.groups()]
#
#         inp = rle_decode(rle)
#
#         new = cls(rule, char)
#
#         x = root[0]
#         y = root[1]
#
#         for c in inp:
#             if c == "!":
#                 return new
#
#             if c == "$":
#                 y += 1
#                 x = root[0]
#                 continue
#
#             if c not in ("o, b"):
#                 continue
#
#             new.set_cell(x, y, (1 if c == "o" else 0))
#
#             if c in ("o", "b"):
#                 x += 1
#
#         return new
#
#     def display(self, b=None):
#         disp = ""
#
#         self.get_bounds()
#
#         if not b:
#             b = self.bounds
#
#         for y in xrange(b[0], b[2] + 1):
#             for x in xrange(b[1], b[3] + 1):
#                 if (x, y) in self.coords:
#                     try:
#                         disp += self.char[self.coords[(x, y)]]
#
#                     except IndexError:
#                         disp += self.unknown_char
#
#                 else:
#                     disp += self.no_char
#
#             disp += "\n"
#
#         return disp
#
#     def _print(self, b=None):
#         print self.display(b)
#
#     def population(self, bias=0):
#         return len([x for x in self.coords.values() if x > bias])
#
# if __name__ == "__main__": # test
#     try:
#         t = GolTable.from_rle_standard(open(sys.argv[1]).read())
#
#     except IndexError:
#         t = GolTable.from_rle_standard(default_rle)
#
#     print_time = 1
#     overhead = 1
#
#     while True:
#         overhead += 1
#         if overhead % print_time == 0:
#             t._print(t.max_bounds)
#
#         try:
#             t.step()
#
#         except ValueError:
#             print "End of simulation!"
#
#         time.sleep(.001)
#
#         if overhead % print_time == 0:
#             os.system("cls")
