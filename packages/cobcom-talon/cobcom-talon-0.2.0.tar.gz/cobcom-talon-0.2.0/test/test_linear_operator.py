# -*- coding: utf-8 -*-
import time
import unittest

import numpy as np
import scipy.sparse

import talon
import talon.core

datatype = talon.core.DATATYPE


def get_example_linear_operator(operator_type='reference'):
    i = np.array([0, 3, 1, 2, 0, 1])
    j = np.array([0, 0, 1, 1, 2, 3])
    data = np.array([0, 1, 2, 2, 0, 1], dtype=datatype)
    t = scipy.sparse.coo_matrix((data, (i, j)), dtype=int)
    weights = np.array([1, 2, 1, 4, 5, 7], dtype=datatype)
    w = scipy.sparse.coo_matrix((weights, (i, j)))
    g = np.array([[1., 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]], datatype)
    full_matrix = np.array([[1, 0, 5, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],  # end b0
                            [0, 0, 0, 0],
                            [0, 0, 0, 7],
                            [0, 1, 0, 0],  # end b1
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 4, 0, 0],  # end b2
                            [0, 0, 0, 0],
                            [2, 0, 0, 0],
                            [0, 0, 0, 0]], dtype=datatype)
    lo = talon.operator(g, t, w, operator_type)
    return lo, (g, t, w, full_matrix)


class TestLinearOperator(unittest.TestCase):
    def test_type(self):
        lo, __ = get_example_linear_operator()
        self.assertIsInstance(lo, talon.core.LinearOperator)

    def test_dimensions(self):
        lo, (g, t, w, full_matrix) = get_example_linear_operator()
        self.assertAlmostEqual(lo.nb_atoms, t.shape[1])
        self.assertAlmostEqual(lo.nb_atoms, w.shape[1])
        self.assertAlmostEqual(lo.nb_data, t.shape[0])
        self.assertAlmostEqual(lo.nb_data, w.shape[0])
        self.assertAlmostEqual(lo.nb_generators, g.shape[0])
        self.assertAlmostEqual(lo.generator_length, g.shape[1])
        self.assertTupleEqual(lo.shape, (g.shape[1] * t.shape[0], t.shape[1]))

        i, j = t.row, t.col
        reduced_i, reduced_j = i[:-1], j[:-1]
        shape = (max(i) + 1, max(j) + 1)
        reduced_data, reduced_weights = t.data[:-1], w.data[:-1]
        reduced_t = scipy.sparse.coo_matrix(
            (reduced_data, (reduced_i, reduced_j)), shape=shape, dtype=int)
        reduced_w = scipy.sparse.coo_matrix(
            (reduced_weights, (reduced_i, reduced_j)), shape=shape)
        with self.assertRaises(ValueError):
            __ = talon.operator(g, reduced_t, w)
            __ = talon.operator(g, t, reduced_w)

    def test_multiplication(self):
        lo, (__, __, __, full_matrix) = get_example_linear_operator()
        x = np.random.rand(lo.shape[1])
        reference_product = full_matrix @ x
        my_product = lo @ x
        np.testing.assert_almost_equal(reference_product, my_product)

        x1 = x[:-1]
        with self.assertRaises(ValueError):
            __ = lo @ x1

    def test_todense(self):
        lo, (__, __, __, full_matrix) = get_example_linear_operator()
        np.testing.assert_almost_equal(lo.todense(), full_matrix)

    def test_iter(self):
        lo, (g, t, w, full_matrix) = get_example_linear_operator()
        iterated = np.array([d for __, __, d in lo])
        ground_truth = np.array(
            [g[idx, :] * w for idx, w in zip(t.data, w.data)])
        np.testing.assert_almost_equal(iterated, ground_truth)


