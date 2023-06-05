import numpy as np
from .shape import Shape
from .lines import Lines
from .text import MathText
from .utils import versor, get_angle

class Arc(Shape):
    def __init__(self, radius=2, start_angle=0, end_angle=np.pi/3, **kw):
        self.center = np.array([0.0, 0.0, 0.0])
        self.radius = radius
        super().__init__(
            lambda t: radius * versor(t),
            start_angle,
            end_angle,
            **kw
        )
    
    def shift(self, array):
        self.center += array
        super().shift(array)
        return self
    
    def scale(self, num, about_point=None):
        if about_point is None:
            about_point = self.get_center()

        super().scale(num, about_point=about_point)
        
        self.radius *= num
        
        self.shift(-about_point)
        self.center *= num
        self.shift(about_point)
        
        return self

class Circle(Arc):
    closed=True

    def __init__(self, radius=2, **kw) -> None:
        super().__init__(radius, 0, 2*np.pi, **kw)

class Dot(Circle):
    def __init__(self, array, **kw):
        super().__init__(0.03, **kw)
        self.shift(array).set_fill('black')

class EllipticalArc(Shape):
    def __init__(self, major_axis=2, minor_axis=1, start_angle=0, end_angle=np.pi/3, **kw):
        def parametric(t):
            v = np.array([major_axis, minor_axis, 0.0])
            return v * versor(t)
        super().__init__(parametric, start_angle, end_angle, **kw)

class Ellipse(EllipticalArc):
    closed=True

    def __init__(self, major_axis=2, minor_axis=1, **kw):
        super().__init__(major_axis, minor_axis, 0, 2*np.pi, **kw)

class Parabola(Shape):
    def __init__(self, parameter=1, start=0, end=5, axis=0, **kw):
        if axis==0:
            def parametric(t):
                return np.array([t**2/(2*parameter), t, 0.0])
        elif axis==1:
            def parametric(t):
                return np.array([t, t**2/(2*parameter), 0.0])
        else:
            raise NotImplementedError('The axis kwargs was only implemented to the values 0 and 1')

        super().__init__(parametric, start, end, **kw)
    
    @classmethod
    def from_three_points(cls, point_1, point_2, point_3, axis=0, **kw):
        matrix = []
        values = []
        points = (point_1, point_2, point_3)

        if axis==0:
            x, y = 1, 0
        elif axis==1:
            x, y = 0, 1
        else:
            raise NotImplementedError('The axis has to be 0 or 1.')
        
        for point in points:
            matrix.append([point[x]**2, point[x], 1])
            values.append(point[y])
        
        a, b, c = np.linalg.solve(matrix, values)

        parameter = 1/(2*a)
        xv = - b * parameter
        yv = c - xv**2 / (2*parameter)

        start = min(points, key=lambda p: p[x])[x]
        end = max(points, key=lambda p: p[x])[x]

        return cls(
            parameter=parameter,
            start=start,
            end=end,
            axis=axis,
            **kw
        ).shift([xv, yv, 0.0])
    
    @classmethod
    def from_vpp(cls, vector, point1, point2, axis=0, **kw):
        if axis==0:
            x, y = 1, 0
        elif axis==1:
            x, y = 0, 1
        else:
            raise NotImplementedError('The axis has to be 0 or 1.')

        matrix = [
            [point1[x]**2, point1[x], 1],
            [point2[x]**2, point2[x], 1],
            [2*point1[x], 1, 0]
        ]
        values = [point1[y], point2[y], -np.tan(vector[y]/vector[x])]
        
        a, b, c = np.linalg.solve(matrix, values)

        parameter = 1/(2*a)
        xv = - b * parameter
        yv = c - xv**2 / (2*parameter)

        start = min(point1[x], point2[x])
        end = max(point1[x], point2[x])

        return cls(
            parameter=parameter,
            start=start,
            end=end,
            axis=axis,
            **kw
        ).shift([xv, yv, 0.0])

class Angle(Arc):
    def __init__(self, A, B, C, radius=0.3, label=None, label_pos=0.5, **kw) -> None:
        A = np.array(A, dtype=np.float64)
        B = np.array(B, dtype=np.float64)
        C = np.array(C, dtype=np.float64)

        v = A - B
        v /= np.linalg.norm(v)

        u = C - B
        u /= np.linalg.norm(u)

        w = u + v
        w /= np.linalg.norm(w)

        super().__init__(
            radius=radius,
            start_angle=get_angle(v),
            end_angle=get_angle(u),
            **kw
        )

        if label is not None:
            text = MathText(label).shift(w*label_pos)
            self.add_subobjs(text)
        
        self.shift(B)

class RightAngle(Lines):
    def __init__(self, A, B, C, size=0.2, dot=True, **kw) -> None:
        A = np.array(A, dtype=np.float64)
        B = np.array(B, dtype=np.float64)
        C = np.array(C, dtype=np.float64)

        v = A - B
        v *= size/np.linalg.norm(v)

        u = C - B
        u *= size/np.linalg.norm(u)

        w = u + v

        super().__init__(v, w, u, **kw)

        if dot:
            self.add_subobjs(Dot(w/2, **kw))

        self.shift(B)
