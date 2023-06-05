import numpy as np

PI = np.pi

BLACK = 'black'
RED = 'red'
BLUE = 'blue'
LIGHTBLUE = 'lightblue'
GRAY = 'gray'
LIGHTGRAY = 'lightgray'

UP = np.array((0.0, 1.0, 0.0))
DOWN = np.array((0.0, -1.0, 0.0))
LEFT = np.array((-1.0, 0.0, 0.0))
RIGHT = np.array((1.0, 0.0, 0.0))

UR = UP + RIGHT
UL = UP + LEFT
DL = DOWN + LEFT
DR = DOWN + RIGHT

IN = np.array((0.0, 0.0, -1.0))
OUT = np.array((0.0, 0.0, 1.0))
