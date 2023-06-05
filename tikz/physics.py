import numpy as np
from .shape import Shape
from .lines import Line
from .arcs import Circle, Dot

class Throw(Shape):
    def __init__(self, velocity, gravity, time, **kw) -> None:
        velocity = np.array(velocity, dtype=np.float64)
        gravity = np.array(gravity, dtype=np.float64)
        def parametric(t):
            return velocity * t + gravity * t**2/2
        super().__init__(parametric, 0.0, time, **kw)

class Pulley(Circle):
    def __init__(self, radius=1, **kw) -> None:
        super().__init__(radius=radius, **kw)
        self.add_subobjs(Dot([0.0, 0.0, 0.0]))

class HoldedPulley(Pulley):
    def __init__(self, center, radius=1, **kw) -> None:
        super().__init__(radius=radius, **kw)
        self.shift(center)
        center = np.array(center, dtype=np.float64)
        dist = np.linalg.norm(center)
        line = Line(
            [0, 0, 0],
            center * (dist - radius) / dist
        )
        self.add_subobjs(line)
