import unittest

import numpy as np
import talon


class TestFibonacci(unittest.TestCase):
    def test_shape(self):
        n = np.random.randint(100) + 1
        sphere = talon.utils.directions(n)

        self.assertTupleEqual((n, 3), sphere.shape)

    def test_error(self):
        with self.assertRaises(ValueError):
            talon.utils.directions(-1)

        with self.assertRaises(ValueError):
            talon.utils.directions(0)

    def test_z_coordinate(self):
        n = np.random.randint(100) + 1
        sphere = talon.utils.directions(n)

        self.assertTrue(np.all(sphere[:, 2] > 0))
