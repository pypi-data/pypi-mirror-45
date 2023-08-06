import unittest

import numpy as np
from scipy.sparse import coo_matrix

from talon.utils_bkp import remove_empty_rows


class TestRemoveEmptyRows(unittest.TestCase):
    """Test the talon.utils.remove_empty_rows function."""

    def test_dense(self):
        """Test for a dense matrix."""

        generators = np.random.randn(10, 20)
        indices = coo_matrix(np.random.randint(1, 10, (10, 10)))
        weights = coo_matrix(np.random.randn(10, 10))

        new_matrix = remove_empty_rows(generators, indices, weights)
        new_generators, new_indices, new_weights = new_matrix

        # Nothing should have changed.
        np.testing.assert_array_almost_equal(indices.shape, new_indices.shape)
        np.testing.assert_array_almost_equal(generators, new_generators)
        np.testing.assert_array_almost_equal(indices.data, new_indices.data)
        np.testing.assert_array_almost_equal(weights.data, new_weights.data)

    def test_all_zeros(self):
        """Test for an empty matrix."""

        generators = np.random.randn(10, 20)
        indices = coo_matrix((10, 10), np.int)
        weights = coo_matrix((10, 10), np.float)

        new_matrix = remove_empty_rows(generators, indices, weights)
        new_generators, new_indices, new_weights = new_matrix

        np.testing.assert_array_almost_equal(new_indices.shape, (0, 10))
        np.testing.assert_array_almost_equal(generators, new_generators)
        np.testing.assert_array_almost_equal(indices.data, new_indices.data)
        np.testing.assert_array_almost_equal(weights.data, new_weights.data)

    def test_normal_case(self):
        """Test the normal case"""

        generators = np.random.randn(10, 20)
        dense_indices = np.random.randint(1, 10, (10, 10))
        dense_indices[3:8] = 0
        indices = coo_matrix(dense_indices)
        dense_weights = np.random.randn(10, 10)
        dense_weights[5:15] = 0
        weights = coo_matrix(dense_weights)

        new_matrix = remove_empty_rows(generators, indices, weights)
        new_generators, new_indices, new_weights = new_matrix

        # Nothing should have changed.
        np.testing.assert_array_almost_equal(new_indices.shape, (5, 10))
        np.testing.assert_array_almost_equal(generators, new_generators)
        np.testing.assert_array_almost_equal(indices.data, new_indices.data)
        np.testing.assert_array_almost_equal(weights.data, new_weights.data)
