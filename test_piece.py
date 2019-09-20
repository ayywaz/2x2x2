import unittest
import piece


class TestCube(unittest.TestCase):
    _solved_position = [0, 1, 2, 3, 4, 5, 6, 7]
    _solved_rotation = [0, 0, 0, 0, 0, 0, 0, 0]

    def setUp(self):
        self.cube = piece.Cube()

    def test_init(self):
        self.assertEqual(self.cube._position, [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(self.cube._rotation, [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.cube.get_index(), 0)

        self.assertRaises(ValueError, piece.Cube, "1")
        self.assertRaises(ValueError, piece.Cube, "01234567")
        self.assertRaises(ValueError, piece.Cube, "a123456700000000")
        self.assertRaises(ValueError, piece.Cube, "abc")

        c1 = piece.Cube("0123456700000000")
        self.assertEqual(c1._position, [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(c1._rotation, [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(c1.get_index(), 0)

        self.assertRaises(ValueError, piece.Cube, "1123456700000000")
        self.assertRaises(ValueError, piece.Cube, "0123456700000001")

        c2 = piece.Cube("4062517300000000")
        self.assertEqual(c2.get_index(), 0)

    def test_swap(self):
        self.cube._swap(piece.turns["z"]["cycles"], False, False)
        self.assertEqual(self.cube._position, [1, 3, 0, 2, 5, 7, 4, 6])

        self.cube.reset()
        self.cube._swap(piece.turns["L"]["cycles"], False, False)
        self.assertEqual(self.cube._position, [4, 1, 0, 3, 6, 5, 2, 7])

    def test_rotate(self):
        self.cube._rotate([0, 2, 1])  # "y"
        self.assertEqual(self.cube._rotation, [0] * 8)

        self.cube._rotate([1, 0, 2])  # "x"
        self.assertEqual(self.cube._rotation, [1] * 8)

    def test_make_turn(self):
        self.cube.make_turn("x")
        self.assertEqual(self.cube._position, [2, 3, 6, 7, 0, 1, 4, 5])
        self.assertEqual(self.cube._rotation, [1] * 8)

    def test_fix_center(self):
        self.cube.apply_scramble("y2")
        self.cube.fix_center()
        self.assertEqual(self.cube._position, self._solved_position)
        self.assertEqual(self.cube._rotation, self._solved_rotation)

        self.cube.apply_scramble("z'")
        self.cube.fix_center()
        self.assertEqual(self.cube._position, self._solved_position)
        self.assertEqual(self.cube._rotation, self._solved_rotation)

        self.cube.apply_scramble("x' y'")
        self.cube.fix_center()
        self.assertEqual(self.cube._position, self._solved_position)
        self.assertEqual(self.cube._rotation, self._solved_rotation)

        self.cube.apply_scramble("x2 y'")
        self.cube.fix_center()
        self.assertEqual(self.cube._position, self._solved_position)
        self.assertEqual(self.cube._rotation, self._solved_rotation)

        self.cube.apply_scramble("y2 x")
        self.cube.fix_center()
        self.assertEqual(self.cube._position, self._solved_position)
        self.assertEqual(self.cube._rotation, self._solved_rotation)

        self.cube.apply_scramble("R y'")
        self.cube.fix_center()
        self.assertEqual(self.cube._position, [0, 1, 2, 3, 5, 7, 4, 6])

        self.cube.apply_scramble("x2 z' y")
        self.cube.fix_center()
        self.assertEqual(self.cube._position, [0, 3, 2, 7, 4, 1, 6, 5])

    def test_reset(self):
        self.cube.make_turn("R'")
        self.cube.reset()
        self.assertEqual(self.cube._position, self._solved_position)
        self.assertEqual(self.cube._rotation, self._solved_rotation)

    def test_apply_scramble(self):
        self.cube.apply_scramble("R x2 y2 x2 y' y' R'")
        self.assertEqual(self.cube._position, self._solved_position)
        self.assertEqual(self.cube._rotation, self._solved_rotation)

        self.cube.apply_scramble("L U' R U2 L' U R' U")
        self.assertEqual(self.cube._position, [5, 1, 3, 6, 4, 0, 2, 7])

    def test_get_index(self):
        self.cube.apply_scramble("L U' R U2 L' U R' U")
        self.assertEqual(self.cube.get_index(), 1961739)


if __name__ == '__main__':
    unittest.main()
