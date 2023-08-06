# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import numpy as np
import scipy.sparse as sp

DATATYPE = np.float64


def concatenate(operators, axis=0):
    """Concatenate a sequence of linear operator along axis 0 or 1.

    This method defines the object that acts as the concatenation of the
    linear operators contained in the list/tuple `operators` along the chosen
    `axis`. The syntax is consistent with the one of `np.concatenate`.

    Args:
        operators: list or tuple of LinearOperator objects to be
            concatenated in the same axis.
        axis: int direction in which we want to concatenate the
            LinearOperator or ConcatenatedLinearOperator objects that we
            want to concatenate. Vertical concatenation is obtained for
            `axis = 0` and horizontal concatenation is obtained for
            `axis = 1` as in np.concatenate. (Default: 0)

    Returns:
        talon.core.ConcatenatedLinearOperator: the concatenated linear operator.
    """
    return ConcatenatedLinearOperator(operators, axis)


def normalize_atoms(generators, indices_of_generators, weights):
    """
    Prepare the input of talon.operator to get a dictionary with normalized
    atoms.

    Given a triplet ``(generators, indices_of_generators, weights)``, this
    function returns a new triplet where the ``weights`` matrix is scaled in
    such a way that the resulting linear operator has columns with norm equal
    to 1.

    Args:
        generators : np.array where each row is a generator.
        indices_of_generators : COO sparse matrix that tells which generator is
            called where in the linear operator.
        weights : COO sparse matrix that encodes the weight applied to each
            generator indexed by indices_of_generators. It has the same
            dimension as indices_of_generators.

    Returns:
        generators : the same as the input.
        indices_of_generators : the same as the input.
        weights : COO sparse matrix where each column is scaled to get a
            normalized set of atoms.

    Raises:
        ValueError : if there are empty columns in `indices_of_generators`.
    """
    if not (len(np.unique(indices_of_generators.col)) ==
            indices_of_generators.shape[1]):
        raise ValueError(
            'There are empty columns in the `indices_of_generators` matrix.')

    norms = np.zeros(indices_of_generators.shape[1])

    # squared norm of each generator
    gg = np.square(np.linalg.norm(generators, axis=1))

    # squared weights
    ww = np.square(weights.data)

    for r, c, i, w in zip(
            indices_of_generators.row,
            indices_of_generators.col,
            indices_of_generators.data,
            ww):
        norms[c] += w * gg[i]
    norms = np.sqrt(norms)

    new_data = np.zeros(weights.data.size, dtype=DATATYPE)

    for i, (c, w) in enumerate(zip(weights.col, weights.data)):
        new_data[i] = w / norms[c] if norms[c] > 0 else 1.0

    normalized_weights = sp.coo_matrix(
        (new_data, (weights.row, weights.col)),
        shape=weights.shape
    )

    return generators, indices_of_generators, normalized_weights


def operator(generators, indices_of_generators, weights, operator_type='fast'):
    """Create a LinearOperator object.

    This method defines the object that describes the linear operator by means
    of its fundamental components. These components are a set of generators, a
    table that encodes the non-zero entries of the operator and indexes the
    proper generator in each entry and another table that encodes the weight
    applied to each called generator in the linear operator.

    Each block of entries of the linear operator A is given by

        .. math:: A[k\cdot i\dots k\cdot(i+1), j] = g_{T_{i,j}} \cdot w_{i,j}

    where `k` is the length of the generators, `T` is the table of indices and
    `w` is the table of weights.

    Args:
        generators : np.array where each row is a generator.
        indices_of_generators : COO sparse matrix that tells which generator is
            called where in the linear operator.
        weights : COO sparse matrix that encodes the weight applied to each
            generator indexed by indices_of_generators. It has the same
            dimension as indices_of_generators.
        operator_type (optional): string
            Operator type to use. Accepted values are ``'fast'`` and
            ``'reference'``. The latter is intended to be used only for testing
            purposes. (default = `fast`).

    Returns:
        talon.core.LinearOperator: the wanted linear operator.

    Raises:
        ValueError: If `reference_type` is not ``'fast'`` or ``'reference'``.
    """

    args = (generators, indices_of_generators, weights)

    if operator_type == 'fast':
        return FastLinearOperator(*args)

    elif operator_type == 'reference':
        return LinearOperator(*args)

    raise ValueError('Invalid reference type {}. Should be "fast" or '
                     '"reference"'.format(operator_type))


