# -*- coding: utf-8 -*-
import unittest
import numpy as np
import scipy.sparse
import talon
from talon.voxelization import *
from talon.voxelization import _voxelize_streamline


def cart2sph(x, y, z):
    radius = np.sqrt(x**2+y**2+z**2)
    elevation = np.arccos(z/radius)
    azimuth = np.arctan2(y, x)
    return radius, elevation, azimuth


def get_example_streamlines():
    i = np.array([[0, 0, 0], [10, 10, 10]])
    j = np.array([[10, 0, 0], [0, 10, 10]])
    k = np.array([[10, 10, 0], [0, 0, 10]])
    s = [i, j, k]

    return s


class TestVoxelize(unittest.TestCase):
    def test_streamline_interpolation(self):
        streamlines = get_example_streamlines()
        s_interp = streamline_interpolation(streamlines[0])
        direction = streamlines[0][1, :] - streamlines[0][0, :]
        radius, theta, phi = cart2sph(direction[0], direction[1], direction[2])

        s_interp_length = len(s_interp)
        r = np.zeros(s_interp_length-1)
        for i in range(1, s_interp_length):
            d = s_interp[i, :] - s_interp[i-1, :]
            r[i-1], t, p = cart2sph(d[0], d[1], d[2])
            self.assertAlmostEqual(theta, t)
            self.assertAlmostEqual(phi, p)

        self.assertAlmostEqual(radius, np.sum(r))

    def test_voxelize_streamline(self):
        streamlines = get_example_streamlines()
        out_voxel, out_vector = _voxelize_streamline(
            streamlines[0], step=1e-05)
        direction = streamlines[0][1, :] - streamlines[0][0, :]
        radius, theta, phi = cart2sph(direction[0], direction[1], direction[2])
        voxel_length = out_voxel.shape[0]
        r = np.zeros(voxel_length)
        for i in range(voxel_length):
            r[i], t, p = cart2sph(
                out_vector[i, 0], out_vector[i, 1], out_vector[i, 2])
            self.assertAlmostEqual(theta, t)
            self.assertAlmostEqual(phi, p)

        self.assertAlmostEqual(radius, np.sum(r), places=2)

    def test_voxelize_tractogram(self):
        streamlines = get_example_streamlines()
        shape = [11, 11, 11]
        u = 1.0/np.sqrt(3)
        vertices = np.array([[u, u, u], [-u, u, u], [-u, -u, u]])
        index_sparse, length_sparse = voxelize_tractogram(streamlines,
                                                          vertices,
                                                          shape)
        index_array = index_sparse.toarray()
        length_array = length_sparse.toarray()
        s0 = index_array[length_array[:, 0] != 0, 0] == 0
        s1 = index_array[length_array[:, 1] != 0, 1] == 1
        s2 = index_array[length_array[:, 2] != 0, 2] == 2

        self.assertTrue(np.all(s0))
        self.assertTrue(np.all(s1))
        self.assertTrue(np.all(s2))
        self.assertEqual(np.sum(s0), 11)
        self.assertEqual(np.sum(s1), 11)
        self.assertEqual(np.sum(s2), 11)


class TestDiagonalize(unittest.TestCase):
    def test_errors(self):
        with self.assertRaises(TypeError):
            talon.diagonalize(1)

        mask = np.array([1, 2, 3])
        with self.assertRaises(ValueError):
            talon.diagonalize(mask)

    def test_output(self):
        basis = np.random.randint(2, 20)
        mask = np.arange(basis ** 3).reshape((basis, ) * 3)

        indices, weights = talon.diagonalize(mask.astype(talon.core.DATATYPE))
        generators = np.array([[1.0]])

        lo = talon.operator(generators, indices, weights)

        reference = np.diag(np.arange(basis ** 3))
        zero_cols = []
        for k, r in enumerate(reference.T):
            if np.all(r == 0.0):
                zero_cols.append(k)
        reference = np.delete(reference, zero_cols, 1)

        np.testing.assert_almost_equal(lo.todense(), reference)