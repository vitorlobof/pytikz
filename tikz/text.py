from .object import TikzObject
from .utils import proj
import numpy as np

class Text(TikzObject):
    def __init__(self, text, **kw) -> None:
        self.text = text
        self.kw = kw
        self.points = np.array([[0.0, 0.0, 0.0]])
        self.subobjs = []
    
    def next_to(self, kobj, direction):
        extreme = kobj.get_extreme(direction)
        center = kobj.get_center()
        vector = proj(extreme - center, direction)
        self.move_to(center).shift(vector + 0.2*direction)
        return self
    
    def render(self) -> str:
        point = f'({", ".join(str(x) for x in self.points[0])})'

        def kw_to_str(key, value):
            if value:
                return key
            else:
                return f'{key}={value}'

        kw = ', '.join(kw_to_str(x, y) for x, y in self.kw.items())
        if kw != '':
            kw = f'[{kw}]'

        text = "{%s}" % self.text

        return f'\\node{kw} at {point} {text};'

class MathText(Text):
    def __init__(self, text, **kw) -> None:
        super().__init__(f'${text}$', **kw)
