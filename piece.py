from typing import List
import json

with open("positions.json", "r") as f:
    P = json.load(f)

with open("possibilities.json", "r") as f:
    R = json.load(f)

with open("case.txt", "r") as f:
    CASES = f.readlines()

rotations = {
    "R": [1, 0, 2],
    "U": [0, 2, 1],
    "F": [2, 1, 0],
}

turns = {
    "R": {"cycles": [[5, 7, 3, 1]], "rotation": "R"},
    "U": {"cycles": [[7, 6, 2, 3]], "rotation": "U"},
    "F": {"cycles": [[6, 7, 5, 4]], "rotation": "F"},
    "L": {"cycles": [[4, 0, 2, 6]], "rotation": "R"},
    "D": {"cycles": [[5, 1, 0, 4]], "rotation": "U"},
    "B": {"cycles": [[2, 0, 1, 3]], "rotation": "F"},
    "x": {"cycles": [[5, 7, 3, 1], [4, 6, 2, 0]], "rotation": "R"},
    "y": {"cycles": [[7, 6, 2, 3], [5, 4, 0, 1]], "rotation": "U"},
    "z": {"cycles": [[6, 7, 5, 4], [2, 3, 1, 0]], "rotation": "F"},
}

reorentations = [  # Where there is index it becomes the value
    {"ids": [0, 1, 2, 3, 4, 5, 6, 7]},
    {"ids": [2, 0, 3, 1, 6, 4, 7, 5], "rotation": ["R", "U", "F"]},
    {"ids": [1, 3, 0, 2, 5, 7, 4, 6], "rotation": ["R", "U", "F"]},
    {"ids": [3, 2, 1, 0, 7, 6, 5, 4]},
    {"ids": [2, 3, 6, 7, 0, 1, 4, 5], "rotation": ["F", "R", "U"]},
    {"ids": [5, 4, 7, 6, 1, 0, 3, 2]},
    {"ids": [6, 7, 4, 5, 2, 3, 0, 1]},
    {"ids": [7, 3, 5, 1, 6, 2, 4, 0], "rotation": "U"},
    {"ids": [0, 2, 4, 6, 1, 3, 5, 7], "rotation": "R"},  # rotation = 1
    {"ids": [0, 4, 1, 5, 2, 6, 3, 7], "rotation": "F"},  # rotation = 2
]


def swap4(f: List[int], t: List[int], this: List):
    (this[f[0]], this[f[1]],
     this[f[2]], this[f[3]]) = (this[t[0]], this[t[1]], this[t[2]], this[t[3]])


class Cube:
    _position: List[int]
    _rotation: List[int]

    _defaultPosition = [0, 1, 2, 3, 4, 5, 6, 7]
    _defaultRotation = [0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, initial_state: str = ''):
        if initial_state == '':
            self._position = self._defaultPosition.copy()
            self._rotation = self._defaultRotation.copy()
            return

        if len(initial_state) != 16:
            raise ValueError("length of initial_state has to be 16")

        try:
            self._position = [int(x) for x in initial_state[:8]]
            self._rotation = [int(x) for x in initial_state[8:16]]
        except ValueError:
            raise ValueError("initial_state should consist of numbers only")

        if set(self._position) != set(self._defaultPosition):
            raise ValueError("initial_state has duplicate keys")

        if self.get_index() == -1:
            raise ValueError("initial_state is impossible")

    def get_index(self):
        self.fix_center()
        positions = "".join(map(str, self._position[1:]))
        rotations = "".join(map(str, self._rotation[1:]))
        try:
            return P[positions] * 729 + R[rotations]
        except KeyError:
            return -1

    def get_solution(self):
        try:
            return CASES[self.get_index()][:-1]
        except KeyError:
            return "No solution"

    def fix_center(self):
        """if self._position[0] == 1:
            if self._rotation[0] == 2:
                self._rotate([list(range(8))], rotations["F"])
            elif self._rotation[0] == 1:
                self._rotate([list(range(8))], rotations["U"])
            elif self._rotation[0] == 0:
                self._rotate([list(range(8))], rotations["R"])
        elif self._position[0] == 4:
            if self._rotation[0] == 1:
                self._rotate([list(range(8))], rotations["R"])
            elif self._rotation[0] == 0:
                self._rotate([list(range(8))], rotations["F"])
            elif self._rotation[0] == 2:
                self._rotate([list(range(8))], rotations["U"])
        elif self._position[0] == 2:
            if self._rotation[0] == 2:
                self._rotate([list(range(8))], rotations["F"])
            elif self._rotation[0] == 1:
                self._rotate([list(range(8))], rotations["U"])
            elif self._rotation[0] == 0:
                self._rotate([list(range(8))], rotations["R"])"""
        self.reorentate(self._position[0])
        if self._rotation[0] == 1:
            self.reorentate(8, True)
        elif self._rotation[0] == 2:
            self.reorentate(9, True)

    def apply_scramble(self, scramble: str):
        moves = scramble.split(' ')
        if len(moves) != 1 or moves[0] != '':
            [self.make_turn(move) for move in moves]

    def make_turn(self, turn: str):
        backward = len(turn) == 2 and turn[1] == "'"
        double = len(turn) == 2 and turn[1] == "2"
        # TODO make some kind of API or methods to return rotation and cycles
        rotation = rotations[turns[turn[0]]["rotation"]]
        cycles = turns[turn[0]]["cycles"]
        self._swap(cycles, backward, double)
        not double and self._rotate(cycles, rotation)

    def reorentate(self, index: int, rotate: bool = False):
        reorentation = reorentations[index]
        ids = reorentation["ids"]
        for i, n in enumerate(self._position):
            self._position[i] = ids[n]

        if "rotation" in reorentation:
            rotation = 0 if len(
                reorentation["rotation"]) == 1 else self._rotation[0]
            self._rotate([list(range(8))],
                         rotations[reorentation["rotation"][rotation]])

    def _swap(self, cycles: List[List[int]], backward: bool, double: bool):
        for cycle in cycles:
            to = list(map(lambda i: cycle[i],
                          [1, 2, 3, 0] if backward
                          else [2, 3, 0, 1] if double else [3, 0, 1, 2]))
            swap4(cycle, to, self._position)
            swap4(cycle, to, self._rotation)

    def _rotate(self, cycles: List[List[int]], rotation: List[int]):
        for piece in [y for x in cycles for y in x]:
            self._rotation[piece] = rotation[self._rotation[piece]]

    def reset(self):
        self._position = self._defaultPosition.copy()
        self._rotation = self._defaultRotation.copy()
