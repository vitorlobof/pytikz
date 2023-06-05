import numpy as np

from .object import TikzObject
from .text import MathText
from .utils import rotate, versor

class Lines(TikzObject):
    def __init__(self, *points, **kw) -> None:
        super().__init__(points, **kw)
    
class Polygon(Lines):
    closed = True

class Rectangle(Polygon):
    def __init__(self, base, height, **kw) -> None:
        points = [
            [base/2, height/2, 0],
            [-base/2, height/2, 0],
            [-base/2, -height/2, 0],
            [base/2, -height/2, 0]
        ]
        super().__init__(*points, **kw)

class RegularPolygon(Polygon):
    def __init__(self, num_of_sides, side=2.0, **kw) -> None:
        angle = 2 * np.pi / num_of_sides
        radius = side/(2*np.sin(angle/2))
        points = []
        for k in range(num_of_sides):
            points.append(radius*versor(k*angle))
        super().__init__(*points, **kw)

        self.side = side
    
    def scale(self, num, about_point=None):
        super().scale(num, about_point=about_point)
        self.side *= num
        return self

class Square(RegularPolygon):
    def __init__(self, side=2.0, **kw) -> None:
        super().__init__(4, side, **kw)
        self.rotate(np.pi/4)
    
class Line(Lines):
    def __init__(self, tail, head, **kw) -> None:
        super().__init__(tail, head, **kw)
    
    @property
    def tail(self):
        return self.points[0]
    
    @property
    def head(self):
        return self.points[1]
    
    def get_versor(self) -> np.array:
        v = self.head - self.tail
        return v / np.linalg.norm(v)
    
    def add_label(self, text, pos=0.3):
        center = self.get_center()
        normal = rotate(self.get_versor(), np.pi/2)
        label = MathText(text).shift(center + pos*normal)
        self.add_subobjs(label)
        return label
    
    def mark_length(self, text, pos=0.5):
        normal = rotate(self.get_versor(), np.pi/2)
        line = Line(self.tail, self.head, **self.kw)
        line.shift(pos*normal).set_tips('<->')
        line.add_label(text, pos=0.3*pos/abs(pos))

        dashed_1 = Line(self.tail, line.tail, dashed=True)
        dashed_2 = Line(self.head, line.head, dashed=True)

        line.add_subobjs(dashed_1, dashed_2)
        self.add_subobjs(line)
        return line


class Arrow(Line):
    def __init__(self, tail, head, **kw) -> None:
        super().__init__(tail, head, **kw)
        self.set_tips('-stealth')

class Vector(Arrow):
    def __init__(self, array, **kw) -> None:
        super().__init__([0.0, 0.0, 0.0], array, **kw)
