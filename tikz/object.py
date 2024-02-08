from typing import Iterable, Union, Optional
import numpy as np
import copy

from .properties import Points, Kwargs
from .utils import rotate, to_array

class TikzObject(Points, Kwargs):
    closed = False
    draw = True

    def __init__(self, points, **kw) -> None:
        self.points = to_array(points)
        self.kw = {x.replace('_', ' '): y for x, y in kw.items()}
        self.subobjs = []
    
    def add_subobjs(self, *objs):
        self.subobjs.extend(objs)
        return self

    def copy(self):
        copied_obj = copy.copy(self)

        # Get a dictionary of all attributes
        attrs = vars(self)

        # Copy each attribute dynamically
        for attr_name, attr_value in attrs.items():
            setattr(copied_obj, attr_name, copy.copy(attr_value))

        copied_obj.subobjs = [obj.copy() for obj in copied_obj.subobjs]

        return copied_obj
    
    def render(self) -> str:
        def point_to_str(point):
            x, y, z = point
            return f'({x}, {y}, {z})'

        points = ' -- '.join(point_to_str(x) for x in self.points)
        
        if self.closed:
            points += ' -- cycle'

        def kw_to_str(key, value):
            if value is True:
                return key
            else:
                return f'{key}={value}'
        
        kw = ', '.join(kw_to_str(x, y) for x, y in self.kw.items())
        if kw != '':
            kw = f'[{kw}]'

        if self.draw is True:
            action = '\\draw'
        else:
            action = '\\path'
        
        subobjs = [obj.render() for obj in self.subobjs]
        return '\n'.join([f'{action}{kw} {points};', *subobjs])

class Union(TikzObject):
    def __init__(self, *kobjs, **kw) -> None:
        points = np.vstack([obj.points for obj in kobjs])
        super().__init__(points, **kw)
        for obj in kobjs:
            self.subobjs += obj.subobjs

class Group(TikzObject):
    def __init__(self, *kobjs) -> None:
        self.kobjs = kobjs

    def copy(self):
        return type(self)(*[kobj.copy() for kobj in self.kobjs])
    
    def shift(self, array):
        for kobj in self.kobjs:
            kobj.shift(array)
        return self
    
    def move_to(self, array):
        for kobj in self.kobjs:
            kobj.move_to(array)
        return self
    
    def linear_transform(self, array, about_point=None):
        for kobj in self.kobjs:
            kobj.transform(array, about_point)
        return self
    
    def scale(self, num):
        for kobj in self.kobjs:
            kobj.scale(num)
        return self
    
    def rotate(self, angle, axis=(0.0, 0.0, 1.0), about_point=None):
        if about_point is None:
            about_point = np.mean(
                [kobj.get_center() for kobj in self.kobjs])
        else:
            about_point = np.array(about_point, dtype=np.float64)
        
        for kobj in self.kobjs:
            kobj.rotate(angle, axis, about_point)
        return self
    
    def render(self):
        return '\n'.join(x.render() for x in self.kobjs)