class TestFastLinearOperator(unittest.TestCase):
    """Test the talon.core.FastLinearOperator class"""

    def test_empty_rows(self):
        """Test the initialization with matrices with many empty rows"""

        i = np.array([0, 3])
        j = np.array([0, 0])
        data = np.array([0, 0], dtype=datatype)

        generators = np.array([[1., 1., 1.]], datatype)

        # Generate two matrices, one normal and one with many empty rows.
        indices_normal = scipy.sparse.coo_matrix(
            (data, (i, j)), shape=(10, 3), dtype=int)
        weights = np.array([1, 2], dtype=datatype)
        weights_normal = scipy.sparse.coo_matrix(
            (weights, (i, j)), shape=(10, 3))
        normal_time = time.time()
        lo_normal = talon.operator(
            generators, indices_normal, weights_normal, 'fast')
        normal_time = time.time() - normal_time

        indices_empty = scipy.sparse.coo_matrix(
            (data, (i, j)), shape=(100000, 3), dtype=int)
        weights = np.array([1, 2], dtype=datatype)
        weights_empty = scipy.sparse.coo_matrix(
            (weights, (i, j)), shape=(100000, 3))
        empty_time = time.time()
        lo_empty = talon.operator(
            generators, indices_empty, weights_empty, 'fast')
        empty_time = time.time() - empty_time

        # The initialization performance should not really depend on the number
        # of empty rows.
        self.assertTrue(abs(normal_time - empty_time) < 0.10)

        # Same thing for the product.
        x = np.array([1, 1, 1], dtype=datatype)
        normal_time = time.time()
        y_hat_normal = lo_normal @ x
        normal_time = time.time() - normal_time

        empty_time = time.time()
        y_hat_empty = lo_empty @ x
        empty_time = time.time() - empty_time

        self.assertTrue(abs(normal_time - empty_time) < 0.10)
        np.testing.assert_array_almost_equal(y_hat_normal, y_hat_empty[:30])

        # and the product of the transpose.
        y = np.full((30,), 1, dtype=datatype)
        normal_time = time.time()
        x_hat_normal = lo_normal.T @ y
        normal_time = time.time() - normal_time

        y = np.full((300000,), 1, dtype=datatype)
        empty_time = time.time()
        x_hat_empty = lo_empty.T @ y
        empty_time = time.time() - empty_time

        self.assertTrue(abs(normal_time - empty_time) < 0.10)
        np.testing.assert_array_almost_equal(x_hat_normal, x_hat_empty)

    def test_type(self):
        lo, __ = get_example_linear_operator('fast')
        self.assertIsInstance(lo, talon.core.FastLinearOperator)

    def test_matmul(self):
        """Test the __matmul__ method"""

        # Generate simple test data.
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[1])

        # The product should match the dense product.
        reference_product = full_matrix @ x
        my_product = lo @ x
        np.testing.assert_almost_equal(reference_product, my_product)
        # Double test due to possible bug on exhausted generator after the
        # first product
        my_product = lo @ x
        np.testing.assert_almost_equal(reference_product, my_product)

        # Verify that a ValueError is raised on dimension mismatch.
        x1 = x[:-1]
        with self.assertRaises(ValueError):
            __ = lo @ x1

    def test_matmul_all_zero_row(self):
        """Test the __matmul__ method with an all zero row."""

        # Generate an edge case where there is an all zero row.
        dense = np.array([
            [1, 0],
            [0, 0],
        ], dtype=talon.core.DATATYPE)
        indices = scipy.sparse.coo_matrix(dense)
        weights = scipy.sparse.coo_matrix(dense)
        generators = np.array([
            [0, 0],
            [1, 1],
        ], dtype=talon.core.DATATYPE)
        operator = talon.operator(generators, indices, weights, 'fast')

        x = np.ones((2,))
        y = operator @ x
        np.testing.assert_array_almost_equal(y, [1, 1, 0, 0])


class TestTransposedLinearOperator(unittest.TestCase):
    def test_type(self):
        lo, __ = get_example_linear_operator()
        self.assertIsInstance(lo.transpose,
                              talon.core.TransposedLinearOperator)
        self.assertIsInstance(lo.T, talon.core.TransposedLinearOperator)

    def test_shape(self):
        lo, (__, __, __, full_matrix) = get_example_linear_operator()
        self.assertTupleEqual(lo.T.shape, full_matrix.T.shape)

    def test_transpose_multiplication(self):
        lo, (__, __, __, full_matrix) = get_example_linear_operator()
        y = np.random.rand(lo.T.shape[1])
        reference_product = full_matrix.T @ y
        my_product = lo.T @ y
        np.testing.assert_almost_equal(reference_product, my_product)
        my_product = lo.transpose @ y
        np.testing.assert_almost_equal(reference_product, my_product)

        y1 = y[:-1]
        with self.assertRaises(ValueError):
            __ = lo.T @ y1
        with self.assertRaises(ValueError):
            __ = lo.transpose @ y1


class TestTransposedFastLinearOperator(unittest.TestCase):
    def test_type(self):
        lo, __ = get_example_linear_operator('fast')
        self.assertIsInstance(lo.transpose,
                              talon.core.TransposedFastLinearOperator)
        self.assertIsInstance(lo.T, talon.core.TransposedFastLinearOperator)

    def test_shape(self):
        lo, (__, __, __, full_matrix) = get_example_linear_operator('fast')
        self.assertTupleEqual(lo.T.shape, full_matrix.T.shape)

    def test_transpose_multiplication(self):
        lo, (__, __, __, full_matrix) = get_example_linear_operator('fast')
        y = np.random.rand(lo.T.shape[1])
        reference_product = full_matrix.T @ y
        my_product = lo.T @ y
        np.testing.assert_almost_equal(reference_product, my_product)
        my_product = lo.transpose @ y
        np.testing.assert_almost_equal(reference_product, my_product)

        y1 = y[:-1]
        with self.assertRaises(ValueError):
            __ = lo.T @ y1
        with self.assertRaises(ValueError):
            __ = lo.transpose @ y1


