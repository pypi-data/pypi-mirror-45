import unittest

import numpy as np
from scipy.sparse import coo_matrix

import talon
import talon.opencl


def build_random_matrix(gen_length, nb_generators, nb_data, nb_columns, density):

    generators = np.random.randn(nb_generators, gen_length)
    nnz = int((nb_data * nb_columns) * density)


def build_full_matrix(generator_length, nb_data, nb_columns):

    # Use a random matrix as a starting point.
    generators = np.random.randn(generator_length, nb_data * nb_columns)
    weights = np.random.randn(1, nb_data * nb_columns)
    weighted_generators = generators * weights
    shape = (generator_length * nb_data, nb_columns)
    matrix = np.zeros(shape)
    for i in range(nb_data):
        start = i * generator_length
        stop = (i + 1) * generator_length
        wg_start = i * nb_columns
        wg_stop = (i + 1) * nb_columns
        matrix[start:stop, :] = weighted_generators[:, wg_start:wg_stop]

    # Split the matrix into the indices and generator format.
    indices = np.arange(nb_data * nb_columns)
    rows = np.tile(np.arange(nb_data)[:, None], (1, nb_columns)).ravel()
    cols = np.tile(np.arange(nb_columns), (nb_data, 1)).ravel()
    indices = coo_matrix((indices, (rows, cols)), (nb_data, nb_columns))
    weights = coo_matrix(weights.reshape(nb_data, nb_columns))

    return matrix, indices, weights, generators.T


def build_almost_empty(generator_length, nb_data, nb_columns):

    # Use a single generator.
    generators = np.random.randn(generator_length, 1)
    weights = np.array([1.0])

    matrix = np.zeros((generator_length * nb_data, nb_columns))

    indices = [0]
    rows = [int(nb_data // 2)]
    cols = [int(nb_columns // 2)]

    start = rows[0] * generator_length
    stop = (rows[0] + 1) * generator_length
    matrix[start:stop, cols[0]] = generators[:, 0]
    indices = coo_matrix((indices, (rows, cols)), (nb_data, nb_columns))
    weights = coo_matrix((weights, (rows, cols)), (nb_data, nb_columns))

    return matrix, indices, weights, generators.T


class TestFullMatrix(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        matrix, indices, weights, generators = build_full_matrix(13, 7, 5)
        cls._matrix = matrix
        cls._indices = indices
        cls._weights = weights
        cls._generators = generators

        cls._x = np.random.randn(cls._matrix.shape[1])
        cls._b = np.dot(matrix, cls._x)
        cls._x_hat = np.dot(matrix.T, cls._b)

    def test_opencl(self):

        # Verify the matmul against the numpy implementation.
        lo = talon.opencl.LinearOperator(
            self._generators, self._indices, self._weights)
        np.testing.assert_array_almost_equal(self._b, lo @ self._x, 4)

        # Also verify the transpose matmul.
        np.testing.assert_array_almost_equal(self._x_hat, lo.T @ self._b, 4)

    def test_fast(self):

        # Verify the matmul against the numpy implementation.
        lo = talon.core.FastLinearOperator(
            self._generators, self._indices, self._weights)
        np.testing.assert_array_almost_equal(self._b, lo @ self._x)

        # Also verify the transpose matmul.
        np.testing.assert_array_almost_equal(self._x_hat, lo.T @ self._b)

    def test_reference(self):

        # Verify the matmul against the numpy implementation.
        lo = talon.core.LinearOperator(
            self._generators, self._indices, self._weights)
        np.testing.assert_array_almost_equal(self._b, lo @ self._x)

        # Also verify the transpose matmul.
        np.testing.assert_array_almost_equal(self._x_hat, lo.T @ self._b)


class TestAlmostEmptyMatrix(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        matrix, indices, weights, generators = build_almost_empty(13, 7, 5)
        cls._matrix = matrix
        cls._indices = indices
        cls._weights = weights
        cls._generators = generators

        cls._x = np.random.randn(cls._matrix.shape[1])
        cls._b = np.dot(matrix, cls._x)
        cls._x_hat = np.dot(matrix.T, cls._b)

    def test_opencl(self):

        # Verify the matmul against the numpy implementation.
        lo = talon.opencl.LinearOperator(
            self._generators, self._indices, self._weights)
        np.testing.assert_array_almost_equal(self._b, lo @ self._x, 4)

        # Also verify the transpose matmul.
        np.testing.assert_array_almost_equal(self._x_hat, lo.T @ self._b, 4)

    def test_fast(self):

        # Verify the matmul against the numpy implementation.
        lo = talon.core.FastLinearOperator(
            self._generators, self._indices, self._weights)
        np.testing.assert_array_almost_equal(self._b, lo @ self._x)

        # Also verify the transpose matmul.
        np.testing.assert_array_almost_equal(self._x_hat, lo.T @ self._b, 4)

    def test_reference(self):

        # Verify the matmul against the numpy implementation.
        lo = talon.core.LinearOperator(
            self._generators, self._indices, self._weights)
        np.testing.assert_array_almost_equal(self._b, lo @ self._x)

        # Also verify the transpose matmul.
        np.testing.assert_array_almost_equal(self._x_hat, lo.T @ self._b, 4)
