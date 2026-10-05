import math
import unittest

from src.heuristics import euclidean, manhattan


class HeuristicsTests(unittest.TestCase):
    def test_same_position(self):
        self.assertEqual(manhattan((2, 3), (2, 3)), 0.0)
        self.assertEqual(euclidean((2, 3), (2, 3)), 0.0)

    def test_manhattan_distance(self):
        self.assertEqual(manhattan((0, 0), (3, 4)), 7.0)
        self.assertEqual(manhattan((5, 2), (1, 8)), 10.0)

    def test_euclidean_distance(self):
        self.assertAlmostEqual(euclidean((0, 0), (3, 4)), 5.0)
        self.assertAlmostEqual(euclidean((1, 1), (4, 5)), 5.0)
        self.assertAlmostEqual(euclidean((0, 0), (1, 1)), math.sqrt(2))

    def test_admissibility_property(self):
        # A distância Euclidiana é sempre <= distância Manhattan (hE <= hM)
        p1 = (1, 2)
        p2 = (6, 9)
        self.assertLessEqual(euclidean(p1, p2), manhattan(p1, p2))


if __name__ == "__main__":
    unittest.main()