class AbstractLinearOperator(ABC):
    """Abstract class for all linear operators

    This abstract class defines the interface that all linear operators in
    talon must implement.

    """

    @property
    @abstractmethod
    def shape(self):
        """Returns the shape of the matrix."""
        pass

    @property
    @abstractmethod
    def todense(self):
        """Returns a dense matrix representation of the linear operator."""
        pass

    @property
    @abstractmethod
    def transpose(self):
        """Returns the transpose of the linear operator."""
        pass

    @property
    def T(self):
        """Returns the transpose of the linear operator."""
        return self.transpose

    @abstractmethod
    def __matmul__(self, x):
        """Dot product between a linear operator and a vector.

        The __matmul__ method is expected to compute the dot product between
        a linear operator and a vector. It is not required to support matrix
        matrix product.

        """
        pass

    def convert_x(self, x):
        """Converts x so that it can be used on the right of a dot product.

        This method converts x so that it has the right dimensions and type to
        be used as a right operand of a dot product with a linear operator.
        That is, it asserts that A @ x will work. Raises exceptions if the
        input cannot be converted to the correct format.

        Args:
            x: The vector to test.

        Returns:
            x: A numpy array that can be used in the dot product.

        Raises:
            TypeError : If x is not a numpy array.
            ValueError : If the length of x does not match the number of
                columns of the linear operator.

        """

        x = np.squeeze(np.asarray(x, dtype=DATATYPE))

        # It needs to be a vector.
        if np.ndim(x) != 1:
            raise ValueError(
                f'x must be a 1D vector, but its shape is {x.shape}')

        if not len(x) == self.shape[1]:
            raise ValueError(
                f'Dimension mismatch ({len(x)} != {self.shape[1]})')

        return x


