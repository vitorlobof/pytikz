import numpy as np
from typing import Sequence

def versor(angle: float) -> np.array:
    return np.array([np.cos(angle), np.sin(angle), 0.0])

def get_angle(array: np.array) -> float:
    x, y, _ = array
    angle = np.arctan2(y, x)

    if angle < 0:
        angle += 2*np.pi
    
    return angle

def LLint(line1_point1, line1_point2, line2_point1, line2_point2):
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
