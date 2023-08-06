import numpy as np
import talon


def directions(number_of_points=180):
    """
    Get a list of 3D vectors representing the directions of the fibonacci
    covering of a hemisphere of radius 1 computed with the golden spiral method.
    The :math:`z` coordinate of the points is always strictly positive.

    Args:
        number_of_points : number of points of the wanted covering (default=180)

    Returns:
        ndarray : ``number_of_points`` x 3 array with the cartesian coordinates
            of a point of the covering in each row.

    Raises:
        ValueError : if ``number_of_points <= 0`` .

    References:
        https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere/44164075#44164075
    """
    number_of_points = int(number_of_points)

    if number_of_points <= 0:
        raise ValueError('The number of points for the covering must be >= 1 .')

    n = 2 * number_of_points
    indices = np.arange(0, n, dtype=float) + 0.5

    phi = np.arccos(1 - 2 * indices / n)
    theta = np.pi * (1 + np.sqrt(5)) * indices

    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)

    x, y, z = map(lambda a: a[:number_of_points], [x, y, z])

    points = np.c_[x, y, z].astype(talon.core.DATATYPE)

    return np.asarray([p / np.linalg.norm(p) for p in points])