class LinearOperator(AbstractLinearOperator):
    def __init__(self, generators, indices_of_generators, weights):
        """Linear operator that maps tractography to signal space.
        The linear operator can be used to compute products with a vector.

        Args:
            generators : np.array where each row is a generator.
            indices_of_generators : COO sparse matrix that tells which
                generator is called where in the linear operator.
            weights : COO sparse matrix that encodes the weight applied to each
                generator indexed by indices_of_generators. It has the same
                dimension as indices_of_generators.
        Raises:
            TypeError: If `generators` is not a numpy ndarray of float.
            TypeError: If `indices_of_generators` is not a COO scipy matrix.
            TypeError: If `weights` is not a COO scipy matrix of float64.
            ValueError: If `weights` does not have the same dimension
                as indices_of_generators.
            ValueError: If `weights` and `indices_of_generators` don't have the
                same sparsity pattern.
        """
        if not isinstance(generators, np.ndarray):
            raise TypeError('Expected type for "generators" is np.ndarray.')
        if not generators.dtype == DATATYPE:
            raise TypeError(
                'Expected dtype for "generators" is {}.'.format(str(DATATYPE)))

        self._generators = generators

        if not sp.isspmatrix_coo(indices_of_generators):
            raise (TypeError(
                'Expected type for "indices_of_generators" is '
                'scipy.sparse.coo_matrix.'))

        self._indices_of_generators = indices_of_generators.astype(int)

        if not sp.isspmatrix_coo(weights):
            raise (TypeError('Expected type for "weights" is np.ndarray.'))
        if not weights.dtype == DATATYPE:
            raise TypeError(
                'Expected dtype for "weights" is {}.'.format(str(DATATYPE)))
        if not weights.shape == indices_of_generators.shape:
            raise ValueError(
                '"indices_of_generators" and "weights" must have the same'
                ' dimension')
        if not (
                len(weights.data) == len(indices_of_generators.data) and
                np.array_equal(
                    sorted(zip(weights.row, weights.col)),
                    sorted(zip(indices_of_generators.row,
                               indices_of_generators.col)))):
            raise ValueError(
                '"indices_of_generators" and "weights" must have the same'
                ' sparsity pattern')

        self._weights = weights

    @property
    def columns(self):
        """int: Returns the indices of the nonzero columns."""
        return self._indices_of_generators.col

    @property
    def nb_generators(self):
        """int: Number of generators."""
        return self._generators.shape[0]

    @property
    def generator_length(self):
        """int: length of each generator (constant across generators)."""
        return self._generators.shape[1]

    @property
    def generators(self):
        """np.ndarray: Returns the generators of the linear operator."""
        return self._generators

    @property
    def indices(self):
        """np.ndarray: Returns the generator indices."""
        return self._indices_of_generators.data

    @property
    def nb_data(self):
        """int: Number of data points."""
        return self._indices_of_generators.shape[0]

    @property
    def nb_atoms(self):
        """int: Number of atoms (columns) in the linear operator."""
        return self._indices_of_generators.shape[1]

    @property
    def rows(self):
        """int: Returns the indices of the nonzero rows."""
        return self._indices_of_generators.row

    @property
    def shape(self):
        """:tuple of int: Shape of the linear operator.

        The shape is given by the number of rows and columns of the linear
        operator. The number of rows is equal to the number of data points
        times the length of the generators. The number of columns is equal to
        the number of atoms.
        """
        return self.nb_data * self.generator_length, self.nb_atoms

    @property
    def transpose(self):
        """TransposedLinearOperator: the transpose of the linear operator."""
        return TransposedLinearOperator(self)

    @property
    def weights(self):
        """np.ndarray: The weights of the nonzero elements"""
        return self._weights.data

    def __matmul__(self, x):
        """Matrix vector product (A @ x)

        Args:
            x: The right operand of the product. It's length must match the
                number of columns of the linear operator.

        Raises:
            TypeError : If x is not a numpy array.
            ValueError : If the length of x does not match the number of
                columns of the linear operator.
        """

        x = self.convert_x(x)

        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for row, column, weighted_generator in self:
            tmp = weighted_generator * x[column]
            product[self.generator_length * row:
                    self.generator_length * (row + 1)] += tmp
        return product

    def todense(self):
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            ndarray: full matrix representing the linear operator.
        """
        dense = np.zeros(self.shape, dtype=DATATYPE)
        length = self.generator_length
        for row, column, generator in self:
            dense[length * row: length * (row + 1), column] = generator

        return dense

    def __iter__(self):
        indices = self._indices_of_generators
        rows, cols, data = indices.row, indices.col, indices.data
        weights = self._weights.data
        for r, c, idx, w in zip(rows, cols, data, weights):
            yield r, c, self._generators[idx, :] * w


class FastLinearOperator(LinearOperator):

    def __init__(self, generators, indices_of_generators, weights):
        """A LinearOperator that computes products quickly.

        The FastLinearOperator class implements a linear operator optimized to
        compute matrix-vector products quickly. It is single threaded and
        written in pure Python, which makes it a good default choice for linear
        operators.

        Args:
            generators : np.array where each row is a generator.
            indices_of_generators : COO sparse matrix that tells which
                generator is called where in the linear operator.
            weights : COO sparse matrix that encodes the weight applied to each
                generator indexed by indices_of_generators. It has the same
                dimension as indices_of_generators.

        Raises:
            TypeError: If generators is not a numpy ndarray of float64.
            TypeError: If indices_of_generators is not a COO scipy matrix.
            TypeError: If weights is not a COO scipy matrix of float64.
            ValueError: if weights does not have the same dimension
                as indices_of_generators.
            ValueError: if weights and indices_of_generators don't have the
                same sparsity pattern.

        """

        super().__init__(generators, indices_of_generators, weights)

        # Find the indices of the row which are not empty. This allows the
        # linear performance to be independent of the number of empty rows.
        row_indices = np.unique(self.rows)

        # The product is computed row by row. Here, we precompute which
        # generators are multiplied by which weight and x, and where the
        # result is placed.
        row_elements = [[] for _ in range(self.nb_data)]
        for i, r in enumerate(self.rows):
            row_elements[r].append(i)
        row_elements = [np.array(re) for re in row_elements if len(re) != 0]

        # The indices of the generator, for each row.
        row_generators = [self.indices[r] for r in row_elements]

        # The indices of nonzero columns for each row.
        row_columns = [self.columns[r] for r in row_elements]

        # The weights of the nonzero elements for each row.
        row_weights = [self.weights[r] for r in row_elements]

        length = self.generator_length

        def row_slice(row):
            return slice(length * row, length * (row + 1))

        row_slices = [row_slice(r) for r in row_indices]

        self._row = list(zip(row_columns, row_generators, row_weights,
                             row_slices))

    @property
    def transpose(self):
        """TransposedFastLinearOperator: transpose of the linear operator."""
        return TransposedFastLinearOperator(self)

    def __matmul__(self, x):
        """Matrix vector product (A @ x)

        Args:
            x: The right operand of the product. It's length must match the
                number of columns of the linear operator.

        Raises:
            TypeError : If x is not a numpy array.
            ValueError : If the length of x does not match the number of
                columns of the linear operator.
        """

        x = self.convert_x(x)

        product = np.zeros(self.shape[0], dtype=DATATYPE)

        for elements, generator_indices, weights, row_slice in self._row:
            row_x = x[elements] * weights
            row_generators = self.generators[generator_indices, :]
            product[row_slice] = np.dot(row_generators.T, row_x)

        return product


class TransposedLinearOperator(AbstractLinearOperator):

    def __init__(self, linear_operator):
        """Transposed of a LinearOperator object.

        Args:
            linear_operator : the LinearOperator object of which the transpose
                is wanted.
        """
        self._linear_operator = linear_operator

    @property
    def shape(self):
        return self._linear_operator.shape[::-1]

    def __matmul__(self, y):
        """Matrix vector product (A.T @ y)

        Args:
            y: The right operand of the product. It's length must match the
                number of columns of the transposed linear operator.

        Raises:
            TypeError if y is not a numpy array.
            ValueError if the length of y does not match the number of
                columns of the transposed linear operator.
        """

        y = self.convert_x(y)

        genlen = self._linear_operator.generator_length
        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for row, col, weighted_generator in self._linear_operator:
            indices_range = range(genlen * row, genlen * (row + 1))
            product[col] += weighted_generator.dot(y[indices_range])
        return product

    def todense(self):
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            ndarray: full matrix representing the linear operator.
        """
        return self._linear_operator.todense().T

    @property
    def transpose(self):
        """LinearOperator: transpose of the transposed linear operator."""
        return self._linear_operator