class TestConcatenatedLinearOperator(unittest.TestCase):
    def test_type(self):
        lo, __ = get_example_linear_operator('fast')
        self.assertIsInstance(talon.concatenate((lo, lo), axis=0),
                              talon.core.ConcatenatedLinearOperator)
        self.assertIsInstance(talon.concatenate((lo, lo), axis=1),
                              talon.core.ConcatenatedLinearOperator)

    def test_shape(self):
        lo, __ = get_example_linear_operator('fast')
        reference_shape = lo.shape[0] * 2, lo.shape[1]
        composite = talon.concatenate((lo, lo), axis=0)
        self.assertTupleEqual(composite.shape, reference_shape)

        reference_shape = lo.shape[0], lo.shape[1] * 2
        composite = talon.concatenate((lo, lo), axis=1)
        self.assertTupleEqual(composite.shape, reference_shape)

    def test_instance_creation(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')

        vertical = talon.concatenate((lo, lo), 0)
        gt_vertical = np.concatenate([full_matrix] * 2, 0)
        np.testing.assert_almost_equal(vertical.todense(), gt_vertical)

        horizontal = talon.concatenate((lo, lo), 1)
        gt_horizontal = np.concatenate([full_matrix] * 2, 1)
        np.testing.assert_almost_equal(horizontal.todense(), gt_horizontal)

        with self.assertRaises(ValueError):
            _ = talon.concatenate([])
        with self.assertRaises(ValueError):
            _ = talon.concatenate(())

        with self.assertRaises(ValueError):
            _ = talon.concatenate([lo, lo], 20)

        with self.assertRaises(ValueError):
            _ = talon.concatenate([horizontal, lo], 0)
        with self.assertRaises(ValueError):
            _ = talon.concatenate((vertical, lo), 1)

        with self.assertRaises(TypeError):
            _ = talon.concatenate(1)
        with self.assertRaises(TypeError):
            _ = talon.concatenate((lo, 1))
        with self.assertRaises(TypeError):
            _ = talon.concatenate([lo, 1])

    def test_multiplication_vertical(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[1])

        reference_product = np.concatenate([full_matrix] * 2, axis=0) @ x
        my_product = talon.concatenate((lo, lo), axis=0) @ x

        np.testing.assert_almost_equal(reference_product, my_product)

    def test_multiplication_horizontal(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[1])
        twice_x = np.concatenate((x, x))

        numpy_concatenate = np.concatenate([full_matrix] * 2, axis=1)
        talon_concatenate = talon.concatenate((lo, lo), axis=1)

        reference_product = numpy_concatenate @ twice_x
        my_product = talon_concatenate @ twice_x

        np.testing.assert_almost_equal(reference_product, my_product)


class TestTransposedConcatenatedLinearOperator(unittest.TestCase):
    def test_shape(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')

        axis = 0
        gt_shape = np.concatenate([full_matrix] * 2, axis).T.shape
        my_shape = talon.concatenate([lo] * 2, axis).T.shape
        self.assertTupleEqual(gt_shape, my_shape)

        axis = 1
        gt_shape = np.concatenate([full_matrix] * 2, axis).T.shape
        my_shape = talon.concatenate([lo] * 2, axis).T.shape
        self.assertTupleEqual(gt_shape, my_shape)

    def test_multiplication_originally_vertical(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[0])
        twice_x = np.concatenate((x, x))

        numpy_concatenated = np.concatenate([full_matrix] * 2, 0)
        reference_product = numpy_concatenated.T @ twice_x

        talon_concatenated = talon.concatenate((lo, lo), axis=0)
        my_product = talon_concatenated.T @ twice_x

        np.testing.assert_almost_equal(reference_product, my_product)

    def test_multiplication_originally_horizontal(self):
        lo, (_, _, _, full_matrix) = get_example_linear_operator('fast')
        x = np.random.rand(lo.shape[0])

        numpy_concatenated = np.concatenate([full_matrix] * 2, 1)
        reference_product = numpy_concatenated.T @ x

        talon_concatenated = talon.concatenate([lo] * 2, axis=1)
        my_product = talon_concatenated.T @ x

        np.testing.assert_almost_equal(reference_product, my_product)


class TestNormalizeAtoms(unittest.TestCase):
    def test_norm(self):
        lo, (g, t, w, full_matrix) = get_example_linear_operator('fast')

        normalized_lo = talon.operator(*talon.normalize(g, t, w))

        expected = np.ones(lo.shape[1])
        computed = np.linalg.norm(normalized_lo.todense(), axis=0)

        np.testing.assert_almost_equal(computed, expected)

    def test_empty_column(self):
        i = np.array([0])
        j = np.array([0])
        data = np.array([1])
        t = scipy.sparse.coo_matrix((data, (i, j)), dtype=int, shape=(2, 2))
        weights = np.array([1.0], dtype=datatype)
        w = scipy.sparse.coo_matrix((weights, (i, j)), shape=(2, 2))
        g = np.array([[1., 0., 0.],
                      [0., 1., 0.],
                      [0., 0., 1.]], datatype)

        with self.assertRaises(ValueError):
            talon.normalize(g, t, w)
