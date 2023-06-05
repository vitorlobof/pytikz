import numpy as np
from typing import Sequence

def versor(angle: float) -> np.array:
    return np.array([np.cos(angle), np.sin(angle), 0.0])

def get_angle(array: np.array) -> float:
    x, y, _ = array
    return np.arctan2(y, x)

def LLint(A, B, C, D) -> 'Vector':
    x1, y1 = tuple(A)
    x2, y2 = tuple(B)
    x3, y3 = tuple(C)
    x4, y4 = tuple(D)

    t = (x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)
    t /= (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)

    return np.array([x1 + t*(x2-x1), y1 + t*(y2-y1)])


def quaternion_mult(*quats: Sequence[float]) -> np.ndarray:
    quats = iter(quats)
    try:
        result = next(quats)
    except StopIteration:
        return np.array([1, 0, 0, 0], dtype=np.float64)
    
    for quat in quats:
        w1, x1, y1, z1 = result
        w2, x2, y2, z2 = quat
        result = [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2,
            w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2,
        ]
    return np.array(result, dtype=np.float64)

def quaternion_conjugate(quaternion) -> np.array:
    result = np.array(quaternion, dtype=np.float64)
    result[1:] *= -1
    return result

def rotate(
    vector: np.array,
    angle: float,
    axis: np.array = (0.0, 0.0, 1.0)
) -> np.array:
    axis = np.array(axis)
    axis *= np.sin(angle/2)/np.linalg.norm(axis)

    x, y, z = tuple(axis)
    u = (np.cos(angle/2), x, y, z)
    u_ = quaternion_conjugate(u)

    x, y, z = tuple(vector)
    return quaternion_mult(u, (0, x, y, z), u_)[1:]

def reflect(point, normal, about_point=(0.0, 0.0, 0.0)):
    point = np.array(point, np.float64)
    normal = np.array(normal, np.float64)
    about_point = np.array(about_point, np.float64)
    v = np.dot(normal, point - about_point) * normal
    v /= np.dot(normal, normal)
    return point - 2 * v

def proj(a, b):
    return np.dot(a, b)/np.dot(b, b) * b

def cumulative(*arrays):
    return np.cumsum(arrays, axis=0)
