from typing import Iterable, Union
import numpy as np
from typing import Sequence
from .constants import ORIGIN, OUT


def to_array(iterable: Iterable[Union[int, float]]):
    """
    Receives an iterable and return it's respective array.
    """
    return np.array(iterable, dtype=np.float64)


def versor(angle: float) -> np.array:
    """
    Returns the rho versor.
    """
    return to_array([np.cos(angle), np.sin(angle), 0.0])


def get_angle(array: np.array) -> float:
    """
    Returns the angle a vector does with respect to the xy plane.
    """
    x, y, _ = array
    angle = np.arctan2(y, x)

    if angle < 0:
        angle += 2*np.pi

    return angle


def LLint(line1_point1, line1_point2, line2_point1, line2_point2):
    """
    Given 4 points, will return the intersection between the two lines.
    """

    A = np.array(line1_point1[:2])
    B = np.array(line1_point2[:2])
    C = np.array(line2_point1[:2])
    D = np.array(line2_point2[:2])

    dir_1 = B - A
    dir_2 = D - C

    normal_1 = [- dir_1[1], dir_1[0]]
    normal_2 = [- dir_2[1], dir_2[0]]

    m = [normal_1, normal_2]
    b = [np.dot(normal_1, A), np.dot(normal_2, C)]

    return np.append(np.linalg.solve(m, b), 0)


def quaternion_mult(*quats: Sequence[float]) -> np.ndarray:
    """
    Receives quaternions and returns the result of their
    multiplication.
    """
    quats = iter(quats)
    try:
        result = next(quats)
    except StopIteration:
        return to_array([1, 0, 0, 0])

    for quat in quats:
        w1, x1, y1, z1 = result
        w2, x2, y2, z2 = quat
        result = [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2,
            w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2,
        ]
    return to_array(result)


def quaternion_conjugate(quaternion) -> np.array:
    """
    Receives a quaternion and returns it's conjugate.
    """
    result = to_array(quaternion)
    result[1:] *= -1
    return result


def rotate(
    vector: np.array,
    angle: float,
    axis: np.array = OUT
) -> np.array:
    """
    Uses quaternion multiplication to rotate a vector by a
    given angle with respect to the axis.
    """
    axis = to_array(axis)
    axis *= np.sin(angle/2)/np.linalg.norm(axis)

    x, y, z = tuple(axis)
    u = (np.cos(angle/2), x, y, z)
    u_ = quaternion_conjugate(u)

    x, y, z = tuple(vector)
    return quaternion_mult(u, (0, x, y, z), u_)[1:]


def reflect(point, normal, about_point=ORIGIN):
    """
    Reflects a point with respect to a plane that is defined by
    about_point and normal.
    """
    point = to_array(point)
    normal = to_array(normal)
    about_point = to_array(about_point)
    vector = np.dot(normal, point - about_point) * normal
    vector /= np.dot(normal, normal)
    return point - 2 * vector


def proj(vector, direction):
    """
    Projects vector on direction.
    """
    return (
        np.dot(vector, direction) /
        np.dot(direction, direction)
        * direction
    )


def cumulative(*arrays):
    """
    Returns the cumulative sum of the given arrays.
    """
    return np.cumsum(arrays, axis=0)
