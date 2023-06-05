from typing import Iterable, Union, Optional
import numpy as np
from .utils import rotate, reflect

class Points:
    def get_center(self) -> np.array:
        return np.mean(self.points, axis=0)
    
    def shift(self, vector: Iterable[Union[int, float]]):
        vector = np.array(vector, dtype=np.float64)
        self.points += vector
        for obj in self.subobjs:
            obj.points += vector
        return self
    
    def move_to(self, vector:Iterable[Union[int, float]]):
        vector = np.array(vector, dtype=np.float64)
        self.shift(vector - self.get_center())
        return self
    
    def get_top(self):
        return np.max(self.points[:, 1])
    
    def get_bottom(self):
        return np.min(self.points[:, 1])
    
    def get_left(self):
        return np.min(self.points[:, 0])
    
    def get_right(self):
        return np.max(self.points[:, 0])
    
    def get_extreme(self, direction: Iterable) -> np.array:
        cache = float('-inf')
        
        for vector in self.points:
            value = np.dot(direction, vector)
            if cache < value:
                cache = value
                max_vector = vector
        
        return max_vector
    
    def align_to(self, kobj, angle: float):
        v = kobj.get_center() - self.get_center()
        d = versor(angle)
        self.shift(np.dot(v, d)/np.dot(d, d) * d)
        return self
    
    def linear_transform(
        self,
        array: np.array,
        about_point: Optional[Iterable[Union[int, float]]] = None
    ):
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
        axis = (0.0, 0.0, 1.0),
        about_point: Optional[Iterable[Union[int, float]]] = None
    ):
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
        self.kw['color'] = color
        return self
    
    def set_fill(self, color):
        self.kw['fill'] = color
        return self
    
    def set_tips(self, tip):
        self.kw[tip] = True
        return self
