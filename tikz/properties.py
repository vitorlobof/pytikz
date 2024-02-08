from typing import Iterable, Union, Optional
import numpy as np
from .utils import rotate, reflect, to_array, proj
from .constants import OUT


class Points:
    def get_center(self) -> np.array:
        """
        Property that returns the object's center.
        """
        return np.mean(self.points, axis=0)

    def get_top(self):
        """
        Property that returns the object's top.
        """
        return np.max(self.points[:, 1])

    def get_bottom(self):
        """
        Property that returns the object's bottom.
        """
        return np.min(self.points[:, 1])

    def get_left(self):
        """
        Property that returns the object's left.
        """
        return np.min(self.points[:, 0])

    def get_right(self):
        """
        Property that returns the object's right.
        """
        return np.max(self.points[:, 0])

    def get_extreme(self, direction: Iterable) -> np.array:
        """
        Receives a vector denoting a direction and returns the
        farthermost point on that direction.
        """
        cache = float('-inf')

        for vector in self.points:
            value = np.dot(direction, vector)
            if cache < value:
                cache = value
                max_vector = vector

        return max_vector

    def shift(self, vector: Iterable[Union[int, float]]):
        """
        Shift the object and it's subobjects through a given
        vector.
        """
        vector = to_array(vector)
        self.points += vector
        for obj in self.subobjs:
            obj.shift(vector)
        return self

    def move_to(self, vector: Iterable[Union[int, float]]):
        """
        Moves the center of the object to a position given by
        vector.
        """
        vector = to_array(vector)
        self.shift(vector - self.get_center())
        return self

    def align_to(self, kobj, direction: Iterable[Union[int, float]]):
        """
        Aligns the object center with the given objects center
        on a line normal to the given direction.
        """
        direction = to_array(direction)
        v = kobj.get_center()
        self.shift(proj(v, direction))
        return self

    def linear_transform(
        self,
        array: np.array,
        about_point: Optional[Iterable[Union[int, float]]] = None
    ):
        """
        Applies a linear transformation to the points that
        constitutes the object and recursively applies it on
        submobjects.
        """
        if about_point is None:
            about_point = self.get_center()

        self.shift(-about_point)
        for idx, point in enumerate(self.points):
            self.points[idx] = np.dot(point, array.T)
        self.shift(about_point)

        for obj in self.subobjs:
            obj.linear_transform(array, about_point=about_point)

        return self

    def scale(self, num: float, about_point=None):
        """
        Scales the object points with respect to the about_point.
        """
        if about_point is None:
            about_point = self.get_center()

        self.shift(-about_point)
        self.points *= num
        self.shift(about_point)

        for obj in self.subobjs:
            obj.scale(num, about_point=about_point)

        return self

    def rotate(
        self,
        angle: float,
        axis=OUT,
        about_point: Optional[Iterable[Union[int, float]]] = None
    ):
        """
        Rotates the object about and axis defined by axis and
        about_point.
        """
        if about_point is None:
            about_point = self.get_center()

        self.shift(-about_point)
        for idx, point in enumerate(self.points):
            self.points[idx] = rotate(point, angle, axis)
        self.shift(about_point)

        for obj in self.subobjs:
            obj.rotate(angle, axis=axis, about_point=about_point)

        return self

    def reflect(self, normal, about_point=None):
        """
        Reflects object about a plane.
        """
        if about_point is None:
            about_point = self.get_center()
        else:
            about_point = np.array(about_point, dtype=np.float64)

        self.shift(-about_point)
        for idx, point in enumerate(self.points):
            self.points[idx] = reflect(point, normal, about_point)
        self.shift(about_point)

        for obj in self.subobjs:
            obj.reflect(normal, about_point=about_point)

        return self


class Kwargs:
    def set_color(self, color):
        """
        Sets the color of the line that draws the object.
        """
        self.kw['color'] = color
        return self

    def set_fill(self, color):
        """
        Sets the object's color.
        """
        self.kw['fill'] = color
        return self

    def set_tips(self, tip):
        """
        Sets the tips of the lines that constitute the object.
        """
        self.kw[tip] = True
        return self
