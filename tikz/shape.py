from .object import TikzObject

class Parametric:
    def __init__(self, function):
        self.function = function
    
    

class Shape(TikzObject):
    samples = 500

    def __init__(self, parametric, start, end, **kw) -> None:
        self.parametric = parametric
        self.start = start
        self.end = end

        dt = (end - start) / self.samples
        points = []
        for k in range(self.samples):
            points.append(self.parametric(start + k*dt))

        super().__init__(points, **kw)