class TransposedFastLinearOperator(TransposedLinearOperator):
    def __init__(self, linear_operator):
        """Transposed of a LinearOperator object.

        Args:
            linear_operator : the LinearOperator object of which the transpose
                is wanted.
        """
        super().__init__(linear_operator)

    def __matmul__(self, y):
        """Matrix vector product (A.T @ y)

        Args:
            y: The right operand of the product. It's length must match the
                number of columns of the transposed linear operator.

        Raises:
            TypeError if y is not a numpy array.
            ValueError if the length of y does not match the number of
                columns of the transposed linear operator.
        """

        y = self.convert_x(y)

        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for (elements, generator_indices,
             weights, row_slice) in self._linear_operator._row:
            row_y = y[row_slice]
            row_generators = self._linear_operator.generators[
                             generator_indices, :]
            product[elements] += row_generators.dot(row_y) * weights

        return product


class ConcatenatedLinearOperator(AbstractLinearOperator):
    def __init__(self, operators, axis):
        """Concatenated LinearOperator object

        The ConcatenatedLinearOperator class implements the vertical or
        horizontal concatenation of LinearOperator objects. It is endowed with
        the multiplication operation (@).

        Args:
            operators: list or tuple of LinearOperator objects to be
                concatenated in the same axis.
            axis: int direction in which we want to concatenate the
                LinearOperator or ConcatenatedLinearOperator objects that we
                want to concatenate. Vertical concatenation is obtained for
                `axis = 0` and horizontal concatenation is obtained for
                `axis = 1` as in np.concatenate. (Default: 0)

        Raises:
            TypeError: If any element of `operator` is not an instance of
                LinearOperator or ConcatenatedLinearOperator.
            TypeError: If `operators` is not a list or a tuple.
            ValueError: If `axis` is not 0 or 1.
            ValueError: If `operators` is an empty list or tuple.
            ValueError: If the operators do not have compatible dimensions.
        """
        if not type(operators) in [list, tuple]:
            raise TypeError('Expected type for `operators` is list or tuple.')

        if axis not in [0, 1]:
            raise ValueError('Expected value for `axis` is 0 or 1.')

        if len(operators) < 1:
            raise ValueError('List of operators must be non-empty.')

        def good_instance(op):
            return (isinstance(op, LinearOperator) or
                    isinstance(op, TransposedLinearOperator) or
                    isinstance(op, ConcatenatedLinearOperator))

        if not all(map(good_instance, operators)):
            raise TypeError('All concatenated operators must be either '
                            'LinearOperator objects or '
                            'ConcatenatedLinearOperator objects.')

        if len(np.unique([op.shape[int(not axis)] for op in operators])) != 1:
            raise ValueError('Trying to concatenate linear operators with '
                             'non compatible dimensions.')

        self._axis = axis
        self._operators = operators
        self._slices = []
        self._transposed_operators = [op.T for op in self._operators]

        start_index = 0
        for linear_operator in self._operators:
            stop_index = start_index + linear_operator.shape[self._axis]
            self._slices.append(slice(start_index, stop_index))
            start_index = stop_index

    def __matmul__(self, x):
        """Matrix vector product (A @ x)

        Args:
            x: The right operand of the product. It's length must match the
                number of columns of the concatenated linear operator.

        Raises:
            TypeError if x is not a numpy array.
            ValueError if the length of x does not match the number of
                columns of the concatenated linear operator.
        """

        x = self.convert_x(x)

        product = np.zeros(self.shape[0], dtype=DATATYPE)
        if self._axis == 0:
            for indices, linear_operator in zip(self._slices, self.operators):
                product[indices] = linear_operator @ x
        else:
            for indices, linear_operator in zip(self._slices, self.operators):
                product += linear_operator @ x[indices]
        return product

    @property
    def axis(self):
        """int: axis in which the concatenation was performed."""
        return self._axis

    @property
    def operators(self):
        """list: list of concatenated operators."""
        return self._operators

    @property
    def shape(self):
        """:tuple of int: Shape of the concatenated linear operator.
        """
        n_rows = np.sum([block.shape[self.axis] for block in self._operators])
        n_columns = self._operators[0].shape[int(not self.axis)]
        the_shape = n_rows, n_columns
        if self.axis:
            the_shape = the_shape[::-1]
        return the_shape

    @property
    def transpose(self):
        """TransposedConcatenatedLinearOperator: transpose of the linear
        operator."""
        return TransposedConcatenatedLinearOperator(
            self, self._transposed_operators)

    def todense(self):
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            ndarray: full matrix representing the linear operator.
        """
        all_dense = []
        for op in self.operators:
            all_dense.append(op.todense())
        return np.concatenate(all_dense, self.axis)


class TransposedConcatenatedLinearOperator(ConcatenatedLinearOperator):
    def __init__(self, concatenated_operator, transposed_operators):
        """Transposed of a ConcatenatedLinearOperator object.

        Args:
            concatenated_operator: the ConcatenatedLinearOperator object
                of which the transpose is wanted.
        """
        self._concatenated_linear_operator = concatenated_operator

        axis = int(not self._concatenated_linear_operator.axis)

        super().__init__(transposed_operators, axis)

    @property
    def transpose(self):
        """LinearOperator: transpose of the transposed linear operator."""
        return self._concatenated_linear_operator
